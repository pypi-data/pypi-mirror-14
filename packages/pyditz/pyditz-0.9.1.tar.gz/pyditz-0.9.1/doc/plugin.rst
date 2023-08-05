=======================
 Creating |PD| plugins
=======================

Several aspects of |PD| can be extended by writing *plugins*.  There are
currently two kinds of plugin available:

* Plugins to define new :ref:`commands <command-plugins>`
* Plugins to define new :ref:`export formats <export-plugins>`

Other kinds may be available in future.  This section gives general
information which applies to all kinds of plugin.

Anatomy of a plugin
===================

A |PD| plugin is simply a python module or package, which contains a class
derived from one of the |PD| plugin classes, and put in a certain location
(see the next section).

Plugins you create should set at least the following class attributes:

.. autoattribute:: ditz.plugin.Plugin.name
.. autoattribute:: ditz.plugin.Plugin.description

There are several others which can also be set:

.. autoattribute:: ditz.plugin.Plugin.version
.. autoattribute:: ditz.plugin.Plugin.author
.. autoattribute:: ditz.plugin.Plugin.package

.. _register-plugin:

Registering a plugin
====================

There are several ways for your plugin to be picked up by |PD|:

* You can put it in ``plugins`` subdirectory of |RCPATH|.  The plugin will
  only be available to you.

* You can put it in a ``plugins`` subdirectory of a |PD| project's issue
  directory.  The plugin will be available to everyone using |PD| on this
  project.

* You can put the plugin in a package and register it as a setuptools_
  ``ditz.plugin`` entrypoint.  The plugin will be available on the system
  where the module is installed.

Any suitably-derived class found in one of these locations is automagically
registered; you don't have to do anything else.

You can check whether your plugin is being seen by |PD| by invoking it with
the :option:`--verbose` option.

Making a standalone plugin
==========================

Here's an example of a plugin.  Suppose |PD| provided an API to send
high-five comments to social media whenever an issue is resolved.  (Not
yet, but watch this space |GRIN|.)  There would be an advertised base class
(say, called :class:`SocialMedia`) which you could subclass to create your
plugin, like this:

.. code-block:: python

   from ditz.social import SocialMedia

   class FriendFace(SocialMedia):
       name = "friendface"
       description = "post to http://friendface.co.uk"
       author = "Moss"

       def post(self, comment):
           ...

To make this plugin visible to |PD|, you would just put it in one of the
``plugins`` directories mentioned in :ref:`register-plugin`.

Making a setuptools plugin
==========================

To convert the standalone plugin to a setuptools_ one (assuming it's in a
file called :file:`friendface.py`), you need a :file:`setup.py` something
like this (note how the package and plugin versions are kept in sync):

.. code-block:: python

   from setuptools import setup
   from friendface import FriendFace

   setup(name = "pyditz-friendface",
	 py_modules = ["friendface"],
	 version = FriendFace.version,
	 install_requires = ['pyditz >= 0.8'],
	 entry_points = {
	     'ditz.plugin': 'friendface = friendface:FriendFace'
	 }
   )

See the setuptools_ documentation for the details.  The advantages of doing
it this way are several:

#. You can distribute it on PyPI_ for others to use.
#. You get all the cool versioning and dependency stuff that setuptools
   supports.

Of course, you can put as many plugins as you want in a single package, in
which case the versioning hack above may not be appropriate.
