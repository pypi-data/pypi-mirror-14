# coding=utf-8

import re


class Element(object):

    """Base element."""

    def __init__(self):
        self._get_attributes()

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
