# coding=utf-8

import requests
import grequests
from lxml import html

from metacrawler.base import Element
from metacrawler.fields import Field


class Crawler(Element):

    """Crawler parse page use fields as rules. May be nested."""

    def __init__(self, url=None, fields=None, collapse=None,
                 session=None, pagination=None, limit=None, timeout=None):
        """Override initialization instance.

        :param url (optional): `str` URL for page.
        :param fields (optional): `dict` fields.
        :param processes (optional): `int` crawl processes.
        :param collapse (optional): `bool` collapse field to upper level.
        :param session (optional): `requests.Session` instance.
        :param pagination (optional): `metacrawler.pagination.Pagination`.
        :param limit (optional): `int` limit.
        :param timeout (optional): `float` request timeout.
        """
        self.__url = url
        self.__collapse = collapse
        self.__session = session
        self.__pagination = pagination
        self.__limit = limit
        self.__timeout = timeout

        self.__dict__.update(fields or {})

        super().__init__()

        self.__data = []

        if not self.fields:
            raise ValueError('Cannot use `Crawler` without fields.')

        if len(self.fields) > 1 and self.collapse:
            raise ValueError(
                'Must not use `collapse` with few fields or/and crawlers.'
            )

    @property
    def fields(self):
        candidates = {}
        candidates.update(self.__dict__)
        candidates.update(self.__class__.__dict__)
        fields = {}

        for name, attribute in candidates.items():
            if isinstance(attribute, (Crawler, Field)):
                fields[name] = attribute

        return fields

    @property
    def data(self):
        """The data property.

        :returns: `list` data.
        """
        return self.__data

    def get_url(self):
        if not self.__url:
            return getattr(self.__class__, 'url', None)

        return self.__url

    def get_pagination(self):
        if not self.__pagination:
            return getattr(self.__class__, 'pagination', None)

        return self.__pagination

    def get_collapse(self):
        if not isinstance(self.__collapse, bool):
            return getattr(self.__class__, 'collapse', False)

        return self.__collapse

    def get_limit(self):
        if not isinstance(self.__limit, int):
            return getattr(self.__class__, 'limit', None)

        return self.__limit

    def get_session(self):
        if not self.__session:
            return getattr(self.__class__, 'session', requests.Session())

        return self.__session

    def get_timeout(self):
        if not self.__timeout:
            return getattr(self.__class__, 'timeout', 3.0)

        return self.__timeout

    def crawl(self, *args, **kwargs):
        """Crawl page.

        :returns: `dict` data.
        """
        self.before()
        data = []

        def parse(response):
            page = html.fromstring(response.content)

            if self.limit is not None and int(self.limit) <= len(data):
                return page

            if self.collapse:
                field = list(self.fields.items())[0][1]
                if field.to is list:
                    data.extend(field.crawl(page))
                else:
                    data.append(field.crawl(page))
            else:
                data.append({n: f.crawl(page) for n, f in self.fields.items()})

            return page

        try:
            iterator = iter(self.pagination)
        except TypeError:
            iterator = None

        if iterator:
            requests_list = []

            for url in iterator:
                requests_list.append(grequests.request(
                    'GET', url, session=self.session, timeout=self.timeout
                ))

            for response in grequests.map(requests_list):
                if response:
                    parse(response)
        else:
            while self.url:
                page = parse(self.session.get(self.url, verify=False))
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
