#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: arkmanager.py
# by Arzaroth Lekva
# arzaroth@arzaroth.com
#

from __future__ import print_function, absolute_import, unicode_literals, division
import os
import zlib
import hashlib
import binascii
import src.xxtea as xxtea
from collections import namedtuple
from struct import pack, unpack

class ArkError(Exception):
    pass


def read_or_raise(file, size):
    data = file.read(size)
    if len(data) != size:
        raise ArkError("Unable to read, truncated or corrupted file")
    return data

class ArkManager(object):
    ARK_VERSION = 1
    HEADER_SIZE = 12
    METADATA_SIZE = 296

    def __init__(self, filename, passwd, create=False, append=False):
        self.filename = filename
        self.passwd = passwd
        self.create = create
        self.append = append

    def __enter__(self):
        class Ark(object):
            def __init__(self, filename, passwd, create, append):
                self.filename = filename
                self.passwd = passwd
                self.create = create
                self.append = append
                try:
                    self._file = open(filename, ('rb+' if append else
                                                 'wb' if create else
                                                 'rb'))
                except Exception as e:
                    raise ArkError(str(e))
                self.file_count = 0
                self.metadata_offset = 0
                self.ark_version = ArkManager.ARK_VERSION
                self.metadatas = []
                if not create:
                    self._parse_header()
                    self._get_metadata()
                else:
                    self._write_header()

            def cleanup(self):
                if self.create or self.append:
                    self._write_header()
                    self._write_metadata()
                self._file.close()

            def _parse_header(self):
                self._file.seek(0, os.SEEK_SET)
                data = read_or_raise(self._file, ArkManager.HEADER_SIZE)
                self.file_count, self.metadata_offset, self.ark_version = unpack('3I', data)
                if self.ark_version != ArkManager.ARK_VERSION:
                    raise ArkError("Bad ark version")

            def _write_header(self):
                self._file.seek(0, os.SEEK_SET)
                self._file.write(pack('3I',
                                      self.file_count,
                                      self.metadata_offset,
                                      self.ark_version))

            def _get_metadata(self):
                self._file.seek(self.metadata_offset, os.SEEK_SET)
                size = self.file_count * ArkManager.METADATA_SIZE
                if size & 3:
                    size &= ~3
                    size += 4
                data = read_or_raise(self._file, size)
                data = xxtea.decrypt(data, self.passwd)
                try:
                    self.metadatas = [Metadata(data[i:i + ArkManager.METADATA_SIZE])
                                      for i in range(0, size, ArkManager.METADATA_SIZE)]
                except:
                    raise ArkError("Unable to decrypt metadatas, bad password or corrupted file")

            def _write_metadata(self):
                self._file.seek(self.metadata_offset, os.SEEK_SET)
                data = b''.join(meta.raw_data for meta in self.metadatas)
                data = xxtea.encrypt(data, self.passwd)
                self._file.write(data)

            def get_file_content(self, meta):
                if not isinstance(meta, Metadata):
                    raise ArkError("Expected Metadata instance, not %s"
                                   % meta.__class__.__name__)
                self._file.seek(meta.file_location, os.SEEK_SET)
                read_size = meta.encrypted_nbytes or meta.compressed_size
                data = read_or_raise(self._file, read_size)
                if meta.encrypted_nbytes:
                    data = xxtea.decrypt(data, self.passwd)
                if meta.compressed_size != meta.original_filesize:
                    data = zlib.decompress(data)
                return data[:meta.original_filesize]

            def add_file(self, path):
                meta = Metadata()
                if path[0] in "=@:+":
                    meta.flag = path[0]
                    path = path[1:]
                else:
                    meta.flag = '='
                meta.filename = os.path.basename(path)
                meta.pathname = os.path.dirname(path)
                meta.original_filesize = os.path.getsize(path)
                meta.timestamp = int(os.path.getmtime(path))
                try:
                    with open(path, 'rb') as f:
                        data = f.read()
                except Exception as e:
                    print('Unable to add %s, skipping (reason: %s)',
                          path, str(e))
                    return
                meta.md5sum = hashlib.md5(data).hexdigest()
                if meta.flag == '@' or meta.flag == '+':
                    data = zlib.compress(data, 9)
                meta.compressed_size = len(data)
                if meta.flag == ':' or meta.flag == '+':
                    data = xxtea.encrypt(data, self.passwd)
                    meta.encrypted_nbytes = len(data)
                if self.metadatas:
                    seek = (self.metadatas[-1].file_location +
                            (self.metadatas[-1].encrypted_nbytes or
                             self.metadatas[-1].compressed_size))
                else:
                    seek = ArkManager.HEADER_SIZE
                self._file.seek(seek, os.SEEK_SET)
                meta.file_location = seek
                self._file.write(data)
                self.metadatas.append(meta)
                self.file_count = len(self.metadatas)
                self.metadata_offset = self._file.tell()


        self._ark_obj = Ark(self.filename, self.passwd, self.create, self.append)
        return self._ark_obj

    def __exit__(self, type, value, traceback):
        self._ark_obj.cleanup()


class Metadata(object):
    def __init__(self, data=None):
        if data is not None:
            self.from_data(data)
        else:
            self.from_data(b'')

    def from_data(self, data):
        data = data.ljust(ArkManager.METADATA_SIZE, b'\x00')
        (filename,
         pathname,
         self.file_location,
         self.original_filesize,
         self.compressed_size,
         self.encrypted_nbytes,
         self.timestamp,
         md5sum,
         self.unknown) = unpack('128s128s5I16sI', data)
        self.filename = filename.rstrip(b'\x00').decode('utf-8')
        self.pathname = pathname.rstrip(b'\x00').decode('utf-8')
        self.md5sum = binascii.hexlify(md5sum).decode('utf-8')
        flag = ((int(bool(self.encrypted_nbytes)) << 1) |
                int(self.compressed_size != self.original_filesize))
        self.flag = "=@:+"[flag]

    @property
    def raw_data(self):
        return pack('128s128s5I16sI',
                    self.filename.encode('utf-8'),
                    self.pathname.encode('utf-8'),
                    self.file_location,
                    self.original_filesize,
                    self.compressed_size,
                    self.encrypted_nbytes,
                    self.timestamp,
                    binascii.unhexlify(self.md5sum),
                    self.unknown)
