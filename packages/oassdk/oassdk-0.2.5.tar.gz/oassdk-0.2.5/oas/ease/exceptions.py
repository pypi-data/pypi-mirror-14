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
import json

from httplib import HTTPException


class OASServerError(Exception):

    def __init__(self, response):
        raw_headers = response.getheaders()
        headers = dict()
        for k, v in raw_headers:
            headers[k.lower()] = v

        self.request_id = headers.get('x-oas-request-id')
        self.status = response.status

        content = ''
        try:
            content = response.read()
            body = json.loads(content)
            self.code = body.get('code')
            self.type = body.get('type')
            self.message = body.get('message')
            msg = 'Expected 2xx, got '
            msg += '(%d, code=%s, message=%s, type=%s, request_id=%s)' % \
                   (self.status, self.code,
                    self.message, self.type, self.request_id)
        except (HTTPException, ValueError):
            msg = 'Expected 2xx, got (%d, content=%s, request_id=%s)' % \
                  (self.status, content, self.request_id)

        super(OASServerError, self).__init__(msg)


class OASClientError(Exception):
    pass


class UploadArchiveError(OASClientError):
    pass


class DownloadArchiveError(OASClientError):
    pass


class HashDoesNotMatchError(OASClientError):
    pass
