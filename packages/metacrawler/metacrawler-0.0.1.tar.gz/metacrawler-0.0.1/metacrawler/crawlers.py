# coding=utf-8

import requests
from lxml import html

class Crawler(object):

    """Crawler parse page use items as rules. May be nested."""

    def __init__(self, url, items, crawlers=None, session=None):
        """Override initialization instance.

        :param url: `str` URL for page.
        :param items: `dict` items.
        :param crawlers (optional): `dict` crawlers.
        :param session (optional): `requests.Session` instance.
        """
        self.__url = url
        self.__items = items or {}
        self.__crawlers = crawlers or {}
        self.__session = session or requests.Session()
        self.__data = {}

    @property
    def data(self):
        """The data property.

        :returns: `list` data.
        """
        return self.__data

    def crawl(self):
        """Crawl page.

        :returns: `dict` data.
        """
        page = html.fromstring(
            self.__session.get(self.__url, verify=False).content
        )

        for name, item in self.__items.items():
            self.__data[name] = item.parse(page)

        for name, crawler in self.__crawlers.items():
            self.__data[name] = crawler.crawl()

        return self.data
