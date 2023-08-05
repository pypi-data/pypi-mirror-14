"""Middleware tests for Aerate."""
from aerate.tests import TestBase
from aerate.tests.test_fixtures import PetCollection, PetItem
from aerate import Aerate
from falcon import testing as test
from falcon import Request, Response
from falcon import HTTP_404, HTTP_200
import json


class TestMiddleware(TestBase):
    """Middleware Test Class."""

    def setUp(self):
        """Test setup."""
        super(TestMiddleware, self).setUp()
        from aerate.auth import BasicAuth
        from aerate.validate import Validate
        self.validate = Validate()
        self.app = Aerate(
            spec_file='./aerate/tests/petstore_simple.json',
            auth=[BasicAuth()]
        )
        self.resource = PetCollection(definition='Pet')
        self.item_resource = PetItem(definition='Pet')
        self.app.add_resource(self.resource)
        self.valid = {'name': 'fido', 'id': 23, 'tag': 'this tag'}
        self.partial = {'name': 'fido', 'id': 23}
        self.partial_extra = {'name': 'fido', 'extra': 23}
        self.extra = {
            'name': 'fido', 'id': 23, 'tag': 'this tag', 'foo': 'bar'
        }
        self.middleware = self.app.aerate_middleware

    def test_process_resource_returns_true(self):
        """Test that process_resource returns true."""
        env = test.create_environ(
            path='/',
            method='GET',
            body=json.dumps({'sf': 'afad'}),
            headers={'Content-Type': 'application/json'})
        req = Request(env)
        resp = None
        self.assertTrue(
            self.middleware.process_resource(req, resp, self.resource)
        )

    def test_process_resource_raises_server_error_if_no_resource(self):
        """Test that process_resource raises an error if no resource given."""
        env = test.create_environ(
            path='/',
            method='GET',
            body=json.dumps({'sf': 'afad'}),
            headers={'Content-Type': 'application/json'})
        req = Request(env)
        resp = None
        self.assertFalse(self.middleware.process_resource(req, resp, None))

    def test_do_auths_raises_server_error_no_auth_key(self):
        """Test that do auths needs an auth key."""
        env = test.create_environ(
            path='/',
            method='BAD_METHOD',
            body=json.dumps({'sf': 'afad'}),
            headers={'Content-Type': 'application/json'})
        req = Request(env)
        resp = None
        self.assertRaises(
            ValueError,
            self.middleware.do_auths,
            req, resp, self.resource, None
        )

    def test_do_auths_passes_if_request_is_not_in_auth_map(self):
        """Test that do_auths is okay if no auth required."""
        env = test.create_environ(
            path='/',
            method='GET',
            body=json.dumps({'sf': 'afad'}),
            headers={'Content-Type': 'application/json'})
        req = Request(env)
        resp = None
        self.assertTrue(
            self.middleware.do_auths(
                req, resp, self.item_resource, key='GET'
            )
        )

    def test_process_response_not_found(self):
        """Process response cannot find a resource.

        The server said there was an error,
        no need to create an etag
        """
        resp = Response()
        resp.status = HTTP_404
        self.middleware.process_response(None, resp, self.item_resource)
        self.assertIsNone(resp.etag)

    def test_process_response_no_body(self):
        """Process response does not have a body.

        The server said the response is good but there is no body
        """
        resp = Response()
        resp.status = HTTP_200
        self.middleware.process_response(None, resp, self.item_resource)
        self.assertIsNone(resp.etag)

    def test_process_response_etag(self):
        """Process response has an etag."""
        resp = Response()
        resp.body = json.dumps({'sf': 'afad'})
        resp.status = HTTP_200
        self.middleware.process_response(
            None, resp, self.item_resource)
        self.assertIsNotNone(resp.etag)
