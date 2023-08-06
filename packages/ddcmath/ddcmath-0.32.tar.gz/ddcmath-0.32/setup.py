#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from setuptools import setup
from ddcmath import infos


setup(name='ddcmath',
      version=infos.__version__,
      description='Math functions related to DDC control',
      author=infos.__author__,
      author_email=infos.__email__,
      url=infos.__url__,
      download_url = infos.__download_url__,
      keywords = ['bacnet', 'building', 'automation', 'test'],
      packages=[
          'ddcmath',
          ],
#      install_requires=[
#          'pandas',
#          'bacpypes',
#          'bokeh',
#          ],
      long_description=open('README.rst').read(),
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Utilities",
          ],)