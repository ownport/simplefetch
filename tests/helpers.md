# Helpers 

### parse_url(url)

returns parsed url parameters as dictionary with keys: scheme, host, port, query

```python
>>> import simplefetch
>>> simplefetch.parse_url('http://localhost:8080')
{'username': None, 'scheme': 'http', 'host': u'localhost', 'password': None, 'port': 8080, 'full_path': ''}
>>>
>>> simplefetch.parse_url('https://localhost:8080')
{'username': None, 'scheme': 'https', 'host': u'localhost', 'password': None, 'port': 8080, 'full_path': ''}
>>>
>>> simplefetch.parse_url('http://127.0.0.1:8080')
{'username': None, 'scheme': 'http', 'host': u'127.0.0.1', 'password': None, 'port': 8080, 'full_path': ''}
>>>
>>> simplefetch.parse_url('http://localhost:8080/test')
{'username': None, 'scheme': 'http', 'host': u'localhost', 'password': None, 'port': 8080, 'full_path': '/test'}
>>>
>>> simplefetch.parse_url('http://localhost:8080/test?id=1&name=tt')
{'username': None, 'scheme': 'http', 'host': u'localhost', 'password': None, 'port': 8080, 'full_path': '/test?id=1&name=tt'}
>>>
>>> simplefetch.parse_url('http://localhost:8080/test?id=1&name=tt#12')
{'username': None, 'scheme': 'http', 'host': u'localhost', 'password': None, 'port': 8080, 'full_path': '/test?id=1&name=tt#12'}
>>>
>>> simplefetch.parse_url('http://localhost:8080/#12')
{'username': None, 'scheme': 'http', 'host': u'localhost', 'password': None, 'port': 8080, 'full_path': '/#12'}
>>>
```
