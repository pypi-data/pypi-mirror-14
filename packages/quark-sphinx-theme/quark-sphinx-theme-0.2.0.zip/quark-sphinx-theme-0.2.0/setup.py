#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from io import open
import os
import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

dist_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(dist_dir, 'quark_sphinx_theme'))
from __version__ import __version__  # noqa

readme = os.path.join(dist_dir, 'README.rst')
with open(readme, 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='quark-sphinx-theme',
    version=__version__,
    description='A Sphinx theme designed for QTextBrowser',
    long_description=long_description,
    url='https://bitbucket.org/fk/quark-sphinx-theme',
    author='Felix Krull',
    author_email='f_krull@gmx.de',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Sphinx :: Theme',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Documentation',
    ],

    packages=['quark_sphinx_theme', 'quark_sphinx_theme.ext'],
    package_data={
        'quark_sphinx_theme': ['quark/*.*', 'quark/*/*.*'],
    },
    entry_points={
        'sphinx_themes': [
            'path = quark_sphinx_theme:get_path',
        ]
    }
)
