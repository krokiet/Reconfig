#!/bin/python3
import glob
import logging
import os
import Crawler
import sync_utils
import statistics
import sys
import ddoser
from time import sleep

# level=CRITICAL, ERROR, WARNING,INFO, DEBUG, NOTSET
logging.basicConfig(level=logging.ERROR, format='(%(threadName)-10s) %(message)s',)


def clear_cookies():
    files = glob.glob('cookies/*')
    for f in files:
        os.remove(f)

print("\n\n\n 400 users, 20 times login -logout, inserted with varying frequency \n\n\n")

# timed_users
def test1():
    for num_of_users_per_sec in [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]:
        number_of_runs = 1

        all_threads = []
        for run in range(number_of_runs):
            clear_cookies()
            thread_count = 400
            cut_length = int(0.1 * thread_count)

            if sync_utils.synchronized_start:
                sync_utils.barrier.acquire()
                sync_utils.running = True
                sync_utils.barrier.notify_all()
                sync_utils.barrier.release()

            for i in range(thread_count):
                sleep(1.0 / num_of_users_per_sec * i)
                thread = ddoser.ddoser(i, 20)
                thread.start()
                all_threads.append(thread)

            for thread in all_threads:
                thread.join()

            sync_utils.running = False

        list_of_tuples = [item for sublist in [item.responses for item in all_threads] for item in sublist]
        if cut_length != 0:
            list_of_tuples = list_of_tuples[cut_length:-cut_length]

        longest_time = max(list_of_tuples, key=lambda item: item[1])
        lowest_time = min(list_of_tuples, key=lambda item: item[1])
        mean_time = statistics.mean([item[1] for item in list_of_tuples])
        median_time = statistics.median([item[1] for item in list_of_tuples])
        std_deviation = statistics.stdev([item[1] for item in list_of_tuples])
        length = len(list_of_tuples)
        error_count = length - [item[0] for item in list_of_tuples].count('HTTP200')

        print('longest time: {0} lowest time: {1} mean time: {2} median time: {3} deviation: {4} numOf responses: {5} error count: {6} with {7} log-in, log-out x20 users inserted per second, 400 total users'
              .format(longest_time, lowest_time, mean_time, median_time, std_deviation, length, error_count, num_of_users_per_sec))
        sys.stdout.flush()
test1()

print("\n\n\n crawl x20 \n\n\n")

# parallel crawling
def test2():
    for num_of_users in [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400]:
        number_of_runs = 1

        all_threads = []
        for run in range(number_of_runs):
            clear_cookies()
            thread_count = num_of_users
            cut_length = int(0.1 * thread_count)

            for i in range(thread_count):
                thread = Crawler.Crawler(i, 20)
                thread.start()
                all_threads.append(thread)

            if sync_utils.synchronized_start:
                sync_utils.barrier.acquire()
                sync_utils.running = True
                sync_utils.barrier.notify_all()
                sync_utils.barrier.release()

            for thread in all_threads:
                thread.join()

            sync_utils.running = False

        list_of_tuples = [item for sublist in [item.responses for item in all_threads] for item in sublist]
        if cut_length != 0:
            list_of_tuples = list_of_tuples[cut_length:-cut_length]

        longest_time = max(list_of_tuples, key=lambda item: item[1])
        lowest_time = min(list_of_tuples, key=lambda item: item[1])
        mean_time = statistics.mean([item[1] for item in list_of_tuples])
        median_time = statistics.median([item[1] for item in list_of_tuples])
        std_deviation = statistics.stdev([item[1] for item in list_of_tuples])
        length = len(list_of_tuples)
        error_count = length - [item[0] for item in list_of_tuples].count('HTTP200')

        print('longest time: {0} lowest time: {1} mean time: {2} median time: {3} deviation: {4} numOf responses: {5} error count: {6} with {7} 20-times crawling users'
              .format(longest_time, lowest_time, mean_time, median_time, std_deviation, length, error_count, num_of_users))
        sys.stdout.flush()
test2()

print("\n\n\n login - logout x100 \n\n\n")

# parallel login
def test3():
    for num_of_users in [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400]:
        number_of_runs = 1

        all_threads = []
        for run in range(number_of_runs):
            clear_cookies()
            thread_count = num_of_users
            cut_length = int(0.1 * thread_count)

            for i in range(thread_count):
                thread = ddoser.ddoser(i, 100)
                thread.start()
                all_threads.append(thread)

            if sync_utils.synchronized_start:
                sync_utils.barrier.acquire()
                sync_utils.running = True
                sync_utils.barrier.notify_all()
                sync_utils.barrier.release()

            for thread in all_threads:
                thread.join()

            sync_utils.running = False

        list_of_tuples = [item for sublist in [item.responses for item in all_threads] for item in sublist]
        if cut_length != 0:
            list_of_tuples = list_of_tuples[cut_length:-cut_length]

        longest_time = max(list_of_tuples, key=lambda item: item[1])
        lowest_time = min(list_of_tuples, key=lambda item: item[1])
        mean_time = statistics.mean([item[1] for item in list_of_tuples])
        median_time = statistics.median([item[1] for item in list_of_tuples])
        std_deviation = statistics.stdev([item[1] for item in list_of_tuples])
        length = len(list_of_tuples)
        error_count = length - [item[0] for item in list_of_tuples].count('HTTP200')

        print('longest time: {0} lowest time: {1} mean time: {2} median time: {3} deviation: {4} numOf responses: {5} error count: {6} with {7} logging in logging out x100 users'
              .format(longest_time, lowest_time, mean_time, median_time, std_deviation, length, error_count, num_of_users))
        sys.stdout.flush()
test3()



