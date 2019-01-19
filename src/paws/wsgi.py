#
# Mock request cycle for WSGI publishing
#
import re
from base64 import b64decode
from cgi import parse_header
from http.cookies import SimpleCookie
from io import BytesIO
from urllib.parse import parse_qs, urlunsplit

from .multipart import parse_multipart
from .utils import HeaderDict, MultiDict, cached_property
from .response import response


class WsgiRequest:
    def __init__(self, environ):
        self.environ = environ
        self.content_type, self.content_data = parse_header(environ.get('CONTENT_TYPE', ''))

    @property
    def path(self):
        return self.environ.get('PATH_INFO', b'/')

    @cached_property
    def body(self):
        try:
            content_length = int(self.environ.get('CONTENT_LENGTH'))
        except (ValueError, TypeError):
            content_length = 0

        return self.environ['wsgi.input'].read(content_length)

    @cached_property
    def cookies(self):
        # Direct copy
        jar = SimpleCookie()
        if self.event['headers'].get('Cookie'):
            jar.load(self.event['headers']['Cookie'].encode('utf-8'))
        return jar

    @cached_property
    def form(self):
        if self.content_type == 'application/x-www-form-urlencoded':
            data = parse_qs(self.body)
        if self.content_type == 'multipart/form-data':
            data = parse_multipart(BytesIO(self.body), self.content_data)
        return MultiDict(data)

    @cached_property
    def headers(self):
        return HeaderDict({
            k[5:].replace('_', '-'): v
            for k, v in self.environ.items()
            if k.startswith('HTTP_')
        })

    @property
    def method(self):
        return self.environ['REQUEST_METHOD'].upper()

    @property
    def params(self):
        # XXX matched path parameters
        return {}

    @property
    def query(self):
        return parse_qs(self.environ.get('QUERY_STRING', ''))

    @property
    def stage(self):
        return 'wsgi'

    @property
    def stageVar(self):
        return {}

    def absolute_url(self, path):
        # Direct copy
        return urlunsplit(
            ('https', self.headers['Host'], '/'.join([self.stage, path]), '', ''),
        )


class Route:
    def __init__(self, pattern, view):
        self.pattern = re.compile(pattern)
        self.view = view

    def matches(self, request):
        m = self.pattern.match(request.path)
        if m:
            return m.groupdict()


class Application:
    def __init__(self, routes):
        self.routes = [ Route(*route) for route in routes ]

    def __call__(self, environ, callback):
        request = WsgiRequest(environ)
        # map to view
        for route in self.routes:
            kwargs = route.matches(request)
            if kwargs is not None:
                resp = route.view.dispatch(request, **kwargs)
                break
        else:
            resp = response(status=404)

        # XXX Deal with cookies
        callback(str(resp['statusCode']), list(resp['headers'].items()))
        body = resp['body']
        if resp.get('isBase64Encoded', False):
            body = b64decode(body)
        else:
            body = body.encode('utf-8')
        yield body

