# Helpers 

### parse_url(url)

returns parsed url parameters as dictionary with keys: scheme, host, port, query

```python
>>> import simplefetch
>>> simplefetch.parse_url('http://localhost:8080')
{'query': '', 'host': u'localhost', 'scheme': 'http', 'port': 8080}
>>>
>>> simplefetch.parse_url('https://localhost:8080')
{'query': '', 'host': u'localhost', 'scheme': 'https', 'port': 8080}
>>>
>>> simplefetch.parse_url('http://127.0.0.1:8080')
{'query': '', 'host': u'127.0.0.1', 'scheme': 'http', 'port': 8080}
>>>
>>> simplefetch.parse_url('http://localhost:8080/test')
{'query': '/test', 'host': u'localhost', 'scheme': 'http', 'port': 8080}
>>>
>>> simplefetch.parse_url('http://localhost:8080/test?id=1&name=tt')
{'query': '/test?id=1&name=tt', 'host': u'localhost', 'scheme': 'http', 'port': 8080}
>>>
>>> simplefetch.parse_url('http://localhost:8080/test?id=1&name=tt#12')
{'query': '/test?id=1&name=tt', 'host': u'localhost', 'scheme': 'http', 'port': 8080}
>>>
>>> simplefetch.parse_url('http://localhost:8080/#12')
{'query': '/', 'host': u'localhost', 'scheme': 'http', 'port': 8080}
>>>
```
