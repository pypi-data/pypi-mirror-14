#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

with open('README') as f:
    README = f.read()

setup(name='rudix',
      version='2016.2.29',
      license='BSD',
      description='Rudix Package Manager',
      long_description=README,
      author='Rudá Moura',
      author_email='ruda.moura@gmail.com',
      url='http://rudix.org/',
      keywords='package manager',
      classifiers = ["Programming Language :: Python", 
                     "License :: OSI Approved :: BSD License",
                     "Environment :: MacOS X",
                     "Operating System :: MacOS :: MacOS X",
                     "Topic :: System :: Installation/Setup",
                     "Topic :: System :: Software Distribution"],
      scripts=["rudix"],
)
