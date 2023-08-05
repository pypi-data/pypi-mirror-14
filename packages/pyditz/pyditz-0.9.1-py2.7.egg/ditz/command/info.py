"""
Info commands.
"""

import re
import sys
import six

from ditz.config import config as userconfig
from ditz import display


class CmdInfo(object):
    def do_todo(self, arg):
        "todo [-a,all] [release] -- Generate todo list"

        flag = self.getarg(arg, 1)
        if flag in ("-a", "all"):
            release = self.getrelease(arg, 2, optional=True)
            closed = True
        else:
            release = self.getrelease(arg, 1, optional=True)
            closed = False

        text = display.show_todo(self.db, release, closed)
        self.write(text)

    def do_show(self, arg):
        "show <issue> -- Describe a single issue"

        issue, _ = self.getissue(arg, 1)
        text = display.show_issue(self.db, issue)
        self.write(text)

    def do_log(self, arg):
        """log [count] -- Show recent activity

        If no count is given, the value is taken from the 'log_lines'
        configuration value (default: 5).  If a count is given, it becomes
        the new default.  A count of zero means show all log entries."""

        if not hasattr(self, "last_log"):
            self.config.add('lines', 5)
            self.last_log = self.config.getint('lines')

        count = self.getint(arg, 1)
        if count is None:
            count = self.last_log
        else:
            self.last_log = count

        text = display.log_events(self.db, count=count, verbose=True)
        self.write(text)

    def do_shortlog(self, arg):
        """shortlog [count] -- Show recent activity (short form)

        If no count is given, the value is taken from the 'shortlog_lines'
        configuration value (default: 20).  If a count is given, it becomes
        the new default.  A count of zero means show all log entries."""

        if not hasattr(self, "last_shortlog"):
            self.config.add('lines', 20)
            self.last_shortlog = self.config.getint('lines')

        count = self.getint(arg, 1)
        if count is None:
            count = self.last_shortlog
        else:
            self.last_shortlog = count

        text = display.log_events(self.db, count=count)
        self.write(text)

    def do_changelog(self, arg):
        "changelog <release> -- Generate a changelog for a release"

        name = self.getrelease(arg, 1)
        text = display.show_changelog(self.db, name)
        self.write(text)

    def do_list(self, arg):
        "list [<regexp>] -- List all issues, optionally matching a regexp"

        try:
            regexp = re.compile(arg or ".*")
        except re.error as msg:
            self.error("invalid regexp: %s" % six.text_type(msg))

        text = display.show_grep(self.db, regexp)
        self.write(text or "No matching issues")

    def do_status(self, arg):
        "status [release] -- Show project status"

        release = self.getrelease(arg, 1, optional=True)
        text = display.show_status(self.db, release)
        self.write(text)

    def do_releases(self, arg):
        "releases -- Show releases"

        text = display.show_releases(self.db)
        self.write(text or "No releases")

    def do_config(self, arg):
        "config [<section>] -- show configuration settings"

        section = self.getarg(arg, 1)

        if not section:
            userconfig.write(sys.stdout)
        elif userconfig.has_section(section):
            for name in sorted(userconfig.options(section)):
                self.write(name, '=', userconfig.get(section, name))
        else:
            self.error("no config section called '%s'" % section)

    def do_path(self, arg):
        "path -- show the root Ditz database path"

        self.write(self.db.path)
