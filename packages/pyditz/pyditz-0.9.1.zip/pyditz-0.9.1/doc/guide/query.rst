=============================
 Querying the Issue Database
=============================

.. highlight:: ditzsession

OK, we now have a bunch of issues.  How do we know what state they're in?
A good way to get a summary is the :kbd:`todo` command.  In the command
loop, this is run by default if you just press RETURN.  Here's the output
for the issues we have so far:

.. command: todo

.. literalinclude:: /include/todo1.txt

This says that we have three issues, none of which are assigned to a
release (more on those later).  They're printed in reverse order of
creation (newest first).  The underscore at the start of each line is a
*status indicator flag*; in this case it means the issue is unstarted.

Each issue can be in one of four states:

.. list-table::
   :header-rows: 1
   :widths: 1 2 6

   * - Flag
     - Meaning
     - Details

   * - ``_``
     - Unstarted
     - No work has yet begun on the issue.

   * - ``>``
     - In progress
     - Work has started on the issue.

   * - ``=``
     - Paused
     - Some work has been started, but now it is stopped.

   * - ``x``
     - Closed
     - The issue is closed.

Normally, closed issues are not shown by the :kbd:`todo` command.  But if
you give the :option:`-a` (for 'all') option, they are.

To look closer at a single issue, we use the :kbd:`show` command.  This
displays all the detailed issue information, including a history of all the
events which have occurred to the issue (and their comments).  Here's an
example:

.. command: show prog-1

.. literalinclude:: /include/show1.txt

The only thing needing explanation here is the long identifier.  This is a
SHA-1__ message digest built from several of the issue attributes, and
uniquely identifies the issue.  Even if the issue name changes (which it
might when issue components are changed), this remains constant.

__ https://en.wikipedia.org/wiki/SHA-1

As well as events in individual issues, you can get a recent-event history
over all issues in the database.  The :kbd:`shortlog` command produces a
one-line summary of each recent event:

.. command: shortlog

.. literalinclude:: /include/shortlog.txt

If you give a numeric argument, then that many events will be shown.  (A
value of zero will show *all* of them.)  This value becomes the default for
future commands.  You can change the initial default in your :doc:`config`.

To get a more detailed summary of log entries, there is the :kbd:`log`
command:

.. command: log

.. literalinclude:: /include/log.txt

Again, a numeric argument will show that many events.

Finally, there's also a :kbd:`list` command which, with no arguments, will
list all issues in the database.  If given a regexp__ argument, it will
list only those issues whose description or comments match.  Here's an
example:

__ http://www.regular-expressions.info

.. command: list world

.. literalinclude:: /include/list.txt

.. versionadded:: 0.9
   List-all-issues command.
