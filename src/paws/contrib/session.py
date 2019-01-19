

class Session(dict):
    '''
    Dict which tracks dirty status.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clean = True

    def __setitem__(self, *args, **kwargs):
        super().__setitem__(*args, **kwargs)
        self.clean = False

    def mark_dirty(self):
        self.clean = False


class jwt_session(object):
    '''
    Decorator to add JWT Session support to requests.

    You _MUST_ set the secret!
    '''
    cookie_name = 'session'
    secret = None
    algorithm = 'HS512'

    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):
        import jwt
        if self.cookie_name in request.cookies:
            try:
                value = request.cookies[self.cookie_name].value
                data = jwt.decode(value, self.secret)
                request.session = Session(data)
            except:
                pass
        else:
            request.session = Session()

        resp = self.func(request, *args, **kwargs)
        if not request.session.clean:
            data = dict(request.session)
            value = jwt.encode(request.session, self.secret, algorith=self.algorithm)
            resp.cookies[self.cookie_name] = value
        return resp
