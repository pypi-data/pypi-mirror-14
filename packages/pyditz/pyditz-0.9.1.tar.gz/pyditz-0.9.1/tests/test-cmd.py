"""
Command tests.
"""

import os
import shutil

import ditz.util
from ditz.database import DitzDB
from ditz.commands import DitzCmd
from ditz.files import read_yaml_file

from mock import Mock


def test_commands(name="example"):
    "Test commands"

    ditz.util.editor = Mock(return_value='nosuch')
    ditz.util.run_editor = Mock()

    dbname = name + "-cmd"
    if os.path.isdir(dbname):
        shutil.rmtree(dbname)

    db = DitzDB.read(name)
    db.write(dbname)

    for test in read_yaml_file("test-cmd.yaml"):
        cmd = test.pop("cmd")
        for testcase in test.pop("tests"):
            args = testcase.pop("args") or ""
            command = cmd + " " + str(args)
            print(("=== Running '%s' ===" % command))
            run_command(dbname, command, **testcase)


def run_command(dbname, cmd, **kw):
    ditzcmd = DitzCmd(dbname, usecache=True, autosave=True, highlight=False)

    for method in "line", "text", "choice", "yesno":
        if method in kw:
            effect = kw[method]
        else:
            effect = Exception('no %s input' % method)

        setattr(ditzcmd, "get" + method, Mock(spec=DitzCmd,
                                              side_effect=effect))

    ditzcmd.onecmd(cmd)


if __name__ == "__main__":
    test_commands()
