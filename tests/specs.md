## SimpleFecth specification
```python
>>> import simplefetch
>>> resp = simplefetch.get("http://localhost:8080")
>>>
```

## GET method

```python
>>> resp = simplefetch.get("http://localhost:8080")
>>>
```

## POST method

```python
>>> resp = simplefetch.post("http://localhost:8080")
>>>
```

## HEAD method

```python
>>> resp = simplefetch.head("http://localhost:8080")
>>>
```

## Fetch 

```python
>>> resp = simplefetch.head("http://localhost:8080")
>>>
```

## User-Agent usage (default)

```python
>>> resp = simplefetch.get("http://localhost:8080")
>>>
```

## User-Agent usage (user specfic)

```python
>>> headers = { 'User-Agent': 'my-simplefetch/0.1', }
>>> resp = simplefetch.get("http://localhost:8080", headers=headers)
>>>
```

## Proxy support via HTTP_PROXY & HTTPS_PROXY environment variables

In case when HTTP\_PROXY HTTPS\_PROXY defined simplefetch can detect it automaticaly and 
used without any actions from users

```python
>>> resp = simplefetch.get("http://localhost:8080")
>>>
```

## Proxy support via fetch interface

```python
>>> resp = simplefetch.get("http://localhost:8080" , proxy={ 'http': 'http://127.0.0.1:8000', 'https': 'https://127.0.0.1:8000', })
>>>
```


