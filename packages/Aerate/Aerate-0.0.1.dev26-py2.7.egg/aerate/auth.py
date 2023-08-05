from falcon import HTTPUnauthorized
from aerate.utils import log


class AuthProvider():

    KEY = 'wsgi.authenticated'

    def __init__(self, auths=[]):
        self.auths = auths

    def authenticate(self, req, resp, **kwargs):
        if 0 < len(self.auths):
            Auth.init_request(req)
            for auth in self.auths:
                log.info('calling authenticate with {0} for {1}'.format(
                    auth.__class__, req.path))
                # iterate through the authenticate providers
                if not req.env[AuthProvider.KEY]:
                    req.env[AuthProvider.KEY] = True and \
                        auth.check_auth(req, resp, **kwargs)

            Auth.last_check(req)


class Auth():

    def check_auth(self, req, resp, **kwargs):
        raise NotImplementedError

    @staticmethod
    def init_request(req):
        req.env[AuthProvider.KEY] = None

    @staticmethod
    def last_check(req):
        if not req.env[AuthProvider.KEY]:
            raise HTTPUnauthorized(
                'Unauthorized.', 'User is not authenticated.'
            )


class BasicAuth(Auth):
    """ Implements BasicAuth for Aerate


    """
    def check_auth(self, req, resp):
        return True


class JWTAuth(Auth):
    """ Implements JWT Token-based Auth for Aerate

    """
    def check_auth(self, req, resp):
        return True


class TestingAuth(Auth):
    """ Implements a testing authentication object with some usefull hooks
    for testing Aerate apps.

    """
    def check_auth(self, req, resp):
        return True
