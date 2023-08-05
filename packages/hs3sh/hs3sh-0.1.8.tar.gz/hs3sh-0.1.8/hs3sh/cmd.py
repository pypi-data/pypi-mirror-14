# The MIT License (MIT)
#
# Copyright (c) 2016 Thorsten Simons (sw@snomis.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



import sys
import os
import time
from textwrap import wrap
import boto3
import botocore
from botocore.utils import fix_s3_host
from botocore.vendored.requests.packages.urllib3 import disable_warnings
import cmd

from .conf import readconf
from .init import AWS_REGIONS

from pprint import pprint

class HS3shell(cmd.Cmd):
    intro = 'HS3 Shell\n' \
            '========='
    prompt = '--> '

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint = None     # the aws region or the target HCP Tenant
        self.mode = None         # 'aws' or 'compatible'
        self.ssl = True          # if https shall be used
        self.s3 = None           # the connection
        self.bucket = None       # the bucket object to work with
        self.bucketname = None   # its name
        self.encrypted = False   # if objects shall be server side encrypted
        self.profiles = None     # a dict of dicts per profile in .hs3sh.conf
        self.profile = None      # the profile in use

    def preloop(self):
        disable_warnings()
        # read the configuration file(s)
        try:
            self.profiles = readconf()
        except Exception as e:
            sys.exit('error: no config file loaded...\nhint: {}'.format(e))

        # if we have a ~/.hs3shrc file, read it and execute the commands...
        try:
            startupfile = os.path.join(os.path.expanduser("~"), ".hs3shrc")
            with open(startupfile, 'r') as inhdl:
                for cmnd in inhdl.readlines():
                    self.cmdqueue.append(cmnd.strip())
        except Exception:
            pass

    def emptyline(self):
        'Disable repetition of last command by pressing Enter'
        pass

    def do_lsp(self, arg):
        'lsp\n'\
        '    show the loaded profiles'
        print('{:1} {:20} {:>8}  {}'.format('C', 'profile', 'tag', 'value'))
        print('{:1} {:20} {:8}- {}'.format('-', '-'*20, '-'*8, '-'*45))
        for p in sorted(self.profiles.keys()):
            for tag in ['comment', 'endpoint', 'region', 'https']:
                if self.profiles[p][tag]:
                    print('{:1} {:20} {:>8}: {}'
                          .format('|' if p == self.profile else '',
                                  p if tag == 'comment' else '',
                                  tag,
                                  self.profiles[p][tag]))
        print()



    def do_connect(self, arg):
        'connect <profile_name>\n'\
        '    Connect to an S3 endpoint using profile <profile_name>\n'\
        '    from from ~/.hs3sh.conf or ./.hs3sh.conf'
        try:
            para = paramcheck(arg, flags='')
        except Exception as e:
            print('error: parameters invalid...\nhint: {}'.format(e))
            return
        else:
            if len(para.args) != 1:
                print('error: a profile_name as explicit parameter is required')
                return
            try:
                self.mode = 'aws' if self.profiles[para.args[0]]['region'] else 'compatible'
            except KeyError:
                print('error: profile {} unavailable...'.format(para.args[0]))
                return
            else:
                self.profile = para.args[0]

            try:
                if self.mode == 'aws':
                    d = boto3.session.Session(aws_access_key_id=self.profiles[self.profile]['aws_access_key_id'],
                                              aws_secret_access_key=self.profiles[self.profile]['aws_secret_access_key'],
                                              region_name=self.profiles[self.profile]['region'])
                    self.s3 = d.resource('s3',
                                         config=boto3.session.Config(signature_version='s3v4'))
                else:
                    endpoint = ('https://' if self.profiles[self.profile]['https'] else 'http://') + \
                               self.profiles[self.profile]['endpoint']
                    d = boto3.session.Session(aws_access_key_id=self.profiles[self.profile]['aws_access_key_id'],
                                              aws_secret_access_key=self.profiles[self.profile]['aws_secret_access_key'])
                    self.s3 = d.resource('s3', endpoint_url=endpoint,
                                         verify=False)
                    self.s3.meta.client.meta.events.unregister('before-sign.s3',
                                                               fix_s3_host)
            except Exception as e:
                print('error: connect failed\nhint: {}'.format(e))
            else:
                self.bucket = self.bucketname = None

    def do_mkbucket(self, bucket):
        'mkbucket bucket\n' \
        '    Create a new bucket at the connected *endpoint*.'
        if not self.profile:
            print('error: you need to connect, first...')
            return

        if not bucket:
            print('error: exactly one parameter is required...')
        else:
            try:
                bkt = self.s3.Bucket(bucket)
                bkt.create(CreateBucketConfiguration={'LocationConstraint': self.profiles[self.profile]['region'] or ''})
            except Exception as e:
                _print('error: create bucket failed...\nhint: {}'.format(e))
        print()

    def do_rmbucket(self, bucket):
        'rmbucket bucket\n' \
        '    Delete the named bucket, which needs to be empty.\n'\
        '    Empty in case of HS3 means, that all objects, all folders and\n'\
        '    all versions must have been deleted, and HCP Garbage Collection\n'\
        '    has cleaned up everything.'
        if not self.profile:
            print('error: you need to connect, first...')
            return

        if not bucket:
            print('error: exactly one parameter is required...')
        else:
            try:
                bkt = self.s3.Bucket(bucket)
                bkt.delete()
            except Exception as e:
                _print('error: delete bucket failed...\nhint: {}'.format(e))
        print()

    def do_bucketacl(self, arg):
        'bucketacl -a|-l|-r bucket\n'\
        '    -a add an ACL to bucket\n'\
        '    -l list the bucket\'s ACLs\n'\
        '    -r remove an ACL from bucket'
        if not self.profile:
            print('error: you need to connect, first...')
            return

        try:
            para = paramcheck(arg, flags='alr')
        except Exception as e:
            print('error: parameters invalid...\nhint: {}'.format(e))
            return
        else:
            if len(para.args) != 1 and not self.bucket:
                print('error: you need to specify a bucket...')
                return
            else:
                bucket = para.args[0] if len(para.args) else self.bucketname

        if 'l' in para.flags:
            try:
                print('ACLs for bucket {}'.format(bucket))
                acl = self.s3.Bucket(bucket).Acl()
                acl.load()
                out = {'Owner': acl.owner, 'Grantees': acl.grants}
                pprint(out)
            except Exception as e:
                _print('error: unable to access bucket ACLs...\nhint: {}'
                       .format(e))
                return

        else:
            print('sorry: not yet implemented...')

    def do_objectacl(self, arg):
        'objectacl -a|-l|-r object\n'\
        '    This command works on the attached bucket!\n'\
        '    -a add an ACL to object\n'\
        '    -l list the object\'s ACLs\n'\
        '    -r remove an ACL from object'
        if not self.profile:
            print('error: you need to connect, first...')
            return
        if not self.bucket:
            print('error: you need to attach a bucket, first...')
            return

        try:
            para = paramcheck(arg, flags='alr')
        except Exception as e:
            print('error: parameters invalid...\nhint: {}'.format(e))
            return
        else:
            if len(para.args) != 1:
                print('error: you need to specify an object...')
                return
            else:
                object = para.args[0]

        if 'l' in para.flags:
            print('ACLs for object {}'.format(object))
            try:
                acl = self.s3.Object(self.bucketname, object).Acl()
                acl.load()
                out = {'Owner': acl.owner, 'ACLs': acl.grants}
                pprint(out)
            except Exception as e:
                _print('error: unable to access object ACLs...\nhint: {}'
                       .format(e))
        else:
            print('sorry: not yet implemented...')

    def do_attach(self, bucket):
        'attach <bucket_name>\n' \
        '    Attaches the bucket to be used by further commands. Think of\n'\
        '    change directory...'
        if not self.profile:
            print('error: you need to connect, first...')
            return

        try:
            self.bucket = self.s3.Bucket(bucket)
            # switch this of, as it causes an error (404) when attaching a
            # bucket which is not owned by this user
            # self.bucket.load()
        except Exception as e:
            _print('error: attach of bucket "{}" failed\nhint: {}'
                  .format(bucket, e))
        else:
            self.bucketname = bucket

    def do_lsb(self, arg):
        'lsb [-a]\n' \
        '    List the buckets available through the connected endpoint.\n'\
        '    -a shows ACLs as well.'
        if not self.profile:
            print('error: you need to connect, first...')
            return

        try:
            para = paramcheck(arg, flags='a')
        except Exception as e:
            _print('error: parameters invalid...\nhint: {}'.format(e))
            return

        _acls = True if 'a' in para.flags else False

        # test to get access to the region in AWS
        if self.mode == 'aws':
            try:
                cl = botocore.session.Session().create_client('s3',
                                                              aws_access_key_id=
                                                              self.profiles[
                                                                  self.profile][
                                                                  'aws_access_key_id'],
                                                              aws_secret_access_key=
                                                              self.profiles[
                                                                  self.profile][
                                                                  'aws_secret_access_key'],
                                                              region_name=
                                                              self.profiles[
                                                                  self.profile][
                                                                  'region'])
            except Exception as e:
                _print('error: lsb failed...\nhint: {}'.format(e))
                return

        print('{:>17} {:30} {:14} {:40}'
              .format('created',
                      'owner|ID' + (' '*15+'grantee' if _acls else ''),
                      'region',
                      'bucket name' + (' '*25+'ACLs' if _acls else ''),
                      ))
        print('-'*17, '-'*30, '-'*14, '-'*40)

        try:
            for b in self.s3.buckets.all():
                location = 'compatible' if self.mode != 'aws' else \
                    cl.get_bucket_location(Bucket=b.name)['LocationConstraint']
                try:
                    acl = b.Acl()
                    acl.load()
                    try:
                        owner = acl.owner['DisplayName']
                    except Exception:
                        owner = acl.owner['ID']
                    print('{:17} {:30} {:14} {:40}'
                          .format(b.creation_date.strftime('%y/%m/%d-%H:%M:%S'),
                                  _(owner, 30),
                                  location, b.name))
                except botocore.exceptions.ClientError as e:
                    acl = None
                    if self.mode == 'aws':
                        print('{:17} {:30} {:14} {:40}'
                              .format(b.creation_date.strftime('%y/%m/%d-%H:%M:%S'),
                                      '**not avail. through region**', location,
                                      b.name))
                    else:
                        print('{:17} {:30} {:14} {:40}'
                              .format(b.creation_date.strftime('%y/%m/%d-%H:%M:%S'),
                                      '**GetBucketAcl not impl.**', location,
                                      b.name))


                if _acls and acl:
                    for g in acl.grants:
                        if g['Grantee']['Type'] == 'CanonicalUser':
                            print(' ' * 17, '{:>30} {:14} {:>40}'
                                  .format(
                                g['Grantee']['DisplayName'] if 'DisplayName' in
                                                               g['Grantee'].keys() else
                                                               _(g['Grantee']['ID'],30),
                                '', g['Permission']))
                        elif g['Grantee']['Type'] == 'Group':
                            print(' '*17, '{:>30} {:14} {:>40}'
                                  .format(g['Grantee']['URI'].split('/')[-1],
                                          '', g['Permission']))
                        else:
                            print(' '*17, 'unknown')

        except Exception as e:
            _print('error: listing buckets failed...\nhint: {}'.format(e))
        print()

    def do_ls(self, arg):
        'ls [-mv] [prefix]\n' \
        '    List the objects within the active bucket.\n'\
        '    -m prints metadata pairs per object, if available,\n'\
        '    -v prints each object\'s versions, if there are some.\n'\
        '    If prefix is given, list objects starting with the prefifx, only.'
        if not self.profile:
            print('error: you need to connect, first...')
            return

        if not self.bucket:
            print('error: you need to attach to a bucket, first...')
            return

        try:
            para = paramcheck(arg, flags='mv')
        except Exception as e:
            _print('error: parameters invalid...\nhint: {}'.format(e))
            return

        if len(para.args) > 1:
            print('error: maximal one parameter is required')
            return
        else:
            prefix = '' if not len(para.args) else para.args[0]

        _meta = True if 'm' in para.flags else False
        _versions = True if 'v' in para.flags else False

        try:
            if _versions:
                print('{:>17} {:>15} {:32} {} {}'
                      .format('last modified', 'size', 'version_id', 'A',
                              'object name/metadata' if _meta else 'object name'))
                print('-'*17, '-'*15, '-'*32, '-', '-'*28)
            else:
                print('{:>17} {:>15} {:32} {}'
                      .format('last modified', 'size', 'version_id',
                              'object name/metadata' if _meta else 'object name'))
                print('-'*17, '-'*15, '-'*32, '-'*28)

            query = self.bucket.objects.filter if not _versions else self.bucket.object_versions.filter

            for obj in query(Prefix=prefix):
                if not _versions:
                    obj = obj.Object()
                    obj.load()
                    print('{:>17} {:>15,} {:32} {}'
                          .format(obj.last_modified.strftime('%y/%m/%d-%H:%M:%S'),
                                  obj.size or 0 if _versions else obj.content_length,
                                  _(obj.version_id,32) or 'null',
                                  obj.key))
                else:
                    print('{:>17} {:>15,} {:32} {} {}'
                          .format(obj.last_modified.strftime('%y/%m/%d-%H:%M:%S'),
                                  obj.size or 0 if _versions else obj.content_length,
                                  _(obj.version_id,32),
                                  ' ' if not _versions else 'X' if obj.is_latest else ' ',
                                  obj.key))
                try:
                    if _meta:
                        if _versions:
                            resp = obj.head()
                            if resp['Metadata']:
                                print('{:>68} {}'.format('', resp['Metadata']))
                        else:
                            if obj.metadata:
                                print('{:>66} {}'.format('', obj.metadata))
                except Exception as f:
                    print(f)
                    pass

        except Exception as e:
            _print('error: ls failed\nhint: {}'.format(e))
        print()

    def do_copy(self, arg):
        'copy [-v version_id] source target ["metakey:metavalue"]*\n' \
        '    Request HCP to perform a server-side copy of (a defined\n'\
        '    version_id of) source to target object, replacing eventually\n'\
        '    existing source metadata pairs with the named metadata pairs,\n'\
        '    if given; else copy the existing metadata pairs, along with the\n'\
        '    object.\n\n'\
        '    You can use the copy command to copy the source object to\n'\
        '    itself to create a new version of the source object with\n'\
        '    changed metadata pairs.'
        if not self.profile:
            print('error: you need to connect, first...')
            return

        if not self.bucket:
            print('error: you need to attach to a bucket, first...')
            return

        try:
            para = paramcheck(arg, flags='v', meta=True)
        except Exception as e:
            _print('error: parameters invalid...\nhint: {}'.format(e))
            return
        else:
            _version = True if 'v' in para.flags else False
            if len(para.args) < (3 if _version else 2):
                print('error: at least {} parameter are required'
                      .format('three' if _version else 'two'))
                return
            else:
                if 'v' in para.flags:
                    _ver = para.args[0]
                    _src = para.args[1]
                    _tgt = para.args[2]
                else:
                    _ver = None
                    _src = para.args[0]
                    _tgt = para.args[1]

        try:
            obj = self.s3.Object(self.bucketname, _tgt)
            if para.metadict:
                response = obj.copy_from(CopySource={'Bucket': self.bucketname,
                                                     'Key': _src,
                                                     'VersionId': _ver},
                                         Metadata=para.metadict,
                                         MetadataDirective='REPLACE')
            else:
                response = obj.copy_from(CopySource={'Bucket': self.bucketname,
                                                     'Key': _src,
                                                     'VersionId': _ver},
                                         MetadataDirective='COPY')
            if 'CopySourceVersionId' in response:
                print('CopySourceVersionId: {}'
                      .format(response['CopySourceVersionId']))
            if 'VersionId' in response:
                print('          VersionId: {}'.format(response['VersionId']))
        except Exception as f:
            _print('error: copy_from failed...\nhint: {}'.format(f))

        print()

    def do_put(self, arg):
        'put [-m] localfile object ["metakey:metavalue"]*\n' \
        '    Put (store) localfile as object into the attached bucket,\n'\
        '    adding metadata pairs, if specified.\n'\
        '    -m will try do do a multi-part put.'
        if not self.profile:
            print('error: you need to connect, first...')
            return

        if not self.bucket:
            print('error: you need to attach to a bucket, first...')
            return

        try:
            para = paramcheck(arg, flags='m', meta=True)
        except Exception as e:
            _print('error: parameters invalid...\nhint: {}'.format(e))
            return
        else:
            if len(para.args) != 2:
                print('error: at least 2 parameters are required...')
                return

            if 'm' in para.flags:
                print('sorry: multi-part put not yet implemented...')
                return

            _src = para.args[0]
            _tgt = para.args[1]
            _metadict = para.metadict

            try:
                with open(_src, 'br') as inhdl:
                    obj = self.s3.Object(self.bucketname, _tgt)
                    response = obj.put(Body=inhdl.read(), Metadata=_metadict)
                    if 'VersionId' in response:
                        print('VersionId = {}'.format(response['VersionId']))
            except Exception as f:
                _print('error: put failed...\nhint: {}'.format(f))

        print()

    def do_get(self, arg):
        'get [-v version_id] object [localfile]\n' \
        '    Get (read) the latest (or a named version_id) of object and\n'\
        '    print it. If localfile is specified, write the object to it.'
        if not self.profile:
            print('error: you need to connect, first...')
            return

        if not self.bucket:
            print('error: you need to attach to a bucket, first...')
            return

        try:
            para = paramcheck(arg, flags='v', meta=False)
        except Exception as e:
            _print('error: parameters invalid...\nhint: {}'.format(e))
            return
        else:
            _version = True if 'v' in para.flags else False
            if len(para.args) < (2 if _version else 1):
                print('error: at least {} parameter are required'
                      .format('two' if _version else 'one'))
                return
            else:
                if 'v' in para.flags:
                    _ver = para.args[0]
                    _src = para.args[1]
                    _tgt = para.args[2] if len(para.args) > 2 else None
                else:
                    _ver = None
                    _src = para.args[0]
                    _tgt = para.args[1] if len(para.args) > 1 else None

        try:
            obj = self.s3.Object(self.bucketname, _src) if not _ver \
                else self.s3.ObjectVersion(self.bucketname, _src, _ver)
            response = obj.get()
            if _tgt:
                with open(_tgt, 'wb') as outhdl:
                    outhdl.write(response['Body'].read())
            else:
                print('-'*79)
                print(response['Body'].read().decode())
                print('-'*79)
        except Exception as e:
            _print('error: get failed...\nhint: {}'.format(e))
        print()

    def do_rm(self, arg):
        'rm object [version_id]\n' \
        '    Delete object (or it\'s version_id) from the attached bucket.'
        if not self.profile:
            print('error: you need to connect, first...')
            return

        if not arg:
            print('error: at least one parameter is required...')
            return

        if len(arg.split()) == 1:
            object = arg
            version = None
            try:
                obj = self.s3.Object(self.bucketname, object)
                response = obj.delete()
                print('deleted "{}", version_id {}'
                      .format(object,
                              response['VersionId'] if 'VersionId' in response else 'null'))
            except Exception as e:
                _print('error: delete failed...\nhint: {}'.format(e))
        else:
            try:
                object, version = arg.split()
            except Exception as e:
                print('error: one or two parameters are required...\nhint: {}'
                      .format(e))
            else:
                try:
                    obj = self.s3.Object(self.bucketname, object)
                    response = obj.delete(VersionId=version)
                    print('deleted "{}", version_id {}'
                          .format(object,
                                  response['VersionId'] if 'VersionId' in response else 'null'))
                except Exception as e:
                    _print('error: delete failed...\nhint: {}'.format(e))
        print()

    def do_status(self, arg):
        'status\n' \
        '    Show the session status (the connected endpoint and the\n'\
        '    attached bucket)'
        print('{:>20} {}'.format('config item', ' value'))
        print('-'*20, '-'*58)

        print('{:>20} {}'.format('mode', self.mode or 'not set'))
        print('{:>20} {}'.format('profile', self.profile or 'not set'))
        if self.profile:
            print('{:>20} {}'.format('profile comment',
                                     '  '+self.profiles[self.profile]['comment']))
            print('{:>20} {}'.format('session mode',
                                     '  '+'secure (https)' if  self.profiles[self.profile]['https'] else 'insecure (http)'))
            print('{:>20} {}'.format('endpoint',
                                     '  '+(self.profiles[self.profile]['endpoint'] or 'Amazon S3')))
            print('{:>20} {}'.format('region',
                                     '  '+(self.profiles[self.profile]['region'] or 'n/a')))
        print('{:>20} {}'.format('attached bucket', self.bucketname or 'not set'))
        print()


    def do_time(self, arg):
        'time <command args>\n'\
        '    measure the time <command> takes to complete'
        p = arg.split(maxsplit=1)
        cmd, params = p if len(p) > 1 else (arg, '')

        st = time.time()
        result = eval('self.do_{}("{}")'.format(cmd, params))
        print('[time: {}]'.format(calcTime(time.time() - st)))
        return result

    # def do_test(self, arg):
    #     'test [-flags] [args]* [metapairs]*\n'\
    #     '    test the argument processor'
    #     try:
    #         para = paramcheck(arg, flags='abc', meta=True)
    #     except Exception as e:
    #         _print('error: parameters invalid...\nhint: {}'.format(e))
    #         return
    #     print('flags: {}'.format(para.flags))
    #     print(' args: {}'.format(para.args))
    #     print(' meta: {}'.format(para.metadict))

    def do_quit(self, arg):
        'Exit hs3sh gracefully.'
        print('Ending gracefully...')
        return True


class ParamReturn(object):
    'class holding the result of a paramcheck'
    def __init__(self):
        self.flags = []      # given flags
        self.args  = []      # remainings parameter
        self.metadict = {}   # metadata pairs

def paramcheck(arg, flags='', meta=False):
    '''
    Check the parameters given to a command:
        [-flags | -f -l -a -g -s] arg [arg ...] [meta:data ...]
    :param arg:     the parameter string given to the cmd
    :param flags:   allowed flags
    :param meta:    if we shall look for metadata pairs
    :return:        a dict
    '''
    ret = ParamReturn()
    if not arg:     # dummy on empty input
        return ret

    # crawl through the parameters
    inflags = searchargs = True
    for pa in arg.split():
        if inflags:     # make sure the flags given are allowed
            if pa.startswith('-'):
                for i in pa[1:]:
                    if i in flags:
                        ret.flags.append(i)
                    else:
                        raise ValueError('invalid flag: -{}'.format(i))
            else:
                inflags = False     # first param w/o '-' ends flag processing

        if not inflags: # now its about the params and metapairs
            if searchargs:
                if len(pa.split(':')) == 2:
                    searchargs = False
                else:
                    ret.args.append(pa)

            if not searchargs and meta:
                pas = pa.split(':')
                if len(pas) != 2:
                    raise ValueError('invalid metapair: {}'.format(pa))
                else:
                    ret.metadict[pas[0]] = pas[1]

    return ret

def calcTime(t):
    '''
    Calculate a string 'H:M:S.ms' out of a given no. of seconds.
    '''
    msec    = int("{0:.2f}".format(t%1)[2:])
    minute  = int(t//60)
    sec     = int(t%60)
    hour    = int(minute//60)
    minute  = int(minute%60)
    return("{0:02}:{1:02}:{2:02}.{3}".format(hour, minute, sec, msec))

def _print(string):
    '''
    Print a string, first line as it is, following lines wrapped to 78 chars.

    :param string:  the string to print
    '''

    strings = string.split('\n')
    print(strings[0])
    lines = wrap('\n'.join(strings[1:]),
                 initial_indent='    ', subsequent_indent='    ')
    for l in lines:
        print(l)

def _(string, width):
    '''
    Return the string cut to num characters.

    :param string:  the string to work on
    :param num:     the number of characters wanted
    :return:        the cut string
    '''
    string = string or ''
    return string if len(string) <= width else string[:width-3]+'...'
