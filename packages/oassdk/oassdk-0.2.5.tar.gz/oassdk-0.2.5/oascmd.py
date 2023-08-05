#!/usr/bin/env python2.7
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
import ConfigParser
import os
import sys
import time

from collections import namedtuple
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from oas.oas_ops import OASCMD
from oas.oas_ops import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_CONFIGFILE
from oas.oas_ops import CONFIGSECTION

AuthInfo = namedtuple(
    'AuthInfo', ['host', 'port', 'accessId', 'accessKey'], verbose=False)

HELP = \
    '''Usage: oascmd <action> [<args>]:

General Use:
    ls
    cv                   oas://vault
    rm                   oas://vault [archive_id]
    upload               oas://vault filename [-p PART_SIZE] [--desc desc]
    createjob            oas://vault [archive_id] [--start start] [--size size] [--desc desc]
    fetch                oas://vault jobid localfile [--start start] [--size size] [-f]

Vault Operations:
    createvault          oas://vault
    deletevault          oas://vault
    listvault            [--marker marker] [--limit limit]
    getvaultdesc         oas://vault

Archive Operations:
    postarchive          oas://vault local_file [etag] [tree_etag] [--desc desc]
    deletearchive        oas://vault archive_id

Etag Operations:
    fileetag             local_file
    partetag             local_file start end

Multipart Archive Operations:
    createmupload        oas://vault part_size [--desc desc]
    listmupload          oas://vault [--marker marker] [--limit limit]
    completemupload      oas://vault upload_id file_size [tree_etag]
    deletemupload        oas://vault upoad_id
    postmpart            oas://vault upload_id local_file start end [etag] [tree_etag]
    listmpart            oas://vault upload_id [--maker marker] [--limit limit]

Job Operations:
    createjob            oas://vault [archive_id] [--desc desc] [--start start] [--size size]
    createclodbackjob    oas://vault [--desc desc] host bucket object
    createdefrozenjob    oas://vault [--desc desc] host bucket object
    getjobdesc           oas://vault job_id
    fetchjoboutput       oas://vault job_id local_file [--start start] [--size size]
    listjob              oas://vault [--marker marker] [--limit limit]

Other Operations:
    config               [--host host] [-p,--port port] -i,--id=accessid -k,--key=accesskey
    help

'''

def fetch_credentials(args):
    try:
        host, port = args.host, args.port
        accessid, accesskey = args.id, args.key
        if not (host and port and accessid and accesskey):
            config = ConfigParser.ConfigParser()
            cfgfile = args.config_file or DEFAULT_CONFIGFILE
            config.read(cfgfile)
            # user defined inputs have higher priority
            host = host or config.get(CONFIGSECTION, 'host')
            port = port or int(config.get(CONFIGSECTION, 'port'))
            accessid = accessid or config.get(CONFIGSECTION, 'accessid')
            accesskey = accesskey or config.get(CONFIGSECTION, 'accesskey')
        return AuthInfo(host, port, accessid, accesskey)
    except:
        sys.stderr.write("Cannot get accessid/accesskey. " \
                         "Setup use: oascmd.py config\n")
        sys.exit(1)

def cmd_configure(args):
    config = ConfigParser.RawConfigParser()
    config.add_section(CONFIGSECTION)
    config.set(CONFIGSECTION, 'host', args.host)
    config.set(CONFIGSECTION, 'port', args.port)
    config.set(CONFIGSECTION, 'accessid', args.id)
    config.set(CONFIGSECTION, 'accesskey', args.key)
    # set config_file
    cfgfile = args.config_file or DEFAULT_CONFIGFILE
    if os.path.isfile(cfgfile):
        ans = raw_input('File existed. Do you wish to overwrite it?(y/n)')
        if ans.lower() != 'y':
            print 'Answer is No. Quit now'
            return
    with open(cfgfile, 'w+') as f:
        config.write(f)
    print 'Your configuration is saved to %s.' % cfgfile

def cmd_help(args):
    print HELP

def add_config(parser):
    parser.add_argument('--host', type=str, help='service host')
    parser.add_argument('--port', type=int, help='service port',
                        default=DEFAULT_PORT)
    parser.add_argument('-i', '--id', type=str, help='access ID')
    parser.add_argument('-k', '--key', type=str, help='access key')
    parser.add_argument('--config-file', type=str, help='configuration file')

if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    subcmd = parser.add_subparsers(dest='cmd', title='Supported actions', \
            metavar='cmd', description=\
            """
            Commands {ls, cv, rm, upload, createjob, cp, fetch} provide easier
            ways to use OAS by combining commands below them. Generally they will
            suffice your daily use. For advanced operations, use commands like
            {createvault...}
            """)

    cmd = 'config'
    pcfg = subcmd.add_parser(cmd, help='config oascmd')
    pcfg.add_argument('--host', type=str, help='service host', required=True)
    pcfg.add_argument('-p', '--port', type=int, help='service port',
                      default=DEFAULT_PORT)
    pcfg.add_argument('-i', '--id', type=str, help='access ID', required=True)
    pcfg.add_argument('-k', '--key', type=str, help='access key', required=True)
    pcfg.add_argument('--config-file', type=str, help=\
            'file to save configuration')

    cmd = 'help'
    phelp = subcmd.add_parser(cmd, help='show a detailed help message and exit')

    cmd = 'ls'
    pls = subcmd.add_parser(cmd, help='list all vaults')
    pls.add_argument('--marker', type=str, help='to retrieve following list')
    pls.add_argument('--limit', type=int, help='number of vaults to be listed')
    add_config(pls)

    # only Python 3 supports aliases
    cmd = 'cv'
    pcv = subcmd.add_parser(cmd, help='create a vault')
    pcv.add_argument('vault', type=str, help='format oas://vault-name')
    add_config(pcv)

    cmd = 'rm'
    prm = subcmd.add_parser(cmd, help='remove a vault or an archive')
    prm.add_argument('vault', type=str, help='format oas://vault-name')
    prm.add_argument('archiveId', nargs='?', type=str, help=
            'ID of archive to be deleted')
    add_config(prm)

    cmd = 'upload'
    pupload = subcmd.add_parser(cmd, help='upload a local file')
    pupload.add_argument('vault', type=str, help='vault to store the file')
    pupload.add_argument('filename', type=str, help='file to be uploaded')
    pupload.add_argument('uploadid', nargs='?', type=str, help=\
            'MultiPartUpload ID upload returned to resume last upload')
    pupload.add_argument('--desc', type=str, help='description of the file')
    pupload.add_argument('-p', '--part-size', type=str, help=
            'multipart upload part size')
    add_config(pupload)

    cmd = 'createjob'
    pcj = subcmd.add_parser(cmd, help=\
            'create an inventory/archive retrieval job')
    pcj.add_argument('vault', type=str, help='vault to create the job')
    pcj.add_argument('archiveId', nargs='?', help='ID of archive to be ' \
            'downloaded. If not provided, an inventory-retrieval job will be ' \
            'created')
    pcj.add_argument('--start', help=\
            'start position of archive to retrieve, default to be 0')
    pcj.add_argument('--size', help=\
            'size to retrieve, default to be (totalsize - start)')
    pcj.add_argument('--desc', type=str, help='description of the job')
    add_config(pcj)

    cmd = 'cp'
    pcp = subcmd.add_parser(cmd, help='copy between OSS and OAS')
    pcp.add_argument('--osshost', type=str, help=\
            'OSS host address. Read from OAS config file then ' \
            '~/.osscredentials if not provided')
    pcp.add_argument('source', type=str, help=\
            'source OSS object full path or OAS archive path')
    pcp.add_argument('destination', type=str, help=\
            'destination OSS object full path or full archive path')
    pcp.add_argument('--desc', type=str, help='description of the copy job')
    add_config(pcp)

    cmd = 'fetch'
    pfj = subcmd.add_parser(cmd, help='fetch job output')
    pfj.add_argument('vault', type=str, help='format oas://vault-name')
    pfj.add_argument('jobid', type=str, help='jobId createjob returned')
    pfj.add_argument('localfile', type=str, help='local file output written to')
    pfj.add_argument('-f', '--force', action='store_true', help=\
            'force overwrite if file exists')
    pfj.add_argument('--start', type=str, help=\
            'start position to download output retrieved, default to be 0')
    pfj.add_argument('--size', type=str, help=\
            'size to download, default to be (totalsize - start)')
    add_config(pfj)

    cmd = 'createvault'
    pcvault = subcmd.add_parser(cmd, help='create a vault')
    pcvault.add_argument('vault', type=str, help='format oas://vault-name')
    add_config(pcvault)

    cmd = 'deletevault'
    pdvault = subcmd.add_parser(cmd, help='delete a vault')
    pdvault.add_argument('vault', type=str, help='format oas://vault-name')
    add_config(pdvault)

    cmd = 'listvault'
    plsv = subcmd.add_parser(cmd, help='list all vaults')
    plsv.add_argument('--marker', type=str, help='to retrieve following list')
    plsv.add_argument('--limit', type=int, help='number of vaults to be listed')
    add_config(plsv)

    cmd = 'getvaultdesc'
    pgv = subcmd.add_parser(cmd, help='get detailed vault description')
    pgv.add_argument('vault', type=str, help='format oas://vault name')
    add_config(pgv)

    cmd = 'postarchive'
    ppost = subcmd.add_parser(cmd, help='upload a local file')
    ppost.add_argument('vault', type=str, help='vault to store the file')
    ppost.add_argument('filename', type=str, help='file to be uploaded')
    ppost.add_argument('etag', nargs='?', type=str, help='etag fileetag returned')
    ppost.add_argument('tree_etag', nargs='?', type=str, help=\
            'tree_etag fileetag returned')
    ppost.add_argument('--desc', type=str, help='description of the file')
    add_config(ppost)

    cmd = 'deletearchive'
    pdar = subcmd.add_parser(cmd, help='delete an archive')
    pdar.add_argument('vault', type=str, help='format oas://vault-name')
    pdar.add_argument('archiveId', type=str, help='ID of archive to be deleted')
    add_config(pdar)

    cmd = 'fileetag'
    pfetag = subcmd.add_parser(cmd, help='calculate tree etag of a file')
    pfetag.add_argument('filename', type=str, help='file to be calculated')
    add_config(pfetag)

    cmd = 'partetag'
    ppetag = subcmd.add_parser(cmd, help=\
            'calculate tree etag of a multipart upload part')
    ppetag.add_argument('filename', type=str, help='file to be read from')
    ppetag.add_argument('start', type=str, help='start position to read')
    ppetag.add_argument('end', type=str, help='end position to read')
    add_config(ppetag)

    cmd = 'createmupload'
    pcm = subcmd.add_parser(cmd, help='initiate a multipart upload')
    pcm.add_argument('vault', type=str, help='format oas://vault-name')
    pcm.add_argument('part_size', type=str, help='size of each multipart upload')
    pcm.add_argument('--desc', type=str, help='description of the upload')
    add_config(pcm)

    cmd = 'deletemupload'
    pdm = subcmd.add_parser(cmd, help='cancel a multipart upload')
    pdm.add_argument('vault', type=str, help='format oas://vault-name')
    pdm.add_argument('uploadid', type=str, help=
            'ID of multipart upload to be cancelled')
    add_config(pdm)

    cmd = 'listmupload'
    plm = subcmd.add_parser(cmd, help='list all multipart uploads in a vault')
    plm.add_argument('vault', type=str, help='format oas://vault-name')
    plm.add_argument('--marker', type=str, help='to retrieve following list')
    plm.add_argument('--limit', type=int, help='number to be listed')
    add_config(plm)

    cmd = 'postmpart'
    ppm = subcmd.add_parser(cmd, help='upload one part')
    ppm.add_argument('vault', type=str, help='vault to store the part')
    ppm.add_argument('uploadid', type=str, help='ID createmupload returned')
    ppm.add_argument('filename', type=str, help='file to read from')
    ppm.add_argument('start', type=str, help=
            'read start position, start must be divided by partsize')
    ppm.add_argument('end', type=str, help=
            'read end position, end+1 must be the size of file or '
            'partsize larger than start')
    ppm.add_argument('etag', nargs='?', help='etag partetag returned')
    ppm.add_argument('tree_etag', nargs='?', help='tree_etag partetag returned')
    add_config(ppm)

    cmd = 'listmpart'
    plp = subcmd.add_parser(cmd, help='list all parts uploaded in one upload')
    plp.add_argument('vault', type=str, help='format oas://vault-name')
    plp.add_argument('uploadid', type=str, help='ID of multipart upload')
    plp.add_argument('--marker', type=str, help='to retrieve following list')
    plp.add_argument('--limit', type=int, help='number to be listed')
    add_config(plp)

    cmd = 'completemupload'
    pcm = subcmd.add_parser(cmd, help='complete the multipart upload')
    pcm.add_argument('vault', type=str, help='vault where the upload initiated')
    pcm.add_argument('uploadid', type=str, help='ID createmupload returned')
    pcm.add_argument('size', type=str, help='size of the file')
    pcm.add_argument('tree_etag', type=str, help='tree_etag fileetag returned')
    add_config(pcm)

    cmd = 'getjobdesc'
    pgj = subcmd.add_parser(cmd, help='get job status')
    pgj.add_argument('vault', type=str, help='format oas://vault-name')
    pgj.add_argument('jobid', type=str, help='jobId createjob returned')
    add_config(pgj)

    cmd = 'fetchjoboutput'
    pfjob = subcmd.add_parser(cmd, help='fetch job output')
    pfjob.add_argument('vault', type=str, help='format oas://vault-name')
    pfjob.add_argument('jobid', type=str, help='jobId createjob returned')
    pfjob.add_argument('localfile', type=str, help='local file output written to')
    pfjob.add_argument('-f', '--force', action='store_true', help=\
            'force overwrite if file exists')
    pfjob.add_argument('--start', type=str, help=\
            'start position to download output retrieved, default to be 0')
    pfjob.add_argument('--size', type=str, help=\
            'size to download, default to be (totalsize - start)')
    add_config(pfjob)

    cmd = 'listjob'
    plj = subcmd.add_parser(cmd, help='list all jobs except expired')
    plj.add_argument('vault', type=str, help='format oas://vault-name')
    plj.add_argument('--marker', type=str, help=\
            'listjob returned to retrieve following list')
    plj.add_argument('--limit', type=int, help='number to be listed')
    add_config(plj)

    args = parser.parse_args()

    if args.cmd == 'help':
        cmd_help(args)
        sys.exit(0)
    elif args.cmd == 'config':
        cmd_configure(args)
        sys.exit(0)

    # fetch auth_info
    auth_info = fetch_credentials(args)

    # error command
    method = OASCMD.__dict__.get('cmd_%s' % args.cmd)
    if method == None:
        sys.stderr.write('Unsupported command: %s\nUse help for more ' \
                         'information\n' % args.cmd)
        sys.exit(1)

    # execute command
    begin = time.time()
    oas_cmd = OASCMD(auth_info)
    method(oas_cmd, args)
    end = time.time()
    sys.stderr.write('%.3f(s) elapsed\n' % (end - begin))

