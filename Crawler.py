import threading
import logging
import pycurl
from os.path import devnull


class Crawler(threading.Thread):

    def __init__(self):
        super(Crawler, self).__init__()
        self.c = pycurl.Curl()
        self.login_string = "krokiet"
        self.password_string = "pkpk11"

    def run(self):
        self.init()
        self.login()
        self.page("flat")
        self.logout()
        return

    def init(self):
        self.c.setopt(self.c.COOKIEFILE, 'cookies.txt')
        self.c.setopt(self.c.COOKIEJAR, 'cookies.txt')
        return

    def login(self):
        logging.debug('trying to login')
        self.c.setopt(self.c.URL, 'http://piotrkomar.pl/HelloWorld/login')
        self.c.setopt(self.c.POSTFIELDS, 'login='+self.login_string+'&password='+self.password_string)
        self.c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
        self.c.perform()
        self.print_response()
        return

    def logout(self):
        logging.debug('trying to logout')
        self.c.setopt(self.c.URL, 'http://piotrkomar.pl/HelloWorld/logout')
        self.c.perform()
        self.print_response()
        return

    def page(self, page):
        logging.debug('trying to acces '+page)
        self.c.setopt(self.c.URL, 'http://piotrkomar.pl/HelloWorld/'+page)
        self.c.perform()
        self.print_response()
        return

    def print_response(self):
        print('Status: %d' % self.c.getinfo(self.c.RESPONSE_CODE))
        print('Response time: %f' % self.c.getinfo(self.c.TOTAL_TIME))
        return
