import Connector
import random
import logging


class Crawler(Connector.Connector):

    def __init__(self, thread_id, crawling_steps):
        super(Crawler, self).__init__(thread_id)
        self.crawling_steps = crawling_steps

    def run(self):
        super(Crawler, self).run()
        self.login()
        self.crawl()
        self.logout()
        logging.debug('All responses: {1}'.format(self.thread_id, self.responses))
        return

    def crawl(self):
        for i in range(1, self.crawling_steps):
            self.visit_page(random.choice(self.pages))
            sleep(0.5 + random.uniform(0, 2))
        return
