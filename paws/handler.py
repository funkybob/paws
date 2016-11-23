import logging

from .request import Request
from .response import Response, response

log = logging.getLogger()


class http_handler(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, event, context):
        request = Request(event, context)
        kwargs = event.get('pathParameters', {})
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
