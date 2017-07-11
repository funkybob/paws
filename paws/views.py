
from .request import Request
from .response import Response, response

import logging
log = logging.getLogger()


class View:

    def __call__(self, event, context):
        request = Request(event, context)
        resp = self.prepare(request)
        if resp:
            return resp
        kwargs = event.get('pathParameters') or {}
        func = getattr(self, request.method.lower())
        try:
            resp = func(request, **kwargs)
        except:
            import traceback
            log.error(self)
            log.error(traceback.format_exc())
            return response(body='Internal server Error', status=500)
        if isinstance(resp, Response):
            resp = resp.render()
        return resp

    def prepare(self, request):
        pass
