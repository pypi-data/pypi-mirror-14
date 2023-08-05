"""
Main console program.
"""

from __future__ import print_function

import os
import sys
import argparse

from .settings import Settings
from .config import config, config_path
from .logger import init_logging
from .plugin import loader
from .util import terminal_size
from .version import __version__

# Name of the main program.
progname = "pyditz"


def main(args=sys.argv[1:]):
    # Build command parser.
    parser = argparse.ArgumentParser(prog=progname)

    parser.add_argument("--version", action="version",
                        version="%(prog)s version " + __version__)

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="be verbose about things")

    parser.add_argument("--traceback", action="store_true",
                        help="print traceback on error")

    group = parser.add_argument_group("global arguments")

    group.add_argument("-i", "--issue-dir", type=str, metavar="DIR",
                       help="use the given issue directory")

    group.add_argument("-u", "--user-config", type=str, metavar="FILE",
                       help="use the given user config file")

    group.add_argument("-c", "--config", type=str, action="append",
                       metavar="SECTION.OPTION=VALUE",
                       help="set a config option explicitly")

    group.add_argument("-S", "--no-search", action="store_true",
                       help="turn off searching of parent directories")

    group.add_argument("-P", "--no-pager", action="store_true",
                       help="turn off paging of output")

    group.add_argument("-H", "--no-highlight", action="store_true",
                       help="turn off syntax highlighting")

    group.add_argument("-X", "--no-plugins", action="store_true",
                       help="turn off loading of external plugins")

    group.add_argument("-V", "--no-vcs", action="store_true",
                       help="turn off use of version control")

    group = parser.add_argument_group("command arguments")

    group.add_argument("-m", "--comment", type=str, metavar="STRING",
                       help="specify a comment")

    group.add_argument("-n", "--no-comment", action="store_true",
                       help="skip asking for a comment")

    # Prepend arguments from environment, if any.
    flags = os.environ.get("DITZFLAGS", None)
    if flags:
        args = flags.split() + args

    # Parse arguments.
    opts, args = parser.parse_known_args(args)

    try:
        # Initialise.
        init_logging(opts.verbose)

        if opts.user_config:
            config.set_file(opts.user_config)

        if opts.config:
            for setting in opts.config:
                config.set_option(setting)

        settings = Settings(autosave=True, usecache=True)

        if opts.no_highlight:
            settings.highlight = False
        else:
            settings.highlight = config.getboolean('highlight', 'enable')

        if opts.no_vcs:
            settings.versioncontrol = False
        else:
            settings.versioncontrol = config.getboolean('vcs', 'enable')

        cols, lines = terminal_size()
        settings.termlines = 0 if opts.no_pager else lines
        settings.termcols = cols

        settings.externalplugins = not opts.no_plugins
        settings.searchparents = not opts.no_search
        settings.nocomment = opts.no_comment
        settings.comment = opts.comment

        # Set up plugin load paths.
        if settings.externalplugins:
            # Load plugins from user config directory.
            path = config_path("plugins")
            loader.add_path(path)

            # Load setuptools plugins.
            loader.add_entrypoint('ditz.plugin')

        # Load plugins.
        loader.load()

        # Build common options to pass to Ditz command.
        path = opts.issue_dir or "."

        # Run things.
        from .commands import DitzCmd

        if not args:
            cmd = DitzCmd(path, settings=settings, interactive=True)
            cmd.cmdloop()
        else:
            cmd = DitzCmd(path, settings=settings)
            command = " ".join(args)
            if not cmd.onecmd(command):
                sys.exit(99)

    except KeyboardInterrupt:
        if opts.traceback:
            raise
        else:
            print()
            sys.exit("%s: aborted" % progname)

    except Exception as msg:
        if opts.traceback:
            raise
        else:
            sys.exit("%s: error: %s" % (progname, msg))


if __name__ == "__main__":
    main()
