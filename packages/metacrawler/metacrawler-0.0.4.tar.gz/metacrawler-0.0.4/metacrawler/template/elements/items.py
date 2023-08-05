# coding=utf-8

from metacrawler.items import Field, Item


class YourItem(Item):

    field_name = Field(xpath='//h1/text()')
