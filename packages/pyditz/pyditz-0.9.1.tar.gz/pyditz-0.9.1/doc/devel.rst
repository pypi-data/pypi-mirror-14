=====================
 Development Roadmap
=====================

.. epigraph::

   Roads?  Where we're going, we don't need roads. 

   -- Dr Emmett Brown, `Back To The Future`__

   __ http://www.imdb.com/title/tt0088763

This section contains a few notes and ideas about possible future
development of |PD|.  There's no definite date for any of this; most of my
itch has been scratched by what already exists, and development mode is
turning into maintenance mode.

Compatibility with original Ditz
================================

As of version 0.8, |PD| is pretty much roundtrip-compatible with the
original Ditz.  If the original were still being developed, I guess I'd try
to keep in step with it.  But it's not.  So the question is, what price
compatibility?

I think |PD| being able to read original Ditz databases is important.  I'm
not sure about the other direction: once a database has migrated to |PD|, I
don't see a use-case for going back again.

Extending the file formats
==========================

The original Ditz had hooks to support extra features, such as
issue-claiming and issue priorities.  These added new fields to the issue
files.  I intend to implement these features, but not via plugins.

This raises the problem of how to extend the file formats while maintaining
compatibility with old formats.  One idea that springs to mind is to
extend the :mod:`ditz.objects` classes with different YAML tags.  Then,
when an 'old' object is read, it can be transparently converted to a newer
one.
