import testall
import simplefetch
import unittest


class TestHelpers(unittest.TestCase):

    def test_parse_url(self):
        url = 'http://www.example.com'
        parsed_url = simplefetch.parse_url(url)
        self.assertEqual(parsed_url['scheme'], 'http')
        self.assertEqual(parsed_url['host'], 'www.example.com')

        url = 'http://www.example.com:8800'
        parsed_url = simplefetch.parse_url(url)
        self.assertEqual(parsed_url['scheme'], 'http')
        self.assertEqual(parsed_url['host'], 'www.example.com')
        self.assertEqual(parsed_url['port'], 8800)

        url = 'https://www.example.com'
        parsed_url = simplefetch.parse_url(url)
        self.assertEqual(parsed_url['scheme'], 'https')

        url = 'http://www.example.com/path'
        parsed_url = simplefetch.parse_url(url)
        self.assertEqual(parsed_url['query'], '/path')

        url = 'http://www.example.com/path?key1=value1&key2=value2'
        parsed_url = simplefetch.parse_url(url)
        self.assertEqual(parsed_url['query'], '/path?key1=value1&key2=value2')

        url = 'http://www.example.com/path?key1=value1&key2=value2#fragment'
        parsed_url = simplefetch.parse_url(url)
        self.assertEqual(parsed_url['query'], '/path?key1=value1&key2=value2')

        url = 'https://username:password@www.example.com'
        parsed_url = simplefetch.parse_url(url)
        self.assertEqual(parsed_url['scheme'], 'https')
        self.assertEqual(parsed_url['username'], 'username')
        self.assertEqual(parsed_url['password'], 'password')


if __name__ == '__main__':
    unittest.main()
