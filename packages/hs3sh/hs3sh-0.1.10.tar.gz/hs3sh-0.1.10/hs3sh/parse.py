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

import shlex

# Constants
PERMISSIONS = ['FULL_CONTROL', 'WRITE', 'WRITE_ACP', 'READ', 'READ_ACP']
CANNED = ['private', 'public-read', 'public-read-write', 'authenticated-read']
BUCKET = 'b'
GRANT = 'g'
OBJECT = 'o'
SET = 's'

class AclReturn(object):
    'class holding the result of parse_acl'
    def __init__(self):
        self.isbucket = None    # True, if bucket, False if Object
        self.name = None        # the bucket's or object's name
        self.flags = []         # given flags
        self.pairs = []         # list of tuples of acl pairs
        self.canned = None      # a canned ACL

    def __str__(self):
        ret = []
        ret.append(' type: {}'
                   .format(None if self.isbucket == None else 'bucket' if self.isbucket else 'object'))
        ret.append(' name: {}'.format(self.name))
        ret.append('flags: {}'.format(self.flags))
        ret.append('grant: {}'.format(self.pairs))

        return '\n'.join(ret)


def parse_acl(args, debug=False):
    '''
    Parse the parameters for the acl command

    :param args:    a string holding the entire parameters
    :param debug:   turn of shlex debug output of True
    :return:        an AclReturn object
    '''
    s = shlex.shlex(args, posix=True)
    s.debug = 1 if debug else 0

    flags  = 'bgos'   # b=bucket, g = grant, o = object, s=set

    isfirst = newpair = True
    isflags = False
    p1 = p2 = None
    ret = AclReturn()

    while True:
        t = s.get_token()

        # end if there's no more token
        if not t:
            break

        # handle flags
        if isflags:
            for f in t:
                if f in flags:
                    ret.flags.append(f)
                    if f in [BUCKET, OBJECT]:
                        if ret.isbucket != None:
                            raise ValueError('-{} and -{} are exclusive'
                                             .format(BUCKET,OBJECT))
                        else:
                            ret.isbucket = True if f == BUCKET else False
                    elif f == SET:
                        x = s.get_token()
                        if x in CANNED:
                            ret.canned = x
                        else:
                            raise ValueError('argument following -{} ({}) must be one of {}'
                                             .format(SET, x, CANNED))

                else:
                    raise ValueError('flag "{}" not acceptable'.format(f))
            isflags = False
            continue
        if t == '-':
            isflags = True
            continue

        # handle the first token (should be bucket or /object)
        if isfirst:
            # ret.isbucket = True if not t.startswith('/') else False
            ret.name = t
            isfirst = False
            continue

        # handle value pairs
        # if we find a comma or a semicolon, a new pair starts
        if t in [',', ';']:
            newpair = True
            p1 = p2 = None
            continue

        if newpair:
            if not p1:
                p1 = t
            elif not p2:
                if not t.upper() in PERMISSIONS:
                    raise ValueError("'{}':'{}'.upper() not in {}"
                                     .format(p1, t, PERMISSIONS))
                p2 = t.upper()
            else:
                raise ValueError('acl settings have to be grantee / permission'
                                 ' pairs ({} {} - bad: {})'.format(p1, p2, t))
            if p1 and p2:
                ret.pairs.append((p1,p2))
            continue

        # as we should never end up here, RAISE!
        raise Exception('we should never have gotten to this point...')

    # Not having 'o' or 'b' in flags is an error...
    if ret.isbucket == None:
        raise ValueError('use -{}|-{} to identify bucket or object'
                         .format(BUCKET,OBJECT))

    elif not GRANT in ret.flags and ret.pairs:
        raise ValueError('use -{} if you want to set ACLs'.format(GRANT))

    elif GRANT in ret.flags and not ret.pairs:
        raise ValueError('-{} requires user/permission pair(s)'.format(GRANT))


    return ret
