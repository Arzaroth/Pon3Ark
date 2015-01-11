#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: setup.py
# by Arzaroth Lekva
# arzaroth@arzaroth.com
#

from __future__ import print_function, absolute_import, unicode_literals
import os
from setuptools import setup, find_packages
from Pon3Ark import VERSION

setup(
    name='Pon3Ark',
    version=VERSION,
    license='BSD',

    url='https://gitlab.bi.tk/mlp/Pon3Ark',
    download_url='https://gitlab.bi.tk/mlp/Pon3Ark/repository/archive.zip?ref=%s' % VERSION,

    author='Marc-Etienne Barrut',
    author_email='lekva@arzaroth.com',

    description='A data extractor for the ark files from the mobile game "My Little Pony"',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    keywords='pony cheat hack ark extractor',

    packages=find_packages(),
    scripts=['Pon3Ark.py'],

    install_requires=open('requirements.txt').read().split('\n'),
)
