# SimpleFecth specification

Simple HTTP client.

This file is specification but doctest for simplefetch library as well. To run tests 
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

