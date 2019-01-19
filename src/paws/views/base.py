
from ..request import Request
from ..response import Response, response

import logging
log = logging.getLogger()


class View:

    def __call__(self, event, context):
        request = Request(event, context)
        kwargs = event.get('pathParameters') or {}
        return self.dispatch(request, **kwargs)

    def dispatch(self, request, **kwargs):
        func = getattr(self, request.method.lower())
        try:
            resp = func(request, **kwargs)
        except:
            import traceback
            log.exception('Error handling request %s %r', request.method, request)
            return response('Internal server Error', status=500)
        if isinstance(resp, Response):
            resp = resp.render()
        return resp
