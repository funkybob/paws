from urlparse import parse_qs

from utils import cached_property, MultiDict


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

    @property
    def stage(self):
        return self.event['stage']

    @property
    def stageVar(self):
        return self.event['stageVariables']

    @property
    def params(self):
        return self.event['pathParameters']
