## SimpleFecth specification

>>> import simplefetch
>>> resp = simplefetch.get("http://localhost:8080")
>>>

## GET method

>>> resp = simplefetch.get("http://localhost:8080")
>>>

## POST method

>>> resp = simplefetch.post("http://localhost:8080")
>>>

## HEAD method

>>> resp = simplefetch.head("http://localhost:8080")
>>>

## Fetch 

>>> resp = simplefetch.head("http://localhost:8080")
>>>

## User-Agent usage (default)

>>> resp = simplefetch.get("http://localhost:8080")
>>>

## User-Agent usage (user specfic)

>>> headers = { 'User-Agent': 'my-simplefetch/0.1', }
>>> resp = simplefetch.get("http://localhost:8080", headers=headers)
>>>

## Proxy support via HTTP_PROXY & HTTPS_PROXY environment variables

>>> resp = simplefetch.get("http://localhost:8080", 
            proxy={ 
                    'http': 'http://127.0.0.1:8000', 
                    'https': 'https://127.0.0.1:8000', 
                    }
)
>>>

## Proxy support via fetch interface

>>> resp = simplefetch.get("http://localhost:8080", 
            proxy={ 
                    'http': 'http://127.0.0.1:8000', 
                    'https': 'https://127.0.0.1:8000', 
                    }
)
>>>

