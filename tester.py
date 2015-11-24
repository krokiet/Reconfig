#!/bin/python3
import glob
import logging
import os
import Crawler
import timed_user
import sync_utils

# level=CRITICAL, ERROR, WARNING,INFO, DEBUG, NOTSET
logging.basicConfig(level=logging.ERROR, format='(%(threadName)-10s) %(message)s',)


def clear_cookies():
    files = glob.glob('cookies/*')
    for f in files:
        os.remove(f)


# timed_users
def test1():
    for num_of_users_per_sec in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 200]:
        number_of_runs = 5
        total_mean_response_time = 0
        total_longest_response_time = ('', 0)
        total_lowest_response_time = ('', 123456789)

        for run in range(number_of_runs):
            clear_cookies()
            thread_count = num_of_users_per_sec
            cut_length = int(0.1 * thread_count)
            all_threads = []

            for i in range(thread_count):
                thread = timed_user.timed_user(i, 1/num_of_users_per_sec * i)
                thread.start()
                all_threads.append(thread)

            if sync_utils.synchronized_start:
                sync_utils.barrier.acquire()
                sync_utils.running = True
                sync_utils.barrier.notify_all()
                sync_utils.barrier.release()

            for thread in all_threads:
                thread.join()

            list_of_tuples = [item for sublist in [item.responses for item in all_threads] for item in sublist]
            if cut_length != 0:
                list_of_tuples = list_of_tuples[cut_length:-cut_length]

            longest_response_time = max(list_of_tuples, key=lambda item: item[1])
            if longest_response_time[1] > total_longest_response_time[1]:
                total_longest_response_time = longest_response_time
            lowest_response_time = min(list_of_tuples, key=lambda item: item[1])
            if lowest_response_time[1] < total_lowest_response_time[1]:
                total_lowest_response_time = lowest_response_time
            mean_response_time = float(sum(y for x, y in list_of_tuples)) / max(len(list_of_tuples), 1)
            total_mean_response_time += mean_response_time

            sync_utils.running = False

        total_mean_response_time /= number_of_runs
        print('Longest response time: {0}s, Lowest response time: {1}s Mean response time: {2}s with {3} instant log-in, log-out users introduced per second'
              .format(total_longest_response_time, total_lowest_response_time, total_mean_response_time, num_of_users_per_sec))
test1()


# parallel crawling
def test2():
    for num_of_users in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]:
        number_of_runs = 5
        total_mean_response_time = 0
        total_longest_response_time = ('', 0)
        total_lowest_response_time = ('', 123456789)

        for run in range(number_of_runs):
            clear_cookies()
            thread_count = num_of_users
            cut_length = int(0.1 * thread_count)
            all_threads = []

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

            list_of_tuples = [item for sublist in [item.responses for item in all_threads] for item in sublist]
            if cut_length != 0:
                list_of_tuples = list_of_tuples[cut_length:-cut_length]

            longest_response_time = max(list_of_tuples, key=lambda item: item[1])
            if longest_response_time[1] > total_longest_response_time[1]:
                total_longest_response_time = longest_response_time
            lowest_response_time = min(list_of_tuples, key=lambda item: item[1])
            if lowest_response_time[1] < total_lowest_response_time[1]:
                total_lowest_response_time = lowest_response_time
            mean_response_time = float(sum(y for x, y in list_of_tuples)) / max(len(list_of_tuples), 1)
            total_mean_response_time += mean_response_time

            sync_utils.running = False

        total_mean_response_time /= number_of_runs
        print('Longest response time: {0}s, Lowest response time: {1}s Mean response time: {2}s with {3} crawling users'
              .format(total_longest_response_time, total_lowest_response_time, total_mean_response_time, num_of_users))
test2()


# parallel login
def test3():
    for num_of_users in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 200]:
        number_of_runs = 5
        total_mean_response_time = 0
        total_longest_response_time = ('', 0)
        total_lowest_response_time = ('', 123456789)

        for run in range(number_of_runs):
            clear_cookies()
            thread_count = num_of_users
            cut_length = int(0.1 * thread_count)
            all_threads = []

            for i in range(thread_count):
                thread = Crawler.Crawler(i, 0)
                thread.start()
                all_threads.append(thread)

            if sync_utils.synchronized_start:
                sync_utils.barrier.acquire()
                sync_utils.running = True
                sync_utils.barrier.notify_all()
                sync_utils.barrier.release()

            for thread in all_threads:
                thread.join()

            list_of_tuples = [item for sublist in [item.responses for item in all_threads] for item in sublist]
            if cut_length != 0:
                list_of_tuples = list_of_tuples[cut_length:-cut_length]

            longest_response_time = max(list_of_tuples, key=lambda item: item[1])
            if longest_response_time[1] > total_longest_response_time[1]:
                total_longest_response_time = longest_response_time
            lowest_response_time = min(list_of_tuples, key=lambda item: item[1])
            if lowest_response_time[1] < total_lowest_response_time[1]:
                total_lowest_response_time = lowest_response_time
            mean_response_time = float(sum(y for x, y in list_of_tuples)) / max(len(list_of_tuples), 1)
            total_mean_response_time += mean_response_time

            sync_utils.running = False

        total_mean_response_time /= number_of_runs
        print('Longest response time: {0}s, Lowest response time: {1}s Mean response time: {2}s with {3} instant log-in, log-out users'
              .format(total_longest_response_time, total_lowest_response_time, total_mean_response_time, num_of_users))
test3()



