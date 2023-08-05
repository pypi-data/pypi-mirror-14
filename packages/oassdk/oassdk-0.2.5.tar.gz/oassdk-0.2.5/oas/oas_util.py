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
import base64
import hashlib
from hashlib import sha1 as sha
import hmac
import urllib
from datetime import tzinfo, timedelta

SELF_DEFINE_HEADER_PREFIX = "x-oas-"


class UTC(tzinfo):

    """UTC"""

    def __init__(self, offset=0):
        self._offset = offset

    def utcoffset(self, dt):
        return timedelta(hours=self._offset)

    def tzname(self, dt):
        return "UTC +%s" % self._offset

    def dst(self, dt):
        return timedelta(hours=self._offset)


def safe_get_element(name, container):
    for k, v in container.items():
        if k.strip().lower() == name.strip().lower():
            return v
    return ""


def format_header(headers=None):
    '''
        format the headers that self define
        convert the self define headers to lower.
    '''
    if not headers:
        headers = {}
    tmp_headers = {}
    for k in headers.keys():
        if isinstance(headers[k], unicode):
            headers[k] = headers[k].encode('utf-8')

        if k.lower().startswith(SELF_DEFINE_HEADER_PREFIX):
            k_lower = k.lower()
            tmp_headers[k_lower] = headers[k]
        else:
            tmp_headers[k] = headers[k]
    return tmp_headers


def get_assign(secret_access_key, method, headers=None, resource="/", result=None):
    '''
        Create the authorization for BC based on header input.
        You should put it into "Authorization" parameter of header.
    '''
    if not headers:
        headers = {}
    if not result:
        result = []

    canonicalized_bc_headers = ""
    date = safe_get_element('Date', headers)
    canonicalized_resource = resource
    tmp_headers = format_header(headers)
    if len(tmp_headers) > 0:
        x_header_list = tmp_headers.keys()
        x_header_list.sort()
        for k in x_header_list:
            if k.startswith(SELF_DEFINE_HEADER_PREFIX):
                canonicalized_bc_headers += k + ":" + tmp_headers[k] + "\n"
    string_to_sign = method + "\n" + date + "\n" + \
        canonicalized_bc_headers + canonicalized_resource
    result.append(string_to_sign)
    h = hmac.new(secret_access_key, string_to_sign, sha)
    return base64.encodestring(h.digest()).strip()


def append_param(url, params):
    '''
        convert the parameters to query string of URI.
    '''
    l = []
    for k, v in params.items():
        k = k.replace('_', '-')
        if k == 'maxkeys':
            k = 'max-keys'
        if isinstance(v, unicode):
            v = v.encode('utf-8')
        if v is not None and v != '':
            l.append('%s=%s' % (urllib.quote(k), urllib.quote(str(v))))
        elif k == 'acl':
            l.append('%s' % (urllib.quote(k)))
        elif v is None or v == '':
            l.append('%s' % (urllib.quote(k)))
    if len(l):
        url = url + '?' + '&'.join(l)
    return url
