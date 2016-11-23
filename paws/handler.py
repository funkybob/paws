import logging

from .request import Request
from .response import Response, response

log = logging.getLogger()


class Handler(object):
    '''
    Simple dispatcher class.
    # WARNING # This code assumes SINGLE THREADED

    Usage:

    class MyHandler(Handler):
        def get(self, request, *args):
            ...
            return Response(...)

    my_handler = MyHandler()
    '''
    http_method_names = {'get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace'}

    def __call__(self, event, context):
        self.request = Request(event, context)
        if self.request.method.lower() in self.http_method_names:
            func = getattr(self, self.event['httpMethod'].lower(), self.invalid)
        else:
            func = self.invalid
        try:
            resp = func(self.request, *self.event['pathParameters'])
        except Exception:
            import traceback
            log.error(self)
            log.error(traceback.format_exc())
            return response(body='Internal server Error', status=500)
        if isinstance(resp, Response):
            resp = resp.render()
        return resp

    def __str__(self):
        return "<Request: {%s} %s (%r)" % (
            self.request.method,
            self.request.path,
            self.requeste.params,
        )

    def invalid(self, *args):
        # XXX Build list of valid methods?
        valid_methods = {
            method
            for method in self.http_method_names
            if hasattr(self, method)
        }
        return response(
            status=405,
            headers={'Allow': ', '.join(valid_methods)},
        )
