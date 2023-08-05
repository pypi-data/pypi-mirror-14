===============================
 Creating and Modifying Issues
===============================

.. highlight:: ditzsession

OK, now you have an issue database, you can add issues to it.  This is done
using the :kbd:`add` command.  You're prompted for the issue name, type,
and a possibly multi-line description.  You can also add comments.

There are three different types of issue in |PD|:

:Feature:
    A new feature you want to add to your project, which typically is
    visible to its users.

:Task:
    A thing that needs doing, but doesn't necessarily add new functionality
    for users.

:Bugfix:
    Something broken that needs mending.

Here's an example:

.. command: add

.. prompt: Title:
.. reply:  Implement a hello-world program

.. prompt: >
.. reply:  Pretty lame, but one has to start somewhere.

.. prompt: >
.. reply:  .

.. prompt: .+ask.
.. reply:  f

.. prompt: Issue creator .*:
.. reply:  

.. prompt: >
.. reply:  I already have a prototype for this, off the Interweb.

.. prompt: >
.. reply:  .

.. literalinclude:: /include/add1.txt

As you can see from the final line, each issue is assigned a name of the
form ``<name>-<num>``, where ``<name>`` is the name of the *component*
assigned to the issue, and ``<num>`` is the next number available for that
component.  If issue names are mentioned in comments and descriptions,
they're treated specially---more on that later.

Note that if the issue database had any releases defined, we'd be asked if
we wanted to assign it to one of them.  More on that in :doc:`assign`.

On creation, each issue database has one component: the name of the
project.  For simple projects, you might want to stick with this.  But for
more complex projects, it's a good idea to group issues by component.

Here's how to add a component, say, for issues related to programs:

.. command: add-component

.. prompt: Name:
.. reply: prog

.. literalinclude:: /include/addcomp1.txt

Let's suppose we need another for the documentation:

.. command: add-component

.. prompt: Name:
.. reply: doc

.. literalinclude:: /include/addcomp2.txt

Now you have multiple components, you can assign issues to them:

.. command: set-component helloworld-1

.. prompt: Choose a component .+:
.. reply: 1

.. prompt: >
.. reply:  This is a programming issue.

.. prompt: >
.. reply:  .

.. literalinclude:: /include/setcomp.txt

Note that, in the command loop, |PD| remembers the last issue created or
referred to by commands.  So the ``helloworld-1`` argument could have been
omitted here.

You'll also notice that |PD| reports a change in the issue name---as you'd
expect, since the name is partly determined by its component.  This might
also affect the names of other issues.  But note that references to issue
names in comments and descriptions are *not* affected---again, more on that
later.

Issues can also have *references*\---that is, links to other files not
included in the issue database.  Here's an example (omitting the issue name
here, since we're referring to the last and only one):

.. command: add-reference

.. prompt: Reference:
.. reply:  http://warez.com/hello-world-trojan.c

.. prompt: >
.. reply:  Prototype for the program.

.. prompt: >
.. reply:  .

.. literalinclude:: /include/addref.txt

To pad out the example a bit more, let's add a couple more issues:

.. command: add

.. prompt: Title:
.. reply:  Write some documentation

.. prompt: >
.. reply:  Sigh.  I suppose it's gotta be done.

.. prompt: >
.. reply:  .

.. prompt: .+ask.
.. reply:  t

.. prompt: Choose a component .*:
.. reply:  3

.. prompt: Issue creator .*:
.. reply:  

.. prompt: >
.. reply:  .

.. literalinclude:: /include/add2.txt

Notice here that, now we have more than one component, we're asked which
one to assign the issue to.

Now, for completeness, let's add a bug report:

.. command: add

.. prompt: Title:
.. reply:  Prototype prints the Wrong Thing

.. prompt: >
.. reply:  It writes "goodbye cruel world".  Hmm, looks like a memory

.. prompt: >
.. reply:  corruption to me.

.. prompt: >
.. reply:  .

.. prompt: .+ask.
.. reply:  b

.. prompt: Choose a component .*:
.. reply:  2

.. prompt: Issue creator .*:
.. reply:  wally@cubicle.com

.. prompt: >
.. reply:  .

.. literalinclude:: /include/add3.txt
