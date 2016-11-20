class MultiDict(dict):

    def __getitem__(self, key):
        return super(MultiDict, self).__getitem__(key)[0]

    def getlist(self, key, default=None):
        try:
            return super(MultiDict, self).__getitem__(key)
        except KeyError:
            if default is None:
                default = []
            return default

    def items(self):
        return [
            (k, v[0])
            for k, v in super(MultiDict, self).items()
        ]

    def lists(self):
        return super(MultiDict, self).items()


class cached_property(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        value = instance.__dict__[self.func.__name__] = self.func(instance)
        return value


class HeaderDict(dict):
    '''
    Dict for containing response headers.

    Keys are matched case insensitive.
    title_items() will title-case keys.

    XXX Non-destructive set?
    '''
    def __getitem__(self, key):
        return super(HeaderDict, self).__getitem__(key.lower())

    def __setitem__(self, key, value):
        return super(HeaderDict, self).__setitem__(key.lower(), value)

    def __delitem__(self, key):
        return super(HeaderDict, self).__delitem__(key.lower())

    def title_items(self):
        return ((key.title(), value) for key, value in self.items())
