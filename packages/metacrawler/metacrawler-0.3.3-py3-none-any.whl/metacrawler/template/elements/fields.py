# coding=utf-8

from metacrawler.fields import Field


class HeaderField(Field):

    xpath = '//h1'
    to = dict

    text = Field(xpath='text()')

    def clean(self, value):
        value['cap'] = 'Test'
        return value
