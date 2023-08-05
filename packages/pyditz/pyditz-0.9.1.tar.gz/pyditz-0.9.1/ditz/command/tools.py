"""
Utility commands.
"""

import os


class CmdTools(object):
    def do_ipython(self, arg):
        "ipython -- enter embedded IPython interpreter"

        try:
            from IPython import embed
        except ImportError:
            self.error("IPython is not available")

        embed()

    def do_shell(self, arg):
        "shell -- run a system command"
        os.system(arg)
