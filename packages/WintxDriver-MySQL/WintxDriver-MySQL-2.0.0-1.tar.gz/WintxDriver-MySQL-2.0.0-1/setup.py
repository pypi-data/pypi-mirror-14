#!/usr/bin/env python

__version__ = '2.0.0-1'
__license__ = ''

try:
  from setuptools import setup
except ImportError:
  from disutils.core import setup

setup(name='WintxDriver-MySQL',
      version=__version__,
      description='MySQL support for Wintx',
      long_description='The Wintx MySQL Driver provides the underlying support '\
          'to store and interact with meteorological geospatial data on a MySQL '\
          'server for the Wintx library.',
      author='Seth Cook',
      author_email='sethcook@purdue.edu',
      license=__license__,
      packages=['wintx',
                'wintx.drivers',
                'wintx.drivers.MySQL',],
      namespace_packages=['wintx',
                          'wintx.drivers'],
      classifiers=['Programming Language :: Python :: 2.6',
                   'Operating System :: Unix',
                   'Development Status :: 5 - Production/Stable'],
      install_requires=['hashlib',
                        'mysql-connector-python >= 1.2.0',
                        'wintx >= 2.0.0',
                        'voluptuous',],
)
