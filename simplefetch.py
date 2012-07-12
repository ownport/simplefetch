#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#   simplefetch, Simple HTTP client library
#


__version__ = '0.2.0-c_concept'
__author__ = 'Andrey Usov <http://devel.ownport.net>'
__url__ = 'https://github.com/ownport/simplefetch'
__license__ = '''
Copyright (c) 2012, Andrey Usov <http://devel.ownport.net>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
#   TODO
#   Connection.request
#   Connection.response

import os
import sys
import socket
import base64

if sys.version_info >= (3, 0):
    py3k = True
    unicode = str
else:
    py3k = False

if py3k:
    import http.cookies as Cookie
    import urllib.parse as urlparse
    from http.client import HTTP_PORT, HTTPS_PORT
    from http.client import HTTPConnection, HTTPSConnection, HTTPException
    from urllib.parse import urlencode, quote as urlquote, quote_plus as urlquote_plus
    basestring = (str, bytes)
    def b(s):
        return s.encode('latin-1')
    def u(s):
        return s
else:
    import Cookie
    import urlparse
    from httplib import HTTP_PORT, HTTPS_PORT
    from httplib import HTTPConnection, HTTPSConnection, HTTPException
    from urllib import urlencode, quote as urlquote, quote_plus as urlquote_plus
    def b(s):
        return s
    def u(s):
        return unicode(s, "unicode_escape")

from io import BytesIO
from functools import partial

_ALLOWED_METHODS = ("GET", "DELETE", "HEAD", "OPTIONS", "PUT", "POST", "TRACE", "PATCH")

#
#   Exceptions
#


#
#   Classes
#
class Headers(object):
    ''' Headers '''
    pass

class Body(object):
    ''' Body '''
    pass

class Connection(object):
    ''' HTTP/S Connection '''
    
    def __init__(self, conn_type='http', host=None, port=0, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        pass

    def request(self, method, url, body, headers):
        pass        

    def response(self):
        pass
        
#
#   Helpers
#

def parse_url(url):
    ''' returns dictionary of parsed url 
    
    username, password, scheme, host, port, query
    '''
    # TODO add extraction username and password from url, for example: http://username:password@host:port/    
    result = {
                'username': None, 'password': None, 
                'scheme': None, 'host': None, 'port': None, 
                'query': None, 
            }
    _scheme, _netloc, _path, _params, _query, _fragment = urlparse.urlparse(url)
    
    result['scheme'] = _scheme
    result['query'] = _path
    if _query: result['query'] += '?' + _query
    
    # handle 'Host'
    if ':' in _netloc:
        result['host'], result['port'] = _netloc.rsplit(':', 1)
        result['port'] = int(result['port'])
    else:
        result['host'], result['port'] = _netloc, None
    result['host'] = result['host'].encode('idna').decode('utf-8')
    
    return result



