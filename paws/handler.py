from .request import Request
from .response import response


class Handler(object):
    '''
    Simple dispatcher class.
    '''

    def __call__(self, event, context):
        self.request = Request(event, context)
        func = getattr(self, self.event['httpMethod'], self.invalid)
        return func(request, *self.event['pathParameters'])

    def invalid(self, *args):
        return response(status=405)
