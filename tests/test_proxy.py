import testall
import simplefetch
import unittest


class ProxyTest(unittest.TestCase):

    def test_no_env_defined(self):
        simplefetch.PROXIES = dict()
        resp = simplefetch.get('http://127.0.0.1:8800')
        self.assertEqual(resp.status,200)

    def test_env_defined_but_empty(self):
        simplefetch.PROXIES['http'] = None
        resp = simplefetch.get('http://127.0.0.1:8800')
        self.assertEqual(resp.status,200)        

    def test_get_via_proxy(self):
        simplefetch.PROXIES['http'] = 'http://127.0.0.1:8800'
        resp = simplefetch.get('http://www.example.com')
        self.assertEqual(resp.status,200)

    def test_ignored_host(self):
        simplefetch.PROXIES['http'] = 'http://127.0.0.1:8800'
        resp = simplefetch.get('http://localhost:8800')
        self.assertEqual(resp.status,200)
        


if __name__ == '__main__':
    unittest.main()
