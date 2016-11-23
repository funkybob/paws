from Cookie import SimpleCookie
from urlparse import parse_qs

from utils import MultiDict, cached_property


class Request(object):
    def __init__(self, event, context):
        self.event = event
        self.context = context

    @property
    def method(self):
        return self.event['httpMethod']

    @property
    def query(self):
        return self.event['queryStringParameters']

    @cached_property
    def post(self):
        return MultiDict(parse_qs(self.event.get('body', '') or ''))

    @cached_property
    def cookies(self):
        jar = SimpleCookie()
        if self.event['headers'].get('Cookie'):
            jar.load(self.event['headers']['Cookie'].encode('utf-8'))
        return jar

    @property
    def stage(self):
        return self.event['stage']

    @property
    def stageVar(self):
        return self.event['stageVariables']

    @property
    def params(self):
        return self.event['pathParameters']
