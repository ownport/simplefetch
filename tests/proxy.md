# Proxy

```python
>>> import simplefetch
>>> conn = simplefetch.Connection(conn_type='http')
>>> conn.request('GET', 'http://devel.ownport.net', None, {})
>>> resp = conn.response()
>>> resp.status
200
>>> len(resp.content) > 0
True

```

```python
>>> resp = simplefetch.get('http://devel.ownport.net')
>>> resp.status
200
>>> len(resp.content) > 0
True

```

```python
>>> resp = simplefetch.get('https://github.com')
>>> resp.status
200
>>> len(resp.content) > 0
True

```
