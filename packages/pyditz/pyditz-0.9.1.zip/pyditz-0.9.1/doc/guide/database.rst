====================
 Database Internals
====================

The |PD| issue database consists of a single directory containing a bunch
of files in YAML_ format.  There are two kinds of file:

#. A single project file, called :file:`project.yaml`, specifying all the
   releases in the project.

#. An issue file for each issue, named :file:`issue-{id}.yaml`, where
   *id* is its hexadecimal issue ID.

Here's an example issue file from |PD|\'s own issue database, which also
gives an example of how referenced issues are stored in the file (in the
form ``{issue [id]}``):

.. literalinclude:: /include/issue.yaml

.. _YAML: http://yaml.org
