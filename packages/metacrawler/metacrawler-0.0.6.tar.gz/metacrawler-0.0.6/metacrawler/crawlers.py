# coding=utf-8

import requests
from lxml import html

from metacrawler.items import Item, Field


class Crawler(object):

    """Crawler parse page use items as rules. May be nested."""

    def __init__(self, url=None, items=None,
                 crawlers=None, session=None, pagination=None):
        """Override initialization instance.

        :param url (optional): `str` URL for page.
        :param items (optional): `dict` items.
        :param crawlers (optional): `dict` crawlers.
        :param session (optional): `requests.Session` instance.
        :param pagination (optional): `metacrawler.pagination.Pagination`.
        """
        self.url = url or getattr(self.__class__, 'url', None)
        self.pagination = pagination or getattr(
            self.__class__, 'pagination', None
        )

        self.session = session or requests.Session()

        self.__items = self._get_class_items()
        for name, item in (items or {}).items():
            assert isinstance(item, (Item, Field)), (
                '`items` must be `Item` instances.'
            )
            self.__items[name] = item

        self.__crawlers = self._get_class_crawlers()
        for name, crawler in (crawlers or {}).items():
            assert isinstance(crawler, Crawler), (
                '`crawler` must be `Crawler` instances.'
            )
            self.__crawlers[name] = crawler

        self.__data = {}

    @property
    def data(self):
        """The data property.

        :returns: `list` data.
        """
        return self.__data

    def _get_class_items(self):
        """Get class items.

        :returns: `dict` items.
        """
        items = {}

        for name, attribute in self.__class__.__dict__.items():
            if isinstance(attribute, (Item, Field)):
                items[name] = attribute

        return items

    def _get_class_crawlers(self):
        """Get class crawlers.

        :returns: `dict` crawlers.
        """
        crawlers = {}

        for name, attribute in self.__class__.__dict__.items():
            if isinstance(attribute, Crawler):
                crawlers[name] = attribute

        return crawlers

    def crawl(self):
        """Crawl page.

        :returns: `dict` data.
        """
        while self.url:
            page = html.fromstring(
                self.session.get(self.url, verify=False).content
            )

            for name, item in self.__items.items():
                self.__data[name] = item.parse(page)

            for name, crawler in self.__crawlers.items():
                self.__data[name] = crawler.crawl()

            self.paginate(page)

        return self.data

    def paginate(self, page):
        """Paginate.

        :param page: `lxml.Element` instance.
        """
        self.url = None
