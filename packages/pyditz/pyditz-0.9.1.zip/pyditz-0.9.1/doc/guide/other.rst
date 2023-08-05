=================
 Other Commmands
=================

Here are a few other |PD| commands you might find useful:

:kbd:`validate`
    Do a check on the |PD| issue database to make sure it's consistent, and
    fix any fixable problems (and warn about unfixable ones).

:kbd:`config`
    Print the current configuration settings.  This includes the defaults
    and any settings you've overridden in your :doc:`config`.  If you give
    a section argument, only the settings for that section are printed.
    For example, ``config ui`` will print only the user interface
    settings.

:kbd:`path`
    Print the pathname of the top-level directory where the |PD| database
    is found.  This is the root pathname of your project.

:kbd:`shell`
    Execute a shell command outside the |PD| command loop.  You can also do
    this using ``!``.  For example: ``!ls`` will list the current directory
    (on Linux, at least).
