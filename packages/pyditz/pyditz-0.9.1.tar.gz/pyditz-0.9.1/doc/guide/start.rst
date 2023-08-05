=================
 Getting Started
=================

.. highlight:: ditzsession

There are two ways to use |PD| from the command line: either by running a
single command, which |PD| will run and then exit, or (if no command is
given), entering a command loop with a |PDP| prompt.  The examples in this
guide will use the command loop.

To begin using |PD| in a project, you will need to initialize an issue
database.  This can be done explicitly using the :kbd:`init` command, or,
if entering the command loop, it will be done if needed.

When initializing a database, |PD| will prompt you for some details about
you and your project.  You can set global defaults for some of these in
your :doc:`config`.  Here's an example of what happens when you type |CMD|
in a place with no issue database:

.. prompt: Your name .*:
.. reply:

.. prompt: Your email .*:
.. reply:

.. prompt: Issue directory .*:
.. reply:

.. prompt: Project name .*:
.. reply:  helloworld

.. literalinclude:: /include/init.txt

By default, when |PD| creates a new database in a directory, it writes a
|CONF| file there containing the settings.  If you want to change these at
any point, you can either manually edit this file, or run the
:kbd:`reconfigure` command and get prompted for the new settings.

If there's a |CONF| file in or above the current directory, that's what
|PD| uses to find the issue database.  This means you can run the |CMD|
command from subdirectories of your project, and things will work as
expected.

|PD| has quite a few commands available.  To see them, you can use the
:kbd:`help` command.  If you give a command name as an argument, you'll get
more detailed help on that command.  For example:

.. command: help
.. command: help todo

.. literalinclude:: /include/help.txt

You can set up command aliases (i.e., shortcuts) via your :doc:`config`.
If you're in the |PD| command loop, you can also use TAB completion on
commands.
