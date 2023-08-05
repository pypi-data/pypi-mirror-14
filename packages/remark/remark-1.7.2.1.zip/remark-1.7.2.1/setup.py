#!/usr/bin/env python

# Description: Setuptools packaging for Remark
# Documentation: dependencies.txt

# Remark 1.7.2
# Copyright (c) 2009 - 2016
# Kalle Rutanen
# Distributed under the MIT license (see license.txt).

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
from Remark.Version import remarkVersion

setup(name = 'remark',
      version = remarkVersion() + '.1',
      description = 'Generates html documentation for software libraries from lightweight markup.',
      keywords = 'lightweight markup software documentation html',
      author = 'Kalle Rutanen',
      author_email = 'kalle.rutanen@hotmail.com',
      url = 'http://kaba.hilvi.org/remark',
      packages = find_packages(),
      include_package_data = True,
      license = 'MIT',
      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Environment :: Console',
        'Topic :: Software Development :: Documentation',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        ],
      scripts = ['remark.py',],
      install_requires = [
        'jsonschema>=2.4',
        'markdown>=2.6', 
        'pillow>=2.0',
        'pygments>=1.5',
        ],
      zip_safe = False,
     )
