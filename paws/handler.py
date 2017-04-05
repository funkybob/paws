import logging

from .request import Request
from .response import Response, response

log = logging.getLogger()


class http_handler(object):
    def __init__(self, func):
        self.func = func
        self.url = None
        self.__name__ = func.__name__

    def __str__(self):
        return 'HTTP %s' % (self.func.__name__,)

    def __call__(self, event, context):
        request = Request(event, context)
        kwargs = event.get('pathParameters') or {}
        try:
            resp = self.func(request, **kwargs)
        except:
            import traceback
            log.error(self)
            log.error(traceback.format_exc())
            return response(body='Internal server Error', status=500)
        if isinstance(resp, Response):
            resp = resp.render()
        return resp


class url(object):
    '''
    @url(path[, cores=False][, method='GET'])
    def http_function(request, ...):

    http_function.url.path == path
    '''
    def __init__(self, path, cors=False, method='GET'):
        self.path = path
        self.cors = cors
        self.method = method

    def __call__(self, func):
        func = http_handler(func)
        func.url = self
        return func
