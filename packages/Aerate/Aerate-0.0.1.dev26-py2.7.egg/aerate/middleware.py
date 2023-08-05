"""
Aerate Middleware.

Implements the falcon middleware API with Aerate-specific functionality.

"""
from aerate.auth import AuthProvider
from aerate.utils import log, document_etag
from aerate.validate import validate_headers
from falcon import HTTP_OK
import simplejson as json


class AerateMiddleware(object):
    """Define the AerateMiddleware object."""

    def __init__(self):
        """Initialize an AerateMiddleware object."""
        self.auth_map = {}

    """
    Handles Authorization, and Validation for Aerate
    """
    def process_resource(self, req, resp, resource, **kwargs):
        """Middleware functionality based on request resource object."""
        log.info("called process_resource in AerateMiddleware()")
        if resource:
            key = resource.name() + "_on_" + req.method.lower()
            self.do_auths(req, resp, resource, key=key, **kwargs)
            validate_headers(req, resp, resource, **kwargs)
            resource.validate(req.method)(req, resp, **kwargs)
        else:
            return False
        return True

    def process_response(self, req, resp, resource, **kwargs):
        """Middleware functionality associated with response objects."""
        if HTTP_OK == resp.status:
            if resp.body:
                resp.set_header(
                    'Etag',
                    document_etag(json.loads(resp.body), encoder=resource.encoder)
                )

    def do_auths(self, req, resp, resource, key=None, **kwargs):
        """Middleware functionality to execute Authentication."""
        if not key:
            raise ValueError
        if key in self.auth_map:
            a = AuthProvider(self.auth_map[key])
            a.authenticate(req, resp, **kwargs)
            resource.authorize(req.method)(req, resp, **kwargs)
        return True

    def add_auths(self, key, auth_fns):
        """Middleware functionality to add Authentication."""
        self.auth_map[key] = auth_fns
