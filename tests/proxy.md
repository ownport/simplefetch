# Proxy

Before running these examples HTTP_PROXY and HTTPS_PROXY should be defined in your system

```sh
export http_proxy=http://127.0.0.1:8800
export https_proxy=https://<proxy_server>:<port>
```
HTTPS_PROXY is not defined as test server is not support this type of connection at the moment

Connect to server devel.ownport.net via Connection class. When system environment variables 
(HTTP_PROXY,HTTPS_PROXY) defined in the system, Connection class detect it and used it for requests.

```python
>>> import simplefetch
>>> conn = simplefetch.Connection(scheme='http')
>>> conn.request('GET', 'http://www.example.com', None, {})
>>> resp = conn.response()
>>> resp.status
200
>>> len(resp.content) > 0
True

```

More simple way to make GET request is use get() alias. It will make the same operations as described above.

```python
>>> resp = simplefetch.get('http://www.example.com')
>>> resp.status
200
>>> len(resp.content) > 0
True

```

HTTPS proxy is used but due to the issue https://github.com/ownport/simplefetch/issues/1 it's not working properly.

```python
>>> resp = simplefetch.get('https://github.com')
>>> resp.status
200
>>> len(resp.content) > 0
True

```
