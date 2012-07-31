# Using threads with simplefetch

There's no thread in support in simplefetch library. To run many request in parallel you will need to use 
standard python module - thread

For testing threads you need to use asynchttpsrv.py as test server. It's support multiple connections

```
$ python tests/package/asynchttpsrv.py
HTTP Server ('127.0.0.1', 8800) is starting
```

Example: get HTTP status of urls (without threads)

```python
>>> import datetime
>>> import simplefetch
>>> def worker(i):
...     resp = simplefetch.get('http://127.0.0.1:8800')
...     if resp.status <> 200:
...         raise Exception('Unsuccessful request')
...
>>> total_threads = 10000
>>> now = datetime.datetime.now()
>>> for i in range(total_threads):
...     worker(i)
>>> no_threads_time = datetime.datetime.now() - now

```

Example: get HTTP status of urls (with threads)

```python
>>> import threading
>>> now = datetime.datetime.now()
>>> for i in range(total_threads):
...     t = threading.Thread(target=worker, args=(i,))
...     t.setDaemon(True)
...     t.start()
...
>>> main_thread = threading.currentThread()
>>> for t in threading.enumerate():
...     if t is main_thread:
...         continue
...     t.join()
>>> threads_time = datetime.datetime.now() - now
>>> print no_threads_time, threads_time
>>> no_threads_time > threads_time
True

```
As you can see from the code below the duration of execution requests with no threads and 
with threads is different. On my laptop it's 8 times faster with threads than no threads.

