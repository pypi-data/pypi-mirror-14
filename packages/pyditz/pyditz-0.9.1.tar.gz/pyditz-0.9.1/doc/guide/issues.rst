===================
 Working on Issues
===================

.. highlight:: ditzsession

You can record the start of work on an issue by using the :kbd:`start`
command:

.. command: start prog-1

.. prompt: >
.. reply:  I estimate this will take no time at all.

.. prompt: >
.. reply:  .

.. literalinclude:: /include/start.txt

This adds a 'start-work' event to the issue's event log, and puts the issue
into the 'in process' state.  Similarly, you can stop working on it using
the :kbd:`stop` command:

.. command: stop

.. prompt: >
.. reply:  Checked over the prototype, and it looks good.

.. prompt: >
.. reply:  .

.. literalinclude:: /include/stop.txt

This adds a 'stop-work' event to the event log, and the issue state becomes
'paused'.

Whatever state an issue is in, you can add a comment to it via the
:kbd:`comment` command, which adds another event to the log:

.. command: comment

.. prompt: >
.. reply:  Wally reported an error (prog-2), but it's probably nothing.

.. prompt: >
.. reply:  .

.. literalinclude:: /include/comment.txt

Notice, in this comment, a reference to another issue name.  As mentioned
in :doc:`query`, |PD| will replace this with the unique identifier of the
issue behind the scenes.

When an issue has been resolved, you can close it via the :kbd:`close`
command:

.. command: close

.. prompt: Choose a disposition .+:
.. reply:  1

.. prompt: >
.. reply:  Yeah, it works fine.  Job's a good 'un!

.. prompt: >
.. reply:  .

.. literalinclude:: /include/close.txt

As you can see above, there are three possible *dispositions* for a closed
issue, with these intended meanings:

:Fixed:
    Resolved successfully (feature implemented, task done, bug fixed).

:Won't fix:
    Rejected (feature or task aborted, bug wasn't a bug or isn't serious
    enough to fix).

:Reorganized:
    Split up or rearranged into other issues.

At this point, let's look at the event log to see what happened:

.. command: show

.. literalinclude:: /include/show2.txt

Finally, if you decide that an issue has become completely redundant, you
can remove it from the database completely.  This is done using the
:kbd:`drop` command:

.. command: drop doc-1

.. literalinclude:: /include/drop.txt

Like the :kbd:`set-component` command, this potentially rearranges issue
names.

Note here that you don't get to include a comment.  This is because there's
no longer anywhere to store it.  [#]_

.. [#]
   Though if there were, in this case it would probably be "We don't need
   no stinkin' documentation!"
