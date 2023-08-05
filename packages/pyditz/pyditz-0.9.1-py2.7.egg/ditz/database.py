"""
Ditz database interface.
"""

import os
import re
import glob

from collections import Counter, defaultdict
from datetime import datetime

from six.moves import cPickle as pickle

from .objects import Config, Project, Issue, Component, Release, find_config
from .files import write_file, write_config, read_object_file
from .util import default_name, default_email, DitzError
from .config import config as userconfig
from .settings import Settings
from .plugin import loader

from .vcs import VCS
from .logger import log

from .flags import (RELEASED, UNRELEASED, BUGFIX, UNSTARTED, STATUS,
                    DISPOSITION)

#: Regexp matching an issue name.
re_issue_name = r'\b([A-Za-z]+-[0-9]+)\b'

#: Regexp matching an issue ID.
re_issue_id = r'{issue ([0-9a-f]+)}'


class DitzDB(object):
    """
    A Ditz issue database.
    """

    project = None
    issues = []

    def __init__(self, project, username=None, email=None, issuedir=None,
                 path=".", settings=None, **kw):
        #: Global settings.
        self.settings = settings or Settings(**kw)

        #: Configuration data.
        self.config = Config(username or default_name(),
                             email or default_email(),
                             issuedir or ".ditz-issues")

        #: Location.
        self.path = os.path.realpath(path)

        #: Project (a :class:`Project` object).
        self.project = Project(project)

        #: List of issues.  Each entry is an :class:`Issue`.
        self.issues = []

        #: Version control handle.
        self.vcs = VCS(self.path)

        #: Mapping of issue IDs to assigned names.
        self._id2name = {}

        #: Mapping of assigned names to issues.
        self._name2issue = {}

    # Database input/output methods.

    @staticmethod
    def read(dirname, settings=None, **kw):
        """
        Read a Ditz database.
        """

        # Create an empty database.
        db = DitzDB("empty", settings=settings, **kw)

        # Find the Ditz config file.
        dirname, config = find_config(dirname, error=True,
                                      search=db.settings.searchparents)
        dirname = os.path.realpath(dirname)

        # Extract the issue directory name.
        issuedir = config.issue_dir

        # Read the project file.
        path = os.path.join(dirname, issuedir, Project.filename)
        log.info("reading project from %s" % path)
        project = read_object_file(path)

        # Read the issues.
        issues = []
        path = os.path.join(dirname, issuedir)
        match = os.path.join(path, Issue.template % "*")
        issue_files = set(glob.glob(match))
        log.info("found %d issues in %s", len(issue_files), path)

        path = os.path.join(dirname, db.settings.cachefile)
        cached_issues = db.readcache(path)
        cache_changed = False

        if cached_issues:
            # Check for new, modified or deleted issues.
            cached_files = set()
            modtime = os.stat(path).st_mtime

            for issue in cached_issues:
                path = os.path.join(dirname, issuedir, issue.filename)

                # Skip issue if it's deleted.
                if not os.path.exists(path):
                    log.info("skipping deleted issue in %s", path)
                    continue

                # Reread issue file if invalid, or newer than cache.
                reread = os.stat(path).st_mtime > modtime

                try:
                    issue.validate()
                except DitzError:
                    reread = True

                if reread:
                    log.info("reading changed issue from %s" % path)
                    issue = read_object_file(path)
                    cache_changed = True

                cached_files.add(path)
                issues.append(issue)

            # Read all the new issues.
            for path in issue_files - cached_files:
                log.info("reading new issue from %s" % path)
                issue = read_object_file(path)
                issues.append(issue)
                cache_changed = True
        else:
            path = os.path.join(dirname, issuedir)
            log.info("reading issues from %s" % path)
            for path in issue_files:
                issue = read_object_file(path)
                issues.append(issue)
                cache_changed = True

        # Initialise database.
        db.path = dirname
        db.config = config
        db.project = project
        db.issues = issues

        if cache_changed:
            db.update_cache()

        db._reassign_names()
        db.vcs = VCS(db.path)

        # Read extra config settings if they exist.
        path = os.path.join(config.issue_dir, "project.cfg")
        if os.path.exists(path):
            log.info("reading %s", path)
            userconfig.read(path)

        # Load any extra plugins from the issue directory.
        path = os.path.join(config.issue_dir, "plugins")
        loader.add_path(path)
        loader.load()

        return db

    def readcache(self, path):
        """
        Read cached issues if possible.
        """

        # Do nothing unless cache is there and wanted.
        if not self.settings.usecache or not os.path.exists(path):
            return None

        # Read cache, checking for errors.
        with open(path, "rb") as fp:
            try:
                issues = pickle.load(fp)
                log.info("found %d issues cached in %s", len(issues), path)
            except Exception as msg:
                log.warning("can't read issue cache (%s)", str(msg))
                issues = None

        # If no issues could be read, remove it.
        if issues is None:
            log.warning("removing unusable issue cache")
            os.unlink(path)

        return issues

    def validate(self):
        """
        Validate the database.  Return the changes made.
        """

        # Changes made.
        changes = defaultdict(list)

        # Update each issue.
        for issue in self.issues:
            changed = False

            # Check issue IDs.
            desc = self.convert_to_id(issue.desc)
            if desc != issue.desc:
                issue.desc = desc
                changes[issue.id].append("fixed issue IDs in description text")
                changed = True

            for idx, event in enumerate(issue.log_events):
                comment = self.convert_to_id(event[3])
                if comment != event[3]:
                    event[3] = comment
                    changes[issue.id].append("fixed issue IDs in "
                                             "log comment %d" % idx)
                    changed = True

            # Check issue UUID.
            uuid = issue.id.lower()
            if uuid != issue.id:
                issue.id = uuid
                changes[issue.id].append("fixed UUID")
                changed = True

            # If issue was changed, write it.
            if changed:
                issue.write(self.issuedir)
                log.info("fixed issue %s" % issue.id)

        # Update issue cache if required.
        if changes:
            self.update_cache()

        return changes

    def write(self, dirname=None):
        """
        Write the database.
        """

        if not dirname:
            dirname = self.path
        else:
            self.path = dirname

        # Write the config file.
        write_config(self.config, dirname)

        # Write the project file.
        path = os.path.join(dirname, self.config.issue_dir)

        projpath = os.path.join(path, self.project.filename)
        exists = os.path.exists(projpath)

        self.project.write(path)
        if self.vcs and self.settings.versioncontrol and not exists:
            self.vcs.add(projpath)

        # Write the issues.
        for issue in self.issues:
            issue.write(path)

        # Update issue cache.
        self.update_cache()

    def save(self, issue=None):
        """
        Save database file if required.
        """

        if not self.settings.autosave:
            return

        if issue:
            log.info("saving issue %s" % self.issue_name(issue))
            path = issue.write(self.issuedir)
            self.update_cache()
        else:
            log.info("saving project")
            path = self.project.write(self.issuedir)

        return path

    def update_cache(self):
        """
        Update the issue cache.
        """

        if self.settings.usecache:
            path = os.path.join(self.path, self.settings.cachefile)
            with open(path, "wb") as fp:
                pickle.dump(self.issues, fp)

            log.info("wrote %d cached issues to %s", len(self.issues), path)

    # High-level database commands.

    def add_issue(self, title, desc="", type=BUGFIX, status=UNSTARTED,
                  disposition=None, creation_time=None, reporter=None,
                  component=None, release=None, comment=None):
        """
        Add a new issue.
        """

        issue = Issue(title, self.convert_to_id(desc), type, status,
                      disposition, creation_time,
                      reporter or self.config.username)

        self.set_component(issue, component, event=False)
        self.set_release(issue, release, event=False)

        self.issues.append(issue)
        self.add_event(issue, "created", comment)
        self._reassign_names()
        self.save(issue)

        if self.vcs and self.settings.versioncontrol:
            path = self.issue_filename(issue)
            self.vcs.add(path)

        return issue

    def add_component(self, name):
        """
        Add a new component.
        """

        comp = Component(name)

        if name not in self.components:
            self.project.components.append(comp)
        else:
            raise DitzError("component already exists: %s" % name)

        self.save()
        return comp

    def add_release(self, name, status=UNRELEASED, release_time=None,
                    comment=None):
        """
        Add a new release.
        """

        if not self.get_release(name):
            rel = Release(name, status, release_time)
            self.add_event(rel, "created", comment)
            self.project.releases.append(rel)
        else:
            raise DitzError("release already exists: %s" % name)

        self.save()
        return rel

    def add_reference(self, issue, reference, comment=None):
        """
        Add a reference to an issue.
        """

        num = issue.add_reference(reference)
        self.add_event(issue, "added reference %d" % num, comment)
        self.save(issue)

    def set_status(self, issue, status, disposition=None, comment=None):
        """
        Set the status of an issue.
        """

        prevstatus = issue.status

        issue.set_status(status)
        issue.set_disposition(disposition)

        if disposition:
            text = "closed with disposition %s" % DISPOSITION[disposition]
        else:
            text = "changed status from %s to %s" % \
                   (STATUS[prevstatus], STATUS[status])

        self.add_event(issue, text, comment)
        self.save(issue)

    def set_component(self, issue, component=None, comment=None, event=True):
        """
        Set the component of an issue.
        """

        if not component:
            component = self.project.name
        elif component not in self.components:
            raise DitzError("unknown component: %s" % component)

        if event:
            text = "assigned to component %s from %s" \
                   % (component, issue.component)
            self.add_event(issue, text, comment)

        issue.component = component
        self._reassign_names()
        self.save(issue)

    def set_release(self, issue, release=None, comment=None, event=True):
        """
        Set the release of an issue.
        """

        if release and not self.get_release(release):
            raise DitzError("unknown release: %s" % release)

        if issue.release == release:
            return

        if event:
            if release:
                text = "assigned to release " + release
                if issue.release:
                    text += " from release " + issue.release
                else:
                    text += " from unassigned"
            else:
                text = "unassigned from release %s" % issue.release

            self.add_event(issue, text, comment)

        issue.release = release
        self.save(issue)

    def release_release(self, name, comment=None):
        """
        Release a release.
        """

        rel = self.get_release(name)
        if not rel:
            raise DitzError("unknown release: %s" % name)

        if rel.released:
            raise DitzError("release '%s' is already released" % name)

        count = 0
        for issue in self.issues:
            if issue.release == name:
                count += 1
                if not issue.closed:
                    raise DitzError("open issue %s must be reassigned"
                                    % self.issue_name(issue))

        if count == 0:
            raise DitzError("no issues assigned to release '%s'" % name)

        rel.status = RELEASED
        rel.release_time = datetime.now()

        self.add_event(rel, "released", comment)
        self.save()

    def archive_release(self, name, path):
        """
        Archive a release.
        """

        rel = self.get_release(name)
        if not rel:
            raise DitzError("unknown release: %s" % name)

        if not rel.released:
            raise DitzError("release '%s' has not been released" % name)

        keep = []
        archive = []
        for issue in self.issues:
            if issue.release == name:
                archive.append(issue)
            else:
                keep.append(issue)

        if not archive:
            raise DitzError("no issues assigned to release %s" % name)

        try:
            os.makedirs(path)
        except OSError as msg:
            raise DitzError("can't create %s: %s" % (path, str(msg)))

        self.project.write(path)
        for issue in archive:
            issue.write(path)

        for issue in archive:
            self.remove_issue(issue)

        self.issues = keep
        self._reassign_names()

        self.save()

    def edit_issue(self, issue, issuetext):
        """
        Edit an issue, by replacing its text and rereading it.
        """

        # Remove the issue.
        self.issues.remove(issue)

        # Write new issue text.
        path = os.path.join(self.issuedir, issue.filename)
        write_file(path, issuetext)

        # Reread the issue.
        issue = read_object_file(path)
        self.issues.append(issue)
        self._reassign_names()

        self.save()

    def drop_issue(self, issue):
        """
        Drop an issue.
        """

        self.remove_issue(issue)
        self.issues.remove(issue)
        self._reassign_names()

        self.save()

    def remove_issue(self, issue):
        """
        Remove an issue file.
        """

        path = self.issue_filename(issue)

        if os.path.exists(path):
            os.remove(path)

        if self.vcs and self.settings.versioncontrol:
            self.vcs.remove(path)

    def add_comment(self, issue, comment):
        """
        Add a comment to an issue.
        """

        self.add_event(issue, "commented", comment)
        self.save(issue)

    def export(self, fmt, path):
        """
        Export issue database to the specified path.
        """

        from .exporter import get_exporter

        exporter = get_exporter(fmt)
        if not exporter:
            raise DitzError("unknown export format: %s" % fmt)

        exporter(self).export(path)

    # Low-level commands and properties.

    def add_event(self, item, text, comment=None):
        """
        Add an event to a database item.
        """

        if comment:
            comment = self.convert_to_id(comment)

        item.event(self.config.username, text, comment)

    def get_issue(self, name):
        """
        Return an issue given its assigned issue name.
        """

        return self._name2issue.get(name, None)

    def issue_name(self, issue):
        """
        Return the assigned issue name of an issue.
        """

        return self._id2name.get(issue.id, "<invalid-issue>")

    def issue_filename(self, issue):
        """
        Return the filename of an issue.
        """

        return os.path.join(self.path, self.config.issue_dir, issue.filename)

    def get_release(self, name):
        """
        Return a release given its name.
        """

        name = str(name)
        for rel in self.project.releases:
            if rel.name == name:
                return rel

        return None

    def get_releases(self, name=None):
        """
        Return list of all releases, or a named release.
        """

        if not name:
            releases = self.project.releases
            return [r for r in releases if not r.released] + [None]

        return [self.get_release(name)]

    @property
    def issue_names(self):
        """
        All existing issue names.
        """

        return sorted(self._name2issue.keys())

    @property
    def issue_events(self):
        """
        Yield all issue-related events and their issues.

        Each yielded event is a tuple containing:

        - date (:class:`datetime`)
        - user (string)
        - description (string)
        - comment (string)
        - issue (:class:`Issue`)
        """

        for issue in self.issues:
            for date, user, text, comment in issue.log_events:
                yield date, user, text, comment, issue

    @property
    def components(self):
        """
        List of defined components.
        """

        return [comp.name for comp in self.project.components]

    @property
    def releases(self):
        """
        List of defined releases.
        """

        return [rel.name for rel in self.project.releases]

    # Issue name/ID handling methods.

    def convert_to_id(self, text):
        """
        Replace names with ``{issue ...}`` in text.

        Args:
            text (str): Text to convert.

        Returns:
            Converted text (str).
        """

        def repl(m):
            issue = self._name2issue.get(m.group(1), None)

            if issue:
                return "{issue %s}" % issue.id
            else:
                return m.group(0)

        return re.sub(re_issue_name, repl, text)

    def convert_to_name(self, text, idmap={}):
        """
        Replace ``{issue ...}`` with names in issue text.

        Args:
            text (str): Text to convert.
            idmap (dict, optional): ID mapping.

        If the ID mapping is specified and contains the issue's ID as a
        key, the replacement is the mapping value.  Otherwise, it's the
        issue's name.

        Returns:
            Converted text (str).
        """

        def repl(m):
            idx = m.group(1)
            if idx in idmap:
                return idmap[idx]
            elif idx in self._id2name:
                return self._id2name[idx]
            else:
                return "[unknown issue %s]" % idx

        return re.sub(re_issue_id, repl, text)

    def related_issues(self, issue):
        """
        Return set of all issues related to an issue.

        That is, those that mention this one, and those that this one
        mentions.
        """

        return self.issues_mentioning(issue) | self.mentioned_issues(issue)

    def relation_mapping(self):
        """
        Return a mapping of each issue to the set of its related issues.
        """

        mapping = defaultdict(set)

        for issue in self.issues:
            for other in self.mentioned_issues(issue):
                mapping[issue].add(other)
                mapping[other].add(issue)

        return mapping

    def issues_mentioning(self, issue):
        """
        Return set of all issues mentioning an issue.
        """

        return set([i for i in self.issues
                    if issue in self.mentioned_issues(i)])

    def mentioned_issues(self, issue):
        """
        Return set of all issues mentioned in an issue's text.
        """

        issues = set()
        for ref in self._issues_in_text(issue.desc):
            issues.add(ref)

        for event in issue.log_events:
            for ref in self._issues_in_text(event[3]):
                issues.add(ref)

        return issues

    def _issues_in_text(self, text):
        """
        Yield all the issues found in the given text.
        """

        for match in re.finditer(re_issue_id, text):
            idx = match.group(1)
            if idx in self._id2name:
                name = self._id2name[idx]
                yield self._name2issue[name]

    def _reassign_names(self):
        """
        Reassign issue names after changes to issue status.
        """

        self.issues.sort()
        counts = Counter()

        self._id2name = {}
        self._name2issue = {}

        for issue in sorted(self.issues, key=lambda x: x.creation_time):
            comp = issue.component.lower()
            counts[comp] += 1
            name = "%s-%d" % (comp, counts[comp])
            self._id2name[issue.id] = name
            self._name2issue[name] = issue

    # Miscellaneous other stuff.

    @property
    def issuedir(self):
        return os.path.join(self.path, self.config.issue_dir)

    def __iter__(self):
        return iter(self.issues)

    def __repr__(self):
        return "<DitzDB: %s>" % self.path
