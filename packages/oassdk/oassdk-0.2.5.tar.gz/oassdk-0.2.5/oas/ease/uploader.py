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
from __future__ import division

import logging
import random
import time
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict
from multiprocessing.pool import ThreadPool

from exceptions import *
from merkle import *
from utils import *

log = logging.getLogger(__name__)


class Uploader(object):
    _MEGABYTE = 1024 * 1024
    _GIGABYTE = 1024 * _MEGABYTE

    MinimumPartSize = 64 * _MEGABYTE
    MaximumNumberOfParts = 10000
    NumberThread = 8
    NumberRetry = 3

    ResponseDataParser = (('ArchiveDescription', 'description', None),
                          ('CreationDate', 'creation_date', None),
                          ('MultipartUploadId', 'id', None),
                          ('PartSizeInBytes', 'part_size', 0))

    def __init__(self, vault, response, file_path=None):
        self.vault = vault
        for response_name, attr_name, default in self.ResponseDataParser:
            value = response.get(response_name)
            setattr(self, attr_name, value or default)
        self.parts = OrderedDict()
        self.file_path = file_path
        self.size_total = 0

        if self.file_path is not None:
            self._prepare(self.file_path)

    def __repr__(self):
        return 'Multipart Upload: %s' % self.id

    @classmethod
    def calc_part_size(cls, size_total, part_size=MinimumPartSize):
        if size_total > 4*10000 * cls._GIGABYTE:
            raise ValueError('File too big: %d' % size_total)

        if size_total < cls.MinimumPartSize:
            raise ValueError('File too small: %d, '
                             'please use vault.upload_archive' %
                             size_total)

        if part_size % cls._MEGABYTE != 0 or \
                part_size < cls.MinimumPartSize or \
                part_size > size_total:
            part_size = cls.MinimumPartSize

        number_parts = calc_num_part(part_size, size_total)
        if number_parts > cls.MaximumNumberOfParts:
            part_size_refer = math.ceil(
                size_total / cls.MaximumNumberOfParts / cls._MEGABYTE)
            part_size_refer = int(part_size_refer * cls._MEGABYTE)
            part_bit_len = part_size_refer.bit_length() - 1
            part_size = 1<< part_bit_len
            while True:
                if(part_size >= part_size_refer):
                    break
                part_bit_len += 1
                part_size = 1<< part_bit_len
        return part_size

    @classmethod
    def parse_range_from_str(cls, string):
        return tuple([int(num) for num in string.split('-')])

    def _prepare(self, file_path):
        self.file_path = file_path
        f = open_file(self.file_path)
        with f:
            self.size_total = content_length(f)
        for byte_range in calc_ranges(self.part_size, self.size_total):
            self.parts[byte_range] = None

    def resume(self, file_path):
        self._prepare(file_path)

        result = self.vault.api.list_parts(self.vault.id, self.id)

        for parts in result['Parts']:
            byte_range = self.parse_range_from_str(parts['RangeInBytes'])
            self.parts[byte_range] = (
                parts['ContentEtag'], parts['TreeEtag'])
            etag = compute_etag_from_file(
                self.file_path, offset=byte_range[0],
                size=range_size(byte_range))
            if etag != self.parts[byte_range][0]:
                raise HashDoesNotMatchError(
                    'Hash does not match for %d-%d: %s, which %s excepted' %
                    (byte_range[0], byte_range[1], etag,
                     self.parts[byte_range][0]))

        return self.start()

    def start(self):
        def upload_part(byte_range):
            try:
                time.sleep(random.randint(256, 4096) / 1000)

                offset = byte_range[0]
                size = range_size(byte_range)
                etag = compute_etag_from_file(
                    self.file_path, offset=offset, size=size)
                tree_etag = compute_tree_etag_from_file(
                    self.file_path, offset=offset, size=size)

                f = open_file(self.file_path)
                with f:
                    for cnt in xrange(self.NumberRetry):
                        try:
                            if self.part_size % mmap.ALLOCATIONGRANULARITY == 0:
                                target = mmap.mmap(f.fileno(), length=size,
                                                   offset=offset,
                                                   access=mmap.ACCESS_READ)
                            else:
                                f.seek(offset)
                                target = f

                            self.vault.api.upload_part(
                                self.vault.id, self.id, target, byte_range,
                                etag = etag, tree_etag=tree_etag)
                            self.parts[byte_range] = (etag, tree_etag)
                            log.info('Range %d-%d upload success.' % byte_range)
                            return
                        except OASServerError as e:
                            log.error('upload %s range %d-%d upload failed. etag: %s. Reason: %s' %
                                      (self.id, byte_range[0], byte_range[1], etag, e))
                            if e.code != 'InvalidDigest' or e.type != 'client':
                                return
                        except IOError as e:
                            log.error('uploadid %s range %d-%d upload failed. Reason: %s' %
                                      (self.id, byte_range[0], byte_range[1], e))
                            continue
                        except Exception as e:
                            log.error('upload %s range %d-%d upload failed. etag: %s. Error: %s' %
                                      (self.id, byte_range[0], byte_range[1], etag, e))
                            continue
                        finally:
                            if 'target' in locals() and target is not f:
                                target.close()
            except Exception as e:
                log.error('Upload %s range %d-%d upload finally failed. Reason: %s' %
                               (self.id, byte_range[0], byte_range[1], e))
                raise


        log.info('Start upload %s from %s.' % (self.id, self.file_path))
        try:
            pool = ThreadPool(processes=min(self.NumberThread, len(self.parts)))
            pool.map(upload_part, [byte_range
                                   for byte_range, tag in self.parts.items()
                                   if tag is None])

            size = self.size_completed
            if size != self.size_total:
                raise UploadArchiveError(
                    'Incomplete upload %s : %d / %d' % (self.id, size, self.size_total))


            response = self.vault.api.complete_multipart_upload(
                self.vault.id, self.id, self.size_total,
                 self.tree_hash)

            log.info('Upload %s finish.' % (self.id ))
            return response['x-oas-archive-id']
        except UploadArchiveError as e:
            errorinfo = 'upload %s failed, cause:%s' % (self.id, e)
            log.error(errorinfo)
            raise e
        except Exception as e:
            errorinfo = 'upload %s failed, cause:%s' % (self.id, e)
            log.error(errorinfo)
            raise ValueError(errorinfo)

    def cancel(self):
        return self.vault.api.cancel_multipart_upload(self.vault.id, self.id)

    @property
    def size_completed(self):
        size_list = [range_size(byte_range)
                     for byte_range, tag in self.parts.items()
                     if tag is not None]
        return sum(size_list)


    @property
    def tree_hash(self):
        tree_etag_list = [tag[1] for _, tag in self.parts.items()
                          if tag is not None]
        return MerkleTree().load(tree_etag_list).digest() \
            if len(tree_etag_list) == len(self.parts) else ''
