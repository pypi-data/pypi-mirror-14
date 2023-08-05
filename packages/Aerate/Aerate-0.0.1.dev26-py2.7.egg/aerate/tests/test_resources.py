from aerate.tests import TestBase
from aerate.tests.test_fixtures import PetCollection
from aerate import Aerate


class TestResources(TestBase):

    def setUp(self):
        super(TestResources, self).setUp()
        from aerate.auth import BasicAuth
        self.app = Aerate(
            spec_file='./aerate/tests/petstore_simple.json',
            auth=[BasicAuth()]
        )

    # def test_validate_function_args(self):
    #     self.resource = PetCollection(definition='Pet')
    #     self.app.add_resource(self.resource)
    #     op = type('Operation', (object,), {'http_method': ''})()
    #     self.assertRaises(
    #         ValueError,
    #         self.resource._validate_function_args,
    #         op)

    def test_spec_is_empty_on_resource_init(self):
        self.resource = PetCollection(definition='Pet')
        self.assertTrue(self.resource.schema is None)

    def test_spec_is_preserved_if_set_on_resource_init(self):
        expected = {'test': 'item'}
        self.resource = PetCollection(definition='Pet', schema=expected)
        self.app.add_resource(self.resource)
        self.assertTrue(self.resource.schema == expected)

    def test_add_resource_is_set_by_add_resource(self):
        self.resource = PetCollection(definition='Pet')
        self.app.add_resource(self.resource)
        self.assertTrue(
            self.resource.schema == self.app.spec_dict['definitions']['Pet'])

    def test_resource_initialization_sets_definition_with_argument(self):
        self.resource = PetCollection(definition='Tiger')
        self.assertTrue(self.resource.definition == 'Tiger')

    def test_add_resource_sets_http_methods(self):
        self.resource = PetCollection(definition='Pet')
        self.assertTrue(not self.resource.methods)
        self.app.add_resource(self.resource)
        self.assertTrue(len(self.resource.methods) > 0)

    def test_kwargs_added_to_resource_on_init(self):
        self.resource = PetCollection(definition='Pet', foo='bar')
        self.assertTrue(self.resource.foo == 'bar')
