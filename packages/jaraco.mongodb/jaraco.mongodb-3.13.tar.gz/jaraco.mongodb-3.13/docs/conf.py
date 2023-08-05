#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools_scm

extensions = [
    'sphinx.ext.autodoc',
]

# General information about the project.
project = 'jaraco.mongodb'
copyright = '2015 Jason R. Coombs'

import os
root = os.path.relpath(os.path.join(os.path.dirname(__file__), '..'))

# The short X.Y version.
version = setuptools_scm.get_version(root=root)
# The full version, including alpha/beta/rc tags.
release = version

master_doc = 'index'
