"""
Ditz command handler.
"""

from __future__ import print_function

import os
import sys
import six

from cmd import Cmd
from textwrap import wrap

from .command import CmdProject, CmdIssue, CmdInfo, CmdTools

from .database import DitzDB
from .settings import Settings
from .config import config as userconfig
from .config import ConfigSection
from .colorize import colorize
from .objects import Project, Config, find_config
from .files import write_config
from .plugin import Plugin, get_plugins
from .util import print_columns, default_name, default_email, DitzError

from six.moves import input


class DitzCmd(Cmd, CmdProject, CmdIssue, CmdInfo, CmdTools):
    #: The :class:`DitzDB` database.
    db = None

    #: Whether running interactively.
    interactive = False

    #: Last issue name mentioned.
    last_issuename = None

    #: Last release name mentioned.
    last_releasename = None

    def __init__(self, path=".", settings=None, interactive=False, **kw):
        Cmd.__init__(self)

        #: Command prompt.
        self.prompt = "Ditz: "

        #: Pager prompt.
        self.moreprompt = "-- More (Y/n/q) --"

        #: Global settings.
        self.settings = settings or Settings(**kw)

        #: Configuration variables.
        self.config = ConfigSection(None, 'command', userconfig)

        #: Pathname of the database.
        self.dbpath = os.path.realpath(path)

        self.interactive = interactive
        self.last_issuename = None
        self.last_releasename = None

        # In interactive mode, write status (and do interactive setup
        # if creating a new database).
        dirname, _ = find_config(self.dbpath,
                                 search=self.settings.searchparents)

        if not dirname:
            self.write("Setting up Ditz database in", path)
            self.write()
            self.setup()
        elif self.interactive:
            path = os.path.realpath(dirname)
            self.write("Reading Ditz database in", path)
            self.write()

        # Read the database.
        self.db = DitzDB.read(self.dbpath, settings=settings)

        # Register plugin commands.
        for cls in get_plugins(CommandSet):
            for name in dir(cls):
                if name.startswith(("do_", "help_")):
                    func = six.get_unbound_function(getattr(cls, name))
                    meth = six.create_bound_method(func, self)
                    setattr(DitzCmd, name, meth)

        # Set the list of known commands.
        self.commands = set()
        for name in self.get_names():
            if name.startswith("do_"):
                self.commands.add(name[3:])

        # Highlight the prompts if required.
        if self.interactive and self.settings.highlight:
            self.prompt = colorize(self.prompt.strip()) + " "
            self.moreprompt = colorize(self.moreprompt)

    def setup(self, oldconfig=None):
        """
        Set up a database interactively.
        """

        config = self.getconfig(oldconfig)
        if config:
            name = config.name
            email = config.email
            issuedir = config.issue_dir
        else:
            return False

        path = os.path.join(self.dbpath, issuedir, Project.filename)

        if os.path.exists(path):
            if write_config(config):
                self.write()
                self.write("Configuration written")
        else:
            default = os.path.basename(self.dbpath)
            project = self.getline("Project name", default)
            if not project:
                return False

            db = DitzDB(project, name, email, issuedir, self.dbpath,
                        settings=self.settings)
            db.write()

            self.write()
            self.write("Ditz database created in", self.dbpath)

        return True

    # Builtin command methods.

    def do_init(self, arg):
        "init -- Initialize the issue database for a new project"

        # This is a no-op, kept for Ditz compatibility, since
        # initialization is automatically done if no database exists.
        pass

    def do_reconfigure(self, arg):
        "reconfigure -- Rerun configuration script"

        self.setup(self.db.config)

    def do_help(self, arg):
        "help [command] -- Display help, optionally on a command"

        if arg:
            arg = self.findcmd(arg)

        if arg is not None:
            Cmd.do_help(self, arg)

    def do_quit(self, arg):
        "quit -- quit the interactive command loop"
        sys.exit()

    do_EOF = do_quit

    # Completion methods.

    def match_issue(self, text, line, beg, end):
        return startswith(self.db.issue_names, text)

    complete_add_reference = match_issue
    complete_assign = match_issue
    complete_close = match_issue
    complete_comment = match_issue
    complete_drop = match_issue
    complete_edit = match_issue
    complete_set_component = match_issue
    complete_show = match_issue
    complete_start = match_issue
    complete_stop = match_issue
    complete_unassign = match_issue

    def match_release(self, text, line, beg, end):
        return startswith(self.db.releases, text)

    complete_archive = match_release
    complete_changelog = match_release
    complete_release = match_release
    complete_status = match_release
    complete_todo = match_release

    def match_command(self, text):
        return startswith(self.commands, text)

    # Command hook methods.

    def onecmd(self, cmdline):
        # Get command and arguments.
        bits = cmdline.strip().split(None, 1)
        cmd = args = ""

        if len(bits) == 1:
            cmd = bits[0]
        elif len(bits) > 1:
            cmd, args = bits

        # Run it.
        retval = False

        try:
            cmd = self.config.name = self.findcmd(cmd)
            Cmd.onecmd(self, cmd + " " + args)
            retval = True
        except DitzError as msg:
            self.write("Error:", msg)
        except (KeyboardInterrupt, EOFError):
            self.write()
            self.write("Aborted")

        return None if self.interactive else retval

    def findcmd(self, cmd):
        if cmd:
            # Substitute aliases, if any.
            if userconfig.has_option('alias', cmd):
                cmd = userconfig.get('alias', cmd)

            # Replace hyphens in command, to support original Ditz-style
            # commands.
            cmd = cmd.replace('-', '_')

            # Do completion on it.
            if cmd not in self.commands:
                matches = self.match_command(cmd)
                if len(matches) == 1:
                    cmd = matches[0]
                elif len(matches) > 1:
                    self.error("ambiguous command: %s (%s)"
                               % (cmd, ", ".join(matches)))

        return cmd

    def emptyline(self):
        return self.onecmd("todo")

    def default(self, arg):
        msg = "unknown command: " + arg
        if self.interactive:
            msg += " (type 'help' for a list)"

        self.error(msg)

    # Input/output methods.

    def getarg(self, arg, idx):
        """
        Get a string argument.

        Args:
            arg (str): Raw command string.
            idx (int): Argument index (numbered from 1).

        Returns:
            Value (str), or None if out of range.
        """

        args = arg.split()
        if 0 < idx <= len(args):
            return args[idx - 1]

        return None

    def getint(self, arg, idx, default=None):
        """
        Get an integer argument.

        Args:
            arg (str): Raw command string.
            idx (int): Argument index (numbered from 1).
            default (int, optional): Default value.

        Returns:
            Value (int), or None.
        """

        value = self.getarg(arg, idx)
        if not value:
            return default

        try:
            return int(value)
        except ValueError:
            self.error("expected an integer, not", value)

    def getissue(self, arg, idx):
        """
        Get an issue by name or ID.  Return it and its assigned name.

        Args:
            arg (str): Raw command string.
            idx (int): Argument index (numbered from 1).

        Returns:
            Tuple(Issue, str).
        """

        name = self.getarg(arg, idx)
        if not name and self.last_issuename:
            name = self.last_issuename

        if not name:
            self.error("no issue specified")

        self.last_issuename = name
        issue = self.db.get_issue(name)

        if not issue:
            issues = [i for i in self.db.issues if i.id.startswith(name)]
            count = len(issues)
            if count == 1:
                issue = issues.pop()
            elif count > 1:
                self.error("%d issues match ID '%s'" % (count, name))

        if not issue:
            self.error("no issue with name or ID '%s'" % name)

        return issue, self.db.issue_name(issue)

    def getrelease(self, arg, idx, optional=False):
        """
        Get a release by name.

        Args:
            arg (str): Raw command string.
            idx (int): Argument index (numbered from 1).
            optional (bool): Whether to allow unspecified.

        Returns:
            Release name (str).
        """

        name = self.getarg(arg, idx)
        if not name and optional:
            return None

        if not name and self.last_releasename:
            name = self.last_releasename

        if not name:
            self.error("no release specified")

        self.last_releasename = name
        if name not in self.db.releases:
            self.error("no release with name '%s'" % name)

        return name

    def getline(self, prompt="> ", default="", allowempty=True):
        """
        Get a single line of input.

        Args:
            prompt (str): Prompt string.
            default (str): Default value.
            allowempty (bool): Whether value is optional.

        Returns:
            Reply (str).
        """

        if default:
            prompt = "%s (default '%s'): " % (prompt, default)

        while True:
            if self.use_rawinput:
                reply = input(prompt)
            else:
                self.stdout.write(prompt)
                self.stdout.flush()
                reply = self.stdin.readline()

            if not len(reply.strip()):
                reply = default

            reply = reply.rstrip('\r\n')
            if reply or allowempty:
                return reply

    def gettext(self, title=None, prompt="> ", endchar='.'):
        """
        Get multiline text.

        Args:
            title (str): Initial title text.
            prompt (str): Prompt for each line of input.
            endchar (str): Character terminating input.

        Returns:
            Text (str).
        """

        if title:
            self.write(title + " (ctrl-c to abort, %s to finish)" % endchar)

        lines = []
        while True:
            line = self.getline(prompt)
            if line == endchar:
                return "\n".join(lines)

            lines.append(line)

    def getchoice(self, thing, choices):
        """
        Get a choice of several things.

        Args:
            thing (str): Description of thing being chosen.
            choices (list): List of available options.

        Returns:
            Choice made (str).
        """

        items = []
        for num, entry in enumerate(choices, 1):
            item = "%3d) %s" % (num, entry)
            items.append(item)

        print_columns(items)
        prompt = "Choose a %s (1--%d): " % (thing, len(choices))

        while True:
            reply = self.getline(prompt)

            try:
                return choices[int(reply) - 1]
            except (ValueError, IndexError):
                pass

    def getcomment(self):
        """
        Get a comment string.

        Returns:
            Comment text (str).
        """

        if self.settings.nocomment:
            return ""
        elif not self.interactive and self.settings.comment:
            return self.settings.comment
        else:
            return self.gettext("Comments")

    def getyesno(self, question, default=False):
        """
        Get the answer to a yes/no question.

        Args:
            question (str): The question.
            default (bool): Default if no reply given.

        Returns:
            Reply (bool).
        """

        prompt = question + " [%s] " % ("yes" if default else "no")

        while True:
            reply = self.getline(prompt)
            if not reply:
                return default
            if reply[0] in "yY":
                return True
            elif reply[0] in "nN":
                return False

    def getconfig(self, oldconfig=None):
        """
        Prompt for and return database configuration info.
        """

        default = oldconfig.name if oldconfig else default_name()
        name = self.getline("Your name", default)

        default = oldconfig.email if oldconfig else default_email()
        email = self.getline("Your email", default)

        issuedirs = userconfig.get('config', 'issuedirs').split()
        issuedir = issuedirs[0] if issuedirs else ".ditz-issues"
        default = oldconfig.issue_dir if oldconfig else issuedir
        issuedir = self.getline("Issue directory", default)

        return Config(name, email, issuedir)

    def write(self, *args):
        """
        Write the given list of arguments to stdout.

        Also performs syntax highlighting and paging.
        """

        def output(args):
            args = [six.text_type(s) for s in args]
            items = " ".join(args).split("\n")
            cols = self.settings.termcols
            trunc = userconfig.get('ui', 'linetrunc')

            for line in items:
                if not cols or len(line) <= cols:
                    yield line
                elif trunc:
                    yield line[:cols-len(trunc)] + trunc
                else:
                    for text in wrap(line, width=cols):
                        yield text

        if args:
            lines = self.settings.termlines

            for num, line in enumerate(output(args), 1):
                if not six.PY3:
                    line = line.encode('utf-8')

                if self.settings.highlight:
                    line = colorize(line)

                print(line)
                if lines and num % (lines - 1) == 0:
                    reply = input(self.moreprompt)
                    if reply and reply[0] in "nqNQ":
                        break
        else:
            print()

    def error(self, *args):
        """
        Signal an error.
        """

        raise DitzError(" ".join(args))

    # Miscellaneous other stuff.

    def unimplemented(self):
        """
        Write a 'not implemented yet' message.
        """

        cmd = self.lastcmd.split()[0]
        self.error("'%s' is not implemented yet" % cmd)


class CommandSet(Plugin):
    """
    Base class for plugin commands.
    """

    category = "command"

    #: Name of the command set.
    name = None

    #: One-line description (currently unused).
    description = "undocumented"


def startswith(items, text):
    return [x for x in items if x.startswith(text)]
