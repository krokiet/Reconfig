import threading
import logging
import pycurl

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)


class MyThread(threading.Thread):
    def run(self):
        logging.debug('running')
        c = pycurl.Curl()
        c.setopt(c.URL, 'http://piotrkomar.pl/HelloWorld/flat')
        # c.setopt(c.POSTFIELDS, 'login=krokiet&password=pkpk11')
        # c.setopt(c.COOKIEJAR, 'cookies.txt')
        c.setopt(c.COOKIEFILE, 'cookies.txt')
        c.perform()

        return

for i in range(1):
    thread = MyThread()
    thread.start()
