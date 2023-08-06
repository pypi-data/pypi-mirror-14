# coding=utf-8

from urllib.parse import urlparse


class Pagination(object):

    """Pagination using for navigation on website."""

    def __init__(self, xpath=None, host=None, urls=None):
        """Override initialization instance.

        :param xpath (optional): `str` xpath for search next link.
        :param host (optional): `str` host URL.
        :param urls (optional): `list` urls.
        """
        self.xpath = xpath
        self.host = host
        self.urls = urls
        self.index = -1

    def __iter__(self):
        return iter(self.urls)

    def next(self, page=None):
        """Return next link.

        :param page (optional): `lxml.Element` instance.
        :returns: `str` link.
        """
        if self.xpath is not None and self.host is not None:
            try:
                url = page.xpath(self.xpath)[0]
                return urlparse(self.host + url).geturl()
            except IndexError:
                return None
        elif self.urls:
            try:
                self.index += 1
                return self.urls[self.index]
            except IndexError:
                return None
        else:
            raise AttributeError(
                'Cannot call `.next()` as no `xpath=` and `host=` or '
                '`urls=` keywords argument was passed when instantiating '
                'the pagination instance.'
            )

    def __next__(self):
        return self.next()
