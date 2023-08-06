# coding=utf-8

import requests
import grequests
from lxml import html

from metacrawler.base import Element
from metacrawler.fields import Field


class Crawler(Element):

    """Crawler parse page use fields as rules. May be nested."""

    def __init__(self):
        super().__init__()

        self.data = []

        if not self.fields:
            raise ValueError('Cannot use `Crawler` without fields.')

        if len(self.fields) > 1 and self.collapse:
            raise ValueError(
                'Must not use `collapse` with few fields or/and crawlers.'
            )

    @property
    def fields(self):
        fields = {}

        for name, attribute in self.__class__.__dict__.items():
            if isinstance(attribute, (Crawler, Field)):
                fields[name] = attribute

        return fields

    def get_url(self):
        return getattr(self.__class__, 'url', None)

    def get_pagination(self):
        return getattr(self.__class__, 'pagination', None)

    def get_collapse(self):
        return getattr(self.__class__, 'collapse', False)

    def get_limit(self):
        return getattr(self.__class__, 'limit', None)

    def get_session(self):
        return getattr(self.__class__, 'session', requests.Session())

    def get_timeout(self):
        return getattr(self.__class__, 'timeout', 3.0)

    def get_authentication(self):
        return getattr(self.__class__, 'authentication', None)

    def crawl(self, *args, **kwargs):
        """Crawl page.

        :returns: `dict` data.
        """
        self.before()
        data = []

        if self.authentication is not None:
            self.session = self.authentication.authentication(self.session)

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
            self.data.extend(data)
        else:
            self.data = data[0]

        return self.clean(self.data)

    def paginate(self, page):
        """Paginate.

        :param page: `lxml.Element` instance.
        """
        if self.pagination:
            self.url = self.pagination.next(page)
        else:
            self.url = None
