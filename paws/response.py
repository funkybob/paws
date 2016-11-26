import json
from Cookie import SimpleCookie


def response(body='', status=200, headers=None):
    '''
    Generate a response dict for Lambda Proxy
    '''
    if headers is None:
        headers = {}
    if isinstance(body, unicode):
        body = body.encode('utf-8')
    elif not isinstance(body, str):
        body = json.dumps(body, default=str)
        headers.setdefault('Content-Type', 'application/json')
    return {
        'statusCode': status,
        'headers': headers,
        'body': body,
    }


class Response(object):
    '''
    Light container to help building up a response.
    '''
    __slots__ = ('body', 'status', 'headers',)

    def __init__(self, body='', status=200, headers=None):
        self.body = body
        self.status = status
        self.headers = headers or {}  # Smart Headers container?
        self.cookies = SimpleCookie()

    def render(self):
        if self.cookies:
            self.headers['Set-Cookies'] = self.cookies.output(header='', sep=', ').strip()
        return response(self.body, self.status, self.headers)


class Redirect(Response):
    def __init__(self, location, body='', status=303, headers=None):
        super(Redirect, self).__init__(body=body, status=status, headers=headers)
        self.headers.setdefault('Location', location)


class TemporaryRedirect(Response):
    def __init__(self, location, body='', status=307, headers=None):
        super(Redirect, self).__init__(body=body, status=status, headers=headers)
        self.headers.setdefault('Location', location)


class PermanentRedirect(Response):
    def __init__(self, location, body='', status=308, headers=None):
        super(Redirect, self).__init__(body=body, status=status, headers=headers)
        self.headers.setdefault('Location', location)


class BadRequest(Response):
    def __init__(self, body='', status=400, headers=None):
        super(Unauthorized, self).__init__(body=body, status=status, headers=headers)


class Unauthorized(Response):
    def __init__(self, body='', status=401, headers=None):
        super(Unauthorized, self).__init__(body=body, status=status, headers=headers)


class NotFound(Response):
    def __init__(self, body='', status=404, headers=None):
        super(NotFound, self).__init__(body=body, status=status, headers=headers)
