#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=bad-whitespace,redefined-builtin

"""
nwid setup
"""


from codecs import open
from setuptools import setup, find_packages
from os import path


with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
    
HERE = path.abspath(path.dirname(__file__))

setup(
    name = 'nwid',
    version = '0.1',
    description = 'A terminal widget framework for humans.',
    long_description = readme,
    url = 'https://github.com/hbradleyiii/nwid',
    download_url = 'https://github.com/hbradleyiii/nwid/archive/v0.1-planning.tar.gz',
    author = 'Harold Bradley III',
    author_email = 'harold@bradleystudio.net',
    license = 'MIT License',
    keywords = ['server development', 'terminal programming', 'terminal', 'terminal widgets'],
    classifiers = [  # See https://pypi.python.org/pypi?%3Aaction = list_classifiers
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages = find_packages(),
    install_requires = [],
    test_requires = ['pytest>=2.8.0', 'mock'],
    package_data = { '' : ['LICENSE'], },
    entry_points = { },
)
