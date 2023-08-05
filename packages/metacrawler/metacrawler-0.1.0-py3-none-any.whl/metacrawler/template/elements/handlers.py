# coding=utf-8

from metacrawler.handlers import Handler

from . import crawlers, constants
from .settings import CustomSettings


class CustomHandler(Handler):

    settings = CustomSettings.load_from_file(constants.SETTINGS_PATH)

    index = crawlers.IndexCrawler()

    def set_cli_arguments(self):
        self.argparser.add_argument('url')

    def before(self):
        self.index.url = self.cli['url']
        self.session.headers.update({'User-Agent': self.settings.user_agent})
