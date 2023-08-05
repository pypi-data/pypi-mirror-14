#!/usr/bin/env python

__copyright__=''
__license__=''
__version__='2.0.0'

try:
  from setuptools import setup
except ImportError:
  from disutils.core import setup

setup(name='Wintx',
      version=__version__,
      description='A sharded meteorological database.',
      long_description='Wintx is a meteological database that is designed to '\
          'be sharded across multiple machines using the MySQL Fabric framework.',
      author='Seth Cook',
      author_email='cook71@purdue.edu',
      packages=['wintx',
                'wintx.drivers',
                'wintx.drivers.dummy',
                'wintx.interfaces',
                'wintx.importers',
                ],
      license=__license__,
      classifiers=['Programming Language :: Python :: 2.6',
                   'Operating System :: Unix',
                   'Development Status :: 5 - Production/Stable'],
      scripts=[],
      install_requires=['argparse',
                        'ConfigParser',
                        'simplejson',
                        'voluptuous',]
)

