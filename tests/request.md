# Class Request

This class is used to prepare parameters before send request to server. Only URL parameter is mandatory. If method is not defined by default will be used GET method.

```python
>>> import simplefetch
>>> req = Request(url)
>>> 
```

```python
Request(url, method="GET", timeout=socket._GLOBAL_DEFAULT_TIMEOUT, proxy=None):
    ''' initial definitions 
        
    url:        URL to be requested
    method:     HTTP method, one of HEAD, GET, POST, DELETE,  OPTIONS, PUT, TRACE. GET is used by default.
    timeout:    timeout in seconds, socket._GLOBAL_DEFAULT_TIMEOUT by default
    proxy:      http/https proxy parameters. if None, it will be checked system environment HTTP/S_PROXY
                parameters. Example of defined proxy parameters: 
                proxy = {'http': 'http://192.168.1.1:8800', 'https': 'http://192.168.1.1:8800'}
    '''
```

For sending request you need to use send() method
```python
>>> req = Request(url)
>>> resp = req.send()
```
as result Response object will be returned


### Proxy (how to use it with httplib)

Example of usage proxy with httplib

To get HTTP/S_PROXY details from environment

```python
import os
_env = dict((k.lower(),v) for k,v in os.environ.items())
http_proxy = _env.get('http_proxy', None)
https_proxy = _env.get('https_proxy', None)

h1 = httplib.HTTPConnection(http_proxy, http_proxy_port)
h1.request("GET", "http://www.python.org/")

h1 = httplib.HTTPConnection(https_proxy, https_proxy_port)
h1.request("GET", "https://www.python.org/")
```
Note: host and port should be splitted for proxy

Links

 * (Using httplib through a Proxy)[http://www.pha.com.au/kb/index.php/Using_httplib_through_a_Proxy]
 * (simplest useful HTTPS with basic proxy authentication (Python recipe))[http://code.activestate.com/recipes/301740-simplest-useful-https-with-basic-proxy-authenticat/]

