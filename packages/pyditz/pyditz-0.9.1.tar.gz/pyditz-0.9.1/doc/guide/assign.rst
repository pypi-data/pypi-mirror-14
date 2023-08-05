==============================
 Assigning Issues to Releases
==============================

.. highlight:: ditzsession

At various stages during a project's development, it will be released into
the wild for users to pick apart and find fault with.  Each release is made
up of a set of issues which go into making it.

In order to assign issues to a release, we first need to create the release
in the issue database.  The :kbd:`add-release` command does that:

.. command: add-release

.. prompt: Name:
.. reply: 1.0

.. prompt: >
.. reply:  First release.  It's gonna be AWESOME.

.. prompt: >
.. reply:  .

.. literalinclude:: /include/addrel1.txt

Now we can assign issues to it, using the :kbd:`assign` command:

.. command: assign prog-1

.. prompt: >
.. reply:  .

.. literalinclude:: /include/assign.txt

Note that, since there's only one release at present, we're not prompted
for which one to assign the issue to.

There's also an :kbd:`unassign` command, which reverts the issue back to
its initial 'unassigned' state.  We won't be using it in the examples.

Now let's look at the TODO list again:

.. command: todo

.. literalinclude:: /include/todo2.txt

We have a release 1.0, with one issue assigned to it, and two unassigned
issues.  The release is currently *unreleased*, and we'll see how to change
that in :doc:`release`.
