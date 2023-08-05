================================
 Exporting and Archiving Issues
================================

.. highlight:: ditzsession

To keep the public (who may not have access to |PD|) apprised of the
current status of your project, you can *export* the database.  To do an
export, you use the :kbd:`export` command followed by the name of the
format you want to export.  By default, it writes the exported files into a
directory with the same name as the export format.  If you give an extra
pathname argument, it'll use that instead.

Typing :kbd:`help export` will list the available export formats:

.. command: help export

.. literalinclude:: /include/export.txt

Here's an example of exporting to HTML:

.. command: export html .ditz-html

.. literalinclude:: /include/html.txt

.. note::

   The original ``ditz`` program only offered one export format: HTML.  As
   a result, its command to produce HTML was just called ``html``.  If you
   want compatibility with the original, you can create a command alias in
   your :doc:`config` to do that.  Just add ``html = export html`` to the
   ``[alias]`` section.

For an example of the HTML output itself, see the output from |PD|\'s
`issue tracker`__.  The only thing that may not be obvious when browsing
the HTML is that you can click on table headers, which sorts the table on
that field.  Clicking again reverses the sort order.

__ ../_static/index.html

.. versionadded:: 0.9
   HTML markup.

   If you have installed the Markups__ module, |PD| will use that to convert
   recognized markup in the issue text to the corresponding HTML (bold,
   italic, links, etc).  The default markup is *markdown*, but you can change
   that by setting ``html_markup`` in the ``[export]`` section of your
   :doc:`config` to one of the supported markups: ``markdown``,
   ``restructuredtext`` or ``textile``.  (If you want different markup for
   different projects, you can do that using per-project config files.)

   __ https://pypi.python.org/pypi/Markups

If the pathname argument to the :kbd:`export` command looks like the name
of a file archive (e.g., ``issues.zip``, or ``issues.tar.gz``), the output
directory is bundled into the archive of that name and removed.

When you decide that a previously-released release and its issues is no
longer useful to keep around in your issue database, you can *archive* it
using the :kbd:`archive` command.  This moves all issues from that release
to an archive directory.  If not specified, it is ``ditz-archive-<num>``
where, ``<num>`` is the release number.

.. command: archive 1.0 .ditz-archive-1.0

.. literalinclude:: /include/archive.txt
