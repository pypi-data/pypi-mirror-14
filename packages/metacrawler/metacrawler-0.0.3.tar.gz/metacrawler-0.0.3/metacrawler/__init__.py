# coding=utf-8

import copy

import requests

from metacrawler.settings import Settings
from metacrawler.crawlers import Crawler


class Handler(object):

    """Handler control crawling process."""

    def __init__(self, crawlers=None):
        """Override initialization object.

        :param crawlers (optional): `dict` crawlers.
        """
        self.__crawlers = self._get_class_crawlers()
        for name, crawler in (crawlers or {}).items():
            assert isinstance(crawler, Crawler), (
                '`crawler` must be `Crawler` instances.'
            )
            self.__crawlers[name] = crawler

        self.session = getattr(self.__class__, 'session', requests.Session())
        self.settings = getattr(self.__class__, 'settings', Settings())
        self.__data = {}

    @property
    def data(self):
        """The data property."""
        return copy.deepcopy(self.__data)

    def _get_class_crawlers(self):
        """Get class crawlers.

        :returns: `dict` crawlers.
        """
        crawlers = {}

        for name, attribute in self.__class__.__dict__.items():
            if isinstance(attribute, Crawler):
                crawlers[name] = attribute

        return crawlers

    def before(self):
        """Any actions before start."""
        pass

    def start(self):
        """Start crawling."""
        self.before()

        for name, crawler in self.__crawlers.items():
            self.__data[name] = crawler.crawl()

        return self.data
