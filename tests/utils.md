### Passing parameters in URL

Time to time is needed to send some sort of data in URL's query string. For this task better to use urlencode() function from standard Python library urllib.
```python
>>> import urllib
>>> urllib.urlencode({'key1': 'value1', 'key2': 'value2'})
'key2=value2&key1=value1'

```

to join query string with url
```python
>>> url = 'http://localhost:8800'
>>> urllib.urlencode({'key1': 'value1', 'key2': 'value2'})
'key2=value2&key1=value1'

```

