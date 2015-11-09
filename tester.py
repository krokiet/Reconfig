#!/bin/python3
import logging
import Crawler

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

for i in range(20):
    thread = Crawler.Crawler()
    thread.start()
