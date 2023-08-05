=====
 FAQ
=====

Well, not asked at all yet.  But if they were...

How complete is it?
===================

All the existing Ditz commands are implemented apart from one: ``edit``.
In Ditz, this invoked ``vi`` (or another editor defined by the ``EDITOR``
environment variable) to edit the raw YAML source of an issue.  I have
plans to do something similar, or knock up a Tkinter_ graphical edit
window.

Why did you rewrite Ditz in Python?
===================================

Good question.  Here are a few answers:

* I didn't intend to.  I originally wanted a way to summarize the status of
  a particular Ditz project in a printable, non-HTML way.  I tried to learn
  Ruby to the extent that I could hack together what I wanted, but in the
  end I decided it was easier to go with Python and PyYAML_.

  That was it for a while: a simple module that read issues in a Ditz
  database.  Then I discovered the Cmd_ module in the standard library, and
  wondered what I could do with it.  And here we are.

* A modular Python implementation enables a whole load of Ditz interfacing
  possibilities with other Python modules I haven't even considered.  Most
  of which I hope other people develop.

* Programming is fun!

Can I join in with this?
========================

By all means.  Grab the PyDitz_ code base on Bitbucket and go for it.
Here's a few guidelines:

* If you decide to work on one of the tasks on the `issue tracker`__, let
  me know.  No point in duplicating work!

  __ _static/index.html

* Source formatting should follow PEP8_.  I use flake8_ to make sure.

* Any new features should have a corresponding unit test in the ``tests``
  directory.

Having said all that, I will gladly accept any patches.  I am Glenn
Hutchings <zondo42@gmail.com>.
