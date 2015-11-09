#!/bin/python3
import glob
import logging
import os
import Crawler
import sync_utils

# level=CRITICAL, ERROR, WARNING,INFO, DEBUG, NOTSET
logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

# remove old cookies
files = glob.glob('cookies/*')
for f in files:
    os.remove(f)

thread_count = 15
all_threads = []

for i in range(thread_count):
    thread = Crawler.Crawler(i)
    thread.verbose = True
    thread.start()
    all_threads.append(thread)
    if not sync_utils.synchronized_start:
        thread.join()

if sync_utils.synchronized_start:
    sync_utils.barrier.acquire()
    sync_utils.running = True
    sync_utils.barrier.notify_all()
    sync_utils.barrier.release()
    for thread in all_threads:
        thread.join()

for thread in all_threads:
    thread.join()

full_time_taken = sum(map(lambda x: thread.responseTimes, all_threads))
longest_response_time = max(map(lambda x: thread.responseTimes, all_threads))

print('Time fully spent on querying server: {0}s, longest response time: {1}s'.format(full_time_taken, longest_response_time))
