#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

setup(
  name = 'pybythec',
  version = '0.1.1',
  author = 'glowtree',
  author_email = 'tom@glowtree.com',
  url = 'https://github.com/glowtree/pybythec',
  description = 'a lightweight python build system for c/c++',
  long_description = open('README.rst').read(),
  packages = ['pybythec'],
  scripts = ['bin/pybythec'],
  license = 'LICENSE',
  test_suite = 'example.test'
)
