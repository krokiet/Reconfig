#!/bin/python3
import glob
import logging
import os
import Crawler
import sync_utils

# level=CRITICAL, ERROR, WARNING,INFO, DEBUG, NOTSET
logging.basicConfig(level=logging.ERROR, format='(%(threadName)-10s) %(message)s',)

# remove old cookies
number_of_runs = 5
total_mean_response_time = 0
total_longest_response_time = 0
for run in range(1, number_of_runs+1):
    files = glob.glob('cookies/*')
    for f in files:
        os.remove(f)
    cut_length = 4
    thread_count = 20
    all_threads = []

    for i in range(thread_count):
    thread = Crawler.Crawler(i, 50)
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

    list_of_tuples = [item for sublist in [item.responses for item in all_threads] for item in sublist]
    list_of_tuples = list_of_tuples[cut_length:-cut_length]

    print(list_of_tuples)

    longest_response_time = max(list_of_tuples, key=lambda item:item[1])
    if longest_response_time > total_longest_response_time:
        total_longest_response_time = longest_response_time
    mean_response_time = float(sum(y for x, y in list_of_tuples))/max(len(list_of_tuples), 1)
    total_mean_response_time += mean_response_time
    print('Longest response time: {0}s, Mean response time: {1}s in {2} run'
      .format(longest_response_time, mean_response_time, run))

total_mean_response_time /= number_of_runs
print('Longest response time: {0}s, Mean response time: {1}s in {2} runs'
      .format(total_longest_response_time, total_mean_response_time, number_of_runs))
