# Helpers 

### parse_url(url)

returns parsed url parameters as dictionary with keys: scheme, host, port, query

```python
>>> import simplefetch
>>> simplefetch.parse_url('http://localhost:8080')
{'username': None, 'password': None, 'host': u'localhost', 'query': '', 'scheme': 'http', 'port': 8080}
>>>
>>> simplefetch.parse_url('https://localhost:8080')
{'username': None, 'password': None, 'host': u'localhost', 'query': '', 'scheme': 'https', 'port': 8080}
>>>
>>> simplefetch.parse_url('http://127.0.0.1:8080')
{'username': None, 'password': None, 'host': u'127.0.0.1', 'query': '', 'scheme': 'http', 'port': 8080}
>>>
>>> simplefetch.parse_url('http://localhost:8080/test')
{'username': None, 'password': None, 'host': u'localhost', 'query': '/test', 'scheme': 'http', 'port': 8080}
>>>
>>> simplefetch.parse_url('http://localhost:8080/test?id=1&name=tt')
{'username': None, 'password': None, 'host': u'localhost', 'query': '/test?id=1&name=tt', 'scheme': 'http', 'port': 8080}
>>>
>>> simplefetch.parse_url('http://localhost:8080/test?id=1&name=tt#12')
{'username': None, 'password': None, 'host': u'localhost', 'query': '/test?id=1&name=tt', 'scheme': 'http', 'port': 8080}
>>>
>>> simplefetch.parse_url('http://localhost:8080/#12')
{'username': None, 'password': None, 'host': u'localhost', 'query': '/', 'scheme': 'http', 'port': 8080}
>>>
```
