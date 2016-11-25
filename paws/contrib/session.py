import jwt


def Session(dict):
    '''
    Dict which tracks dirty status.
    '''
    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)
        self.clean = True

    def __setitem__(self, *args, **kwargs):
        super(Session, self).__setitem__(*args, **kwargs)
        self.clean = False

    def mark_dirty(self):
        self.clean = False


def factory(SECRET, cookie_name='session'):
    '''
    Decorator factory:

    Pass secret for signing JWT, and optionally cookie name.

    Returns a handler decorator for loading/saving session.
    '''

    class with_session(object):
        def __init__(self, func):
            self.func = func

        def __call__(self, request, *args, **kwargs):
            if cookie_name in request.cookies:
                try:
                    request.session = Session(jwt.decode(request.cookies[cookie_name].value, SECRET))
                except:
                    pass
            else:
                request.session = Session()

            resp = self.func(request, *args, **kwargs)
            if not request.session.clean:
                resp.cookies[cookie_name] = jwt.encode(request.session, SECRET, algorith='')
            return resp

    return with_session
