import os


class env:
    '''
    Allows specifying a default value which can still be overidden by an env
    var.
    '''
    def __init__(self, default=None):
        self.name = None
        self.default = default

    def __get__(self, obj, cls=None):
        return os.environ.get(self.name.upper(), self.default)


class MetaConfig(type):
    '''Quickly tell the env attrs their names.'''
    def __new__(mcs, name, bases, attrs):
        for name, attr in attrs.items():
            if isinstance(attr, env):
                attr.name = name
        return super().__new__(mcs, name, bases, attrs)

    def __getattr__(cls, key):
        return os.environ[key]


class Conf(metaclass=MetaConfig):
    '''
    Handy wrapper and placeholder of config values.
    '''
    def __init__(self):
        raise RuntimeError(
            'Can not create instance of singleton {}. Use class directly.'.format(self.__class__.__name__)
        )
