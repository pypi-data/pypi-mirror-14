# coding=utf-8

from metacrawler.base import Element


AVAILABLE_TYPES = (list, dict, int, float, str)


class Field(Element):

    """Field is minimum structure unit. Contains certain value.
    May be nested.
    """

    def __init__(self, value=None, xpath=None, fields=None, to=str):
        """Override initialization instance.

        :param value (optional): value cap.
        :param xpath (optional): `str` xpath for extracting value from page.
        :param fields (optional): `dict` fields.
        :param to (optional): `type` to representation as.
        """
        self.value = value
        self.xpath = xpath
        self.to = to

        self.__dict__.update(fields or {})

        super().__init__()

    @property
    def fields(self):
        candidates = {}
        candidates.update(self.__dict__)
        candidates.update(self.__class__.__dict__)
        fields = {}

        for name, attribute in candidates.items():
            if isinstance(attribute, Field):
                fields[name] = attribute

        return fields

    def get_value(self):
        return self.value or getattr(self.__class__, 'value', None)

    def get_xpath(self):
        return self.xpath or getattr(self.__class__, 'xpath', None)

    def get_to(self):
        to = getattr(self.__class__, 'to', self.to)

        assert to in AVAILABLE_TYPES, (
            '`to` must be one of next types: {}'.format(
                ', '.join(AVAILABLE_TYPES)
            )
        )

        return to

    def crawl(self, page):
        """Crawl value from page.

        :param page: `lxml.Element` instance.
        :returns: value.
        """
        self.before()

        if self.value:
            return self.value
        elif self.fields:
            value = self.crawl_subfields(page)
        elif self.xpath is not None:
            value = page.xpath(self.xpath)

            if self.to is not list:
                try:
                    value = self.to(value[0])
                except IndexError:
                    value = None
            else:
                if not all(isinstance(item, str) for item in value):
                    raise ValueError('Items of list value must be a string.')

                value = list(value)
        else:
            raise AttributeError(
                'Cannot call `.crawl()` as no `value=`, `xpath=` or '
                'keywords argument was passed when instantiating '
                'the field instance.'
            )

        if not value:
            value = self.clean(value)

        return value

    def crawl_subfields(self, page):
        """Crawl subfields.

        :param page: `lxml.Element` instance.
        :returns: value.
        """
        if self.to is dict:
            value = {}

            if self.xpath:
                try:
                    page = page.xpath(self.xpath)[0]
                except IndexError:
                    return {key: None for key in self.fields.keys()}

            for name, field in self.fields.items():
                value[name] = field.crawl(page)
        elif self.to is list:
            value = []

            if not self.xpath:
                raise AttributeError(
                    'For list type need pass `xpath=` keyword argument.'
                )

            for block in page.xpath(self.xpath):
                value.append(
                    {n: f.crawl(block) for n, f in self.fields.items()}
                )
        else:
            raise ValueError(
                'For nested fields keyword argument `to=` '
                'must be `dict` or `list`.'
            )

        return value
