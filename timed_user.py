import Connector
import random
import logging
from time import sleep


class timed_user(Connector.Connector):

    def __init__(self, thread_id, time_to_wait):
        super(timed_user, self).__init__(thread_id)
        self.time_to_wait = time_to_wait

    def run(self):
        super(timed_user, self).run()
        sleep(self.time_to_wait)
        self.login()
        self.logout()
        logging.debug('All responses: {1}'.format(self.thread_id, self.responses))
        return
