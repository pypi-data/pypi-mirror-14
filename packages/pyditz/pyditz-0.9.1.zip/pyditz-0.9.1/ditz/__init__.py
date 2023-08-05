"""
Python implementation of Ditz (http://rubygems.org/gems/ditz).
"""

import pkg_resources as pkg

from .plugin import loader

path = pkg.resource_filename(__name__, "plugins")
loader.add_path(path)

del path, loader, pkg
