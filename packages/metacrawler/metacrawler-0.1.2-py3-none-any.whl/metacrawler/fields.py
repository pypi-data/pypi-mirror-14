# coding=utf-8


class Field(object):

    """Field is minimum structure unit. Contains certain value.
    May be nested.
    """

    def __init__(self, xpath=None, fields=None, postprocessing=None, to=str):
        """Override initialization instance.

        :param xpath (optional): `str` xpath for extracting value from page.
        :param fields (optional): `dict` fields.
        :param postprocessing (optional): `function` postprocessing function.
        :param to (optional): `type` to representation as.
        """
        self.xpath = xpath or getattr(self.__class__, 'xpath', None)
        self.postprocessing = (
            postprocessing or getattr(self.__class__, 'postprocessing', None)
        )
        self.to = getattr(self.__class__, 'to', to)

        self.__fields = self._get_fields(fields or {})

    def _get_fields(self, passed_fields):
        """Get fields.

        :param passed_fields: `dict` passed fields.
        :returns: `dict` fields.
        """
        passed_fields.update(self.__class__.__dict__)
        fields = {}

        for name, attribute in passed_fields.items():
            if isinstance(attribute, Field):
                fields[name] = attribute

        return fields

    def before(self):
        """Any actions before crawl."""
        pass

    def crawl(self, page):
        """Crawl value from page.

        :param page: `lxml.Element` instance.
        :returns: value.
        """
        self.before()

        if self.__fields:
            value = self.crawl_subfields(page)
        elif self.xpath is not None:
            value = page.xpath(self.xpath)

            if self.to not in (list, tuple):
                try:
                    value = self.to(value[0])
                except IndexError:
                    value = None
            else:
                for item in value:
                    if not isinstance(item, str):
                        raise ValueError(
                            'Items of iterable value must be a string.'
                        )
                value = self.to(value)
        else:
            raise AttributeError(
                'Cannot call `.search()` as no `value=`, `xpath=` or '
                '`function=` keywords argument was passed when instantiating '
                'the field instance.'
            )

        if value is not None and self.postprocessing is not None:
            value = self.postprocessing(value)

        return value

    def crawl_subfields(self, page):
        """Crawl subfields."""
        value = None

        if self.to is dict:
            value = {}

            if self.xpath:
                try:
                    page = page.xpath(self.xpath)[0]
                except IndexError:
                    for name, field in self.__fields.items():
                        value[name] = None
                    return value

            for name, field in self.__fields.items():
                value[name] = field.crawl(page)
        elif self.to in (list, tuple):
            value = []

            if not self.xpath:
                raise AttributeError(
                    'For iterable types need pass `xpath=` keyword argument.'
                )

            for block in page.xpath(self.xpath):
                block_fields = {}
                for name, field in self.__fields.items():
                    block_fields[name] = field.crawl(block)
                value.append(block_fields)

            value = self.to(value)
        else:
            raise ValueError(
                'For nested fields keyword argument `to=` '
                'must be `dict`, `list` or `tuple`.'
            )

        return value
