#!/usr/bin/env python

__license__ = ''
__version__ = '2.0.0-1'

try:
  from setuptools import setup
except ImportError:
  from disutils.core import setup

setup(name='Wintx',
      version=__version__,
      description='A library for interacting with meteorological geospatial data',
      long_description='Wintx is a meteological database library that is designed to '\
          'provide a generic API to store and interact with meteorological '\
          'geospatial data on varying backing stores.',
      author='Seth Cook',
      author_email='sethcook@purdue.edu',
      license=__license__,
      packages=['wintx',
                'wintx.drivers',
                'wintx.drivers.dummy',
                'wintx.interfaces',
                'wintx.importers',],
      classifiers=['Programming Language :: Python :: 2.6',
                   'Operating System :: Unix',
                   'Development Status :: 5 - Production/Stable'],
      install_requires=['argparse',
                        'ConfigParser',
                        'simplejson',
                        'voluptuous',]
)

