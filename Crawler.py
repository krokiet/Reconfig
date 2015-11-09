import threading
import logging
import pycurl


class Crawler(threading.Thread):

    def __init__(self):
        super(Crawler, self).__init__()
        self.c = pycurl.Curl()
        self.loginString = "krokiet"
        self.passwordString = "pkpk11"

    def run(self):
        self.login()
        self.logout()
        return

    def login(self):
        logging.debug('trying to login')
        self.c.setopt(self.c.URL, 'http://piotrkomar.pl/HelloWorld/login')
        self.c.setopt(self.c.POSTFIELDS, 'login='+self.loginString+'&password='+self.passwordString)
        self.c.setopt(self.c.COOKIEJAR, 'cookies.txt')
        self.c.perform()
        return

    def logout(self):
        logging.debug('trying to logout')
        self.c.setopt(self.c.URL, 'http://piotrkomar.pl/HelloWorld/logout')
        self.c.setopt(self.c.COOKIEFILE, 'cookies.txt')
        self.c.setopt(self.c.COOKIEJAR, 'cookies.txt')
        self.c.perform()
        return
