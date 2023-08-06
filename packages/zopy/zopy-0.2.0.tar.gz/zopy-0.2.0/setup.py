#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from version import __version__

setup(
  name = 'zopy',
  packages = ['zopy'],
  version = '.'.join(str(x) for x in __version__),
  description = "Zoho API integration for Python",
  author = 'Dharwin Perez',
  author_email = 'dhararon@hotmail.com',
  url = 'https://github.com/dhararon/zopy',
  download_url = 'https://github.com/dhararon/Zopy/tarball/master',
  keywords = ['crm', 'CRM', 'zoho'],
  classifiers=[],
  license='MIT license',
  install_requires=[
    'requests',
    'marshmallow'
  ],
)
