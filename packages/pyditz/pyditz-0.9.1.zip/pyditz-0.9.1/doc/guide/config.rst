====================
 Configuration File
====================

|PD| provides a few user configuration options, by the use of a INI-style
configuration file called |RC| in a |RCDIR| subdirectory of your home
directory.  You can also specify per-project configuration settings, which
override those in |RC|, in a file called ``project.cfg`` in the project's
issue directory.

.. versionadded:: 0.9
   Per-project config files.

Here's the default settings:

.. literalinclude:: ../../ditz/config.cfg
   :language: ini
