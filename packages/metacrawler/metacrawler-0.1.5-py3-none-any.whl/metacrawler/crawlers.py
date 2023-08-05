# coding=utf-8

import requests
from lxml import html

from metacrawler.fields import Field


class Crawler(object):

    """Crawler parse page use items as rules. May be nested."""

    def __init__(self, url=None, fields=None,
                 collapse=False, session=None, pagination=None, limit=None):
        """Override initialization instance.

        :param url (optional): `str` URL for page.
        :param fields (optional): `dict` fields.
        :param collapse (optional): `bool` collapse one field to upper level.
        :param session (optional): `requests.Session` instance.
        :param pagination (optional): `metacrawler.pagination.Pagination`.
        :param limit (optional): `int` limit.
        """
        self.url = url or getattr(self.__class__, 'url', None)
        self.pagination = pagination or getattr(
            self.__class__, 'pagination', None
        )
        self.collapse = collapse or getattr(self.__class__, 'collapse', None)

        if limit is not None:
            self.limit = limit
        else:
            self.limit = getattr(self.__class__, 'limit', None)

        self.session = session or requests.Session()

        self.__fields = self._get_fields(fields or {})

        if len(self.__fields) > 1 and self.collapse:
            raise ValueError(
                'Must not use `collapse` with few fields or/and crawlers.'
            )

        self.__data = [] if self.pagination else {}

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
        data = []

        while self.url:
            if self.limit is not None and int(self.limit) <= len(data):
                break

            page = html.fromstring(
                self.session.get(self.url, verify=False).content
            )
            page_data = {}

            for name, field in self.__fields.items():
                page_data[name] = field.crawl(page)

                if self.collapse:
                    collapse_field = name

            if self.collapse:
                if self.__fields[collapse_field].to is list:
                    data.extend(page_data[collapse_field])
                else:
                    data.append(page_data[collapse_field])
            else:
                data.append(page_data)

            self.paginate(page)

        if self.pagination:
            self.__data.extend(data)
        else:
            self.__data = data[0]

        return self.data

    def paginate(self, page):
        """Paginate.

        :param page: `lxml.Element` instance.
        """
        if self.pagination:
            self.url = self.pagination.next(page)
        else:
            self.url = None
