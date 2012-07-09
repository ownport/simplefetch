# SimpleFetch (generic) specification

## Introduction

SimpleFetch is a python module for downloading content (HEAD, GET methods) but another HTTP methods are supported as well. To use Simpleetch, you will need Python 2.6 or later (Python 3 is not tested yet). Simplefetch is not meant to run standalone; it is a module for you to use as part of a larger Python program.

Simplefetch is easy to use; the module is self-contained in a single file, simplefetch.py, and it has several functions for making different HTTP requests. 

Simplefetch code is adapted, simplified, refactored part of the next libraries: 
 - [Universal Feed Parser project](http://packages.python.org/feedparser/). 
 - [lyxint/urlfetch](https://github.com/lyxint/urlfetch)
 - [kennethreitz/requests](https://github.com/kennethreitz/requests)
 - [shazow/urllib3](https://github.com/shazow/urllib3)

## Testing

This file is specification but it is doctest for simplefetch library as well. To run tests 
```sh
$ python -m doctest -v tests/specs.md
```

Before running doctests the test server should be up and running
```sh
$ python tests/server.py
```

The test server can be started as service/daemon (not implemented yet)
```sh
$ python tests/server.py -d -l tests/server.log
```

## Simple usage

### GET method

The simplest way to get a web page 

```python
>>> import simplefetch
>>> resp = simplefetch.get("http://localhost:8800")
>>> type(resp)
<class 'simplefetch.Response'>

```
as result, the variable "resp" is Response object. All information like headers or content of this request we can get it from this object.

### POST method

To make simple POST request just use

```python
>>> resp = simplefetch.post("http://localhost:8800")
>>> type(resp)
<class 'simplefetch.Response'>

```

### HEAD, PUT, DELETE, OPTIONS and TRACE methods

Another HTTP requests are also very simple

```python
>>> resp = simplefetch.head("http://localhost:8800")
>>> type(resp)
<class 'simplefetch.Response'>

>>> resp = simplefetch.put("http://localhost:8800")
>>> type(resp)
<class 'simplefetch.Response'>

>>> resp = simplefetch.delete("http://localhost:8800")
>>> type(resp)
<class 'simplefetch.Response'>

>>> resp = simplefetch.options("http://localhost:8800")
>>> type(resp)
<class 'simplefetch.Response'>

>>> resp = simplefetch.trace("http://localhost:8800")
>>> type(resp)
<class 'simplefetch.Response'>

```

### Request (universal method for all HTTP requests) 

In case GET method the request will be the next

```python
>>> resp = simplefetch.request(method="GET", url="http://localhost:8800")
>>>
```

```python
def request(url, method="GET", data=None, headers={}, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
            files={}, length_limit=None, proxy = None):
            
    ''' request an URL
    
    method: HTTP method, one of HEAD, GET, POST, DELETE,  OPTIONS, PUT, TRACE. GET is used by default.
    url: URL to be requested.
    headers: HTTP request headers
    timeout: timeout in seconds, socket._GLOBAL_DEFAULT_TIMEOUT by default
    files: files to be sended
    length_limit: if None, no limits on content length, if the limit reached raised ContentLengthLimitException 
    
    returns Response object
    '''
```


### User-Agent usage (default)

```python
>>> resp = simplefetch.get("http://localhost:8800")
>>>
```

### User-Agent usage (user specfic)

```python
>>> headers = { 'User-Agent': 'my-simplefetch/0.1', }
>>> resp = simplefetch.get("http://localhost:8800", headers=headers)
>>>
```

### Basic Authentication
```python
>>>
>>>
```


### Proxy support via HTTP_PROXY & HTTPS_PROXY environment variables

In case when HTTP\_PROXY HTTPS\_PROXY defined simplefetch can detect it automaticaly and 
used without any actions from users

```python
>>> resp = simplefetch.get("http://localhost:8800")
>>>
```

### Proxy support via fetch interface

```python
>>> resp = simplefetch.get("http://localhost:8800" , proxy={ 'http': 'http://127.0.0.1:8000', 'https': 'https://127.0.0.1:8000', })
>>>
```

## Advanced usage

### ETag and Last-Modified Headers

ETags and Last-Modified headers are two ways that content publishers can save bandwidth, but they only work if clients take advantage of them. UrlFetch gives you the ability to take advantage of these features, but you must use them properly.

The basic concept is that a content publisher may provide a special HTTP header, called an ETag, when it publishes a content. You should send this ETag back to the server on subsequent requests. If the content has not changed since the last time you requested it, the server will return a special HTTP status code (304) and no content data. For more information see HTTP ETag on [Wikipedia](http://en.wikipedia.org/wiki/HTTP_ETag)

### Using ETags headers to reduce bandwidth

There is a related concept which accomplishes the same thing, but slightly differently. In this case, the server publishes the last-modified date of the content in the HTTP header. You can send this back to the server on subsequent requests, and if the content has not changed, the server will return HTTP status code 304 and no content data.

```python
>>>
>>>
```


### Using Last-Modified headers to reduce bandwidth

```python
>>>
>>>
```

### Upload file

```python
>>>
>>>
```

