# coding=utf-8

import requests
from lxml import html

from metacrawler.fields import Field


class Crawler(object):

    """Crawler parse page use items as rules. May be nested."""

    def __init__(self, url=None, fields=None, session=None, pagination=None):
        """Override initialization instance.

        :param url (optional): `str` URL for page.
        :param fields (optional): `dict` fields.
        :param session (optional): `requests.Session` instance.
        :param pagination (optional): `metacrawler.pagination.Pagination`.
        """
        self.url = url or getattr(self.__class__, 'url', None)
        self.pagination = pagination or getattr(
            self.__class__, 'pagination', None
        )

        self.session = session or requests.Session()

        self.__fields = self._get_fields(fields or {})

        self.__data = {}

    @property
    def data(self):
        """The data property.

        :returns: `list` data.
        """
        return self.__data

    def _get_fields(self, passed_fields):
        """Get fields.

        :param passed_fields: `dict` passed fields.
        :returns: `dict` fields.
        """
        passed_fields.update(self.__class__.__dict__)
        fields = {}

        for name, attribute in passed_fields.items():
            if isinstance(attribute, (Field, Crawler)):
                fields[name] = attribute

        return fields

    def before(self):
        """Any actions before crawl."""
        pass

    def crawl(self, *args, **kwargs):
        """Crawl page.

        :returns: `dict` data.
        """
        self.before()

        while self.url:
            page = html.fromstring(
                self.session.get(self.url, verify=False).content
            )

            for name, field in self.__fields.items():
                self.__data[name] = field.crawl(page)

            self.paginate(page)

        return self.data

    def paginate(self, page):
        """Paginate.

        :param page: `lxml.Element` instance.
        """
        self.url = None
