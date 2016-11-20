from .request import Request
from .response import response, Response

import logging
log = logging.getLogger()


class Handler(object):
    '''
    Simple dispatcher class.
    '''
    def __init__(self, event, context):
        self.request = Request(event, context)

    def __call__(self, event, context):
        func = getattr(self, self.event['httpMethod'].lower(), self.invalid)
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
        return response(status=405)
