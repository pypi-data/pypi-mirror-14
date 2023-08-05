# coding=utf-8

import copy
import argparse
import json

import requests

from metacrawler.settings import Settings
from metacrawler.crawlers import Crawler


class Handler(object):

    """Handler control crawling process."""

    def __init__(self, crawlers=None):
        """Override initialization object.

        :param crawlers (optional): `dict` crawlers.
        """
        self.session = requests.Session()
        self.settings = getattr(self.__class__, 'settings', Settings())

        self.__crawlers = self._get_crawlers(crawlers or {})
        self.__data = {}

        self.argparser = argparse.ArgumentParser()
        self.argparser.add_argument(
            '-o', '--output', default='output.json', help='Output file.'
        )
        self.set_cli_arguments()
        self.__cli = {}

    @property
    def data(self):
        """The data property."""
        return copy.deepcopy(self.__data)

    @property
    def cli(self):
        """The cli property."""
        if not self.__cli:
            self.__cli = vars(self.argparser.parse_args())

        return copy.deepcopy(self.__cli)

    def _get_crawlers(self, passed_fields):
        """Get crawlers.

        :param passed_fields: `dict` passed fields.
        :returns: `dict` fields.
        """
        passed_fields.update(self.__class__.__dict__)
        fields = {}

        for name, attribute in passed_fields.items():
            if isinstance(attribute, Crawler):
                fields[name] = attribute

        return fields

    def set_cli_arguments(self):
        """Set CLI arguments."""
        pass

    def before(self):
        """Any actions before start."""
        pass

    def start(self):
        """Start crawling."""
        self.before()

        for name, crawler in self.__crawlers.items():
            self.__data[name] = crawler.crawl()

        return self.data

    def output(self, compact=False):
        """Output to file.

        :param compact (optional): `bool` compact output.
        """
        if compact:
            data = json.dumps(self.data, ensure_ascii=False)
        else:
            data = json.dumps(self.data, indent=4, ensure_ascii=False)

        with open(self.cli['output'], 'w') as f:
            f.write(data)
