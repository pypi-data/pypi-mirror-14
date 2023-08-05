# -*- coding=UTF-8 -*-
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
import json
import httplib
import socket
import string
import sys
import time

from oas.oas_util import get_assign, append_param


class OASAPI(object):
    DefaultContentType = 'application/octet-stream'
    DefaultSendBufferSize = 8192
    DefaultGetBufferSize = 1024 * 1024 * 10
    provider = 'OAS'

    def __init__(self, host, accessId, accessKey, port=80, is_security=False):
        self.host = host
        self.port = port
        self.is_security = is_security
        self.access_id = accessId
        self.secret_access_key = accessKey

    def __get_connection(self):
        if self.is_security or self.port == 443:
            self.is_security = True
            return httplib.HTTPSConnection(host=self.host, port=self.port, timeout=100)
        else:
            return httplib.HTTPConnection(host=self.host, port=self.port, timeout=100)

    def __get_resource(self, params=None):
        if not params:
            return ''
        tmp_headers = {}
        for k, v in params.items():
            tmp_k = k.lower().strip()
            tmp_headers[tmp_k] = v
        override_response_list = [
            'limit', 'marker', 'response-content-type', 'response-content-language',
            'response-cache-control', 'logging', 'response-content-encoding',
            'acl', 'uploadId', 'uploads', 'partNumber', 'group',
            'delete', 'website', 'location', 'objectInfo',
            'response-expires', 'response-content-disposition']
        override_response_list.sort()
        resource = ''
        separator = '?'
        for i in override_response_list:
            if tmp_headers.has_key(i.lower()):
                resource += separator
                resource += i
                tmp_key = str(tmp_headers[i.lower()])
                if len(tmp_key) != 0:
                    resource += '='
                    resource += tmp_key
                separator = '&'
        return resource

    def __http_request(self, method, url, headers=None, body='', params=None):
        headers = headers or dict()
        headers['Date'] = time.strftime(
            '%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
        headers['User-Agent'] = 'OAS Python SDK'
        headers['Host'] = self.host
        headers['x-oas-version'] = '0.2.5'
        if len(body) > 0:
            headers['Content-Length'] = str(len(body))
        resource = url + self.__get_resource(params)
        if params is not None:
            url = append_param(url, params)
        headers['Authorization'] = self.__create_sign_for_normal_auth(
            method, headers, resource)
        conn = self.__get_connection()
        try:
            conn.request(method, url, body, headers)
            return conn.getresponse()
        except socket.timeout, e:
            raise Exception('Connect or send timeout! ' + e.message)

    def __http_reader_huge_cache_request(self, method, url, headers, content):
        try:
            conn = self.__get_connection()
            resource = url
            conn.putrequest(method, url)
            for k in headers.keys():
                conn.putheader(str(k), str(headers[k]))
            if '' != self.secret_access_key and '' != self.access_id:
                auth = self.__create_sign_for_normal_auth(
                    method, headers, resource)
                conn.putheader('Authorization', auth)

            conn.endheaders()
            send_buffer_size = 1024 * 1024
            sended_size = 0
            content_length = len(content)
            left_length = content_length
            while True:
                if sended_size == content_length:
                    break
                elif sended_size > content_length:
                    raise Exception(
                        'Sended data more than content_length set.')

                left_length = content_length - sended_size
                if left_length > send_buffer_size:
                    #buf = reader.read(send_buffer_size)
                    buf = content[sended_size:(send_buffer_size+sended_size)]
                else:
                    #buf = reader.read(left_length)
                    buf = content[sended_size:content_length]
                buf_len = len(buf)
                if buf_len > 0:
                    conn.send(buf)
                    sended_size = sended_size + buf_len
                else:
                    break

            if sended_size < content_length:
                raise Exception('Sended data less than content_length set.')

            return conn.getresponse()

        except socket.timeout, e:
            raise Exception('Connect or send timeout! ' + e.message)
        except socket.error, e:
            error_info = str(e)
            bpipe_error = '[Errno 32] Broken pipe'
            if string.find(error_info, bpipe_error) >= 0:
                return conn.getresponse()
            else:
                raise Exception('Request error! ' + str(e))

    def __http_reader_request(self, method, url, headers, reader, content_length):
        try:
            conn = self.__get_connection()
            resource = url
            conn.putrequest(method, url)
            for k in headers.keys():
                conn.putheader(str(k), str(headers[k]))
            if '' != self.secret_access_key and '' != self.access_id:
                auth = self.__create_sign_for_normal_auth(
                    method, headers, resource)
                conn.putheader('Authorization', auth)

            conn.endheaders()
            send_buffer_size = 1024 * 1024
            sended_size = 0
            left_length = content_length
            while True:
                if sended_size == content_length:
                    break
                elif sended_size > content_length:
                    raise Exception(
                        'Sended data more than content_length set.')

                left_length = content_length - sended_size
                if left_length > send_buffer_size:
                    buf = reader.read(send_buffer_size)
                else:
                    buf = reader.read(left_length)
                buf_len = len(buf)
                if buf_len > 0:
                    conn.send(buf)
                    sended_size = sended_size + buf_len
                else:
                    break

            if sended_size < content_length:
                raise Exception('Sended data less than content_length set.')

            return conn.getresponse()

        except socket.timeout, e:
            raise Exception('Connect or send timeout! ' + e.message)
        except socket.error, e:
            error_info = str(e)
            bpipe_error = '[Errno 32] Broken pipe'
            if string.find(error_info, bpipe_error) >= 0:
                return conn.getresponse()
            else:
                raise Exception('Request error! ' + str(e))

    def __create_sign_for_normal_auth(self, method, headers=None, resource='/'):
        '''
        NOT public API
        Create the authorization for BC based on header input.
        it should be put into "Authorization" parameter of header.

        :type method: string
        :param:one of PUT, GET, DELETE, HEAD

        :type headers: dict
        :param: HTTP header

        :type resource: string
        :param:path of bucket or object, eg: /bucket/ or /bucket/object

        Returns:
            signature string
        '''
        auth_value = '%s %s:%s' % (self.provider, self.access_id, get_assign(
            self.secret_access_key, method, headers, resource))
        return auth_value

    def create_vault(self, vault_name):
        url = '/vaults/%s' % (vault_name)
        method = 'PUT'
        return self.__http_request(method, url)

    def delete_vault(self, vault_id):
        url = '/vaults/%s' % (vault_id)
        method = 'DELETE'
        return self.__http_request(method, url)

    def list_vault(self, marker=None, limit=None):
        '''
            @param marker: not required , string, marker of start
            @param limit:  not required , int, retrive size
        '''
        url = '/vaults'
        method = 'GET'
        params = dict()
        if marker is not None:
            params['marker'] = marker
        if limit is not None:
            params['limit'] = limit
        return self.__http_request(method, url, params=params)

    def get_vault_desc(self, vault_id):
        url = '/vaults/%s' % (vault_id)
        method = 'GET'
        return self.__http_request(method, url)

    def post_archive(self, vault_id, content, etag, tree_etag, desc=None):
        '''
            Post content to oas as archive
            @param content: required , string , content of archive
        '''
        url = '/vaults/%s/archives' % vault_id
        method = 'POST'
        headers = dict()
        headers['Host'] = self.host
        headers['x-oas-content-etag'] = etag
        headers['x-oas-tree-etag'] = tree_etag
        if desc is not None:
            headers['x-oas-archive-description'] = desc
        date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
        headers['Content-Length'] = len(content)
        headers['Date'] = date

        if(len(content) < 512*1024*1024):
            return self.__http_request(method, url, headers, content)
        else:
            return self.__http_reader_huge_cache_request(method, url, headers, content)

    def post_archive_from_reader(self, vault_id, reader, content_length, etag, tree_etag, desc=None):
        '''
            Post archive from reader to oas
            @param content_length: required , int , byte length of archive
        '''
        url = '/vaults/%s/archives' % vault_id
        method = 'POST'
        headers = dict()
        headers['Host'] = self.host
        headers['x-oas-content-etag'] = etag
        headers['x-oas-tree-etag'] = tree_etag
        if desc is not None:
            headers['x-oas-archive-description'] = desc
        date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
        headers['Content-Length'] = content_length
        headers['Date'] = date

        return self.__http_reader_request(method, url, headers, reader, content_length)

    def delete_archive(self, vault_id, archive_id):
        url = '/vaults/%s/archives/%s' % (vault_id, archive_id)
        method = 'DELETE'
        headers = {}
        res = self.__http_request(method, url, headers)
        return res

    def head_archive(self, vault_id, archive_id):
        url = '/vaults/%s/archives/%s/meta' % (vault_id, archive_id)
        method = 'GET'
        headers = {}
        res = self.__http_request(method, url, headers)
        return res

    def create_multipart_upload(self, vault_id, partsize, desc=None):
        '''
            @param partsize:required, int, size of per part should be large than 64M(67108864) and mod 1M equals 0
        '''
        url = '/vaults/%s/multipart-uploads' % (vault_id)
        headers = {}
        headers['x-oas-part-size'] = str(partsize)
        if desc != None:
            headers['x-oas-archive-description'] = desc
        method = 'POST'
        res = self.__http_request(method, url, headers)
        return res

    def list_multipart_upload(self, vault_id, marker=None, limit=None):
        '''
            list all multipart uploads
        '''
        url = '/vaults/%s/multipart-uploads' % (vault_id)
        method = 'GET'
        params = {}
        if marker is not None:
            params['marker'] = marker
        if limit is not None:
            params['limit'] = limit
        headers = {}
        body = ''
        res = self.__http_request(method, url, headers, body, params)
        return res

    def complete_multipart_upload(self, vault_id, upload_id, filesize, tree_etag):
        '''
            complete multipart upload
        '''
        url = '/vaults/%s/multipart-uploads/%s' % (vault_id, upload_id)
        method = 'POST'
        headers = {}
        headers['x-oas-archive-size'] = str(filesize)
        headers['x-oas-tree-etag'] = tree_etag
        res = self.__http_request(method, url, headers)
        return res

    def delete_multipart_upload(self, vault_id, upload_id):
        '''
            delete multipart upload
        '''
        url = '/vaults/%s/multipart-uploads/%s' % (vault_id, upload_id)
        method = 'DELETE'
        headers = {}
        res = self.__http_request(method, url, headers)
        return res

    def post_multipart(self, vault_id, upload_id, content, prange, etag, tree_etag):
        '''
            post content to oas as multipart

            @param content:required, string, upload data content
            @param prange: required, string, upload data range eg: 0-67108863
        '''
        url = '/vaults/%s/multipart-uploads/%s' % (vault_id, upload_id)
        method = 'PUT'
        headers = {}
        headers['Host'] = self.host
        headers['Content-Length'] = len(content)
        headers['x-oas-content-etag'] = etag
        headers['x-oas-tree-etag'] = tree_etag
        date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
        headers['Date'] = date
        headers['Content-Range'] = prange

        if(len(content) < 512*1024*1024):
            return self.__http_request(method, url, headers, content)
        else:
            return self.__http_reader_huge_cache_request(method, url, headers, content)

    def post_multipart_from_reader(self, vault_id, upload_id, reader, content_length, prange, etag, tree_etag):
        '''
            post multipart from reader to oas

            @param content_length: size of post part , should be equal with the multipart upload setting,the last part can be less
            @param prange: required, string, upload data range eg: 0-67108863
        '''
        url = '/vaults/%s/multipart-uploads/%s' % (vault_id, upload_id)
        method = 'PUT'
        headers = {}
        headers['Host'] = self.host
        headers['Content-Length'] = content_length
        headers['x-oas-content-etag'] = etag
        headers['x-oas-tree-etag'] = tree_etag
        date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
        headers['Date'] = date
        headers['Content-Range'] = prange

        return self.__http_reader_request(method, url, headers, reader, content_length)

    def list_multipart(self, vault_id, upload_id, marker=None, limit=None):
        '''
            list all multiparts belong to one upload
        '''
        url = '/vaults/%s/multipart-uploads/%s' % (vault_id, upload_id)
        method = 'GET'
        params = dict()
        if marker is not None:
            params['marker'] = marker
        if limit is not None:
            params['limit'] = limit
        return self.__http_request(method, url, params=params)

    def create_job(self, vault_id, job_type, archive_id=None, desc=None, byte_range=None):
        '''
            create job
            @param job_type: required, string, can only be archive-retrieval or inventory-retrieval
            @param archive_id: not required, string, when job_type is archive-retrieval , archive_id must be set
        '''
        url = '/vaults/%s/jobs' % (vault_id)
        method = 'POST'
        body = dict()
        body['Type'] = job_type
        if job_type == 'archive-retrieval':
            body['ArchiveId'] = archive_id
            if byte_range is not None:
                body['RetrievalByteRange'] = byte_range
        if desc is not None:
            body['Description'] = desc
        body = json.dumps(body)
        return self.__http_request(method, url, body=body)

    def create_oss_transfer_job(self, vault_id, job_type, osshost, bucket, object, archive_id=None, desc=None):
        '''
            create push-to-oss/pull-from-oss job
            @param job_type: required, string, can only be push-to-oss or pull-from-oss
            @param archiveid: not required, string, when job_type is push-to-oss, archive_id must be set
        '''
        url = '/vaults/%s/jobs' % (vault_id)
        method = 'POST'
        body = dict()
        body['Type'] = job_type
        body['OSSHost'] = osshost
        body['Bucket'] = bucket
        body['Object'] = object
        if archive_id is not None:
            body['ArchiveId'] = archive_id
        if desc is not None:
            body['Description'] = desc
        body = json.dumps(body)
        return self.__http_request(method, url, body=body)

    def get_jobdesc(self, vault_id, job_id):
        url = '/vaults/%s/jobs/%s' % (vault_id, job_id)
        method = 'GET'
        return self.__http_request(method, url)

    def fetch_job_output(self, vault_id, job_id, orange=None):
        '''
           fetch job output
           @param orange: not required , string, fetch byte range like bytes=0-1048575
        '''
        url = '/vaults/%s/jobs/%s/output' % (vault_id, job_id)
        method = 'GET'
        headers = dict()
        if orange is not None:
            headers['Range'] = orange
        return self.__http_request(method, url, headers)

    def list_job(self, vault_id, marker=None, limit=None):
        '''
            fetch all jobs
        '''
        url = '/vaults/%s/jobs' % (vault_id)
        method = 'GET'
        params = dict()
        if marker is not None:
            params['marker'] = marker
        if limit is not None:
            params['limit'] = limit
        return self.__http_request(method, url, params=params)
