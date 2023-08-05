# coding=utf-8

import copy
import argparse
import json

import requests

from metacrawler.base import Element
from metacrawler.settings import Settings
from metacrawler.crawlers import Crawler


class Handler(Element):

    """Handler control crawling process."""

    def __init__(self, crawlers=None, settings=None):
        """Override initialization object.

        :param crawlers (optional): `dict` crawlers.
        :param settings (optional): `metacrawler.settings.Settings` instance.
        """
        self.settings = settings

        self.data = {}
        self.__dict__.update(crawlers or {})
        self.__cli = {}

        super().__init__()

        if not self.crawlers:
            raise ValueError('Cannot use `Handler` without crawlers.')

    @property
    def crawlers(self):
        candidates = {}
        candidates.update(self.__dict__)
        candidates.update(self.__class__.__dict__)
        crawlers = {}

        for name, attribute in candidates.items():
            if isinstance(attribute, Crawler):
                crawlers[name] = attribute

        return crawlers

    @property
    def cli(self):
        """The cli property."""
        if not self.__cli:
            self.__cli = vars(self.argparser.parse_args())

        return copy.deepcopy(self.__cli)

    def get_session(self):
        return requests.Session()

    def get_settings(self):
        if not self.settings:
            return getattr(self.__class__, 'settings', Settings())

        return self.settings

    def get_argparser(self):
        argparser = argparse.ArgumentParser()
        argparser.add_argument(
            '-o', '--output', default='output.json', help='Output file.'
        )
        return argparser

    def start(self):
        """Start crawling."""
        self.before()

        for name, crawler in self.crawlers.items():
            self.data[name] = crawler.crawl()

        return self.data

    def output(self, compact=False, data=None):
        """Output to file.

        :param compact (optional): `bool` compact output.
        :param data (optional): data.
        """
        data = data or self.data

        if compact:
            data = json.dumps(data, ensure_ascii=False)
        else:
            data = json.dumps(data, indent=4, ensure_ascii=False)

        with open(self.cli['output'], 'w') as f:
            f.write(data)
