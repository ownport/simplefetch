# Using threads with simplefetch

There's no thread in support in simplefetch library. To run many request in parallel you will need to use 
standard python module - thread

For testing threads you need to use asynchttpsrv.py as test server. It's support multiple connections

Example: get HTTP status of urls (without threads)

```python
>>> urls = ['http://www.google.com', 'http://www.yahoo.com', 'http://www.yandex.ru', 'http://www.blogger.com/',
...     'http://www.python.org/', 'http://sourceforge.net/', 'http://www.ubuntu.com/', 'http://www.readwriteweb.com/',
...     'http://gigaom.com/', 'http://www.wired.com/',]
>>>
>>> import sys
>>> import datetime
>>> import simplefetch
>>> def worker(url):
...     resp = simplefetch.get(url)
...
>>> now = datetime.datetime.now()
>>> for url in urls:
...     worker(url)
>>> no_threads_time = datetime.datetime.now() - now

```

Example: get HTTP status of urls (with threads)

```python
>>> import Queue
>>> import threading
>>>
>>> def worker():
...     while True:
...         url = q.get()
...         resp = simplefetch.get(url)
...         q.task_done()
...
>>> now = datetime.datetime.now()
>>>
>>> q = Queue.Queue()
>>> total_threads = 5
>>>
>>> for url in urls: q.put(url)
>>>
>>> for i in range(total_threads):
...     t = threading.Thread(target=worker)
...     t.setDaemon(True)
...     t.start()
...
>>> q.join()
>>>
>>> threads_time = datetime.datetime.now() - now
>>> print no_threads_time, threads_time
>>>
>>> no_threads_time > threads_time
True

```
As you can see from the code below the duration of execution requests with no threads and 
with threads is different. On my laptop it's 8 times faster with threads than no threads.

### Links

 * [threading – Manage concurrent threads](http://www.doughellmann.com/PyMOTW/threading/)
