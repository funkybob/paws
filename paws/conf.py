import os


class env(object):
    def __init__(self, default=None):
        self.name = None
        self.default = default

    def __get__(self, obj, cls=None):
        if cls:
            return os.environ.get(self.name.upper(), self.default)


class MetaConfig(type):
    '''Quickly tell the env attrs their names.'''
    def __new__(mcs, name, bases, attrs):
        for name, attr in attrs.items():
            if isinstance(attr, env):
                env.name = name
        return super(MetaConfig, mcs).__new__(mcs, name, bases, attrs)


class Conf(dict):
    '''
    Handy wrapper and placeholder of config values.
    '''
    __metaclass__ = MetaConfig

    def __getattr__(self, key):
        return os.environ[key]
