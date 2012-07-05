#!/usr/bin/env python
#
#   run_test_server.py
#

import bottle
import logging

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

if __name__ == '__main__':
    import sys
    try:
        logfile = sys.argv[1]
    except IndexError:
        logfile = None
    logging.basicConfig(format='%(asctime)s pid:%(process)d <%(levelname)s> %(message)s', 
                        filename = logfile, 
                        level=logging.DEBUG)
    bottle.run(app=app, host='127.0.0.1', port=8800, reloader=True, debug=True)
