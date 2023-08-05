=====================
 Editing Issue Files
=====================

.. versionadded:: 0.9
   Editing of issue files.

There are some occasions when you might want to edit an issue file
directly:

* To change an attribute that |PD| doesn't (yet) let you do with any other
  command (e.g., changing the issue type from a feature to a task).

* To clean up the issue text (e.g., correct speling mistakes).

You could, of course, just go into the issue directory and edit the issue
file outside of |PD|; nothing is stopping you.  But as a convenience,
there's also an :kbd:`edit` command.  This has a couple of advantages:

* It saves you having to search for the correct issue file.

* After the edit, checks are done to make sure that you haven't
  inadvertently produced an inconsistent or unreadable file.

Configuring the editor
======================

In order to edit issue files, you need to tell |PD| the editor you want to
use.  Here's how one is found:

* First, it checks the 'editor' setting in your :doc:`config`.  If set,
  that is used.

* Next, the environment variables ``DITZEDITOR``, ``EDITOR`` and ``VISUAL``
  are examined, in that order.  If any is set, it's used.

* Finally, if the operating system has a suitable default, that's used.  On
  Linux, that's ``vi``.  On Windows, there is no default; you'll have to
  explicitly specify an editor using one of the methods above.

  .. warning::

     On Windows, ``notepad`` and ``wordpad`` are not suitable editors.
     Instead, I recommend you get and use `Notepad++`__.

     __ https://notepad-plus-plus.org

Editing an issue
================

To edit an issue, you can either type |CMD| :kbd:`edit` at a shell prompt,
or just :kbd:`edit` at the |PDP| prompt, specifying the issue you want to
edit.  (From the |PDP| prompt, if no issue is given, the last issue
mentioned in a command will be used.)

Your editor will be invoked on the raw issue text; this is in YAML format,
and you can see an example in :doc:`database`.  You should do your editing,
save the current file, and exit.  After that, one of several things will
happen:

* If you didn't make any changes, |PD| will inform you of the fact and
  nothing will be done.

* If your edits produced an invalid file (either unreadable YAML or an
  invalid |PD| issue format) you'll be told what's wrong and asked whether
  you want to re-edit the text to fix the problem.  If you decide not to,
  the changes are abandoned.

* If your edits were accepted, the issue will be updated accordingly.
