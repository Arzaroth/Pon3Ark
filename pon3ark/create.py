#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: create.py
# by Arzaroth Lekva
# arzaroth@arzaroth.com
#

def do_create(ark, opts):
    for file_path in opts['FILE']:
        if opts['-v']:
            print('Processing %s...' % file_path)
        ark.add_file(file_path, opts['--squash-path'])
