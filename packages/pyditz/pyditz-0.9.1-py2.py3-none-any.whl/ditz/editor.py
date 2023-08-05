"""
Text editor.
"""

from __future__ import print_function

import os
import yaml
import tempfile

from . import util
from .files import read_file, read_yaml_file
from .util import DitzError


class DitzEditor(object):
    """
    An editor for Ditz objects.
    """

    prefix = 'tmp-'
    suffix = '.yaml'
    textmode = False
    filetag = "<input>"

    def __init__(self, path):
        #: Original text.
        self.original = read_file(path)

        #: The text after editing.
        self.text = self.original

        #: Error message from last edit, or None.
        self.error = None

    def edit(self):
        "Edit the text and return it."

        # Get editor program.
        program = util.editor()
        if not program:
            raise DitzError("no text editor is configured")

        # Write text to a temp file.
        fp, filename = tempfile.mkstemp(prefix=self.prefix,
                                        suffix=self.suffix,
                                        text=self.textmode)
        os.write(fp, self.text.encode('utf-8'))
        os.close(fp)

        try:
            # Run the editor.
            util.run_editor(program, filename)

            # Get the edited text.
            self.text = read_file(filename)

            # Check for validity.
            err = self.validate(filename)
            if err:
                self.error = err.replace(filename, self.filetag)
            else:
                self.error = None

        finally:
            # Clean up.
            os.remove(filename)

        return self.text

    def validate(self, path):
        "Return validation error text or None."

        try:
            obj = read_yaml_file(path)
            obj.validate()
        except yaml.error.YAMLError as err:
            return str(err)
        except DitzError as err:
            return str(err)

        return None

    @property
    def modified(self):
        "Whether text has been modified."
        return self.text != self.original


if __name__ == "__main__":
    path = "../bugs/issue-3d1596d37cbd170f512eb939b97f5f22a3834c79.yaml"
    from ditz.objects import DitzObject   # noqa

    editor = DitzEditor(path)
    print(editor.edit())

    print("Modified:", editor.modified)
    print("Error:", editor.error)
