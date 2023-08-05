"""
Internal Ditz objects.
"""

import os
import re
import yaml
import hashlib
import random
import six

from datetime import datetime, timedelta
from functools import total_ordering

from .util import (make_directory, check_value, to_unicode,
                   default_name, default_email, DitzError)

from .flags import (STATUS, RELSTATUS, RELEASED, UNRELEASED, BUGFIX,
                    FEATURE, TASK, DISPOSITION, UNSTARTED, TYPE, SORT,
                    CLOSED)

from .files import read_object_file, write_yaml_file, write_config
from .config import config

from . import schemas

# Regexp matching start of progress on an issue.
re_start = re.compile(r'to in.progress')

# Regexp matching end of progress on an issue.
re_stop = re.compile(r'(from in.progress|closed with disposition)')


class DitzObject(yaml.YAMLObject):
    """
    Base class of a Ditz object appearing in a YAML file.

    Attributes:
        ditz_tag (str): Base YAML tag prefix.
        yaml_tag (str): YAML tag written to file.
        filename (str): YAML filename to read/write.
        attributes (list): List of recognized attributes.
        log_events (list): List of events.
    """

    yaml_loader = yaml.SafeLoader

    ditz_tag = "!ditz.rubyforge.org,2008-03-06"
    yaml_tag = None
    filename = None
    schema = None
    attributes = []

    def write(self, dirname="."):
        """
        Write object to its YAML file.

        Args:
            dirname (str, optional): Directory to write file into.
        """

        make_directory(dirname)
        path = os.path.join(dirname, self.filename)
        write_yaml_file(path, self)

    def event(self, username, text, comment=None, timestamp=None):
        """
        Add an event to the object's ``log_events`` list.

        Args:
            username (str): User name.
            text (str): Event description.
            comment (str, optional): User comment.
            timestamp (datetime, optional): Time of the event.
        """

        time = timestamp or datetime.now()
        text = to_unicode(text)
        comment = to_unicode(comment) or ""
        self.log_events.append([time, username, text, comment])

    def validate(self):
        """
        Check the object is a valid Ditz object.
        """

        if self.schema:
            schemas.validate(self, self.schema, self.filename)
        else:
            raise DitzError("no schema defined for %s"
                            % self.__class__.__name__)


class Project(DitzObject):
    yaml_tag = DitzObject.ditz_tag + '/project'
    filename = "project.yaml"
    schema = schemas.project

    #: Attributes that get saved to file.
    attributes = ["name", "version", "components", "releases"]

    #: Name of the project.
    name = ""

    #: List of components.  Each entry is a :class:`Component`.
    components = []

    #: List of releases.  Each entry is a :class:`Release`.
    releases = []

    def __init__(self, name, version=0.5):
        self.name = to_unicode(name)
        self.version = version
        self.components = [Component(name)]
        self.releases = []


class Release(DitzObject):
    yaml_tag = DitzObject.ditz_tag + '/release'
    schema = schemas.release

    #: Attributes that get saved to file.
    attributes = ["name", "status", "release_time", "log_events"]

    #: Name of the release.
    name = None

    #: Time it was released, or None.
    release_time = None

    #: List of log events.  Each entry is a tuple of (time, username, text,
    #: comment).
    log_events = []

    def __init__(self, name, status=UNRELEASED, release_time=None):
        self.name = to_unicode(name)
        self.status = status
        self.release_time = release_time
        self.log_events = []

        self.set_status(status)

    def set_status(self, status):
        check_value("status", status, RELSTATUS)
        self.status = status

    @property
    def released(self):
        "Whether release has actually been released."
        return self.status == RELEASED

    @property
    def description(self):
        if not self.released:
            tag = "unreleased"
        else:
            tag = "released %s" % (self.release_time.strftime("%Y-%m-%d"))

        return "%s (%s)" % (self.name, tag)

    def __repr__(self):
        return "<Release: %s>" % self.name


class Component(DitzObject):
    yaml_tag = DitzObject.ditz_tag + '/component'
    attributes = ["name"]
    schema = schemas.component

    #: Name of the component.
    name = ""

    def __init__(self, name):
        self.name = to_unicode(name)

    def __repr__(self):
        return "<Component: %s>" % self.name


@total_ordering
class Issue(DitzObject):
    yaml_tag = DitzObject.ditz_tag + '/issue'
    template = "issue-%s.yaml"
    schema = schemas.issue

    #: Attributes that get saved to file.
    attributes = ["title", "desc", "type", "component", "release",
                  "reporter", "status", "disposition", "creation_time",
                  "references", "id", "log_events"]

    #: List of references.  Each entry is a string.
    references = []

    #: List of log events.  Each entry is a tuple of (time, username, text,
    #: comment).
    log_events = []

    def __init__(self, title, desc="", type=BUGFIX, status=UNSTARTED,
                 disposition=None, creation_time=None, reporter=""):
        self.title = to_unicode(title.strip())
        self.desc = to_unicode(desc.strip())
        self.component = None
        self.release = None
        self.reporter = to_unicode(reporter)

        self.set_type(type)
        self.set_status(status)
        self.set_disposition(disposition)

        self.creation_time = creation_time or datetime.now()
        self.id = self.make_id()

        self.references = []
        self.log_events = []

    @property
    def name(self):
        "Name of the issue.  This is the same as its title."
        return self.title

    @property
    def longname(self):
        "Name of the issue, with (bug) or (feature) appended."
        if self.bugfix:
            return self.title + " (bug)"
        elif self.feature:
            return self.title + " (feature)"
        else:
            return self.title

    @property
    def closed(self):
        "Whether the issue is closed."
        return self.status == CLOSED

    @property
    def bugfix(self):
        "Whether the issue is a bugfix."
        return self.type == BUGFIX

    @property
    def feature(self):
        "Whether the issue is a feature."
        return self.type == FEATURE

    @property
    def task(self):
        "Whether the issue is a task."
        return self.type == TASK

    @property
    def filename(self):
        return self.template % self.id

    @property
    def progresstime(self):
        "Total seconds the issue's state has been in-progress."
        total = timedelta()
        start = None

        for time, _, event, _ in self.log_events:
            if re_start.search(event):
                start = time
            elif re_stop.search(event) and start is not None:
                total += time - start
                start = None

        if start is not None:
            total += datetime.now() - start

        return total.total_seconds()

    def set_type(self, type):
        check_value("type", type, TYPE)
        self.type = type

    def set_status(self, status):
        check_value("status", status, STATUS)
        self.status = status

    def set_disposition(self, disposition):
        if disposition:
            check_value("disposition", disposition, DISPOSITION)

        self.disposition = disposition

    def add_reference(self, reference):
        reference = to_unicode(reference)
        self.references.append(reference)
        return len(self.references)

    def grep(self, regexp):
        for attr in "title", "desc", "reporter":
            if regexp.search(getattr(self, attr)):
                return True

        for ref in self.references:
            if regexp.search(ref):
                return True

        for event in self.log_events:
            if regexp.search(event[3]):
                return True

        return False

    def make_id(self):
        data = [self.creation_time, random.random(),
                self.reporter, self.title, self.desc]

        string = "\n".join([six.text_type(item) for item in data])
        return hashlib.sha1(string.encode('utf-8')).hexdigest()

    def __eq__(self, other):
        if hasattr(other, "id"):
            return self.id == other.id

        return False

    def __lt__(self, other):
        this = (SORT[self.status], self.creation_time)
        that = (SORT[other.status], other.creation_time)
        return this < that

    def __hash__(self):
        return int(self.id, 16)

    def __repr__(self):
        return "<Issue: %s>" % self.id


class Config(DitzObject):
    yaml_tag = DitzObject.ditz_tag + '/config'
    filename = ".ditz-config"
    attributes = ["name", "email", "issue_dir"]

    def __init__(self, name, email, issue_dir="issues"):
        self.name = to_unicode(name)
        self.email = to_unicode(email)
        self.issue_dir = issue_dir

    @property
    def username(self):
        return "%s <%s>" % (self.name, self.email)

    def validate(self):
        if not hasattr(self, 'issue_dir'):
            raise DitzError("'issue_dir' not defined")

    def __repr__(self):
        return "<Config: %s>" % self.name


def find_config(basedir=".", error=False, search=True):
    """
    Find Ditz configuration in (or possibly above) a base directory.

    Return the directory and corresponding Config object.
    """

    basedir = os.path.realpath(basedir)
    curdir = basedir

    issuedirs = config.get('config', 'issuedirs').split()

    while True:
        # If Ditz config found, read it.
        path = os.path.join(curdir, Config.filename)
        if os.path.exists(path):
            return curdir, read_object_file(path)

        # If there's an issue directory containing a project file, use
        # that.
        for dirname in issuedirs:
            path = os.path.join(curdir, dirname, Project.filename)
            if os.path.exists(path):
                name = default_name()
                email = default_email()
                conf = Config(name, email, dirname)
                write_config(conf)
                return curdir, conf

        # Otherwise, go to parent directory.
        pardir = os.path.split(curdir)[0]

        # If it's not found, or we're at the top, give up.
        if pardir == curdir or not search:
            if error:
                where = "in or above" if search else "in"
                raise DitzError("can't find '%s' %s '%s'"
                                % (Config.filename, where, basedir))
            else:
                return None, None

        curdir = pardir
