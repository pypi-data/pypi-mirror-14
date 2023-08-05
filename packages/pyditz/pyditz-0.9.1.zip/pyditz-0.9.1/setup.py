# Setup script for PyDitz.

import os

# Bootstrap setuptools.
from conf.ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

# Get package information.
from conf.tools import read_pkginfo
info = read_pkginfo("ditz")

# Do the setup.
setup(name             = info.__title__,
      author           = info.__author__,
      author_email     = info.__email__,
      description      = info.__desc__,
      long_description = "\n" + open("README").read(),
      license          = info.__license__,
      url              = info.__url__,
      classifiers      = info.__classifiers__.strip().split("\n"),

      packages         = ["ditz"],
      include_package_data = True,

      entry_points     = {
          'console_scripts': [
              '%s = ditz.console:main' % os.environ.get("DITZCMD", "pyditz"),
           ],
      },

      setup_requires   = ['setuptools_scm'],
      use_scm_version  = info.__scm_options__,

      install_requires = ['pyyaml', 'jinja2', 'voluptuous', 'six'],
      tests_require    = ['nose', 'mock', 'coverage'],
      test_suite       = 'nose.collector')

# flake8: noqa
