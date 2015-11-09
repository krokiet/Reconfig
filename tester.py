#!/bin/python3
import glob
import logging
import os

import Crawler

# level=CRITICAL, ERROR, WARNING,INFO, DEBUG, NOTSET
logging.basicConfig(level=logging.ERROR, format='(%(threadName)-10s) %(message)s',)

# remove old cookies
files = glob.glob('cookies/*')
for f in files:
    os.remove(f)

for i in range(2):
    thread = Crawler.Crawler(i)
    thread.start()
    thread.join()
    print('Total response time: %f' % thread.responseTimes)
