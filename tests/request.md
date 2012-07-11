# Class Request

This class is used to prepare parameters before send request to server. Only URL parameter is mandatory. If method is not defined by default will be used GET method.

```python
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


