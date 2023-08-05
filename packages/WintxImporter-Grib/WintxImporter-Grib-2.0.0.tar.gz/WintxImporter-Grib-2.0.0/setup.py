#!/usr/bin/env python

__version__ = '2.0.0'

try:
  from setuptools import setup
except ImportError:
  from disutils.core import setup

setup(name='WintxImporter-Grib',
      version=__version__,
      packages=['wintx',
                'wintx.importers',
                'wintx.importers.Grib'],
      namespace_packages=['wintx', 'wintx.importers'],
      install_requires=['wintx >= 2.0.0',
                        'pygrib >= 1.9.9',
                        'numpy >= 1.6.1',
                        'matplotlib',
                        ],
)
