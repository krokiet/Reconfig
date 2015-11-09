import threading
import logging
import pycurl
import random
from time import sleep
import sync_utils

class Crawler(threading.Thread):
    def __init__(self, thread_id):
        super(Crawler, self).__init__()
        self.thread_id = thread_id
        self.c = pycurl.Curl()
        self.responseTimes = 0
        self.verbose = False
        self.login_string = "krokiet"
        self.password_string = "pkpk11"
        self.pages = ['home', 'accountManagement', 'flat', 'mailbox', 'about', 'aboutFlat', 'aboutMoney',
                      'aboutChores']


    def run(self):
        if sync_utils.synchronized_start:
            sync_utils.barrier.acquire()
            while not sync_utils.running:
                sync_utils.barrier.wait()
            sync_utils.barrier.release()
        self.init()
        self.login()
        # self.page("flat")
        # self.revisit_page(100, "flat")
        self.crawl(20)
        self.logout()
        return

    def init(self):
        self.c.setopt(self.c.COOKIEFILE, 'cookies/cookies'+str(self.thread_id)+'.txt')
        self.c.setopt(self.c.COOKIEJAR, 'cookies/cookies'+str(self.thread_id)+'.txt')
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
            self.visit_page(random.choice(self.pages))
            sleep(0.5+random.uniform(0, 2))
        return

    def revisit_page(self, page, visits):
        for i in range(1, visits):
            self.visit_page(page)
        return

    def visit_page(self, page):
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
