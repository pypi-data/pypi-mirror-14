import os


class BaseField(object):

    def __init__(self, not_none=False):
        self.not_none = not_none
        self.value = None

    def __get__(self, instance, owner):
        if self.value:
            return self.value

        self.value = self.fetch_value()
        if self.value is None and self.not_none:
            raise ValueError('Wrong value')
        return self.value

    def __set__(self, instance, value):
        self.value = value

    def fetch_value(self):
        raise NotImplementedError


class EnvField(BaseField):
    def __init__(self, variable, default=None, *args, **kwargs):
        self.variable = variable
        self.default = default
        super(EnvField, self).__init__(*args, **kwargs)

    def fetch_value(self):
        return os.getenv(self.variable, self.default)

    def __set__(self, instance, value):
        raise TypeError('Can not assign value to env field')
