import os
import sys
import random
import string
import unittest

# TODO run test server (run_test_server.py) and test cases ny one script
# TODO server output to log file
# TODO result of test cases in log file

py3k = (sys.version_info[0] == 3)
test_server_host = 'http://127.0.0.1:8800/'

def randstr(l=None, chars=string.ascii_letters+string.digits):
    ''' returns random string '''
    l = l or random.randint(1, 100)
    return ''.join(random.choice(chars) for i in range(l))

def randdict(l=None):
    ''' returns random dictionary '''
    i = l or random.randint(1, 100)
    d = {}
    for i in range(i):
        d[randstr()] = randstr()
    return d

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    tests = [i[:-3] for i in os.listdir(os.path.dirname(os.path.abspath(__file__))) 
            if i.startswith('test_') and i.endswith('.py')]

    tests_logfile = 'tests.log'
    logfile = open(tests_logfile, 'w')

    suite = unittest.defaultTestLoader.loadTestsFromNames(tests)
    result = unittest.TextTestRunner(logfile, verbosity=2).run(suite)

    sys.exit(1 if result.errors or result.failures else 0)
