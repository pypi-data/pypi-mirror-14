# coding=utf-8

import configobj
from validate import Validator


class Settings(object):

    """Class for keep settings."""

    def __init__(self, configspec=None, configuration=None):
        """Override initialization instance.

        :param configspec (optional): `dict` configspec for read from file.
        :param configuration (optional): `dict` configuration.
        """
        self.__configspec = (
            configspec or getattr(self.__class__, 'configspec', None)
        )
        self.__configuration = configuration

    def __getattr__(self, attribute):
        """Override getting not existing attribute."""
        assert not (self.__configspec and not self.__configuration), (
            'Cannot access to settings before call `.load_from_file` method.'
        )
        assert self.__configspec or self.__configuration, (
            'Cannot access to settings as no `configuration=` or '
            '`configspec=` keywords argument was not passed when instantiating'
            ' the settings instance.'
        )

        value = self.__configuration[attribute]
        if isinstance(value, dict):
            return self.__class__(configuration=value)
        return value

    @classmethod
    def load_from_file(cls, filename):
        """
        Load settings from configuration file.

        :param filename: `str` configuration filename.
        :returns: `dict` of settings.
        """
        configuration = configobj.ConfigObj(
            filename, configspec=cls.configspec
        )
        if not configuration.validate(Validator(cls.configspec)):
            raise ValueError('Configuration file not pass validation.')

        return cls(configuration=configuration)

    @classmethod
    def create_configuration_file(cls, filename):
        """
        Create configuration file.

        :param filename: `str` path to write configuration.
        """
        config = configobj.ConfigObj(infile=filename)
        config.update(cls.configspec)
        config.write()
