#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#
# Copyright 2010 Andrey Usov <uandrey@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

'''
-----------------
async HTTP server
-----------------

original: http://github.com/facebook/tornado/blob/master/tornado/httpserver.py
modyfied to work with async module instead of epoll

HTTP methods: 
    GET                                         supported
    POST/application/x-www-form-urlencoded      supported
    POST/multipart/form-data                    supported
    PUT/application/x-www-form-urlencoded       supported
    PUT/multipart/form-data                     supported
    DELETE                                      supported

----------------
TO DO    
----------------
- logging
    
----------------
Example of usage
----------------
import asynchttpsrv

def appl_handler(request):
    message = 'You requested %s via method %s on AsyncHTTPServer-0.1\n' % (request['uri'], request['method'])
    return "HTTP/1.1 200 (OK)\r\nContent-Length: %d\r\nServer: AsyncHTTPServer-0.1\r\n\r\n%s" % (len(message), message)

address = ('127.0.0.1', 8080)

print 'HTTP Server %s is starting' % str(address)
server = asynchttpsrv.HTTPServer(address, appl_handler)
try:
    server.loop(timeout=2)
except KeyboardInterrupt:
    server.stop()
    print 'HTTP Server was stopped'
    
'''



import socket
import asyncore
import urlparse

class HTTPConnection(asyncore.dispatcher):
    def __init__(self, conn, client_address, server):
        self.server = server
        self.client_address = client_address
        
        self._recv_size = 4096
        self._in_buffer = ''
        
        self._is_writable = False
        self._out_buffer = ''
        
        self.request = {}
        self.request['remote_ip'] = self.client_address[0]
        
        asyncore.dispatcher.__init__(self, conn)
    
    def readable(self):
        return True
        
    def handle_read(self):
        data = self.recv(self._recv_size)
        self._in_buffer = ''.join((self._in_buffer, data))
        if len(self._in_buffer) > 0: 
            if 'method' not in self.request:
                self._on_headers()
            else:
                if len(self._in_buffer) == self._recv_size: self._on_request_body()

    def writable(self):
        return self._is_writable
        
    def to_write(self, data):
        self._out_buffer = ''.join((self._out_buffer, data))
        self._is_writable = True

    def handle_write(self):
        if len(self._out_buffer):
            sent = self.send(self._out_buffer)
            self._out_buffer = self._out_buffer[sent:]
        else:
            self._is_writable = False
            self.handle_close()

    def handle_close(self):
        self.close()
    
    def parse_headers(self, lines):
        ''' A dictionary that maintains Http-Header-Case for all keys.
    
        original:  http://github.com/facebook/tornado/blob/master/tornado/httpserver.py '''
        
        def normalize_name(name):
            return "-".join([w.capitalize() for w in name.split("-")])
        
        headers = dict()
        delimeters = [':','=']
        request_body = None
        for i,line in enumerate(lines):
            pairs = line.split(';')
            for pair in pairs:
                for d in delimeters:
                    if pair.find(d) > -1:
                        name, value = pair.split(d, 1)
                        headers[name.strip()] = value.strip().strip('"')
                        continue
        return headers
    
    def _on_headers(self):
        headers, self._in_buffer = self._in_buffer.split('\r\n\r\n', 1)
        headers = headers.splitlines()
        
        self.request['method'], self.request['uri'], self.request['version'] = headers[0].split(' ')
        scheme, netloc, self.request['path'], self.request['query'], fragment = urlparse.urlsplit(self.request['uri'])
        del(headers[0])

        self.request['POST'] = {}
        self.request['PUT'] = {}
        self.request['headers'] = self.parse_headers(headers)
        
        if self.request['method'] in ('POST', 'PUT'):
            if 'Content-Length' in self.request['headers']:
                content_length = int(self.request['headers']['Content-Length'])
                self._recv_size = content_length
                
                # not all information included in header
                if len(self._in_buffer) != content_length:  return
                
                # header contains all information 
                self._on_request_body()
                return 
        
        # run request application
        self._on_application()
        
    def _on_request_body(self):
        content_type = self.request['headers']['Content-Type']
        
        # application/x-www-form-urlencoded
        if content_type == 'application/x-www-form-urlencoded':
            arguments = ''.join(self._in_buffer).split('&')
            method = self.request['method']
            for arg in arguments:
                name,value = arg.split('=') 
                if name in self.request[method]:
                    self.request[method][name].append(value)
                else:
                    self.request[method][name] = [value,]
                    
        # multipart/form-data
        elif content_type == 'multipart/form-data':
            if 'boundary' in self.request['headers']: self._parse_mime_body()

        # run request application
        self._on_application()
    
    def _parse_mime_body(self):
        ''' 
        original:  http://github.com/facebook/tornado/blob/master/tornado/httpserver.py 
        '''
        boundary = self.request['headers']['boundary']
        data = self._in_buffer

        footer_length = len(boundary) + 4
        if data.endswith("\r\n"): 
            footer_length = len(boundary) + 6

        for part in data[:-footer_length].split("--" + boundary + "\r\n"):
            if not part: continue
            eoh = part.find('\r\n\r\n')
            
            # multipart/form-data missing headers
            if eoh == -1: continue
            
            headers = self.parse_headers(part[:eoh].splitlines())
            
            # Invalid multipart/form-data
            if 'Content-Disposition' not in headers: continue
        
            name = headers['name']
            value = part[eoh + 4:-2]
            if name not in self.request['POST']:
                self.request['POST'][name] = []
            if 'filename' in headers:
                self.request['POST'][name].append({
                                                    'filename': headers['filename'], 
                                                    'Content-Type': headers['Content-Type'], 
                                                    'body': value
                                                    })
            else:
                self.request['POST'][name].append(part[eoh + 4:-2])
    
    def _on_application(self):
        data_to_write = self.server.appl_handler(self.request)
        if data_to_write: self.to_write(data_to_write)
        
    
class HTTPServer(asyncore.dispatcher):
    ''' non-blocked HTTP server '''
    def __init__(self, address, appl_handler):
        
        self.appl_handler = appl_handler
        
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.setblocking(0)
        
        self.bind(address)
        self.listen(10)

    def handle_accept(self):
        conn, addr = self.accept()
        #print addr
        HTTPConnection(conn, addr, self)
            
    def loop(self, timeout):
        asyncore.loop(timeout)
    
    def stop(self):
        self.close()
        
        
if __name__ == '__main__':
    import time
    import random
    
    def appl_handler(request):
        message = 'You requested %s via method %s on AsyncHTTPServer-0.1\n' 
        message = message % (request['uri'], request['method'])

        header = "HTTP/1.1 200 (OK)\r\nContent-Length: %d\r\nServer: AsyncHTTPServer-0.1\r\n\r\n%s"
        return  header % (len(message), message)
    
    address = ('127.0.0.1', 8800)
    
    print 'HTTP Server %s is starting' % str(address)
    server = HTTPServer(address, appl_handler)
    try:
        server.loop(timeout=2)
    except KeyboardInterrupt:
        server.stop()
        print 'HTTP Server was stopped'
    
