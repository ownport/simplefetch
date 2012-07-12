# Connection

Connection class supports to create HTTP or HTTPS connection. 
It's used as building block for creation HTTP/S connection to proxy server

### Creation new connection
```python
>>> import simplefetch
>>> http_conn = simplefetch.Connection(conn_type='http', host='localhost', port=8800)
>>> type(http_conn)
<class 'simplefetch.Connection'>
>>>
>>> https_conn = simplefetch.Connection(conn_type='https', host='localhost', port=8800)
>>> type(https_conn)
<class 'simplefetch.Connection'>
>>> https_conn.close()
>>>
>>> ftp_conn = simplefetch.Connection(conn_type='ftp', host='localhost', port=8800)
Traceback (most recent call last):
...
UnknownConnectionTypeException: ftp
>>>

```
In case usage of unknown connection type will be raised exception 'UnknownConnectionTypeException' 
with indication of unknown connection type.

### Send request

```python
>>> http_conn.request('GET', '/', None, {})
>>> resp = http_conn.response()

```

Many HTTP methods are supported: DELETE, HEAD, OPTIONS, PUT, POST, TRACE, PATCH
```python
>>> http_conn.request('DELETE', '/', None, {})
>>> resp = http_conn.response()
>>> http_conn.request('HEAD', '/', None, {})
>>> resp = http_conn.response()
>>> http_conn.request('OPTIONS', '/', None, {})
>>> resp = http_conn.response()
>>> http_conn.request('PUT', '/', None, {})
>>> resp = http_conn.response()
>>> http_conn.request('POST', '/', None, {})
>>> resp = http_conn.response()
>>> http_conn.request('TRACE', '/', None, {})
>>> resp = http_conn.response()
>>> http_conn.request('PATCH', '/', None, {})
>>> resp = http_conn.response()

```

### Get response

```python
>>> http_conn.request('GET', '/', None, {})
>>> resp = http_conn.response()
>>> resp.content
'index'

```

### Get response for TRACE method

_Note_: at the moment HTTP method TRACE is not supported by test server

```python
>>> http_conn.request('TRACE', '/', None, {})
>>> resp = http_conn.response()
>>> len(resp.headers) > 0
True
>>> len(resp.content) > 0
True

```



