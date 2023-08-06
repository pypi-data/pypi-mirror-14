# coding=utf-8

import re


class Element(object):

    """Base element."""

    def __init__(self):
        self._get_attributes()

    def __getattr__(self, name):
        try:
            attributes = {}
            attributes.update(self.__dict__)
            attributes.update(self.__class__.__dict__)
            value = attributes['get_{}'.format(name)](self)
        except KeyError:
            raise AttributeError(
                '{0} has no attribute "{1}" or method "get_{1}".'.format(
                    self.__class__.__name__, name
                )
            )
        setattr(self, name, value)
        return value

    def _get_attributes(self):
        """Get attributes by search and call `get_ATTRIBUTE` methods."""
        template = re.compile(r'get_([\w_]+)')

        for name in dir(self):
            try:
                attribute = template.match(name).group(1)
                function = getattr(self, name)
            except (AttributeError, IndexError):
                continue

            try:
                setattr(self, attribute, function())
            except TypeError:
                continue

    def before(self):
        """Any actions before start crawling."""
        pass

    def clean(self, value):
        return value
