# SimpleFecth specification

## Introduction

SimpleFetch is a python module for downloading content (HEAD, GET methods) but another HTTP methods are supported as well. To use Simpleetch, you will need Python 2.6 or later (Python 3 is not tested yet). Simplefetch is not meant to run standalone; it is a module for you to use as part of a larger Python program.

Simplefetch is easy to use; the module is self-contained in a single file, simplefetch.py, and it has several functions for making different HTTP requests. 

Simplefetch code is adapted, simplified, refactored part of the next libraries: 
 - [Universal Feed Parser project](http://packages.python.org/feedparser/). Some of the code and texts for documentation was taken from this project. 
 - [lyxint/urlfetch](https://github.com/lyxint/urlfetch)
 - [kennethreitz/requests](https://github.com/kennethreitz/requests)
 - [shazow/urllib3](https://github.com/shazow/urllib3)


## Testing

This file is specification but it is doctest for simplefetch library as well. To run tests 
```sh
$ python -m doctest -v tests/specs.md
```

## GET method

```python
>>> import simplefetch
>>> resp = simplefetch.get("http://localhost:8800")
>>>
```

## POST method

```python
>>> resp = simplefetch.post("http://localhost:8800")
>>>
```

## HEAD method

```python
>>> resp = simplefetch.head("http://localhost:8800")
>>>
```

## Fetch 

```python
>>> resp = simplefetch.request(method="GET", url="http://localhost:8800")
>>>
```

## User-Agent usage (default)

```python
>>> resp = simplefetch.get("http://localhost:8800")
>>>
```

## User-Agent usage (user specfic)

```python
>>> headers = { 'User-Agent': 'my-simplefetch/0.1', }
>>> resp = simplefetch.get("http://localhost:8800", headers=headers)
>>>
```

## Basic Authentication
```python
>>>
>>>
```


## Proxy support via HTTP_PROXY & HTTPS_PROXY environment variables

In case when HTTP\_PROXY HTTPS\_PROXY defined simplefetch can detect it automaticaly and 
used without any actions from users

```python
>>> resp = simplefetch.get("http://localhost:8800")
>>>
```

## Proxy support via fetch interface

```python
>>> resp = simplefetch.get("http://localhost:8800" , proxy={ 'http': 'http://127.0.0.1:8000', 'https': 'https://127.0.0.1:8000', })
>>>
```

## Upload file

```python
>>>
>>>
```

