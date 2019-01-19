import json

from paws.response import response

import logging
log = logging.getLogger(__name__)


RPC_MARKER = '_rpc'


def method(view):
    '''Mark a view as accessible via RPC'''
    setattr(view, RPC_MARKER, True)
    return view


def is_rpc_method(m):
    '''Helper for checking if something is marked as a pubishable method.'''
    return getattr(m, RPC_MARKER, False)


class RPCMixin:

    def post(self, request):
        action = request.headers.get('X-Rpc-Action')
        if action:
            method = getattr(self, action, None)
            if is_rpc_method(method):
                if request.body:
                    data = json.loads(request.body)
                else:
                    data = {}
                log.info("Method: %r %r", action, data)
                return method(request, **data)
        return response(status=404)
