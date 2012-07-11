#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#   simplefetch, Simple HTTP client library
#
#   based on lyxint/urlfetch 
#   https://github.com/lyxint/urlfetch 
#   (c) 2011-2012  Elyes Du (lyxint@gmail.com)
#   license: BSD 2-clause License, see LICENSE for details.


__version__ = '0.1'
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
#   Session -> Headers -> Request -> Response -> Session (update)
#


import os
import sys
import socket
import base64
# TODO is it needed here if no codec modification in simplefetch.py?
import codecs

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
# TODO no need to perform codec modification. It's better to make it by specfic library
writer = codecs.lookup('utf-8')[3]


__all__ = [
    'fetch', 'request', 
    'get', 'head', 'put', 'post', 'delete', 'options',
    'Headers', 'Request', 'Response', 'Session',
] 

_allowed_methods = ("GET", "DELETE", "HEAD", "OPTIONS", "PUT", "POST", "TRACE", "PATCH")

#
#   Exceptions
#

class IncorrectFilename(Exception): 
    ''' Incorrect filename exception '''
    pass

class ContentLengthLimitException(Exception):
    ''' Content Length was reached limit '''
    pass

class UnsupportedMethodException(Exception): 
    ''' Method is not supported'''
    pass

class UnsupportedProtocolException(Exception): 
    ''' Protocol is not supported '''    
    pass
    
class ConnectionRequestException(Exception):
    ''' Connection request exception '''    
    pass

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

class Headers(object):
    ''' Headers
    
    to simplify fetch() interface, class Headers helps to manipulate parameters
    '''
    def __init__(self):
        ''' make default headers '''
        self.__headers = {
            'Accept': '*/*',
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

class Request(object):
    ''' class Request '''

    # TODO add proxy support    
    # TODO even if proxy is not defined -> check environment (http_proxy, htts_proxy)
    def __init__(url, method="GET", timeout=socket._GLOBAL_DEFAULT_TIMEOUT, length_limit=None)
        pass
    
    def set_headers(self, headers={}):
        ''' set headers '''
        pass
    
    def set_data(self, data=None):
        ''' set data '''
        pass

    def set_files(self, files={}):
        ''' set files '''
        pass
    
    def set_proxy(self, proxy=None):
        ''' set proxy '''
        pass
    
    def get_response(self):
        ''' get response '''
        pass

class Response(object):
    '''
    Response
    '''
    def __init__(self, r, **kwargs):
        self._r = r # httplib.HTTPResponse
        self.msg = r.msg
        
        #: Status code returned by server.
        self.status = r.status
        
        #: Reason phrase returned by server.
        self.reason = r.reason
        
        #: HTTP protocol version used by server. 10 for HTTP/1.0, 11 for HTTP/1.1.
        self.version = r.version
        self._content = None
        self._headers = None

        # TODO store headers to object Headers 
        self.getheader = r.getheader
        self.getheaders = r.getheaders

        for k in kwargs:
            setattr(self, k, kwargs[k])

        # length_limit: if content (length) size is more than length_limit -> skip
        try:
            self.length_limit = int(kwargs.get('length_limit'))
        except:
            self.length_limit = None
            
        if self.length_limit and int(self.getheader('Content-Length', 0)) > self.length_limit:
            self.close()
            raise ContentLengthLimitException("Content length is more than %d bytes" % length_limit)  
        
    def iter_content(self, chunk_size = 1024):
        ''' read content (for streaming and large files)
        
        chunk_size: size of chunk, default: 1024 bytes
        '''
        while True:
            chunk = self._r.read(chunk_size)
            if not chunk:
                break
            yield chunk
        
    @property
    def content(self):
        '''Response content.'''
        
        if self._content is None:
            content = b("")
            for chunk in self.iter_content():
                content += chunk
                if self.length_limit and len(content) > self.length_limit:
                    raise ContentLengthLimitException("Content length is more than %d bytes" % length_limit)  
            self._content = content
        return self._content
        
    @property
    def headers(self):
        '''
        Response headers
        
        Response headers is a dict with all keys in lower case.
        '''
        
        if self._headers is None:
            self._headers = dict((k.lower(), v) for k, v in self._r.getheaders())
        return self._headers

    def close(self):
        ''' close '''
        if hasattr(self, 'connection'):
            self.connection.close()
        self._r.close()

    def __del__(self):
        ''' delete Response object '''
        self.close()        


def request(url, method="GET", data=None, headers={}, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
            files={}, length_limit=None, proxy = None):
            
    ''' request an URL
    
    method: HTTP method, one of HEAD, GET, POST, DELETE,  OPTIONS, PUT, TRACE. GET is used by default.
    url: URL to be requested.
    headers: HTTP request headers
    timeout: timeout in seconds, socket._GLOBAL_DEFAULT_TIMEOUT by default
    files: files to be sended
    length_limit: if None, no limits on content length, if the limit reached raised ContentLengthLimitException 
    
    returns Response object
    '''

    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    method = method.upper()
    if method not in _allowed_methods:
        raise UnsupportedMethodException("Method should be one of " + ", ".join(_allowed_methods))

    requrl = path
    if query: requrl += '?' + query
    # do not add fragment
    #if fragment: requrl += '#' + fragment
    
    # handle 'Host'
    if ':' in netloc:
        host, port = netloc.rsplit(':', 1)
        port = int(port)
    else:
        host, port = netloc, None
    host = host.encode('idna').decode('utf-8')
    
    if scheme == 'https':
        h = HTTPSConnection(host, port=port, timeout=timeout)
    elif scheme == 'http':
        h = HTTPConnection(host, port=port, timeout=timeout)
    else:
        raise UnsupportedProtocolException('Unsupported protocol %s' % scheme)
        s
    # default request headers
    reqheaders = Headers().items()
    
    if files:
        content_type, data = _encode_multipart(data, files)
        reqheaders['Content-Type'] = content_type
    elif isinstance(data, dict):
        data = urlencode(data, 1)
    
    if isinstance(data, basestring) and not files:
        # httplib will set 'Content-Length', also you can set it by yourself
        reqheaders["Content-Type"] = "application/x-www-form-urlencoded"
        # what if the method is GET, HEAD or DELETE 
        # just do not make so much decisions for users

    for k, v in headers.items():
        reqheaders[k.title()] = v 

    try:
        h.request(method, requrl, data, reqheaders)
    except socket.error, err:
        raise ConnectionRequestException(err)
    response = h.getresponse()
    return Response(response, reqheaders=reqheaders, connection=h, length_limit=length_limit)

# TODO if class Request is used, make new shortcuts 
# some shortcuts
get = partial(request, method="GET")
post = partial(request, method="POST")
put = partial(request, method="PUT")
delete = partial(request, method="DELETE")
head = partial(request, method="HEAD")
options = partial(request, method="OPTIONS")
# No entity body can be sent with a TRACE request. 
trace = partial(request, method="TRACE", files={}, data=None)
patch = partial(request, method="PATCH")

