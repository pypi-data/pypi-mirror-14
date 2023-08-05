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
from oas.oas_api import OASAPI

from exceptions import OASServerError
from response import OASResponse
from utils import *


class APIProxy(object):

    def __init__(self, api):
        self.api = api

    def __getattr__(self, name):
        methods = [
            'create_vault', 'delete_vault', 'list_vault', 'get_vault_desc',
            'post_archive', 'post_archive_from_reader', 'delete_archive', 'head_archive',
            'create_multipart_upload', 'list_multipart_upload',
            'complete_multipart_upload', 'delete_multipart_upload',
            'post_multipart', 'post_multipart_from_reader', 'list_multipart',
            'create_job', 'create_oss_transfer_job', 'get_jobdesc', 'fetch_job_output', 'list_job']

        transform = {'describe_vault': 'get_vault_desc',
                     'describe_job': 'get_jobdesc',
                     'describe_multipart': 'list_multipart',
                     'initiate_multipart_upload': 'create_multipart_upload',
                     'cancel_multipart_upload': 'delete_multipart_upload'}

        if name in transform:
            name = transform[name]

        if name not in methods:
            return object.__getattribute__(self, name)

        def wrapped(*args, **kwargs):
            try:
                res = OASAPI.__getattribute__(self.api, name)(*args, **kwargs)
            except Exception as e:
                raise IOError(str(e))

            if res.status / 100 == 2:
                return OASResponse(res)
            else:
                raise OASServerError(res)
        return wrapped

    def list_vaults(self):
        result = self.list_vault()
        marker = result['Marker']
        while marker:
            res = self.list_vault(marker=marker)
            result['VaultList'].extend(res['VaultList'])
            marker = res['Marker']
        result['Marker'] = None
        return result

    def list_multipart_uploads(self, vault_id):
        result = self.list_multipart_upload(vault_id)
        marker = result['Marker']
        while marker:
            res = self.list_multipart_upload(vault_id, marker=marker)
            result['UploadsList'].extend(res['UploadsList'])
            marker = res['Marker']
        result['Marker'] = None
        return result

    def list_parts(self, vault_id, upload_id):
        result = self.list_multipart(vault_id, upload_id)
        marker = result['Marker']
        while marker:
            res = self.list_multipart(vault_id, upload_id, marker=marker)
            result['Parts'].extend(res['Parts'])
            marker = res['Marker']
        result['Marker'] = None
        return result

    def list_jobs(self, vault_id):
        result = self.list_job(vault_id)
        marker = result['Marker']
        while marker:
            res = self.list_job(vault_id, marker=marker)
            result['JobList'].extend(res['JobList'])
            marker = res['Marker']
        result['Marker'] = None
        return result

    def upload_archive(self, vault_id, content, etag, tree_etag,
                       size=None, desc=None):
        if is_file_like(content):
            return self.post_archive_from_reader(
                vault_id, content, min(size, content_length(content)),
                etag, tree_etag, desc=desc)
        else:
            return self.post_archive(vault_id, content,
                                     etag, tree_etag, desc=desc)

    def upload_part(self, vault_id, upload_id, content, byte_range,
                    etag, tree_etag):
        if is_file_like(content):
            size_total = content_length(content)
            if range_size(byte_range) > size_total:
                raise ValueError('Byte range exceeded: %d-%d' % byte_range)
            return self.post_multipart_from_reader(
                vault_id, upload_id, content, range_size(byte_range),
                '%d-%d' % byte_range, etag, tree_etag)
        else:
            return self.post_multipart(
                vault_id, upload_id, content,
                '%d-%d' % byte_range, etag, tree_etag)

    def get_job_output(self, vault_id, job_id, byte_range=None):
        return self.fetch_job_output(vault_id, job_id,
                                     'bytes=%d-%d' % byte_range)
