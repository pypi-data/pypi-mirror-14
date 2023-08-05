from falcon import Request, HTTPUnauthorized
from falcon import testing as test
from aerate import Aerate
from aerate.tests import TestBase
from aerate import Swagger


class TestInitializeAerate(TestBase):

    def setUp(self):
        super(TestInitializeAerate, self).setUp()
        from aerate.tests.test_fixtures import PetCollection, PetItem
        self.pet_collection = PetCollection(definition='Pet')
        self.pet_item = PetItem(definition='Pet')
        self.spec_file = './aerate/tests/petstore_simple.json'
        self.test_app = Aerate(spec_file=self.spec_file)

    def tearDown(self):
        super(TestInitializeAerate, self).tearDown()

    def test_create_aerate(self):
        self.assertTrue(self.test_app)

    def test_add_resource(self):

        self.test_app.add_resource(self.pet_item)

        self.assertTrue(0 < len(self.config.RESOURCES))
        self.assertTrue('PetItem' in self.config.RESOURCES)
        self.assertTrue(0 < len(self.test_app.op_dict))
        self.assertTrue('PetItem_on_get' in self.test_app.op_dict)
        self.assertTrue('PetItem_on_delete' in self.test_app.op_dict)
        self.assertFalse('PetItem_on_update' in self.test_app.op_dict)
        self.assertFalse('PetItem_on_post' in self.test_app.op_dict)

    def test_add_resource_with_middleware(self):
        self._before = ['test_middleware']
        self.test_app.add_resource(self.pet_item)
        self.assertEquals(1, len(self._before))

    def test_add_resource_bad_object(self):
        from aerate.tests.test_fixtures import Foo
        self.assertRaises(
            ValueError,
            self.test_app.add_resource,
            Foo())

    def test_add_resource_http_method_mismatch_with_spec(self):
        # this should fail because XXX contains one http method and the
        # spec specified another
        from aerate.tests.test_fixtures import XXX
        self.assertRaises(
            ValueError,
            self.test_app.add_resource,
            XXX())

    def test_add_resource_with_no_definition_raises_key_error(self):
        self.pet_collection.definition = None
        self.assertRaises(
            KeyError,
            self.test_app.add_resource,
            self.pet_collection)

    def test_add_resource_with_missing_definition_raises_key_error(self):
        self.pet_collection.definition = 'Cabbage'
        self.assertRaises(
            KeyError,
            self.test_app.add_resource,
            self.pet_collection)

    def test_add_resource_with_no_auth_initialized(self):
        self.assertRaises(
            KeyError,
            self.test_app.add_resource,
            self.pet_collection)

    def test_add_resource_with_auth_initialized(self):
        from aerate.auth import BasicAuth
        b = BasicAuth()
        app = Aerate(
            spec_file=self.spec_file,
            auth=[b]
        )
        self.assertTrue(0 == len(app._before))
        app.add_resource(self.pet_collection)
        # Should be one, because we add AerateMiddleware
        self.assertTrue(1 == len(app._middleware))
        self.assertTrue(0 == len(app._before))

    def test_add_auth(self):
        from aerate.auth import BasicAuth
        b = BasicAuth()
        app = Aerate(
            spec_file=self.spec_file,
            auth=[b]
        )
        app.add_resource(self.pet_collection)
        auths = app.swagger._get_security('PetCollection_on_post')
        self.assertEquals(1, len(auths))
        key = "post" + self.pet_collection.name()
        app._add_auths_to_route(key, ['BasicAuth'])
        self.assertEqual(3, len(app.aerate_middleware.auth_map))

    def test_insert_middleware(self):
        from aerate.auth import BasicAuth
        from aerate.middleware import AerateMiddleware
        from aerate.tests.test_fixtures import TestMiddleware
        app = Aerate(
            spec_file=self.spec_file,
            middleware=[TestMiddleware(), TestMiddleware()],
            auth=[BasicAuth()])
        app.add_resource(self.pet_collection)
        # Make sure that the middleware is added:
        self.assertTrue(len(app._middleware) == 3)

    def test_load_spec_returns_value_error(self):
        app = Aerate(spec_file=self.spec_file)
        self.assertRaises(
            ValueError,
            app.load_spec,
            None)

    def test_get_path_name_by_id_returns_key_error(self):
        op_id = 'bad_op_id'
        app = Aerate(spec_file=self.spec_file)
        self.assertRaises(
            KeyError,
            app._get_path_name_by_id,
            op_id
        )

    def test_get_method_by_id_returns_key_error(self):
        op_id = 'bad_op_id'
        app = Aerate(spec_file=self.spec_file)
        self.assertRaises(
            KeyError,
            app._get_method_by_id,
            op_id
        )


class TestSwagger(TestBase):

    def setUp(self):
        super(TestSwagger, self).setUp()

    def test_create_swagger_object(self):
        this_swagger = Swagger()
        self.assertTrue(this_swagger.__class__.__name__ == 'Swagger')

    def test_create_with_none(self):
        swaggerspec = {"swagger": "2.0"}
        # the following does not like SwaggerValidationError for
        # some reason
        self.assertRaises(
            Exception,
            Swagger, swaggerspec)

    def test_create_with_yaml(self):
        swagger_file = './aerate/tests/petstore.yaml'
        this_swagger = Swagger()
        self.assertTrue(this_swagger.load_spec_from_file(swagger_file))

    def test_create_with_bad_extension(self):
        swagger_file = './aerate/tests/petstore.txt'
        this_swagger = Swagger()
        self.assertRaises(
            TypeError,
            this_swagger.load_spec_from_file,
            swagger_file)


class TestAuth(TestBase):

    def setUp(self):
        super(TestAuth, self).setUp()
        from aerate.auth import Auth, AuthProvider
        self.abstract_auth = AuthProvider([Auth()])
        from aerate.tests.test_fixtures import PetItem
        self.pet_item = PetItem(definition='Pet')

    def test_not_implemented_checkauth(self):
        env = test.create_environ(path='/', method='GET')
        req = Request(env)
        req.env['wsgi.authenticated'] = False
        self.assertRaises(
            NotImplementedError,
            self.abstract_auth.authenticate, req, None)

    def test_testing_auth(self):
        env = test.create_environ(path='/', method='GET')
        req = Request(env)
        req.env['wsgi.authenticated'] = False
        from aerate.auth import TestingAuth, AuthProvider
        auth = TestingAuth()
        a = AuthProvider([auth])
        a.authenticate(req, None)
        self.assertTrue(req.env['wsgi.authenticated'])

    def test_first_auth(self):
        env = test.create_environ(path='/', method='GET')
        req = Request(env)
        self.assertFalse('wsgi.authenticated' in req.env)
        from aerate.auth import Auth
        Auth.init_request(req)
        self.assertTrue('wsgi.authenticated' in req.env)
        self.assertTrue(req.env['wsgi.authenticated'] is None)

    def test_last_auth(self):
        env = test.create_environ(path='/', method='GET')
        req = Request(env)
        req.env['wsgi.authenticated'] = True
        from aerate.auth import Auth
        Auth.last_check(req)
        self.assertTrue('wsgi.authenticated' in req.env)
        self.assertTrue(req.env['wsgi.authenticated'])

    def test_last_auth_fail(self):
        env = test.create_environ(path='/', method='GET')
        req = Request(env)
        req.env['wsgi.authenticated'] = False
        from aerate.auth import Auth
        self.assertRaises(
            HTTPUnauthorized,
            Auth.last_check, req)
