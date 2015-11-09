import threading
import logging
import pycurl


class Crawler(threading.Thread):

    def __init__(self):
        super(Crawler, self).__init__()
        self.c = pycurl.Curl()

    def run(self):
        self.login()

        return

    def login(self):
        logging.debug('trying to login')
        self.c.setopt(self.c.URL, 'http://piotrkomar.pl/HelloWorld/login')
        self.c.setopt(self.c.POSTFIELDS, 'login=krokiet&password=pkpk11')
        self.c.setopt(self.c.COOKIEJAR, 'cookies.txt')
        self.c.setopt(self.c.COOKIEFILE, 'cookies.txt')
        self.c.perform()
        return
