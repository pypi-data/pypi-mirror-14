"""
Demo plugin.
"""

from ditz.commands import CommandSet

class AdventCommands(CommandSet):
    name = 'advent'
    description = 'adventuring commands'

    def do_xyzzy(self, arg):
        self.write("Nothing happens.")

    def help_xyzzy(self):
        self.write("xyzzy -- a secret magic word")

    def do_plugh(self, arg):
        "plugh -- another secret magic word"
        self.write("Nothing happens.")
