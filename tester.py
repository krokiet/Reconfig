import logging
import Crawler

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

for i in range(1):
    thread = Crawler.Crawler()
    thread.start()
