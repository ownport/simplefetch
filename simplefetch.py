#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#   simplefetch, Simple HTTP client library
#


__version__ = '0.3.2'
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

# TODO review which modules can be removed as unsed
import os
import sys
import zlib
import gzip
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

_ALLOWED_SCHEMES = ("http", "https", )
_ALLOWED_METHODS = ("GET", "DELETE", "HEAD", "OPTIONS", "PUT", "POST", "TRACE", "PATCH", )

_PROXY_IGNORE_HOSTS = ('127.0.0.1', 'localhost',)

#
#   Exceptions
#

class UnknownConnectionSchemeException(Exception):
    pass

class ConnectionRequestException(Exception):
    pass

class ContentLengthLimitException(Exception):
    pass

class UnknownContentEncodingException(Exception):
    pass

#
#   Classes
#

class Headers(object):
    ''' Headers
    
    to simplify fetch() interface, class Headers helps to manipulate parameters
    '''
    def __init__(self):
        ''' use default paramters for header '''
        self.__headers = {
            'Accept': '*/*',
            'Accept-Encoding': ', '.join(('identity', 'deflate', 'compress', 'gzip')), 
            'User-Agent':  'simplefetch/' + __version__,
        }
    
    def basic_auth(self, username, password):
        ''' add username/password for basic authentication '''
        auth = '%s:%s' % (username, password)
        auth = base64.b64encode(auth.encode('utf-8'))
        self.__headers['Authorization'] = 'Basic ' + auth.decode('utf-8')

    # TODO support list of parameters
    def put(self, k, v):
        ''' add new parameter to headers '''
        self.__headers[k.title()] = v
    
    # TODO  rename method items() to dump() with support defferent formats 
    #       like dict, list/tuple, json, ...
    def items(self):
        ''' return headers dictionary '''
        return self.__headers

class Body(object):
    ''' Body '''
    pass

class Request(object):
    ''' Request '''
    pass

class Response(object):
    ''' Response '''
    def __init__(self, http_resp, content_limit=None):
    
        self.__http_resp = http_resp
        self.__CONTENT_DECODERS = { 'gzip': decode_gzip,'deflate': decode_deflate, }
        
        # TODO store headers to object Headers 
        self.__headers = dict((k.lower(), v) for k, v in self.__http_resp.getheaders())
        
        self.__content = None

        # content_limit: if content (length) size is more than content_limit -> skip
        try:
            self.__content_limit = int(content_limit)
        except:
            self.__content_limit = None

        setattr(self, 'msg', self.__http_resp.msg)
        setattr(self, 'version', self.__http_resp.version)
        setattr(self, 'status', self.__http_resp.status)
        setattr(self, 'reason', self.__http_resp.reason)
    
    @property
    def headers(self):
        ''' Response headers
        Response headers is a dict with all keys in lower case.
        '''
        return self.__headers

    def iter_content(self, chunk_size = 8192):
        ''' read content (for streaming and large files)
        
        chunk_size: size of chunk, default: 8192 bytes
        '''
        while True:
            chunk = self.__http_resp.read(chunk_size)
            if not chunk:
                break
            yield chunk

    @property
    def content(self):
        '''Response content.'''
        
        if self.__content is None:
            content = b("")
            for chunk in self.iter_content():
                content += chunk
                if self.__content_limit and len(content) > self.__content_limit:
                    raise ContentLengthLimitException("Content length is more than %d bytes" % self.__content_limit)  
            
            # decode content if encoded
            encoding = self.headers.get('content-encoding', None)
            decoder = self.__CONTENT_DECODERS.get(encoding)
            if encoding and not decoder:
                raise UnknownContentEncodingException(encoding)                
            
            if decoder:
                self.__content = decoder(content)
            else:
                self.__content = content
            
        return self.__content

class Connection(object):
    ''' HTTP/S Connection '''
    
    def __init__(self, scheme='http', host=None, port=80, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        ''' initial '''
        
        self.__via_proxy = False
        
        # TODO config file support with exceptions when proxy is needed and when is not
        
        if scheme not in _ALLOWED_SCHEMES:
            raise UnknownConnectionSchemeException(scheme)
        
        if _PROXIES[scheme].get('host', None) and _PROXIES[scheme].get('port', None) and \
            host not in _PROXY_IGNORE_HOSTS:

            host = _PROXIES[scheme]['host']
            port = _PROXIES[scheme]['port']
            self.__via_proxy = True

        self.__conn = None
        if scheme == 'http':
            self.__conn = HTTPConnection(host, port, timeout=timeout)
        elif scheme == 'https':
            self.__conn = HTTPSConnection(host, port, timeout=timeout)
        else:
            raise UnknownConnectionSchemeException(scheme)    

    def request(self, method='GET', url, body, headers):
        ''' 
        send request 
        '''
        try:
            self.__conn.request(method, url, body, headers)
        except socket.error, err:
            raise ConnectionRequestException(err)

    def response(self, content_limit=None):
        '''
        returns response
        '''
        return Response(self.__conn.getresponse(), content_limit=content_limit)
    
    @property
    def  via_proxy(self):
        ''' returns True if proxy is in use '''
        return self.__via_proxy
    
    def close(self):
        '''
        close connection
        '''
        self.__conn.close()
#
#   Helpers
#

def decode_gzip(data):
    ''' decode gzipped content '''
    gzipper = gzip.GzipFile(fileobj=BytesIO(data))
    return gzipper.read()


def decode_deflate(data):
    ''' decode deflate content '''
    try:
        return zlib.decompress(data)
    except zlib.error:
        return zlib.decompress(data, -zlib.MAX_WBITS)

# TODO  data or payload? payload is body content for a POST or PUT request.
# TODO  follow_redirects = (False)/True. If True, responses that are HTTP redirects are followed. 
#       The response data will be from the final location. If False (default), redirects are not followed
# TODO  redirects limitation
# TODO  redirects history

def fetch(url, method="GET", data=None, headers={}, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
            files={}, length_limit=None):
            
    ''' request an URL
    
    method: HTTP method, one of HEAD, GET, POST, DELETE,  OPTIONS, PUT, TRACE. GET is used by default.
    url: URL to be requested.
    headers: HTTP request headers
    timeout: timeout in seconds, socket._GLOBAL_DEFAULT_TIMEOUT by default
    files: files to be sended
    length_limit: if None, no limits on content length, if the limit reached raised ContentLengthLimitException 
    
    returns Response object
    '''
    method = method.upper()
    if method not in _ALLOWED_METHODS:
        raise UnsupportedMethodException(method)

    parsed_url = parse_url(url)
    scheme = parsed_url.get('scheme')

    # connection with proxy support
    # by default for connection object all parameters defined based on information from URL
    # but in case when proxy defined in system environment these parameters will be reassigned
    # To check it, use connection.via_proxy property: True if proxy is used
    conn = Connection(scheme=parsed_url['scheme'], host=parsed_url['host'], port=parsed_url['port'], timeout=timeout)

    # default request headers
    reqheaders = Headers()

    # prepare data 
    if files:
        content_type, data = _encode_multipart(data, files)
        reqheaders.put('Content-Type', content_type)
    elif isinstance(data, dict):
        data = urlencode(data, 1)
    
    if isinstance(data, basestring) and not files:
        reqheaders.put("Content-Type", "application/x-www-form-urlencoded")

    for k, v in headers.items():
        reqheaders.put(k, v) 

    if conn.via_proxy:
        conn.request(method, url, data, reqheaders.items())
    else:
        conn.request(method, parsed_url['full_path'], data, reqheaders.items())
    return conn.response(content_limit=length_limit)

# TODO if class Request is used, make new shortcuts 
# some shortcuts
get = partial(fetch, method="GET")
post = partial(fetch, method="POST")
put = partial(fetch, method="PUT")
delete = partial(fetch, method="DELETE")
head = partial(fetch, method="HEAD")
options = partial(fetch, method="OPTIONS")
# No entity body can be sent with a TRACE request. 
trace = partial(fetch, method="TRACE", files={}, data=None)
patch = partial(fetch, method="PATCH")
    

def parse_url(url):
    ''' returns dictionary of parsed url 
    
    scheme, username, password, host, port, full_path
    
    where full_path is combination of path + query + fragment
    '''
    result = dict()
    if not isinstance(url, (str, unicode)) or not url:
        return result
    
    parsed = urlparse.urlsplit(url)
    
    result['scheme'] = parsed.scheme
    result['username'] = parsed.username
    result['password'] = parsed.password
    result['host'] = parsed.hostname.encode('idna').decode('utf-8')
    result['port'] = parsed.port

    result['full_path'] = parsed.path
    if parsed.query:
        result['full_path'] += '?' + parsed.query
    if parsed.fragment:
        result['full_path'] += '#' + parsed.fragment

    return result

#
#   Proxy definitions (from system environment)
#
def _get_env(param_name):
    ''' get variable from system environment'''
    _env = dict((k.lower(),v) for k,v in os.environ.items())
    return _env.get(param_name.lower(), None)

_PROXIES = {
    'http': dict([(k,v) for k,v in parse_url(_get_env('http_proxy')).items() if k in ('host', 'port')]),
    'https': dict([(k,v) for k,v in parse_url(_get_env('https_proxy')).items() if k in ('host', 'port')]),
}

def cookie2str(cookie):
    # TODO make cookie2str as part of Headers class
    '''
    Convert Set-Cookie header to cookie string.
    '''
    c = Cookie.SimpleCookie(sc)
    sc = ['%s=%s' % (i.key, i.value) for i in c.itervalues()]
    return '; '.join(sc)

_boundary_prefix = None
def choose_boundary():
    '''
    Generate a multipart boundry.
    '''
    
    global _boundary_prefix
    if _boundary_prefix is None:
        _boundary_prefix = "simplefetch"
        import os
        try:
            uid = repr(os.getuid())
            _boundary_prefix += "." + uid
        except AttributeError: pass
        try:
            pid = repr(os.getpid())
            _boundary_prefix += "." + pid
        except AttributeError: pass
    import uuid
    return "(*^__^*)%s.%s" % (_boundary_prefix, uuid.uuid4().hex)

def _encode_multipart(data, files):
    '''
    Encode multipart.
    '''
    
    body = BytesIO()
    boundary = choose_boundary()
    part_boundary = b('--%s\r\n' % boundary)

    if isinstance(data, dict):
        for name, value in data.items():
            body.write(part_boundary)
            writer(body).write('Content-Disposition: form-data; name="%s"\r\n' % name)
            body.write(b'Content-Type: text/plain\r\n\r\n')
            if py3k and isinstance(value, str): 
                writer(body).write(value)
            else:
                body.write(value)
            body.write(b'\r\n')
            
    for fieldname, f in files.items():
        if isinstance(f, tuple):
            filename, f = f
        elif hasattr(f, 'name'):
            filename = os.path.basename(f.name)
        else:
            filename = None
            raise IncorrectFilename("file must has filename")

        if hasattr(f, 'read'):
            value = f.read()
        elif isinstance(f, basestring):
            value = f
        else:
            value = str(f)

        body.write(part_boundary)
        if filename:
            writer(body).write('Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (fieldname, filename))
            body.write(b'Content-Type: application/octet-stream\r\n\r\n')
        else:
            writer(body).write('Content-Disposition: form-data; name="%s"\r\n' % name)
            body.write(b'Content-Type: text/plain\r\n\r\n')

        if py3k and isinstance(value, str):
            writer(body).write(value)
        else:
            body.write(value)
        body.write(b'\r\n')

    body.write(b('--' + boundary + '--\r\n'))

    content_type = 'multipart/form-data; boundary=%s' % boundary
    #body.write(b(content_type))

    return content_type, body.getvalue()


