from .request import Request
from .response import response


class Handler(object):
    '''
    Simple dispatcher class.
    '''
    def __init__(self, event, context):
        self.request = Request(event, context)

    def __call__(self, event, context):
        func = getattr(self, self.event['httpMethod'], self.invalid)
        return func(self.request, *self.event['pathParameters'])

    def invalid(self, *args):
        return response(status=405)
