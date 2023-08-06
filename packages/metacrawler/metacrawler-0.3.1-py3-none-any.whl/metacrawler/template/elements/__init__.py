# coding=utf-8

from metacrawler.pagination import Pagination
from metacrawler.handlers import Handler

from . import crawlers, constants
from .settings import CustomSettings


class CustomHandler(Handler):

    settings = CustomSettings.load_from_file(constants.SETTINGS_PATH)

    index = crawlers.IndexCrawler()

    def get_argparser(self):
        argparser = super().get_argparser()
        argparser.add_argument('url')
        return argparser

    def get_index(self):
        self.index.pagination = Pagination(urls=[
            'https://github.com', 'https://bitbucket.org',
            'https://gitlab.com', self.cli['url'], 'https://google.com',
            'https://linkedin.com', 'https://facebook.com'
        ])
        return self.index

    def get_session(self):
        session = super().get_session()
        session.headers.update({'User-Agent': self.settings.user_agent})
        return session
