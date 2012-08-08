#!/usr/bin/env python
#
#   Pool (Example)
#
#   Links:
#   http://www.doughellmann.com/PyMOTW/threading/
#   http://docs.python.org/library/threading.html
#

if __name__ == '__main__':
    ''' main '''    

    from gevent.pool import Pool
    from gevent import monkey
    monkey.patch_socket()
    
    import time
    import simplefetch
    
    urls = (
        'http://www.google.com', 'http://www.bigmir.net/', 'http://korrespondent.net/',
        'http://vcene.ua/', 'http://www.liveinternet.ru/', 'http://lifehacker.com/',
        'http://gizmodo.com', 'http://www.flickr.com', 'http://en.wikipedia.org',
        'http://www.officesnapshots.com', 'http://instagr.am', 'http://www.deskography.org',
        'http://www.blogger.com', 'http://www.youtube.com', 'http://itunes.apple.com',
        'http://www.amazon.com', 'http://www.bbc.co.uk', 'http://www.logitech.com',
        'http://ru.wikipedia.org', 'http://habrahabr.ru', 'http://www.ibm.com',
        'http://www.python.org', 'http://citforum.ru', 'http://code.activestate.com',
        'http://www.intuit.ru', 'http://code.google.com', 'http://www.djangoproject.com',
        'http://hadoop.apache.org', 'http://www.vmware.com', 'http://www.xen.org',
    )
    
    def fetch(url):
        resp = simplefetch.get(url)
        return (resp.headers, resp.content)

    # gevent 
    start_time = time.time()
    tasks = Pool(size=5)
    for url in urls:
        tasks.spawn(fetch, url)
    tasks.join()
    print 'gevent.time: %0.5f secs' % (time.time() - start_time)

    # sequential 
    start_time = time.time()
    for url in urls:
        fetch(url)
    print 'sequential.time: %0.5f secs' % (time.time() - start_time)


