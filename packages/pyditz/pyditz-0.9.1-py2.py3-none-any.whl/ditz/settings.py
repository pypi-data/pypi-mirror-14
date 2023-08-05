"""
Default global settings.
"""


class Settings(object):
    def __init__(self, **kw):
        #: Whether to save files when changes are made.
        self.autosave = False

        #: Whether to use issue cache.
        self.usecache = False

        #: Issue cache filename.
        self.cachefile = ".ditz-cache"

        #: Whether to load external plugins.
        self.externalplugins = True

        #: Whether to do syntax highlighting.
        self.highlight = False

        #: Whether to skip asking for comments.
        self.nocomment = False

        #: Comment string to use in non-interactive mode.
        self.comment = None

        #: Whether to search in parent directories for database.
        self.searchparents = False

        #: Whether to enable version control.
        self.versioncontrol = False

        #: No. of terminal lines.  Zero turns off paging.
        self.termlines = 0

        #: No. of terminal columns.  If nonzero, output lines longer than
        #: this are truncated or wrapped.
        self.termcols = 0

        #: Line truncation indicator.  If None, wrapping is done instead.
        self.linetrunc = '...'

        # Set keyword values.
        for attr, val in kw.items():
            if hasattr(self, attr):
                setattr(self, attr, val)
            else:
                raise ValueError("no setting called '%s'" % attr)
