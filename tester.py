#!/bin/python3
import logging
import threading
import Crawler

# level=CRITICAL, ERROR, WARNING,INFO, DEBUG, NOTSET
logging.basicConfig(level=logging.ERROR, format='(%(threadName)-10s) %(message)s',)

barrier = threading.Condition()
running = False

for i in range(20):
    thread = Crawler.Crawler()
    thread.start()
    thread.join()
    print('Total response time: %f' % thread.responseTimes)

barrier.acquire()
running = True
barrier.notify_all()
barrier.release()
