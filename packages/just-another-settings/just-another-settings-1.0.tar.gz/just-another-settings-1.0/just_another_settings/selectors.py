import os


class NoSuchSettings(Exception):
    pass


class BaseSelector(object):
    _settings = dict()

    def __init__(self, default=None, **settings):
        """
        :param str or None default: default value if variable not set
        :param settings: dict of variable_value=settings_class pairs
        :return:
        """
        self.default = default
        self.register(**settings)

    def choose(self, *args, **kwargs):
        raise NotImplementedError

    def register(self, **settings):
        self._settings.update(settings)

    def __call__(self, *args, **kwargs):
        return self.choose(*args, **kwargs)

    def __getitem__(self, item):
        return self._settings[item]

    def get(self, item, default=None):
        return self._settings.get(item, default)

    def __contains__(self, item):
        return item in self._settings


class EnvSelector(BaseSelector):

    def __init__(self, variable, default=None, **settings):
        """

        :param str variable: name of env variable
        :param str or None default: default value if variable not set
        :param settings: dict of variable_value=settings_class pairs
        :return:
        """
        self.variable = variable
        super(EnvSelector, self).__init__(default, **settings)

    def choose(self):
        mode = os.getenv(self.variable, self.default)
        if not mode or mode not in self._settings:
            raise NoSuchSettings
        return self._settings.get(mode)


class ValueSelector(BaseSelector):
    def choose(self, mode=None):
        mode = self.default if mode is None else mode

        if mode not in self._settings:
            raise NoSuchSettings
        return self._settings.get(mode)
