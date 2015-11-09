#!/bin/python3
import logging
import Crawler

# level=CRITICAL, ERROR, WARNING,INFO, DEBUG, NOTSET
logging.basicConfig(level=logging.ERROR, format='(%(threadName)-10s) %(message)s',)

for i in range(20):
    thread = Crawler.Crawler()
    thread.start()
    thread.join()
    print('Total response time: %f' % thread.total_response)
