#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: Pon3Ark.py
# by Arzaroth Lekva
# arzaroth@arzaroth.com
#

from __future__ import print_function, absolute_import, unicode_literals
import os
import sys
import getpass
from src import ArkManager, ArkError
from src import do_list
from src import do_extract
from src import do_create

try:
    PRGM = os.path.basename(__file__)
except NameError:
    PRGM = os.path.basename(sys.argv[0])
VERSION = "0.5.0b"

__doc__ = """
{prgm} {ver}
Let's open ark files with some music.

Usage:
  {prgm} -x [-vf FILE] [-o DIR] <ark_file> [FILE...]
  {prgm} -c [-vf FILE] <ark_file> <file>...
  {prgm} -a [-vf FILE] <ark_file> <file>...
  {prgm} -t [-vf FILE] <ark_file>
  {prgm} -h
  {prgm} --version

Arguments:
  ark_file              Path to ark file.
  file                  File to put into the ark file. See "How to create".

Options:
  -x                    Extract giles from the ark file. When given, they specify names of the archive members to be extracted.
  -c                    Create the ark file.
  -a                    Append files to the ark file.
  -t                    List the content of the ark file.
  -f --passfile=FILE    Take password from file instead of standard input.
  -v                    Enable verbose.
  -o --output=DIR       Write files to DIR [default: out].
  --version             Show version number.
  -h --help             Show this help and exit.

How to create:
  When creating a new ark file, you can prepand the filename with special characters:
    - Add @ to compress the file inside the archive.
    - Add : to encrypt the file inside the archive.
    - Add + to do both.
    - Add = to keep the file unencrypted and uncompressed.
  The "=" is the default and should be used only if the filename starts with one of the specified characters.

Listing flags:
  See "How to create".

Notes:
  - The code of this tool is currently open source. If you experiment issues, feel free to report or improve it.

Author:
  Original program by Arzaroth <lekva@arzaroth.com>
""".format(prgm=PRGM, ver=VERSION)

def get_password(opts):
    if opts['--passfile']:
        try:
            with open(opts['--passfile'], 'rb') as f:
                passwd = f.read()
        except Exception as e:
            print('Unable to retrieve password from file (%s)' % str(e),
                  file=sys.stderr)
            sys.exit(1)
    else:
        passwd = getpass.getpass('Enter password: ')
        if opts['-x'] and passwd != getpass.getpass('Verify password: '):
            print('Password verification failed', file=sys.stderr)
            sys.exit(1)
        passwd = passwd.encode('utf-8')
    return passwd

if __name__ == '__main__':
    from docopt import docopt
    opts = docopt(__doc__, version=VERSION)
    passwd = get_password(opts)
    try:
        with ArkManager(opts['<ark_file>'], passwd,
                        opts['-c'], opts['-a']) as ark:
            if opts['-t']:
                do_list(ark, opts)
            elif opts['-x']:
                do_extract(ark, opts)
            elif opts['-c'] or opts['-a']:
                do_create(ark, opts)
    except ArkError as e:
        print(str(e), file=sys.stderr)
    sys.exit(0)
