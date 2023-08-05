# coding=utf-8

import types
import collections

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


class Pagination(object):

    """Pagination using for navigation on website."""

    def __init__(self, xpath=None, host=None, function=None):
        """Override initialization instance.

        :param xpath (optional): `str` xpath for search next link.
        :param host (optional): `str` host URL.
        :param function (optional): `function` function for get next link.
        """
        self.__xpath = xpath
        self.__host = host
        self.__function = function
        self.__last = None

    def __iter__(self):
        """Override instance iteration."""
        if self.__function is not None:
            result = self.__function()
            if isinstance(result, types.GeneratorType):
                return result
            elif isinstance(result, collections.Iterable):
                return iter(result)
            else:
                return self

    def next(self, page=None):
        """Return next link.

        :param page (optional): `lxml.Element` instance.
        :returns: `str` link.
        """
        if self.__function is not None:
            url = self.__function(page)
        elif self.__xpath is not None and self.__host is not None:
            try:
                url = page.xpath(self.__xpath)[0]
                url = urlparse(self.__host + url).geturl()
            except IndexError:
                return None
        else:
            raise AttributeError(
                'Cannot call `.next()` as no `xpath=` and `host=` or '
                '`function=` keywords argument was passed when instantiating '
                'the pagination instance.'
            )

        if self.__last == url:
            raise StopIteration()
        else:
            self.__last = url
            return url

    def __next__(self):
        """Return next link.

        :param page (optional): `lxml.Element` instance.
        :returns: `str` link.
        """
        return self.next()
