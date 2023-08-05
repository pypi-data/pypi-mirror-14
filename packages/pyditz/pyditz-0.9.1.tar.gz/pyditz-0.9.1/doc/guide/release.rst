==================
 Making a Release
==================

.. highlight:: ditzsession

OK, so you've closed all the issues assigned to a release.  Here are the
commands which manage the release process.

Firstly, to see the list of available releases, and what state they're in,
there's the :kbd:`releases` command:

.. command: releases

.. literalinclude:: /include/releases1.txt

To see the status of the current release:

.. command: status 1.0

.. literalinclude:: /include/status.txt

This shows you that release 1.0 is ready.  Another way to see it is via the
:kbd:`todo` command:

.. command: todo

.. literalinclude:: /include/todo3.txt

To make a release, use the :kbd:`release` command, specifying the release
number (but in this case we don't need to, since |PD| remembers the last
release mentioned):

.. command: release

.. prompt: >
.. reply:  It's good to go!

.. prompt: >
.. reply:  .

.. literalinclude:: /include/release.txt

Note that this command will only succeed if all the issues in the release
are closed.

Now, if we run the :kbd:`releases` command again, we get:

.. command: releases

.. literalinclude:: /include/releases2.txt

Finally, you can get a log of all the changes made in a release (of the
kind you'd put into a :file:`NEWS` file) using the :kbd:`changelog`
command:

.. command: changelog

.. literalinclude:: /include/changelog.txt

So there you have it: the entire release process of **helloworld** version
1.0.  Pity about that outstanding bug... I guess they ran out of budget.
|GRIN|
