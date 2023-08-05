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
import datetime
import json
import os
import sys
import time
import hashlib
from collections import namedtuple
import ConfigParser

from oas_api import OASAPI
from oas_util import UTC
from oas.ease.utils import *

OAS_PREFIX = 'oas://'
DEFAULT_HOST = 'cn-hangzhou.oas.aliyuncs.com'
DEFAULT_PORT = 80
DEFAULT_CONFIGFILE = os.path.expanduser('~') + '/.oascredentials'
CONFIGSECTION = 'OASCredentials'

def convert_time_format(t):
    if not t:
        return ''
    t_datetime = datetime.datetime.strptime(t, '%a, %d %b %Y %H:%M:%S GMT')
    utc_timestamp = time.mktime(t_datetime.timetuple())
    utc8_datetime = datetime.datetime.fromtimestamp(utc_timestamp, UTC(16))
    return utc8_datetime.strftime('%Y-%m-%d %H:%M:%S')

def check_response(res):
    try:
        if res.status / 100 != 2:
            errmsg = ''
            errmsg += 'Error Headers:\n'
            errmsg += str(res.getheaders())
            errmsg += '\nError Body:\n'
            errmsg += res.read(1024)
            errmsg += '\nError Status:\n'
            errmsg += str(res.status)
            errmsg += '\nFailed!\n'
            sys.stderr.write(errmsg)
            sys.exit(1)
    except AttributeError, e:
        sys.stderr.write('Error: check response status failed! msg: %s\n' % e)
        sys.exit(1)

def parse_vault_name(path):
    if not path.lower().startswith(OAS_PREFIX):
        sys.stderr.write('oas vault path must start with %s\n' % OAS_PREFIX)
        sys.exit(1)
    path_fields = path[len(OAS_PREFIX):].split('/')
    name = path_fields[0]
    return name

class OASCMD(object):

    def __init__(self, auth_info):
        self.api = OASAPI(auth_info.host, auth_info.accessId,
                          auth_info.accessKey, port=auth_info.port)

    def byte_humanize(self, byte):
        if byte == None: return ''
        unitlist = ['B', 'K', 'M', 'G', 'T', 'P']
        unit = unitlist[0]
        for i in range(len(unitlist)):
            unit = unitlist[i]
            if int(byte) // 1024 == 0:
                break
            byte = float(byte) / 1024
        return '%.2f %s' % (byte, unit if unit == 'B' else unit+'B')

    def parse_size(self, size):
        try:
            if size == None: return size
            if isinstance(size, (int, long)): return size
            size = size.rstrip('B')
            if size.isdigit(): return int(size)
            byte, unit = int(size[:-1]), size[-1].upper()
            unitlist = ['B', 'K', 'M', 'G', 'T', 'P']
            if unit not in unitlist:
                byte = int(size)
            else:
                idx = unitlist.index(unit)
                for _ in range(idx): byte *= 1024
            return byte
        except Exception, e:
            sys.stderr.write('[Error]: Inapropriate size %s provided\n' % size)
            sys.stderr.write('Only numbers, optionally ended with K, M, G, ' \
                             'T, P are accepted, units are case insensitive\n')
            sys.exit(1)

    def kv_print(self, idict, title=None):
        keys = title or idict.keys()
        maxlen = max([len(t) for t in keys])
        fmt = u'{:>{lname}}: {}'
        for k in keys:
            print fmt.format(k, idict[k], lname=maxlen)

    def fetch_vault_id(self, vault_name):
        marker = ''
        while True:
            res = self.api.list_vault(marker, 10)
            check_response(res)
            response_content = res.read()
            rjson = json.loads(response_content, 'UTF8')
            marker = rjson['Marker']
            vault_list = rjson['VaultList']
            if vault_list:
                for vault_info in vault_list:
                    if vault_info['VaultName'] == vault_name:
                        return str(vault_info['VaultId'])

            if not marker:
                break
        sys.stderr.write("Error: vault with name '%s' not found\n" % vault_name)
        sys.exit(1)

    def cmd_ls(self, args):
        return self.cmd_listvault(args)

    def cmd_cv(self, args):
        return self.cmd_createvault(args)

    def cmd_rm(self, args):
        if not args.archiveId:
            return self.cmd_deletevault(args)
        return self.cmd_deletearchive(args)

    def cmd_upload(self, args):
        if not args.filename or not os.path.isfile(args.filename):
            sys.stderr.write("Error: file '%s' not existed\n" % args.filename)
            sys.exit(1)
        size = os.path.getsize(args.filename)
        desc = args.desc or args.filename[:128]
        if (not args.part_size and size >= 100*1024*1024) or \
                (args.part_size and size > 32*1024*1024):
            resume = 0
            if not args.uploadid:
                partsize = self.parse_size(args.part_size)
                if partsize:
                    if partsize % (32*1024*1024) != 0:
                        sys.stderr.write('Error: partsize must be divided by 32MB!\n')
                        sys.exit(1)
                    if partsize * 10000 < size:
                        print 'specified partsize too small, will be adjusted'
                    if partsize > size:
                        print 'specified partsize too large, will be adjusted'
                        while partsize > size:
                            partsize /= 2
                else:
                    print 'File larger than 100MB, multipart upload will be used'
                    partsize = 32*1024*1024
                while partsize * 10000 < size:
                    partsize *= 2
                nparts = size // partsize
                if size % partsize: nparts += 1
                print 'Use %s parts with partsize %s to upload' % \
                        (nparts, self.byte_humanize(partsize))

                Create = namedtuple('Namespace', ['vault', 'part_size', 'desc'])
                cargs = Create(args.vault, partsize, desc)
                uploadid = self.cmd_createmupload(cargs)
            else:
                uploadid = args.uploadid
                vault_name = parse_vault_name(args.vault)
                vaultId = self.fetch_vault_id(vault_name)
                res = self.api.list_multipart(vaultId, uploadid, None, None)
                check_response(res)
                rjson = json.loads(res.read(), 'UTF8')
                plist = rjson['Parts']
                partsize = rjson['PartSizeInBytes']
                nparts = size // partsize
                if size % partsize: nparts += 1
                if plist:
                    resumebytes = max([int(x['RangeInBytes'].split('-')[1]) \
                                       for x in plist]) + 1
                    if resumebytes == size:
                        resume = nparts
                    else:
                        resume = resumebytes // partsize
                print 'Resume last upload with partsize %s' % \
                        self.byte_humanize(partsize)
            Part = namedtuple('Namespace', ['vault', 'uploadid', 'filename',
                'start', 'end', 'etag', 'tree_etag'])
            start = 0
            etaglist = []
            for i in range(nparts):
                end = min(size, start+partsize)-1
                etag, tree_etag = compute_hash_from_file(args.filename, start,
                                                         end-start+1)
                pargs = Part(args.vault, uploadid, args.filename, start,
                             end, etag, tree_etag)
                start += partsize
                etaglist.append(tree_etag)
                if i < resume: continue
                print 'Uploading part %s...' % (i+1)
                self.cmd_postmpart(pargs)
            Complete = namedtuple('Namespace', ['vault', 'uploadid',
                                                'size', 'tree_etag'])
            etree = compute_combine_tree_etag_from_list(etaglist)
            cargs = Complete(args.vault, uploadid, size, etree)
            self.cmd_completemupload(cargs)
            return
        if size <= 32*1024*1204 and args.part_size:
            print 'File smaller than 32MB, part-size will be ignored.'
        Post = namedtuple('Namespace', ['vault', 'filename', 'etag',
                                        'tree_etag', 'desc'])
        etag, tree_etag = compute_hash_from_file(args.filename)
        pargs = Post(args.vault, args.filename, etag, tree_etag, desc)
        return self.cmd_postarchive(pargs)

    def cmd_fetch(self, args):
        return self.cmd_fetchjoboutput(args)

    def cmd_createvault(self, args):
        vault_name = parse_vault_name(args.vault)
        res = self.api.create_vault(vault_name)
        check_response(res)
        vault_id = res.getheader('x-oas-vault-id')
        print 'Vault ID: %s' % vault_id

    def cmd_deletevault(self, args):
        vault_name = parse_vault_name(args.vault)
        vault_id = self.fetch_vault_id(vault_name)
        res = self.api.delete_vault(vault_id)
        check_response(res)
        print 'Delete success'

    def cmd_listvault(self, args):
        marker = args.marker
        limit = args.limit
        res = self.api.list_vault(marker, limit)
        check_response(res)
        rjson = json.loads(res.read(), 'UTF8')
        marker = rjson['Marker']
        vault_list = rjson['VaultList']
        print 'Marker: %s' % marker
        print 'Vault count: %s' % len(vault_list)
        if vault_list:
            max_name = max(max([len(v['VaultName']) for v in vault_list]),
                           len('VaultName')) + 1
            fmt = u'{:<32} {:{lname}} {:<20} {:<16} {:<12} {:<20}'
            title = ('VaultID', 'VaultName', 'CreationDate', 'NumberOfArchives',
                     'TotalSize', 'LastInventoryDate')
            print fmt.format(*title, lname=max_name)
            print '-' * (105+max_name)
            for vault in vault_list:
                print fmt.format(
                     vault['VaultId'], vault['VaultName'],
                     convert_time_format(vault['CreationDate']),
                     vault['NumberOfArchives'],
                     self.byte_humanize(vault['SizeInBytes']),
                     convert_time_format(vault['LastInventoryDate']),
                     lname=max_name)

    def cmd_getvaultdesc(self, args):
        vault_name = parse_vault_name(args.vault)
        vault_id = self.fetch_vault_id(vault_name)
        res = self.api.get_vault_desc(vault_id)
        check_response(res)
        rjson = json.loads(res.read(), 'UTF8')
        title = ('VaultId', 'VaultName', 'CreationDate', 'NumberOfArchives',
                 'SizeInBytes', 'LastInventoryDate')
        for k in ('CreationDate', 'LastInventoryDate'):
            rjson[k] = convert_time_format(rjson[k])
        self.kv_print(rjson, title)

    def cmd_postarchive(self, args):
        vault_name = parse_vault_name(args.vault)
        vault_id = self.fetch_vault_id(vault_name)
        filepath = args.filename
        desc = args.desc or args.filename[:128]
        if not os.path.isfile(filepath):
            sys.stderr.write("Error: file '%s' not existed!\n" % filepath)
            sys.exit(1)

        file_size = os.path.getsize(filepath)
        etag = args.etag.upper() if args.etag else ''
        tree_etag = args.tree_etag.upper() if args.tree_etag else ''
        if not (etag and tree_etag):
            tmpsum, tmptree = compute_hash_from_file(args.filename)
            etag = etag or tmpsum
            tree_etag = tree_etag or tmptree
        with open(filepath, 'rb') as fp:
            res = self.api.post_archive_from_reader(
                vault_id, fp, file_size, etag, tree_etag, desc)
            check_response(res)
        archive_id = res.getheader('x-oas-archive-id')
        print 'Archive ID: %s' % archive_id

    def cmd_deletearchive(self, args):
        vault_name = parse_vault_name(args.vault)
        vault_id = self.fetch_vault_id(vault_name)
        res = self.api.delete_archive(vault_id, args.archiveId)
        check_response(res)
        print 'Delete success'

    def cmd_fileetag(self, args):
        if not os.path.isfile(args.filename):
            sys.stderr.write("Error: file '%s' not existed!\n" % args.filename)
            sys.exit(1)
        etag, tree_etag = compute_hash_from_file(args.filename)
        print "etag     :", etag
        print "tree_etag:", tree_etag

    def cmd_partetag(self, args):
        if not os.path.isfile(args.filename):
            sys.stderr.write("Error: file '%s' not existed!\n" % args.filename)
            sys.exit(1)
        start = self.parse_size(args.start)
        end = self.parse_size(args.end)
        if end % (1024*1024) == 0: end -= 1
        size = end - start + 1
        etag, tree_etag = compute_hash_from_file(args.filename, start, size)
        print "etag     :", etag
        print "tree_etag:", tree_etag

    def cmd_createmupload(self, args):
        vault_name = parse_vault_name(args.vault)
        vault_id = self.fetch_vault_id(vault_name)
        part_size = self.parse_size(args.part_size)
        desc = args.desc
        res = self.api.create_multipart_upload(vault_id, part_size, desc)
        check_response(res)
        upload_id = res.getheader('x-oas-multipart-upload-id')
        print 'MultiPartUpload ID: %s' % upload_id
        return upload_id

    def cmd_listmupload(self, args):
        vault_name = parse_vault_name(args.vault)
        vault_id = self.fetch_vault_id(vault_name)
        marker = args.marker
        limit = args.limit
        res = self.api.list_multipart_upload(vault_id, marker, limit)
        check_response(res)
        rjson = json.loads(res.read(), 'UTF8')
        marker = rjson['Marker']
        upload_list = rjson['UploadsList']
        print 'Marker: %s' % marker
        print 'Multipart upload count: %s' % len(upload_list)
        if upload_list:
            print
            maxdesc = max(max([len(m['ArchiveDescription']) for m in upload_list]),
                          len('ArchiveDescription')) + 1
            fmt = u'{:<32} {:<20} {:<10} {:<{ldesc}}'
            title = ('MultipartUploadId', 'CreationDate', 'PartSize',
                     'ArchiveDescription')
            print fmt.format(*title, ldesc=maxdesc)
            print '-' * (64+maxdesc)
            for upload in upload_list:
                print fmt.format(
                     upload['MultipartUploadId'],
                     convert_time_format(upload['CreationDate']),
                     self.byte_humanize(upload['PartSizeInBytes']),
                     upload['ArchiveDescription'],
                     ldesc=maxdesc)
            print

    def cmd_completemupload(self, args):
        vault_name = parse_vault_name(args.vault)
        vault_id = self.fetch_vault_id(vault_name)
        upload_id = args.uploadid
        file_size = self.parse_size(args.size)
        tree_etag = args.tree_etag.upper() if args.tree_etag else ''

        res = self.api.complete_multipart_upload(
            vault_id, upload_id, file_size,  tree_etag)
        check_response(res)
        archive_id = res.getheader('x-oas-archive-id')
        print 'Archive ID: %s' % archive_id

    def cmd_deletemupload(self, args):
        vault_name = parse_vault_name(args.vault)
        vault_id = self.fetch_vault_id(vault_name)
        res = self.api.delete_multipart_upload(vault_id, args.uploadid)
        check_response(res)
        print 'Delete success'

    def cmd_postmpart(self, args):
        vault_name = parse_vault_name(args.vault)
        vault_id = self.fetch_vault_id(vault_name)
        upload_id = args.uploadid
        filepath = args.filename
        start = self.parse_size(args.start)

        if not filepath or not os.path.isfile(filepath):
            sys.stderr.write("Error: file '%s' not existed!\n" % filepath)
            sys.exit(1)

        totalsize = os.path.getsize(filepath)
        end = args.end
        size = long(end) - long(start) + 1
        etag = args.etag.upper() if args.etag else None
        tree_etag = args.tree_etag.upper() if args.tree_etag else None
        if not (etag and tree_etag):
            tmpsum, tmptree = compute_hash_from_file(args.filename, start, size)
            etag = etag or tmpsum
            tree_etag = tree_etag or tmptree
        with open(filepath, 'rb') as file_reader:
            prange = '%s-%s' % (start, end)
            file_reader.seek(long(start))
            res = self.api.post_multipart_from_reader(
                vault_id, upload_id, file_reader, size,
                prange, etag, tree_etag)
            check_response(res)
        print 'Upload success'

    def cmd_listmpart(self, args):
        vault_name = parse_vault_name(args.vault)
        vault_id = self.fetch_vault_id(vault_name)
        upload_id = args.uploadid
        marker = args.marker
        limit = args.limit
        res = self.api.list_multipart(vault_id, upload_id, marker, limit)
        check_response(res)
        rjson = json.loads(res.read(), 'UTF8')
        rjson['CreationDate'] = convert_time_format(rjson['CreationDate'])
        title = ('MultipartUploadId', 'CreationDate', 'PartSizeInBytes',
                 'ArchiveDescription', 'Marker')
        self.kv_print(rjson, title)
        part_list = rjson['Parts']
        print '-' * 52
        print 'Part count: %s' % len(part_list)
        if len(part_list) > 0:
            print 'Part Ranges: '
            maxlen = max([len(p['RangeInBytes']) for p in part_list])
            fmt = u'{:>{lrange}}: {}'
            for part in part_list:
                print fmt.format(part['RangeInBytes'], part['ContentEtag'],
                                 lrange=maxlen)

    def cmd_createjob(self, args):
        vault_name = parse_vault_name(args.vault)
        vault_id = self.fetch_vault_id(vault_name)
        archive_id = args.archiveId
        desc = args.desc
        start = self.parse_size(args.start)
        size = self.parse_size(args.size)

        jtype = 'archive-retrieval' if args.archiveId else 'inventory-retrieval'
        if jtype == 'inventory-retrieval':
            if start or size:
                print 'Tip: Inventory-retrieval does NOT support range, ignored'
                start = size = None

        byte_range = None
        if (start != None and size != None):
            byte_range = '%s-%s' % (start, start+size-1)
        elif (start != None and size == None):
            res = self.api.head_archive(vault_id, archive_id)
            check_response(res)
            totalsize = json.loads(res.read(), 'UTF8')['ArchiveSizeInBytes']
            byte_range = '%s-%s' % (start, totalsize-1)
        elif (start == None and size != None):
            byte_range = '0-%s' % (size-1)
        if byte_range:
            print 'Archive retrieval range: %s' % byte_range

        res = self.api.create_job(
            vault_id, jtype, archive_id, desc, byte_range)
        check_response(res)
        job_id = res.getheader('x-oas-job-id')
        print '%s job created, job ID: %s' % (jtype, job_id)
        print 'Use\n\n    oascmd.py fetch %s %s <localfile>\n\nto check job ' \
              'progress and download the data when job finished' % \
              (args.vault, job_id)
        print 'NOTICE: Jobs usually take about 4 HOURS to complete.'
        return job_id

    def cmd_cp(self, args):
        src, dst = args.source, args.destination
        if not (src.startswith('oss://') and dst.startswith(OAS_PREFIX)) and \
                not (src.startswith(OAS_PREFIX) and dst.startswith('oss://')):
            sys.stderr.write('[Error]: Only paths startswith oss:// or ' \
                             '%s are supported\n' % OAS_PREFIX)
            return
        bucket = obj = vault_name = archiveId = None
        try:
            if src.startswith('oss://'):
                jtype  = 'pull-from-oss'
                ossstr = src[len('oss://'):]
                slash = ossstr.find('/')
                if slash == -1: raise ValueError
                desc   = args.desc or 'copy from %s' % ossstr
                desc   = desc[:128]
                bucket = ossstr[:slash]
                obj    = ossstr[slash+1:]
                vault_name = parse_vault_name(dst)
                vault_id = self.fetch_vault_id(vault_name)
            else:
                jtype  = 'push-to-oss'
                ossstr = dst[len('oss://'):]
                slash = ossstr.find('/')
                if slash == -1: raise ValueError
                desc   = args.desc or 'copy to %s' % ossstr
                desc   = desc[:128]
                bucket = ossstr[:slash]
                obj    = ossstr[slash+1:]
                vault_name, archiveId = src[len(OAS_PREFIX):].split('/')
                vault_id = self.fetch_vault_id(vault_name)
        except Exception:
            sys.stderr.write('[Error]: Invalid source path or destination ' \
                    'path. \nOnly support OSS path like oss://bucketname/'  \
                    'objectname and OAS path like oas://vaultname or oas:'  \
                    '//vaultname/archiveId\n')
            return
        osshost = args.osshost
        if not osshost:
            try:
                config = ConfigParser.ConfigParser()
                cfgfile = args.config_file or DEFAULT_CONFIGFILE
                config.read(cfgfile)
                if config.has_option(CONFIGSECTION, 'osshost'):
                    osshost = config.get(CONFIGSECTION, 'osshost')
                if not osshost:
                    config = ConfigParser.ConfigParser()
                    config.read(os.path.expanduser('~/.osscredentials'))
                    osshost = config.get('OSSCredentials', 'host')
                    if not osshost: raise
            except:
                sys.stderr.write('OSS host not specified, nor can be read ' \
                    'from OAS config file or ~/.osscredentials\n')
                return

        res = self.api.create_oss_transfer_job(vault_id,
                jtype, osshost, bucket, obj, archive_id=archiveId, desc=desc)
        check_response(res)
        job_id = res.getheader('x-oas-job-id')
        print 'oss transfer job created, job ID: %s' % (job_id)
        tip = '.'
        if jtype == 'pull-from-oss':
            tip = ' and retrieve corresponding Archive ID from job status'
        print 'Use\n\n    oascmd.py getjobdesc oas://%s %s\n\nto check job ' \
              'progress%s' % (vault_name, job_id, tip)
        print 'NOTICE: Jobs usually take about 4 HOURS to complete.'
        return job_id

    def cmd_getjobdesc(self, args):
        vault_name = parse_vault_name(args.vault)
        vault_id = self.fetch_vault_id(vault_name)
        job_id = args.jobid
        res = self.api.get_jobdesc(vault_id, job_id)
        check_response(res)
        rjson = json.loads(res.read(), 'UTF8')

        title = ('JobId', 'Action', 'StatusCode', 'StatusMessage',
                'ArchiveId', 'ArchiveSizeInBytes',
                'TreeEtag', 'ArchiveTreeEtag',
                'RetrievalByteRange', 'Completed', 'CompletionDate',
                'CreationDate', 'InventorySizeInBytes', 'JobDescription')
        rjson['CreationDate'] = convert_time_format(rjson['CreationDate'])
        rjson['CompletionDate'] = convert_time_format(rjson['CompletionDate'])
        self.kv_print(rjson, title)

    def cmd_fetchjoboutput(self, args):
        vault_name = parse_vault_name(args.vault)
        vault_id = self.fetch_vault_id(vault_name)
        job_id = args.jobid
        dst = args.localfile
        start = self.parse_size(args.start)
        size = self.parse_size(args.size)

        vaultid = self.fetch_vault_id(parse_vault_name(args.vault))
        res = self.api.get_jobdesc(vaultid, args.jobid)
        check_response(res)
        job = json.loads(res.read(), 'UTF8')
        status = job['StatusCode'].lower()
        jtype = 'inventory-retrieval' if job['Action'] == 'InventoryRetrieval' \
                else 'archive-retrieval'
        if status == 'inprogress':
            print '%s job still in progress. Repeat this ' \
                  'command later' % jtype
            sys.exit(0)
        elif status == 'failed':
            print '%s job failed.' % jtype
            sys.exit(0)
        brange = None
        if jtype == 'archive-retrieval':
            brange = [int(x) for x in job['RetrievalByteRange'].split('-')]
        else:
            brange = [0, int(job['InventorySizeInBytes']) - 1]

        output_range = None
        if (start != None and size == None):
            size = brange[1] - brange[0] - start + 1
        elif (start == None and size != None):
            start = 0
        if (start != None and size != None):
            output_range = 'bytes=%s-%s' % (start, start+size-1)

        if not args.force and os.path.exists(dst):
            ans = raw_input('Output file %s existed. Do you wish to ' \
                    'overwrite it? (y/n): ' % dst)
            if ans.strip().lower() != 'y':
                print 'Answer is no. Quit now.'
                sys.exit(0)

        res = self.api.fetch_job_output(vault_id, job_id, output_range)
        check_response(res)

        with open(dst, 'wb') as f:
            total_read = 0
            while True:
                data = res.read(1024 * 1024)
                if len(data) > 0:
                    f.write(data)
                    total_read += len(data)
                    totalsize = size or brange[1] - brange[0] + 1
                    percent = total_read * 100 // totalsize
                    nbar = percent // 2
                    sys.stdout.write('\r')
                    msgbar = '[%s] %s%%' % ('='*nbar+'>'+' '*(50-nbar), percent)
                    sys.stdout.write(msgbar)
                    sys.stdout.flush()
                else:
                    break
        sys.stdout.write('\n')
        print 'Download job output success'

    def cmd_listjob(self, args):
        vault_name = parse_vault_name(args.vault)
        vault_id = self.fetch_vault_id(vault_name)
        marker = args.marker
        limit = args.limit
        res = self.api.list_job(vault_id, marker, limit)
        check_response(res)
        rjson = json.loads(res.read(), 'UTF8')
        marker = rjson['Marker']
        job_list = rjson['JobList']
        print 'Marker: %s' % marker
        print 'Job count: %s' % len(job_list)
        if not job_list:
            return
        print
        title = ('JobId', 'Action', 'StatusCode', 'StatusMessage',
                'ArchiveId', 'ArchiveSizeInBytes',
                'TreeEtag', 'ArchiveTreeEtag',
                'RetrievalByteRange', 'Completed', 'CompletionDate',
                'CreationDate', 'InventorySizeInBytes', 'JobDescription')
        for job in job_list:
            print '================ JobId: %s ================' % job['JobId']
            job['CreationDate'] = convert_time_format(job['CreationDate'])
            job['CompletionDate'] = convert_time_format(job['CompletionDate'])
            self.kv_print(job, title)
            print

