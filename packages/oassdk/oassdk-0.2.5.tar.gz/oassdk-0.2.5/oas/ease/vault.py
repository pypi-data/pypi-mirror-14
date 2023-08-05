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
import mmap
import os

from api import APIProxy
from job import Job
from uploader import Uploader
from utils import *


class Vault(object):
    _MEGABYTE = 1024 * 1024

    NormalUploadThreshold = 64 * _MEGABYTE

    ResponseDataParser = (('CreationDate', 'creation_date', None),
                          ('LastInventoryDate', 'last_inventory_date', None),
                          ('NumberOfArchives', 'number_of_archives', 0),
                          ('SizeInBytes', 'size', 0),
                          ('VaultId', 'id', None),
                          ('VaultName', 'name', None))

    def __init__(self, api, response):
        self.api = api
        for response_name, attr_name, default in self.ResponseDataParser:
            value = response.get(response_name)
            setattr(self, attr_name, value or default)

    def __repr__(self):
        return 'Vault: %s' % self.id

    @classmethod
    def create_vault(cls, api, name):
        api = APIProxy(api)
        response = api.create_vault(name)
        return Vault(api, api.describe_vault(response['x-oas-vault-id']))

    @classmethod
    def get_vault_by_id(cls, api, vault_id):
        api = APIProxy(api)
        return Vault(api, api.describe_vault(vault_id))

    @classmethod
    def get_vault_by_name(cls, api, vault_name):
        vaults = cls.list_all_vaults(api)
        for vault in vaults:
            if vault_name == vault.name:
                return vault
        raise ValueError('Vault not exists: %s' % vault_name)

    @classmethod
    def delete_vault_by_id(cls, api, vault_id):
        api = APIProxy(api)
        return api.delete_vault(vault_id)

    @classmethod
    def delete_vault_by_name(cls, api, vault_name):
        vaults = cls.list_all_vaults(api)
        for vault in vaults:
            if vault_name == vault.name:
                return vault.delete()
        raise ValueError('Vault not exists: %s' % vault_name)

    @classmethod
    def list_all_vaults(cls, api):
        api = APIProxy(api)
        result = api.list_vaults()
        return [Vault(api, data) for data in result['VaultList']]

    def list_all_multipart_uploads(self):
        result = self.api.list_multipart_uploads(self.id)
        return [Uploader(self, data) for data in result['UploadsList']]

    def list_all_jobs(self):
        result = self.api.list_jobs(self.id)
        return [Job(self, data) for data in result['JobList']]

    def delete(self):
        return self.api.delete_vault(self.id)

    def upload_archive(self, file_path, desc=None):
        length = os.path.getsize(file_path)
        if length > self.NormalUploadThreshold:
            return self.initiate_uploader(file_path, desc=desc).start()
        elif length > 0:
            return self._upload_archive_normal(file_path, desc=desc)
        else:
            raise ValueError('OAS does not support zero byte archive.')

    def _upload_archive_normal(self, file_path, desc):
        f = open_file(file_path=file_path)
        with f:
            file_size = content_length(f)
            etag = compute_etag_from_file(file_path)
            tree_etag = compute_tree_etag_from_file(file_path)
            mmapped_file = mmap.mmap(f.fileno(), length=file_size, offset=0,
                                     access=mmap.ACCESS_READ)
            try:
                response = self.api.upload_archive(self.id, mmapped_file,
                                                   etag, tree_etag,
                                                   size=file_size, desc=desc)
            finally:
                mmapped_file.close()
        return response['x-oas-archive-id']

    def initiate_uploader(self, file_path, desc=None):
        f = open_file(file_path=file_path)
        with f:
            size_total = content_length(f)
        part_size = Uploader.calc_part_size(size_total)

        response = self.api.initiate_multipart_upload(
            self.id, part_size, desc=desc)
        upload_id = response['x-oas-multipart-upload-id']

        response = self.api.describe_multipart(self.id, upload_id)
        return Uploader(self, response, file_path=file_path)

    def recover_uploader(self, upload_id):
        response = self.api.describe_multipart(self.id, upload_id)
        return Uploader(self, response)

    def delete_archive(self, archive_id):
        return self.api.delete_archive(self.id, archive_id)

    def get_job(self, job_id):
        response = self.api.describe_job(self.id, job_id)
        return Job(self, response)
    
    def pull_from_oss(self, osshost, bucket, object, desc=None):
        response = self.api.create_oss_transfer_job(
                  self.id, 'pull-from-oss', osshost, bucket, object, desc=desc)    
        return self.get_job(response['x-oas-job-id'])

    def push_to_oss(self, archive_id, osshost, bucket, object, desc=None):
        response = self.api.create_oss_transfer_job(
                  self.id, 'push-to-oss', osshost, bucket, object, archive_id=archive_id, desc=desc)    
        return self.get_job(response['x-oas-job-id'])

    def retrieve_archive(self, archive_id, desc=None, byte_range=None):
        response = self.api.create_job(
            self.id, 'archive-retrieval', archive_id=archive_id, desc=desc,
            byte_range='%d-%d' % byte_range
            if byte_range is not None else None)
        return self.get_job(response['x-oas-job-id'])

    def retrieve_inventory(self, desc=None):
        response = self.api.create_job(
            self.id, 'inventory-retrieval', desc=desc)
        return self.get_job(response['x-oas-job-id'])
