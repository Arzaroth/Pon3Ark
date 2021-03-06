#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: extract.py
# by Arzaroth Lekva
# arzaroth@arzaroth.com
#

import os
import errno
import hashlib

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def do_extract(ark, opts):
    for meta in ark.metadatas:
        path = os.path.join(opts['--output'], meta.pathname)
        full_path = os.path.join(path, meta.filename)
        if opts['FILE'] and meta.fullpath not in opts['FILE']:
            continue
        mkdir_p(path)
        if opts['-v']:
            print('Processing %s...' % meta.fullpath)
        data = ark.get_file_content(meta)
        if hashlib.md5(data).hexdigest() != meta.md5sum:
            print('[Warning] %s: checksum mismatch' % meta.fullpath)
        with open(full_path, 'wb') as f:
            f.write(data)
        os.utime(full_path, (meta.timestamp, meta.timestamp))
