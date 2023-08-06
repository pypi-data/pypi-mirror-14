# coding=utf-8

from metacrawler.crawlers import Crawler
from metacrawler.fields import Field

from . import fields


class IndexCrawler(Crawler):

    header = fields.HeaderField()
    first_link_text = Field(xpath='//a/text()')
