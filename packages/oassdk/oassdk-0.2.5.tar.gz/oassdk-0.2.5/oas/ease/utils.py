# -*- coding: utf-8 -*-
# Copyright (C) 2011  Alibaba Cloud Computing
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
import hashlib
import io
import math
import mmap
import os

from merkle import TreeHashGenerator
from merkle import MerkleTree


def is_file_like(obj):
    return callable(getattr(obj, 'read', None))


def content_length(content):
    if hasattr(content, '__len__'):
        return len(content)

    if hasattr(content, 'len'):
        return content.len

    if hasattr(content, 'fileno'):
        try:
            fileno = content.fileno()
        except io.UnsupportedOperation:
            pass
        else:
            return os.fstat(fileno).st_size - content.tell()

    if hasattr(content, 'getvalue'):
        return len(content.getvalue())

    raise ValueError('Unsupported content type')


def open_file(file_path=None, file_obj=None, mode='rb'):
    if file_path is None and file_obj is None:
        raise ValueError(
            'Either file_path or file_name should be provided.')
    if file_obj is not None:
        return file_obj
    else:
        try:
            return open(file_path, mode)
        except Exception:
            raise IOError('Failed to open file: %s' % file_path)


def range_size(byte_range):
    return byte_range[1] - byte_range[0] + 1


def calc_num_part(part_size, size_total):
    return int(math.ceil(float(size_total) / part_size))


def calc_ranges(part_size, size_total):
    result = []
    number_parts = calc_num_part(part_size, size_total)
    for n in xrange(number_parts):
        start = n * part_size
        end = (n + 1) * part_size - 1 \
            if n != number_parts - 1 else size_total - 1
        result.append((start, end))
    return result


def compute_etag_from_file(file_path, offset=0, size=None,
                                  chunk_size=1024 * 1024):
    with open(file_path, 'rb') as f:
        return compute_etag_from_file_obj(
            f, offset=offset, size=size, chunk_size=chunk_size)


def compute_etag_from_file_obj(file_obj, offset=0, size=None,
                                      chunk_size=1024 * 1024):
    etag = hashlib.md5()
     
    size = size or os.fstat(file_obj.fileno()).st_size - offset

    if size != 0 and offset % mmap.ALLOCATIONGRANULARITY == 0:
        target = mmap.mmap(file_obj.fileno(), length=size,
                           offset=offset,
                           access=mmap.ACCESS_READ)
    else:
        target = file_obj
        target.seek(offset)

    while size > 0:
        data = target.read(chunk_size)
        etag.update(data[:min(len(data), size)])
        size -= len(data)

    if target is file_obj:
        file_obj.seek(offset)
    else:
        target.close()
    s= etag.hexdigest().upper()
    return s


def compute_combine_etag(etag_list):
    etag = hashlib.md5()
    etag.update(''.join(etag_list))
    return etag.hexdigest().upper()

def compute_combine_tree_etag_from_list(tree_etag_list):
    merkletree = MerkleTree(hash_list=tree_etag_list)
    return merkletree.digest()

def compute_tree_etag_from_file(file_path, offset=0, size=None,
                                chunk_size=1024 * 1024):
    with open(file_path, 'rb') as f:
        return compute_tree_etag_from_file_obj(
            f, offset=offset, size=size, chunk_size=chunk_size)


def compute_tree_etag_from_file_obj(file_obj, offset=0, size=None,
                                    chunk_size=1024 * 1024):
    generator = TreeHashGenerator()

    size = size or os.fstat(file_obj.fileno()).st_size - offset

    if size != 0 and offset % mmap.ALLOCATIONGRANULARITY == 0:
        target = mmap.mmap(file_obj.fileno(), length=size,
                           offset=offset,
                           access=mmap.ACCESS_READ)
    else:
        target = file_obj
        target.seek(offset)

    while size > 0:
        data = target.read(chunk_size)
        generator.update(data[:min(len(data), size)])
        size -= len(data)

    if target is file_obj:
        file_obj.seek(offset)
    else:
        target.close()
    return generator.generate().digest()


def compute_hash_from_file(file_path, offset=0, size=None, chunk_size=1024*1024):
    with open(file_path, 'rb') as f:
        return compute_hash_from_file_obj(
            f, offset=offset, size=size, chunk_size=chunk_size)
        
def compute_hash_from_file_obj(file_obj, offset=0, size=None,
                                    chunk_size=1024 * 1024):
    etag = hashlib.md5()
    generator = TreeHashGenerator()

    size = size or os.fstat(file_obj.fileno()).st_size - offset

    if size != 0 and offset % mmap.ALLOCATIONGRANULARITY == 0:
        target = mmap.mmap(file_obj.fileno(), length=size,
                           offset=offset,
                           access=mmap.ACCESS_READ)
    else:
        target = file_obj
        target.seek(offset)

    while size > 0:
        data = target.read(chunk_size)
        generator.update(data[:min(len(data), size)])
        etag.update(data[:min(len(data), size)])
        size -= len(data)

    if target is file_obj:
        file_obj.seek(offset)
    else:
        target.close()
    return ( etag.hexdigest().upper(), generator.generate().digest())
