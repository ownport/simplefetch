# Class Request

This class is used to prepare parameters before send request to server. Only URL parameter is mandatory. If method is not defined by default will be used GET method.

```python
>>> req = Request(url)
>>> 
```

```python
Request(url, method="GET", timeout=socket._GLOBAL_DEFAULT_TIMEOUT, length_limit=None)
```

For sending request you need to use send() function
```python
>>> req = Request(url)
>>> resp = req.send()
```
as result Response object will be returned


