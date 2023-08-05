# coding=utf-8

from metacrawler.settings import Settings

# See http://www.voidspace.org.uk/python/configobj.html#configspec


class CustomSettings(Settings):

    configspec = {
    #    'nested': {
    #        'boolean': 'boolean(default=True)'
    #    },
    #    'string': 'string(default="string")',
    }
