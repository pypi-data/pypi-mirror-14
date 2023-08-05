"""Aerate Validation Tests."""

from aerate.tests import TestBase
from aerate.tests.test_fixtures import PetCollection
from aerate import Aerate
from falcon import HTTPBadRequest, HTTPError
from falcon import testing as test
from aerate.validate import validate_partial_object
from aerate.validate import validate_object
from aerate.validate import validate_headers
from falcon import Request
import json
from aerate.config import config
from aerate.errors import HTTPPreconditionRequired


class TestValidation(TestBase):
    """TestValidation Suite."""

    def setUp(self):
        """Test Setup."""
        super(TestValidation, self).setUp()
        from aerate.auth import BasicAuth
        from aerate.validate import Validate
        self.validate = Validate()
        self.app = Aerate(
            spec_file='./aerate/tests/petstore_simple.json',
            auth=[BasicAuth()]
        )
        self.resource = PetCollection(definition='Pet')
        self.app.add_resource(self.resource)
        self.valid = {'name': 'fido', 'id': 23, 'tag': 'this tag'}
        self.partial = {'name': 'fido', 'id': 23}
        self.partial_extra = {'name': 'fido', 'extra': 23}
        self.extra = {
            'name': 'fido', 'id': 23, 'tag': 'this tag', 'foo': 'bar'
        }

    def test_resource_spec_in_res_object(self):
        """Test that resource specification is in the resource object."""
        self.assertTrue(getattr(self.resource, 'schema') is not None)

    def test_validate_object_passes(self):
        """Test that the validation object is okay."""
        self.assertTrue(validate_object(self.resource.schema, self.valid))

    def test_validate_object_list_passes(self):
        """Test that a validation object list passes."""
        obj = [self.valid, self.valid]
        self.assertTrue(validate_object(self.resource.schema, *obj))

    def test_validate_object_fails_with_missing_field(self):
        """Test missing fields."""
        self.assertRaises(
            HTTPBadRequest,
            validate_object,
            self.resource.schema,
            self.partial)

    def test_validate_partial_object_fails_with_extra_field(self):
        """Test partial object with extra fields."""
        self.assertRaises(
            HTTPBadRequest,
            validate_partial_object,
            self.resource.schema,
            self.extra)

    def test_validate_partial_object_list_fails_with_extra_field(self):
        """Test Partial object list with extra fields."""
        obj = [self.valid, self.partial_extra]
        self.assertRaises(
            HTTPBadRequest,
            validate_partial_object,
            self.resource.schema,
            *obj)

    def test_validate_partial_object_passes(self):
        """Test parital object passes."""
        self.assertTrue(
            validate_partial_object(self.resource.schema, self.partial)
        )

    def test_validate_partial_object_list_passes(self):
        """Test list of partial object passes."""
        obj = [self.partial, self.partial]
        self.assertTrue(validate_partial_object(self.resource.schema, *obj))

    def test_validate_object_fails_with_extra_field(self):
        """Test that a object fails validation with an extra field."""
        self.assertRaises(
            HTTPBadRequest,
            validate_object,
            self.resource.schema,
            self.extra)

    def test_validate_object_list_fails_with_extra_field(self):
        """Test that a list of objects fails validation with an extra field."""
        self.assertRaises(
            HTTPBadRequest,
            validate_object,
            self.resource.schema,
            *[self.valid, self.extra])

    def test_validate_calls_validate_object_on_post(self):
        """Test that we call validate_object on POST requests."""
        obj = self.valid
        env = test.create_environ(
            path='/',
            method='POST',
            body=json.dumps(obj),
            headers={
                'Content-Type': 'application/json',
                'If-Match': 'someetagvalue'
            }
        )
        req = Request(env)
        resp = None
        self.assertTrue(self.validate(req, resp, self.resource))

    def test_validate_returns_bad_request_if_no_body(self):
        """Test that empty bodies are bad requests."""
        self.env = test.create_environ(
            path='/',
            method='POST',
            body=None,
            headers={'Content-Type': 'application/json'})
        self.req = Request(self.env)
        self.resp = None
        self.assertRaises(
            HTTPBadRequest,
            self.validate,
            self.req,
            self.resp,
            self.resource
        )

    def test_validate_returns_bad_request_if_content_type_isnt_json(self):
        """Test that validation returns bad request if there is no JSON."""
        env = test.create_environ(
            path='/',
            method='POST',
            body=None,
            headers={'Content-Type': 'not/text'})
        req = Request(env)
        resp = None
        self.assertRaises(
            HTTPError,
            self.validate,
            req,
            resp,
            self.resource
        )

    def test_validate_returns_malformed_json_if_body_isnt_json(self):
        """Test that validation returns bad JSON if that is what it gets."""
        env = test.create_environ(
            path='/',
            method='POST',
            body='{sf:afad,}{s}',
            headers={'Content-Type': 'application/json'})
        req = Request(env)
        resp = None
        self.assertRaises(
            HTTPError,
            self.validate,
            req,
            resp,
            self.resource
        )

    def test_resource_function_validate_on_get_returns_false(self):
        """Test that resource functions fail validation by default."""
        env = test.create_environ(
            path='/',
            method='GET',
            body=json.dumps({'sf': 'afad'}),
            headers={'Content-Type': 'application/json'})
        req = Request(env)
        resp = None
        self.assertFalse(self.validate(req, resp, self.resource))

    def test_validate_returns_true_if_method_is_head(self):
        """Test the Validation doesn't happen on HEAD."""
        env = test.create_environ(
            path='/',
            method='HEAD',
            body=json.dumps({'sf': 'afad'}),
            headers={'Content-Type': 'application/json'})
        req = Request(env)
        resp = None
        self.assertTrue(self.validate(req, resp, self.resource))

    def test_validate_returns_true_if_method_is_delete(self):
        """Test that validation doesn't happen on DELETE."""
        env = test.create_environ(
            path='/',
            method='DELETE',
            body=json.dumps({'sf': 'afad'}),
            headers={'Content-Type': 'application/json'})
        req = Request(env)
        resp = None
        self.assertTrue(self.validate(req, resp, self.resource))

    def test_validate_post_bad_content_type_raises_httperror(self):
        """Test that bad content type raise error on POST."""
        env = test.create_environ(
            path='/',
            method='POST',
            body=json.dumps({'sf': 'afad'}),
            headers={'Content-Type': 'application/xml'})
        req = Request(env)
        resp = None
        self.assertRaises(
            HTTPError,
            validate_headers,
            req, resp, self.resource
        )

    def test_validate_put_bad_content_type_raises_httperror(self):
        """Test that bad content type raise error on PUT."""
        env = test.create_environ(
            path='/',
            method='PUT',
            body=json.dumps({'sf': 'afad'}),
            headers={'Content-Type': 'application/xml'})
        req = Request(env)
        resp = None
        self.assertRaises(
            HTTPError,
            validate_headers,
            req, resp, self.resource
        )

    def test_validate_patch_bad_content_type_raises_httperror(self):
        """Test that bad content type raise error on PATCH."""
        env = test.create_environ(
            path='/',
            method='PATCH',
            body=json.dumps({'sf': 'afad'}),
            headers={'Content-Type': 'application/xml'})
        req = Request(env)
        resp = None
        self.assertRaises(
            HTTPError,
            validate_headers,
            req, resp, self.resource
        )

    def test_validate_headers_with_no_if_match(self):
        """Test that we ignore If-Match if not set in config."""
        env = test.create_environ(
            path='/',
            method='POST',
            body=json.dumps({'sf': 'afad'}),
            headers={'Content-Type': 'application/json'})
        req = Request(env)
        resp = None
        config.IF_MATCH = None
        self.assertTrue(validate_headers(req, resp, self.resource))

    def test_validate_headers_raises_precondition_required_on_put(self):
        """Test that we raise an error if If-Match missing and required."""
        env = test.create_environ(
            path='/',
            method='PUT',
            body=json.dumps({'sf': 'afad'}),
            headers={'Content-Type': 'application/json'})
        req = Request(env)
        resp = None
        config.IF_MATCH = 'If-Match'
        self.assertRaises(
            HTTPPreconditionRequired,
            validate_headers,
            req,
            resp,
            self.resource)

    def test_validate_headers_raises_precondition_required_on_patch(self):
        """Test that we raise an error if If-Match missing and required."""
        env = test.create_environ(
            path='/',
            method='PATCH',
            body=json.dumps({'sf': 'afad'}),
            headers={'Content-Type': 'application/json'})
        req = Request(env)
        resp = None
        config.IF_MATCH = 'If-Match'
        self.assertRaises(
            HTTPPreconditionRequired,
            validate_headers,
            req,
            resp,
            self.resource)

    def test_validate_headers_doesnt_raise_precondition_required_on_post(self):
        """Test that we don't raise error if If-Match missing and required."""
        env = test.create_environ(
            path='/',
            method='POST',
            body=json.dumps({'sf': 'afad'}),
            headers={'Content-Type': 'application/json'})
        req = Request(env)
        resp = None
        config.IF_MATCH = 'If-Match'
        result = validate_headers(req, resp, self.resource)
        self.assertTrue(result)

    def test_validate_bad_content_type_no_httperror_get(self):
        """Test that bad content type headers will pass on GET."""
        env = test.create_environ(
            path='/',
            method='GET',
            headers={'Content-Type': 'application/xml'})
        req = Request(env)
        resp = None
        self.assertTrue(validate_headers(req, resp, self.resource))

    def test_validate_bad_content_type_no_httperror_delete(self):
        """Test that bad content type headers will pass on DELETE."""
        env = test.create_environ(
            path='/',
            method='DELETE',
            headers={'Content-Type': 'application/xml'})
        req = Request(env)
        resp = None
        self.assertTrue(validate_headers(req, resp, self.resource))

    def test_validate_content_type_with_charset(self):
        """Test content type headers with
        extraneous params will pass on POST."""
        env = test.create_environ(
            path='/',
            method='POST',
            body=json.dumps({'sf': 'afad'}),
            headers={'Content-Type': 'application/json;charset=UTF-8'})
        req = Request(env)
        resp = None
        self.assertTrue(validate_headers(req, resp, self.resource))

    def test_resources_can_overload_validation_methods(self):
        """Test that we can overload a validation method."""
        env = test.create_environ(
            path='/',
            method='GET',
            headers={'Content-Type': 'application/json'})
        req = Request(env)
        resp = None
        # Re-assign PetCollection.validate_on_get to new function:
        on_get_fun = lambda req, resp: 'bar'
        setattr(self.resource, 'validate_on_get', on_get_fun)
        # Now PetCollection.validate_on_get returns 'bar':
        result = self.resource.validate(req.method)(req, resp)
        self.assertTrue(result == 'bar')
