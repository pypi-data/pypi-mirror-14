# coding=utf-8

import requests

from metacrawler.settings import Settings


class Handler(object):

    """Handler control crawling process."""

    def __init__(self, crawlers):
        """Override initialization object.

        :param crawlers: `dict` crawlers.
        """
        self.__crawlers = crawlers

        self.session = requests.Session()
        self.settings = Settings()
        self.data = {}

    def before(self):
        """Any actions before start."""
        pass

    def start(self):
        """Start crawling."""
        self.before()

        for name, crawler in self.__crawlers.items():
            self.data[name] = crawler.crawl()
        return self.data
