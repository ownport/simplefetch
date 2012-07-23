import testall
import simplefetch
import unittest


class TestConnection(unittest.TestCase):

    def test_simple_connection(self):
        simplefetch.PROXIES = dict()
        conn = simplefetch.Connection(scheme='http', host='127.0.0.1', port=8800)
        conn.request('GET', '/', None, {})
        resp = conn.response()
        self.assertEqual(resp.status, 200)

    def test_connection_via_proxy(self):
        simplefetch.PROXIES = {'http': 'http://127.0.0.1:8800'}
        conn = simplefetch.Connection(scheme='http')
        conn.request('GET', 'http://www.example.com', None, {})
        resp = conn.response()
        self.assertEqual(resp.status, 200)

    def test_unknown_scheme(self):
        with self.assertRaises(simplefetch.UnknownConnectionSchemeException):
            conn = simplefetch.Connection(scheme='ftp')
        

if __name__ == '__main__':
    unittest.main()
