"""Test the datalayers."""
from aerate.tests import TestBase
from aerate.io.mongo import Mongo, MongoJSONEncoder
from aerate.io import ConnectionException, BaseJSONEncoder
from aerate.config import config
from aerate.resources import Resource
from pymongo import MongoClient
from bson import ObjectId
from falcon import HTTPBadRequest, HTTPNotFound
from aerate.errors import HTTPPreconditionFailed
from aerate.utils import document_etag


class TestDataLayer(TestBase):
    """Test the mongo datalayer."""

    def setUp(self):
        """Set up test."""
        super(TestDataLayer, self).setUp()
        self.pymongo = MongoClient()
        config.from_pyfile('./aerate/tests/test_settings.py')
        self.db = self.pymongo[config.MONGO_DBNAME]
        self.db.pets.drop()
        self.data = Mongo()
        self.resource = Resource(datasource='pets')

    def tearDown(self):
        """Tear down test."""
        super(TestDataLayer, self).tearDown()

    def test_notimplemented_errors(self):
        """Test that NotImplementedErrors are raised."""
        from aerate.tests.test_fixtures import FakeDb
        data = FakeDb()
        self.assertRaises(NotImplementedError, data.create, None, None)
        self.assertRaises(NotImplementedError, data.retrieve_one, None)
        self.assertRaises(
            NotImplementedError, data.retrieve_one_raw, None, None
        )
        self.assertRaises(NotImplementedError, data.retrieve, None, None)
        self.assertRaises(
            NotImplementedError, data.update, None, None, None, None)
        self.assertRaises(NotImplementedError, data.delete, None, None)

    def test_mongo_retrieve_one_raw(self):
        """Test getting a single object in raw format (no filters)."""
        obj = {config.ID_FIELD: ObjectId()}
        _id = self.db.pets.insert(obj)
        found = self.data.retrieve_one_raw(self.resource, _id)
        self.assertTrue(found == obj)

    def test_mongo_init_with_no_config(self):
        """Test initialization with configuration."""
        config.reset()
        self.assertRaises(ConnectionException, Mongo)

    def test_mongo_with_alt_id_field(self):
        """Test creating an object with alternative id field."""
        config.set('ID_FIELD', 'other_id')
        this_id = ObjectId()
        obj = {config.ID_FIELD: this_id}
        self.db.pets.insert(obj)
        self.resource = Resource(id_field=config.ID_FIELD, datasource='pets')
        found = self.data.retrieve_one_raw(self.resource, this_id)
        self.assertTrue(found == obj)

    def test_mongo_create_one(self):
        """Test creating a single object."""
        one_pet = {'name': 'Maebe', 'type': 'dog'}
        a = self.data.create(self.resource, one_pet)
        self.assertTrue(isinstance(a, type(ObjectId())))

    def test_mongo_create_many(self):
        """Test creating a list of objects."""
        two_pets = [
            {'name': 'Maebe', 'type': 'dog'},
            {'name': 'Mimsy', 'type': 'cat'}
        ]
        a = self.data.create(self.resource, two_pets)
        self.assertTrue(len(a) == len(two_pets))

    def test_objects_have_creation_time(self):
        """Test that objects have creation times."""
        config.CREATED = 'created'
        one_pet = {'name': 'Maebe', 'type': 'dog'}
        a = self.data.create(self.resource, one_pet)
        found = self.data.retrieve_one_raw(self.resource, a)
        self.assertTrue(config.CREATED in found)

    def one_test_objects_do_not_have_creation_time_if_created_not_set(self):
        """Test that objects do have creation times."""
        config.CREATED = None
        one_pet = {'name': 'Maebe', 'type': 'dog'}
        a = self.data.create(self.resource, one_pet)
        found = self.data.retrieve_one_raw(self.resource, a)
        self.assertTrue(config.CREATED not in found)

    def many_test_objects_do_not_have_creation_time_if_created_not_set(self):
        """Test that objects do not have creation times."""
        config.CREATED = None
        two_pets = [
            {'name': 'Maebe', 'type': 'dog'},
            {'name': 'Mimsy', 'type': 'cat'}
        ]
        a = self.data.create(self.resource, two_pets)
        for pet in a:
            found = self.data.retrieve_one_raw(self.resource, pet)
            self.assertTrue(config.CREATED not in found)

    def test_mongo_update(self):
        """Test the update function."""
        names = ['pluto', 'goofy']
        obj = {config.ID_FIELD: ObjectId(), 'name': names[0]}
        _id = self.db.pets.insert(obj)
        found = self.data.retrieve_one_raw(self.resource, _id)
        self.assertTrue(found['name'] == names[0])
        update = {'name': names[1]}
        self.data.update(self.resource, update, _id)
        found = self.data.retrieve_one_raw(self.resource, _id)
        self.assertTrue(found['name'] == names[1])

    def test_mongo_update_with_if_match(self):
        """Test the update function using if-match."""
        names = ['pluto', 'goofy']
        config.IF_MATCH = 'If-Match'
        obj = {config.ID_FIELD: ObjectId(), 'name': names[0]}
        _id = self.db.pets.insert(obj)
        update = {'name': names[1]}
        self.assertRaises(
            HTTPPreconditionFailed,
            self.data.update,
            self.resource,
            update,
            _id
        )

    def test_mongo_update_with_bad_id(self):
        """Test the update function with a bad id."""
        names = ['pluto', 'goofy']
        bad_id = 'sdsdgsdg'
        update = {'name': names[1]}
        self.assertRaises(
            HTTPNotFound,
            self.data.update,
            self.resource,
            update,
            bad_id
        )

    def test_mongo_update_with_list(self):
        """Test that update will not work with a list of objects."""
        objs = [{'foo': 'bar'}, {'foo': 'baz'}]
        self.assertRaises(
            HTTPBadRequest,
            self.data.update,
            self.resource,
            objs,
            ObjectId()
        )

    def test_mongo_update_with_good_etag(self):
        """Test that we get a bad update with a bad etag."""
        config.IF_MATCH = 'If-Match'
        names = ['pluto', 'goofy']
        obj = {config.ID_FIELD: ObjectId(), 'name': names[0]}
        _id = self.db.pets.insert(obj)
        found = self.data.retrieve_one_raw(self.resource, _id)
        etag = document_etag(found, encoder=self.resource.encoder)
        update = {'name': names[1]}
        self.data.update(self.resource, update, _id, etag=etag)
        found = self.data.retrieve_one_raw(self.resource, _id)
        self.assertTrue(found['name'] == names[1])

    def test_mongo_update_with_bad_etag(self):
        """Test that we get a bad update with a bad etag."""
        config.IF_MATCH = 'If-Match'
        names = ['pluto', 'goofy']
        obj = {config.ID_FIELD: ObjectId(), 'name': names[0]}
        _id = self.db.pets.insert(obj)
        etag = 'nottherightetag'
        update = {'name': names[1]}
        self.assertRaises(
            HTTPPreconditionFailed,
            self.data.update,
            self.resource,
            update,
            _id,
            etag=etag
        )


class TestBaseJSONEncoder(TestBase):
    """Test the BaseJSONEncoder."""

    def setUp(self):
        """Set up test."""
        super(TestBaseJSONEncoder, self).setUp()
        self.encoder = BaseJSONEncoder()

    def test_BaseJSONEncoder_default_datetime(self):
        """Test datetime objects in default encoder."""
        import datetime
        result = self.encoder.default(datetime.datetime.now())
        self.assertTrue(isinstance(result, str))

    def test_BaseJSONEncoder_default_set(self):
        """Test set objects in default encoder."""
        result = self.encoder.default(set(['a', 'b', 'c']))
        self.assertTrue(isinstance(result, list))


class TestMongoJSONEncoder(TestBase):
    """Test the MongoJSONEncoder."""

    def setUp(self):
        """Set up test."""
        super(TestMongoJSONEncoder, self).setUp()
        self.encoder = MongoJSONEncoder()

    def test_MongoJSONEncoder_default_objectid(self):
        """Test ObjectId objects in default encoder."""
        from bson.objectid import ObjectId
        result = self.encoder.default(ObjectId())
        self.assertTrue(isinstance(result, str))

    def test_MongoJSONEncoder_default_callable(self):
        """Test callable objects in default encoder."""
        result = self.encoder.default(lambda x: x**2)
        self.assertTrue(result == '<callable>')

    def test_MongoJSONEncoder_default_datetime(self):
        """Test datetime objects in Mongo encoder."""
        import datetime
        result = self.encoder.default(datetime.datetime.now())
        self.assertTrue(isinstance(result, str))
