import Connector
import random
import logging
from time import sleep


class ddoser(Connector.Connector):

    def __init__(self, thread_id, relogin_steps):
        super(ddoser, self).__init__(thread_id)
        self.relogin_steps = relogin_steps

    def run(self):
        super(ddoser, self).run()
        self.ddos()
        logging.debug('All responses: {1}'.format(self.thread_id, self.responses))
        return

    def ddos(self):
        for i in range(self.relogin_steps):
            self.login()
            self.logout()
        return
