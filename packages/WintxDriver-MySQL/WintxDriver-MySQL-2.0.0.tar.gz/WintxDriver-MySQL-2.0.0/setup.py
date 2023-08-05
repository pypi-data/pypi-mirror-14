#!/usr/bin/env python

__version__='2.0.0'

try:
  from setuptools import setup
except ImportError:
  from disutils.core import setup

setup(name='WintxDriver-MySQL',
      version=__version__,
      packages=['wintx',
                'wintx.drivers',
                'wintx.drivers.MySQL',
                ],
      namespace_packages=['wintx', 'wintx.drivers'],
      install_requires=['hashlib',
                        'mysql-connector-python >= 1.2.0',
                        'wintx >= 2.0.0',
                        'voluptuous',
                        ],
)
