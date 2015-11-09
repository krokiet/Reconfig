import threading
import logging
import pycurl
import random


class Crawler(threading.Thread):
    def __init__(self):
        super(Crawler, self).__init__()
        self.c = pycurl.Curl()
        self.responseTimes = 0
        self.verbose = False
        self.login_string = "krokiet"
        self.password_string = "pkpk11"
        self.pages = ['home', 'accountManagement', 'flat', 'mailbox', 'about', 'aboutFlat', 'aboutMoney',
                      'aboutChores']

    def run(self):
        self.init()
        self.login()
        # self.page("flat")
        self.crawl(20)
        self.logout()
        return

    def init(self):
        self.c.setopt(self.c.COOKIEFILE, 'cookies.txt')
        self.c.setopt(self.c.COOKIEJAR, 'cookies.txt')
        return

    def login(self):
        logging.debug('trying to login')
        self.c.setopt(self.c.URL, 'http://piotrkomar.pl/HelloWorld/login')
        self.c.setopt(self.c.POSTFIELDS, 'login=' + self.login_string + '&password=' + self.password_string)
        self.c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
        self.c.perform()
        self.handle_response()
        return

    def logout(self):
        logging.debug('trying to logout')
        self.c.setopt(self.c.URL, 'http://piotrkomar.pl/HelloWorld/logout')
        self.c.perform()
        self.handle_response()
        return

    def crawl(self, jumps):
        for i in range(1, jumps):
            self.page(random.choice(self.pages))

        return

    def page(self, page):
        logging.debug('trying to acces ' + page)
        self.c.setopt(self.c.URL, 'http://piotrkomar.pl/HelloWorld/' + page)
        self.c.perform()
        self.handle_response()
        return

    def handle_response(self):
        self.responseTimes += self.c.getinfo(self.c.TOTAL_TIME)
        if self.verbose:
            print('Status: %d' % self.c.getinfo(self.c.RESPONSE_CODE))
            print('Response time: %f' % self.c.getinfo(self.c.TOTAL_TIME))
        return
