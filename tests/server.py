#!/usr/bin/env python
#
#   run_test_server.py
#

import sys
import json

def basic_auth_check(username, password):
    if username == "simplefetch_username" and password == "simplefetch_password":
        return True
    return False

class stream2file:
    ''' Stream wrapper for saving data in file'''
    def __init__(self, filename='stream.data'):

        self.fd = open(filename, 'a', 0)
        
    def write(self, data):
        d = data.rstrip() 
        if d == '': return
        self.fd.write("%s\n" % d)

    def close(self):
        self.fd.close()

try:
    sys.stdout = sys.stderr = stream2file(filename=sys.argv[1])
except IndexError:
    pass

from packages import bottle
from packages.bottle import request, response

def normal_formsdict():
    d = {}
    d['url'] = request.url
    d['path'] = request.path
    d['fullpath'] = request.fullpath
    d['method'] = request.method
    d['query_string'] = request.query_string
    d['script_name'] = request.script_name
    d['is_xhr'] = request.is_xhr
    d['is_ajax'] = request.is_ajax
    d['auth'] = request.auth
    d['remote_addr'] = request.remote_addr
    #d['environ'] = dict(request.environ)
    d['headers'] = dict(request.headers)

    #d['query'] = dict(request.query)
    d['forms'] = dict(request.forms)
    d['params'] = dict(request.params)
    d['get'] = dict(request.GET)
    d['post'] = dict(request.POST)
    d['files'] = dict(request.files)
    for i in d['files']:
        del d['post'][i]
        d['files'][i] = (d['files'][i].name, d['files'][i].filename, mb_code(d['files'][i].value))
    d['cookies'] = dict(request.cookies)
    return json.dumps(d)

app = bottle.app()

@app.route('/', method=['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'OPTIONS', 'PATCH', 'TRACE'])
def index():
    return normal_formsdict()

@app.route('/#fragment', method=['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'OPTIONS', 'PATCH', 'TRACE'])
def index():
    return normal_formsdict()


@app.route('/basic_auth', method=['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'OPTIONS', 'PATCH'])
@bottle.auth_basic(basic_auth_check)
def basic_auth():
    return normal_formsdict()

@app.route('/sleep/<seconds:int>', method=['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'OPTIONS', 'PATCH'])
def sleep(seconds):
    import time
    time.sleep(seconds)

    return normal_formsdict()

@app.route('http://www.example.com', method=['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'OPTIONS', 'PATCH'])
def index():
    return normal_formsdict()



# TODO run test server as service / daemon
bottle.run(app=app, host='127.0.0.1', port=8800, reloader=True)

