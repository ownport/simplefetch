# Proxy

```python
>>> import simplefetch
>>> conn = simplefetch.Connection(conn_type='http',host='localhost', port=8800)
>>> conn.request('GET', 'http://www.google.com', None, {})
>>> resp = conn.response()
>>> resp.status
200

```
