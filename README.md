simplefetch
===========

Simple HTTP library. Initially it was forked from [lyxint/urlfetch](https://github.com/lyxint/urlfetch) but now it's an independent project because of different internal architecture.


Example of usage aliases to GET method. 
```python
>>> import simplefetch
>>> resp  = simplefetch.get('http://devel.ownport.net')
>>> resp.headers
{ 'transfer-encoding': 'chunked', 'expires': 'Wed, 18 Jul 2012 04:58:49 GMT', 'server': 'GSE', 'last-modified': 'Wed, 11 Jul 2012 05:51:27 GMT', 'connection': 'Keep-Alive', 'etag': '"1fc3cfe5-7483-4765-8f67-eee40b813abc"', 'cache-control': 'private, max-age=0', 'date': 'Wed, 18 Jul 2012 04:58:49 GMT', 'content-type': 'text/html; charset=UTF-8' }
>>> len(resp.content)
86641
```

Making few requests to one host without re-establishing new connection
```python
>>> conn = simplefetch.Connection(scheme='http', host='devel.ownport.net')
>>> conn.request('GET', '/', None, {} )
>>> resp = conn.response()
>>> resp.headers
{'transfer-encoding': 'chunked', 'expires': 'Wed, 18 Jul 2012 05:11:54 GMT', 'server': 'GSE', 'last-modified': 'Wed, 11 Jul 2012 05:51:27 GMT', 'connection': 'Keep-Alive', 'etag': '"1fc3cfe5-7483-4765-8f67-eee40b813abc"', 'cache-control': 'private, max-age=0', 'date': 'Wed, 18 Jul 2012 05:11:54 GMT', 'content-type': 'text/html; charset=UTF-8'}
>>> len(resp.content)
86641
>>> conn.request('GET', '/search/label/python', None, {} )
>>> resp = conn.response()
>>> resp.headers
{'transfer-encoding': 'chunked', 'expires': 'Wed, 18 Jul 2012 05:21:02 GMT', 'server': 'GSE', 'last-modified': 'Wed, 11 Jul 2012 05:51:27 GMT', 'connection': 'Keep-Alive', 'etag': '"1fc3cfe5-7483-4765-8f67-eee40b813abc"', 'cache-control': 'private, max-age=0', 'date': 'Wed, 18 Jul 2012 05:21:02 GMT', 'content-type': 'text/html; charset=UTF-8'}
>>> len(resp.content)
127584
```

Using custom headers
```python
>>> simplefetch.get('http://devel.ownport.net', headers={'User-Agent': 'simplefetch/0.3.2'})
```

Using custom headers (via Headers class)
```python
>>> headers = simplefetch.Headers()
>>> headers.basic_auth('username', 'password')
>>> simplefetch.get('http://www.example.com', headers=headers.items())
```

Automatic proxy support

```python
>>> conn = simplefetch.get('http://devel.ownport.net')
>>> resp = conn.response()
>>> resp.headers
{'via': '1.1 PROXY', 'proxy-connection': 'Keep-Alive', 'x-content-type-options': 'nosniff', 'transfer-encoding': 'chunked', 'expires': 'Wed, 18 Jul 2012 05:37:59 GMT', 'server': 'GSE', 'last-modified': 'Wed, 11 Jul 2012 05:51:27 GMT', 'connection': 'Keep-Alive', 'etag': '"1fc3cfe5-7483-4765-8f67-eee40b813abc"', 'cache-control': 'private, max-age=0', 'date': 'Wed, 18 Jul 2012 05:37:59 GMT', 'content-type': 'text/html; charset=UTF-8', 'x-xss-protection': '1; mode=block'}
>>> len(resp.content)
86641
```
or via Connection class
```python
>>> conn = simplefetch.Connection(scheme='http')
>>> conn.request('GET', 'http://devel.ownport.net', None, {} )
>>> resp = conn.response()
>>> resp.headers
{'via': '1.1 PROXY, 'proxy-connection': 'Keep-Alive', 'x-content-type-options': 'nosniff', 'transfer-encoding': 'chunked', 'expires': 'Wed, 18 Jul 2012 05:37:59 GMT', 'server': 'GSE', 'last-modified': 'Wed, 11 Jul 2012 05:51:27 GMT', 'connection': 'Keep-Alive', 'etag': '"1fc3cfe5-7483-4765-8f67-eee40b813abc"', 'cache-control': 'private, max-age=0', 'date': 'Wed, 18 Jul 2012 05:37:59 GMT', 'content-type': 'text/html; charset=UTF-8', 'x-xss-protection': '1; mode=block'}
>>> len(resp.content)
86641
```

## Specifications (doctests)

 * [Class Connection](https://github.com/ownport/simplefetch/blob/master/tests/connection.md)
 * [Helpers](https://github.com/ownport/simplefetch/blob/master/tests/helpers.md)
 * [Proxy](https://github.com/ownport/simplefetch/blob/master/tests/proxy.md)


## TODO

 * sometimes encoding format coming from server in wrong format, make mapping known errors
 * handling exceptions for h.request/h.response
 * non-blocking thread-safe 
 * working in Pool

