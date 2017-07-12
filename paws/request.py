from base64 import b64decode
from cgi import parse_header
from http.cookies import SimpleCookie
from io import BytesIO
from urllib.parse import parse_qs, urlunsplit

from .multipart import parse_multipart
from .utils import HeaderDict, MultiDict, cached_property


class Request:
    def __init__(self, event, context):
        self.event = event
        self.context = context
        self.content_type, self.content_data = parse_header(event['headers'].get('content-type', ''))

    @property
    def body(self):
        return self.event.get('body') or ''

    @cached_property
    def cookies(self):
        jar = SimpleCookie()
        if self.event['headers'].get('Cookie'):
            jar.load(self.event['headers']['Cookie'].encode('utf-8'))
        return jar

    @cached_property
    def form(self):
        if self.content_type == 'application/x-www-form-urlencoded':
            data = parse_qs(self.body)
        if self.content_type == 'multipart/form-data':
            data = parse_multipart(BytesIO(b64decode(self.body)), self.content_data)
        return MultiDict(data)

    @property
    def headers(self):
        return HeaderDict(self.event['headers'])

    @property
    def method(self):
        return self.event['httpMethod']

    @property
    def params(self):
        return self.event['pathParameters'] or {}

    @property
    def query(self):
        return self.event['queryStringParameters'] or {}

    @property
    def stage(self):
        return self.event['requestContext']['stage']

    @property
    def stageVar(self):
        return self.event['stageVariables']

    def absolute_url(self, path):
        return urlunsplit(
            ('https', self.headers['Host'], '/'.join([self.stage, path]), '', ''),
        )
