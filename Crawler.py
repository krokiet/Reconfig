import threading
import logging
import pycurl
import random
from time import sleep
import sync_utils
import sys


class Crawler(threading.Thread):
    pages = ['home', 'accountManagement', 'flat', 'mailbox', 'about', 'aboutFlat', 'aboutMoney', 'aboutChores']
    login_string = "krokiet"
    password_string = "pkpk11"

    def __init__(self, thread_id):
        super(Crawler, self).__init__()
        self.thread_id = thread_id
        self.c = pycurl.Curl()
        self.responses = []
        self.error_count = 0

    def conditionally_wait(self):
        if sync_utils.synchronized_start:
            sync_utils.barrier.acquire()
            while not sync_utils.running:
                sync_utils.barrier.wait()
            sync_utils.barrier.release()

    def run(self):
        self.conditionally_wait()
        self.init()
        self.login()
        # self.page("flat")
        # self.revisit_page(100, "flat")
        self.crawl(5)
        self.logout()
        logging.debug('All responses: {1}'.format(self.thread_id, self.responses))
        return

    def init(self):
        self.c.setopt(self.c.COOKIEFILE, 'cookies/cookies' + str(self.thread_id) + '.txt')
        self.c.setopt(self.c.COOKIEJAR, 'cookies/cookies' + str(self.thread_id) + '.txt')
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
            sleep(0.5 + random.uniform(0, 2))
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
        self.responses.append(('HTTP' + str(self.c.getinfo(self.c.RESPONSE_CODE)), self.c.getinfo(self.c.TOTAL_TIME)))
        if self.c.getinfo(self.c.RESPONSE_CODE) != 200:
            self.error_count += 1
        logging.debug('Status: {1}'.format(self.thread_id, self.c.getinfo(self.c.RESPONSE_CODE)))
        logging.debug('Response time: {1}'.format(self.thread_id, self.c.getinfo(self.c.TOTAL_TIME)))
        return
