#!/usr/bin/env python

__version__ = '2.0.0-1'
__license__ = ''

try:
  from setuptools import setup
except ImportError:
  from disutils.core import setup

setup(name='WintxImporter-Grib',
      version=__version__,
      description='GRIB file importer for Wintx',
      long_description='The Wintx GRIB File Importer provides an extension to '\
          'the Wintx Importer interface to ingest a GRIB file into the '\
          'underlying supporting Wintx datastore.',
      author='Seth Cook',
      author_email='sethcook@purdue.edu',
      license=__license__,
      packages=['wintx',
                'wintx.importers',
                'wintx.importers.Grib'],
      namespace_packages=['wintx',
                          'wintx.importers',],
      classifiers=['Programming Language :: Python :: 2.6',
                   'Operating System :: Unix',
                   'Development Status :: 5 - Production/Stable'],
      install_requires=['wintx >= 2.0.0',
                        'pygrib >= 1.9.9',
                        'numpy >= 1.6.1',
                        'matplotlib',],
)
