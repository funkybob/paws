from http.cookies import SimpleCookie
from urllib.parse import urlunsplit

from .utils import HeaderDict


class MockRequest:
    def __init__(self, method, url, *, cookies=None, headers=None, body=None):
        self.method = method.upper()
        self.cookies = SimpleCookie()
        self.body = body if body is not None else ''
        self.headers = HeaderDict()
        if headers is not None:
            self.headers.update(headers)
        if cookies:
            for name, value in cookies.items():
                cookies[name] = value
        # form
        # params
        # query
        # stage
        # stageVar

    def absolute_url(self, path):
        return urlunsplit(
            ('https', self.headers['Host'], '/'.join([self.stage, path]), '', ''),
        )
