# Class Proxy

The class Proxy allows to make easy requests via HTTP/S proxies

```python
>>> import simplefetch
>>> proxy = Proxy(http='http://127.0.0.1:8080', https='https://127.0.0.1:8080')
>>> proxy.http
'http://127.0.0.1:8080'
>>> proxy.https
'https://127.0.0.1:8080'
```

In case when http and https arguments are not defined Proxy try to get information from system environment, HTTP_PROXY and HTTPS_PROXY

```sh
$ export http_proxy=http://127.0.0.1:8080
$ export https_proxy=https://127.0.0.1:8080
```

```python
>>> proxy = Proxy()
>>> proxy.http
'http://127.0.0.1:8080'
>>> proxy.https
'https://127.0.0.1:8080'
```

The format of http and https arguments is "<scheme>://[<username>:<password>]@<host>:<port>/"

scheme - http or https
host - proxy hostname
port - proxy port
username - optional parameter, if login is required
password - optional parameter, if login is required


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

