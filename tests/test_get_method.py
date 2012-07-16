import json
import socket
import testall
import unittest
import simplefetch

class TestGetMethod(unittest.TestCase):

    def test_fetch(self):
        res = simplefetch.fetch(testall.test_server_host)
        self.assertEqual(res.status, 200)

    def test_get(self):
        res = simplefetch.get(testall.test_server_host)
        self.assertEqual(res.status, 200)

    def test_fragment(self):
        res = simplefetch.get('%s#fragment' % testall.test_server_host)
        self.assertEqual(res.status, 200)

    def test_query_string(self):
        qs = testall.randdict(5)
        query_string = simplefetch.urlencode(qs)
        
        res = simplefetch.get("%s?%s" % (testall.test_server_host, query_string))
        content = json.loads(res.content)

        self.assertEqual(res.status, 200)
        self.assertEqual(content['method'], 'GET')
        self.assertEqual(content['query_string'], query_string)
        self.assertEqual(content['get'], qs)

    def test_fragment_query_string(self):
        qs = testall.randdict(5)
        query_string = simplefetch.urlencode(qs)
        
        res = simplefetch.get("%s?%s#fragment" % (testall.test_server_host, query_string))
        content = json.loads(res.content)

        self.assertEqual(res.status, 200)
        self.assertEqual(content['method'], 'GET')
        self.assertEqual(content['query_string'], "%s#fragment" % query_string)

    def test_basic_auth(self):
        headers = simplefetch.Headers()
        headers.basic_auth('simplefetch_username', 'simplefetch_password')
        res = simplefetch.get("%sbasic_auth" % testall.test_server_host, headers=headers.items())
        content = json.loads(res.content)
        
        self.assertEqual(res.status, 200)
        self.assertEqual(content['method'], 'GET')

    def test_basic_auth_query_string(self):
        qs = testall.randdict(5)
        query_string = simplefetch.urlencode(qs)

        headers = simplefetch.Headers()
        headers.basic_auth('simplefetch_username', 'simplefetch_password')
        res = simplefetch.get("%sbasic_auth?%s" % (testall.test_server_host, query_string), headers=headers.items())
        content = json.loads(res.content)

        self.assertEqual(res.status, 200)
        self.assertEqual(content['method'], 'GET')
        self.assertEqual(content['query_string'], query_string)
        self.assertEqual(content['get'], qs)

    def test_fragment_basic_auth_query_string(self):
        qs = testall.randdict(5)
        query_string = simplefetch.urlencode(qs)
        
        headers = simplefetch.Headers()
        headers.basic_auth('simplefetch_username', 'simplefetch_password')
        res = simplefetch.get("%sbasic_auth?%s#fragment" % (testall.test_server_host, query_string), headers=headers.items())
        content = json.loads(res.content)

        self.assertEqual(res.status, 200)
        self.assertEqual(content['method'], 'GET')
        self.assertEqual(content['query_string'], "%s#fragment" % query_string)

    def test_timeout(self):
        self.assertRaises(socket.timeout, lambda:simplefetch.get("%ssleep/1" % testall.test_server_host, timeout=0.5))

if __name__ == '__main__':
    unittest.main()
