#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Based on https://github.com/pypa/sampleproject
See also: https://packaging.python.org/en/latest/distributing.html
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cliPublish',
    version='0.2.0',

    description='Convenient commandline utility to publish files on a webserver using rsync',
    keywords='rsync upload cli',
    long_description=long_description,

    url='https://github.com/mheistermann/cliPublish',

    author='Martin Heistermann',
    author_email='sieve-git-pushdeploy@mheistermann.de',

    license='GPLv3+',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
    ],

    packages=find_packages(),

    install_requires=[],

    entry_points={
        'console_scripts': [
            'cliPublish=cliPublish:main',
        ],
    },
    package_data={
        'cliPublish': ['README.md', 'cliPublish/remotes.conf'],
    },
    include_package_data=True,
)
