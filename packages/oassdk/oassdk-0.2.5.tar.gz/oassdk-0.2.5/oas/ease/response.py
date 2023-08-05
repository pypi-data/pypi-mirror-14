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
import io
import json
import yaml


class OASResponse(dict):
    def __init__(self, response):
        super(dict, self).__init__()

        raw_headers = response.getheaders()
        headers = dict()
        for k, v in raw_headers:
            headers[k.lower()] = v

        self.status = response.status
        self.request_id = headers['x-oas-request-id']
        self.response = response

        for k, v in headers.items():
            self[k] = v

        content_type = headers.get('content-type')
        if content_type == 'application/octet-stream':
            self.reader = response
            return

        try:
            body = response.read()
            self.reader = io.BytesIO(body)
            if 'content-range' in self:
                return
            if content_type == 'application/json':
                self.update(json.loads(body))
            else:
                content = yaml.load(body)
                if content is not None:
                    self.update(content)
        except Exception as e:
            raise IOError(e.message)

    def read(self, size):
        return self.reader.read(size)
