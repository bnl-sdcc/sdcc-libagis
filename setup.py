#!/usr/bin/env python
#
# Setup prog for AGIS library

import sys
from setuptools import setup

setup(
    name="python-libagis",
    version="1.0",
    description='Library for querying and handling AGIS information.',
    long_description='''Library for querying and handling AGIS information.''',
    license='GPL',
    author='John Hover',
    author_email='jhover@bnl.gov',
    url='https://www.racf.bnl.gov/experiments/usatlas/griddev/',
    packages=[ 'libagis',
              ],
    classifiers=[
          'Development Status :: 3 - Beta',
          'Environment :: Console',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GPL',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: System Administration :: Management',
    ],
)
