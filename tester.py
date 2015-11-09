#!/bin/python3
import glob
import logging
import threading
import os

import Crawler
import sync_utils
import sys

# level=CRITICAL, ERROR, WARNING,INFO, DEBUG, NOTSET
logging.basicConfig(level=logging.ERROR, format='(%(threadName)-10s) %(message)s',)

# remove old cookies
files = glob.glob('cookies/*')
for f in files:
    os.remove(f)

thread_count = 3
all_threads = []

for i in range(thread_count):
    thread = Crawler.Crawler(i)
    thread.verbose = True
    thread.start()
    all_threads.append(thread)
    if not sync_utils.synchronized_start:
        thread.join()
        print('Total response time: %f' % thread.responseTimes)
        sys.stdout.flush()

if sync_utils.synchronized_start:
    sync_utils.barrier.acquire()
    sync_utils.running = True
    sync_utils.barrier.notify_all()
    sync_utils.barrier.release()
    for thread in all_threads:
        thread.join()
        print('Total response time: %f' % thread.responseTimes)
        sys.stdout.flush()

