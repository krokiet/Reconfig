import threading
import logging
import pycurl
import sync_utils
import sys


class Connector(threading.Thread):
    pages = ['home', 'accountManagement', 'flat', 'mailbox', 'about', 'aboutFlat', 'aboutMoney', 'aboutChores']
    login_string = "krokiet"
    password_string = "pkpk11"
    address_base = '192.168.0.100'

    def __init__(self, thread_id):
        super(Connector, self).__init__()
        self.thread_id = thread_id
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.CONNECTTIMEOUT, 30)
        self.c.setopt(self.c.COOKIEFILE, 'cookies/cookies' + str(self.thread_id) + '.txt')
        self.c.setopt(self.c.COOKIEJAR, 'cookies/cookies' + str(self.thread_id) + '.txt')
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
        return

    def login(self):
        logging.debug('trying to login')
        self.c.setopt(self.c.URL, self.address_base + '/HelloWorld/login')
        self.c.setopt(self.c.POSTFIELDS, 'login=' + self.login_string + '&password=' + self.password_string)
        self.c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
        self.c.perform()
        self.handle_response()
        return

    def logout(self):
        logging.debug('trying to logout')
        self.c.setopt(self.c.URL, self.address_base + '/HelloWorld/logout')
        self.c.perform()
        self.handle_response()
        return

    def revisit_page(self, page, visits):
        for i in range(visits):
            self.visit_page(page)
        return

    def visit_page(self, page):
        logging.debug('trying to acces ' + page)
        self.c.setopt(self.c.URL, self.address_base + '/HelloWorld/' + page)
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
