# coding=utf-8


class Field(object):

    """Field is minimum structure unit. Contains certain value."""

    def __init__(self, xpath=None, function=None, postprocessing=None, to=str):
        """Override initialization instance.

        :param xpath (optional): `str` xpath for extracting value from page.
        :param function (optional): `function` function for getting value.
        :param postprocessing (optional): `function` postprocessing function.
        :param to (optional): `type` to representation as.
        """
        self.__xpath = xpath
        self.__function = function
        self.__postprocessing = postprocessing
        self.__to = to

    def parse(self, page):
        """Parse value from page.

        :param page: `lxml.Element` instance.
        :returns: value.
        """
        if self.__xpath is not None:
            value = page.xpath(self.__xpath)
        elif self.__function is not None:
            value = self.__function(page)
        else:
            raise AttributeError(
                'Cannot call `.search()` as no `value=`, `xpath=` or '
                '`function=` keywords argument was passed when instantiating '
                'the field instance.'
            )

        if self.__to not in (list, tuple):
            try:
                value = value[0]
            except IndexError:
                value = None
        else:
            for item in value:
                if not isinstance(item, str):
                    raise ValueError(
                        'Items of iterable value must be a string.'
                    )

        if value is not None and self.__postprocessing is not None:
            value = self.__postprocessing(value)

        return value


class Item(object):

    """Item is aggregate of fields. Items can be nested."""

    def __init__(self, fields=None, xpath='//html'):
        """Override initialization instance.

        :param fields (optional): `dict` fields.
        :param xpath (optional): `str` xpath for extracting blocks from page.
        """
        self.__xpath = xpath or self.__class__.xpath

        self.__fields = self._get_class_fields()

        for name, field in (fields or {}).items():
            assert isinstance(field, (Field, Item)), (
                '`fields` must be `Field` or `Item` instances.'
            )
            self.__fields[name] = field

    def _get_class_fields(self):
        """Get class fields.

        :returns: `dict` fields.
        """
        fields = {}

        for name, attribute in self.__class__.__dict__.items():
            if isinstance(attribute, (Field, Item)):
                fields[name] = attribute

        return fields

    def parse(self, page):
        """Parse process.

        :param page: `lxml.Element` instance.
        :returns: `list` data.
        """
        data = []

        for block in page.xpath(self.__xpath):
            item = {}
            for name, field in self.__fields.items():
                item[name] = field.parse(block)

            data.append(item)

        return data
