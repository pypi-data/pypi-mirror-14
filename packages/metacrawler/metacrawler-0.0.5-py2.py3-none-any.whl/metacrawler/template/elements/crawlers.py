# coding=utf-8

from metacrawler.crawlers import Crawler

from . import items


class YourCrawler(Crawler):

    your_item = items.YourItem()
