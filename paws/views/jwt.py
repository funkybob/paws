import jwt

from paws.response import response

import logging
log = logging.getLogger(__name__)


class JWTMixin:
    CERT = ''
    AUDIENCE = ''
    ALGORITHMS = ['RS256']

    def dispatch(self, request, **kwargs):
        hdr = request.headers.get('Authorization', '')
        if not hdr.startswith('Bearer '):
            return self.handle_no_token(request, **kwargs)

        bearer = hdr.split(' ', 1)[1].strip()
        try:
            request.jwt = jwt.decode(bearer, **self.get_jwt_decode_kwargs(request, **kwargs))
        except jwt.DecodeError as err:
            log.info('Invalid token: %s', err)
            return self.handle_invalid_token(request, err, **kwargs)

        self.handle_valid_token(request, **kwargs)

        return super().dispatch(request, **kwargs)

    def get_jwt_decode_kwargs(self, request, **kwargs):
        return {
            'key': self.CERT,
            'algorithms': self.ALGORITHMS,
            'audience': self.AUDIENCE,
        }

    def handle_no_token(self, request, **kwargs):
        return response('No token provided', status=403)

    def handle_invalid_token(self, request, err, **kwargs):
        return response('Invalid token', status=403)

    def handle_valid_token(self, request, **kwargs):
        pass
