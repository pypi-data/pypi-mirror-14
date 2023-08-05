
"""
aerate.io.mongo.mongo (aerate.io.mongo).

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The actual implementation of the MongoDB data layer.
:copyright: (c) Arable Labs, Inc.
:license: BSD, see LabsICENSE for more details.
"""
from aerate.io.base import DataLayer, ConnectionException, BaseJSONEncoder
from bson.objectid import ObjectId
from aerate.utils import str_to_date
import simplejson as json
import datetime
from pymongo import MongoClient
from aerate.config import config
from falcon import HTTPBadRequest, HTTPNotFound
from aerate.errors import HTTPPreconditionFailed
from aerate.utils import document_etag


class MongoJSONEncoder(BaseJSONEncoder):
    """Proprietary JSONEconder subclass used by the json render function.

    This is needed to address the encoding of special values.
    """

    def default(self, obj):
        """Default encoder behavior."""
        if isinstance(obj, ObjectId):
            # BSON/Mongo ObjectId is rendered as a string
            return str(obj)
        if callable(obj):
            # when SCHEMA_ENDPOINT is active, 'coerce' rule is likely to
            # contain a lambda/callable which can't be jSON serialized
            # (and we probably don't want it to be exposed anyway). See #790.
            return "<callable>"

        # delegate rendering to base class method
        return super(MongoJSONEncoder, self).default(obj)


class Mongo(DataLayer):
    """MongoDB data access layer for Aerate REST API."""

    # Here are some default serializers we will need to use:
    serializers = {
        'objectid': lambda value: ObjectId(value) if value else None,
        'datetime': str_to_date,
        'integer': lambda value: int(value) if value is not None else None,
        'float': lambda value: float(value) if value is not None else None,
        'number': lambda val: json.loads(val) if val is not None else None
    }

    # Here's the set of mongodb operators that queries may be using:
    operators = set(
        ['$gt', '$gte', '$in', '$lt', '$lte', '$ne', '$nin'] +
        ['$or', '$and', '$not', '$nor'] +
        ['$mod', '$regex', '$text', '$where'] +
        ['$options', '$search', '$language'] +
        ['$exists', '$type'] +
        ['$geoWithin', '$geoIntersects', '$near', '$nearSphere'] +
        ['$all', '$elemMatch', '$size']
    )

    def init_driver(self):
        """Initialize the driver."""
        # mongod must be running or this will raise an exception
        self.driver = self.pymongo()
        self.mongo_prefix = None

    def retrieve(self, res, req, **lookup):
        """Retrieve a set of objects that match the lookup query.

        :param res: resource object.
        :param req: a :class:`~falcon.Request` instance or subclass.
        :param **lokup: lookup query as a dictionary.
        """
        return self.pymongo()[res.datasource].find(lookup)

    def retrieve_one_raw(self, res, _id):
        """Retrieve a single raw document.

        :param res: resource object.
        :param _id: unique id.
        .. versionchanged:: 0.6
           Support for multiple databases.
        .. versionadded:: 0.4
        """
        return self.pymongo()[res.datasource].find_one({res.id_field: _id})

    def retrieve_one(self, res, req, **lookup):
        """Retrieve a single document.

        :param resource: resource name.
        :param req: a :class:`falcon.Request` instance.
        :param **lookup: lookup query as a dictionary.
        """
        return self.pymongo()[res.datasource].find_one(lookup)

    def create(self, res, obj):
        """Create a document."""
        if config.CREATED:
            if type(obj) is dict:
                obj[config.CREATED] = datetime.datetime.now()
            elif type(obj) is list:
                for item in obj:
                    item[config.CREATED] = datetime.datetime.now()

        return self.pymongo()[res.datasource].insert(obj)

    def update(self, res, obj, _id, etag=None):
        """Update a database document."""
        if isinstance(obj, list):
            msg = 'cannot update multiple objects'
            raise HTTPBadRequest('RequestError', msg)
        _obj = self.pymongo()[res.datasource].find_one({res.id_field: _id})
        if _obj:
            if config.IF_MATCH:
                if not etag == document_etag(_obj, encoder=res.encoder):
                        raise HTTPPreconditionFailed('If-Match')
            if config.UPDATED:
                    obj[config.UPDATED] = datetime.datetime.now()
            document = self.pymongo()[res.datasource].update(
                {res.id_field: _id}, {'$set': obj})
            return document
        else:
            raise HTTPNotFound

    def pymongo(self):
        """Return the PyMongo instance.

        The instance is stored in self.driver.
        In the future, we may need multiple instances, in which case, this
        function can be refactored to return the appropriate PyMongo
        instance depending on the resource, etc...
        """
        if not self.driver:
            try:
                # instantiate and add to cache
                self.driver = self.PyMongo()
            except Exception as e:
                raise ConnectionException(e)
            return self.driver
        return self.driver[config.MONGO_DBNAME]

    def PyMongo(self):
        """Define the pymongo object."""
        return MongoClient(
            host=config.MONGO_HOST,
            port=config.MONGO_PORT
        )
