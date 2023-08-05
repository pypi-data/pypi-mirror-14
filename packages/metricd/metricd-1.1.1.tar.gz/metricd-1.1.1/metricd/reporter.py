import logging

import requests


class Reporter(object):
    def report(self, metrics):
        NotImplemented()


class HttpReporter(Reporter):
    hostname = None
    url = None
    headers = None
    logger = None

    def __init__(self, hostname, url, headers):
        self.hostname = hostname
        self.url = url
        self.headers = dict(headers.items() + {'X-Agent-Version': "1.1.1"}.items())
        self.logger = logging.getLogger('http-reporter')

    def report(self, metrics):
        try:
            response = requests.post(self.url, json=metrics,
                                     headers=self.headers, timeout=3)
            if response.status_code in [200, 201]:
                self.logger.info('Metrics sent successfully')
            else:
                self.logger.warn('Got unsuccesful http % response from server' % response.status_code)

        except requests.exceptions.RequestException as e:
            self.logger.error("An error occured when sending metrics: %s" % e.message)


class ConsoleReporter(Reporter):
    logger = None

    def __init__(self):
        self.logger = logging.getLogger('console-reporter')

    def report(self, metrics):
        for key, value in metrics.items():
            self.logger.info('%s: %s', key, value)
