# coding=utf-8

from metacrawler import Handler

from . import crawlers
from settings import settings


class YourHandler(Handler):

    settings = settings

    your_crawler = crawlers.YourCrawler('https://github.com')
