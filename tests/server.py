#!/usr/bin/env python
#
#   run_test_server.py
#

import sys

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

import bottle

app = bottle.app()

@app.route('/', method=['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'OPTIONS', 'PATCH'])
def index():
    return 'index'

def basic_auth_check(username, password):
    if username == "urlfetch" and password == "fetchurl":
        return True
    return False

@app.route('/basic_auth', method=['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'OPTIONS', 'PATCH'])
@bottle.auth_basic(basic_auth_check)
def basic_auth():
    return 'basic_auth'

@app.route('/sleep/<seconds:int>', method=['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'OPTIONS', 'PATCH'])
def sleep(seconds):
    import time
    time.sleep(seconds)

    return 'sleep'

# TODO run test server as service / daemon
bottle.run(app=app, host='127.0.0.1', port=8800, reloader=True)

