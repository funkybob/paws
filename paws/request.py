from Cookie import SimpleCookie
from urlparse import parse_qs, urlunsplit

from utils import MultiDict, cached_property


class Request(object):
    def __init__(self, event, context):
        self.event = event
        self.context = context

    @cached_property
    def cookies(self):
        jar = SimpleCookie()
        if self.event['headers'].get('Cookie'):
            jar.load(self.event['headers']['Cookie'].encode('utf-8'))
        return jar

    @cached_property
    def form(self):
        return MultiDict(parse_qs(self.event.get('body', '') or ''))

    @property
    def headers(self):
        return self.event['headers']

    @property
    def method(self):
        return self.event['httpMethod']

    @property
    def params(self):
        return self.event['pathParameters']

    @property
    def query(self):
        return self.event['queryStringParameters']

    @property
    def stage(self):
        return self.event['stage']

    @property
    def stageVar(self):
        return self.event['stageVariables']

    def absolute_url(self, path):
        return urlunsplit(
            ('https', self.headers['Host'], '/'.join([self.stage, path]), '', ''),
        )
