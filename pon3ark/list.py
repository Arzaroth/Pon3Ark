#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: list.py
# by Arzaroth Lekva
# arzaroth@arzaroth.com
#

import os
from datetime import datetime as dt

def do_list(ark, opts):
    total_size = sum(x.original_filesize for x in ark.metadatas)
    len_size = max(len(str(total_size)), len('Length'))
    if opts['-v']:
        print("File:  %s" % ark.filename)
        print(' Flag   %*s     Date    Time    Name' % (len_size,
                                                        'Length'))
        print(' ----  -%s  ---------- -----   ----' % (len_size * '-'))
    for meta in ark.metadatas:
        if opts['-v']:
            print('    %s   %*d  %s   %s' % (meta.flag,
                                             len_size,
                                             meta.original_filesize,
                                             dt.fromtimestamp(meta.timestamp)
                                             .strftime('%Y-%m-%d %H:%M'),
                                             meta.fullpath))
        else:
            print(meta.fullpath)
    if opts['-v']:
        print(' ----  -%s                     -------' % (len_size * '-'))
        print('        %*d%s%d file%s' % (len_size, total_size,
                                          ' ' * 21, ark.file_count,
                                          's' if ark.file_count > 1 else ''))
