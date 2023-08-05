"""
Issue commands.
"""

from ditz import flags
from ditz.editor import DitzEditor


class CmdIssue(object):
    def do_add(self, arg):
        "add -- Add an issue"

        title = self.getline("Title: ", allowempty=False)
        desc = self.gettext("Description")

        types = {'b': flags.BUGFIX, 'f': flags.FEATURE, 't': flags.TASK}

        while True:
            reply = self.getline("Is this a (b)ugfix, (f)eature or (t)ask? ")
            if reply and reply[0] in types:
                issuetype = types[reply[0]]
                break

        choices = self.db.components
        if len(choices) >= 2:
            comp = self.getchoice("component", choices)
        else:
            comp = None

        release = None
        releases = self.db.project.releases
        choices = [r.name for r in releases if r.status == flags.UNRELEASED]
        if choices and self.getyesno("Assign to a release now?"):
            if len(choices) > 1:
                release = self.getchoice("release", choices)
            else:
                release = choices[0]
                self.write("Assigning to release", release)

        default = self.db.config.username
        prompt = 'Issue creator (enter for "%s"): ' % default
        reporter = self.getline(prompt)
        comment = self.getcomment()

        issue = self.db.add_issue(title, desc, type=issuetype,
                                  reporter=reporter, release=release,
                                  component=comp, comment=comment)

        name = self.last_issuename = self.db.issue_name(issue)
        self.write("Added issue", name)

    def do_comment(self, arg):
        "comment <issue> -- Comment on an issue"

        issue, name = self.getissue(arg, 1)
        self.write("Commenting on %s: %s" % (name, issue.title))

        comment = self.getcomment()

        if comment:
            self.db.add_comment(issue, comment)
            self.write("Comments recorded for", name)
        else:
            self.write("Empty comment, aborted")

    def do_edit(self, arg):
        "edit <issue> -- Edit an issue"

        issue, name = self.getissue(arg, 1)
        self.write("Editing %s: %s" % (name, issue.title))

        path = self.db.issue_filename(issue)
        editor = DitzEditor(path)

        while True:
            text = editor.edit()
            if not editor.error:
                break

            reply = self.getyesno("%s\n\nRe-edit to fix problem?"
                                  % editor.error, True)
            if not reply:
                return

        if editor.modified:
            self.db.edit_issue(issue, text)
            self.write("Updated %s: %s" % (name, issue.title))
        else:
            self.write("No changes made")

    def do_set_component(self, arg):
        "set-component <issue> [component] -- Set an issue's component"

        issue, name = self.getissue(arg, 1)
        comp = self.getarg(arg, 2)

        self.write("Changing the component of issue %s: %s"
                   % (name, issue.title))

        choices = self.db.components
        if len(choices) < 2:
            self.error("this project does not use multiple components")

        if comp and comp not in choices:
            self.error("unknown component: %s" % comp)

        if not comp:
            if issue.component in choices:
                choices.remove(issue.component)

            comp = self.getchoice("component", choices)

        comment = self.getcomment()

        self.db.set_component(issue, comp, comment)
        newname = self.db.issue_name(issue)

        if self.last_issuename == name:
            self.last_issuename = newname

        self.write("Issue %s is now %s.  Other issue names may have changed."
                   % (name, newname))

    def do_add_reference(self, arg):
        "add-reference <issue> -- Add a reference to an issue"

        issue, name = self.getissue(arg, 1)
        self.write("Adding a reference to %s: %s" % (name, issue.title))

        text = self.getline("Reference: ", allowempty=False)
        comment = self.getcomment()

        self.db.add_reference(issue, text, comment=comment)
        self.write("Added reference to", name)

    def do_start(self, arg):
        "start <unstarted_issue> -- Start work on an issue"

        issue, name = self.getissue(arg, 1)

        if issue.status == flags.IN_PROGRESS:
            self.error("already marked as", flags.STATUS[issue.status])

        self.write("Starting work on %s: %s" % (name, issue.title))
        comment = self.getcomment()

        self.db.set_status(issue, flags.IN_PROGRESS, comment=comment)
        self.write("Recorded start of work for", name)

    def do_stop(self, arg):
        "stop <started_issue> -- Stop work on an issue"

        issue, name = self.getissue(arg, 1)

        if issue.status == flags.PAUSED:
            self.error("already marked as", flags.STATUS[issue.status])

        self.write("Stopping work on %s: %s" % (name, issue.title))
        comment = self.getcomment()

        self.db.set_status(issue, flags.PAUSED, comment=comment)
        self.write("Recorded stopping of work for", name)

    def do_assign(self, arg):
        "assign <issue> [release] -- Assign an issue to a release"

        issue, name = self.getissue(arg, 1)

        if issue.release:
            self.write("Issue %s currently assigned to release %s"
                       % (name, issue.release))
        else:
            self.write("Issue %s not currently assigned to any release" % name)

        release = self.getarg(arg, 2)

        if not release:
            releases = self.db.project.releases
            choices = [r.name for r in releases
                       if r.status == flags.UNRELEASED]

            if issue.release and issue.release in choices:
                choices.remove(issue.release)

            if not choices:
                self.error("no other release available")

            if len(choices) > 1:
                release = self.getchoice("release", choices)
            else:
                release = choices[0]

        if release == issue.release:
            self.error("already assigned to release %s" % release)

        if not self.db.get_release(release):
            self.error("no release with name %s" % release)

        self.write("Assigning to release", release)
        comment = self.getcomment()

        self.db.set_release(issue, release, comment=comment)
        self.write("Assigned", name, "to", release)

    def do_unassign(self, arg):
        "unassign <assigned_issue> -- Unassign an issue from any releases"

        issue, name = self.getissue(arg, 1)

        if not issue.release:
            self.error("not assigned to a release")

        relname = issue.release
        self.write("Unassigning %s: %s" % (name, issue.title))
        comment = self.getcomment()

        self.db.set_release(issue, None, comment=comment)
        self.write("Unassigned", name, "from", relname)

    def do_close(self, arg):
        "close <open_issue> -- Close an issue"

        issue, name = self.getissue(arg, 1)

        self.write("Closing issue %s: %s" % (name, issue.title))

        disp = flags.DISPOSITION
        revdisp = {disp[x]: x for x in disp}
        choices = (disp[flags.FIXED], disp[flags.WONTFIX], disp[flags.REORG])
        choice = self.getchoice("disposition", choices)
        disp = revdisp[choice]

        comment = self.getcomment()

        self.db.set_status(issue, flags.CLOSED, disposition=disp,
                           comment=comment)

        self.write("Closed issue", name, "with disposition", choice)

    def do_drop(self, arg):
        "drop <issue> -- Drop an issue"

        issue, name = self.getissue(arg, 1)

        self.db.drop_issue(issue)
        self.write("Dropped %s.  Other issue names may have changed." % name)
