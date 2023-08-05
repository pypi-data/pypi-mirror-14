"""
aerate.io.base.

    Standard interface implemented by Aerate data layers.
    :copyright: (c) 2016 by Arable Labs, Inc.
    :license: BSD, see LICENSE for more details.
"""
import simplejson as json
import datetime
from aerate.utils import date_to_str


class BaseJSONEncoder(json.JSONEncoder):
    """Proprietary JSONEconder subclass used by the json render function.

    This is needed to address the encoding of special values.
    """

    def default(self, obj):
        """Default JSONEncoder."""
        if isinstance(obj, datetime.datetime):
            # convert any datetime to RFC 1123 format
            return date_to_str(obj)
        elif isinstance(obj, (datetime.time, datetime.date)):
            # should not happen since the only supported date-like format
            # supported at dmain schema level is 'datetime' .
            return obj.isoformat()
        elif isinstance(obj, set):
            # convert set objects to encodable lists
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class ConnectionException(Exception):
    """Raise when DataLayer subclasses cannot find/activate a db connection.

    :param driver_exception: the original exception raised by the source db
                             driver
    """

    def __init__(self, driver_exception=None):
        """Initialize the class object."""
        self.driver_exception = driver_exception

    def __str__(self):
        """String representation of the class object."""
        msg = ("Error initializing the driver. Make sure the database server"
               "is running. ")
        if self.driver_exception:
            msg += "Driver exception: %s" % repr(self.driver_exception)
        return msg


class DataLayer(object):
    """Create a base data layer class.

    Defines the interface that actual data-access
    classes, being subclasses, must implement.

    """

    def __init__(self):
        """Initialize the object."""
        self.driver = None
        self.init_driver()

    def init_driver(self):
        """Initialize the db driver."""
        raise NotImplementedError

    def filter(self, resource, req, **kwargs):
        """Create a filter for queries to the datalayer."""
        raise NotImplementedError

    def retrieve(self, resource, req):
        """Retrieve a set of documents (rows), matching the current request.

        Consumed when a request hits a collection/document endpoint
        (`/pets/`).
        :param resource: resource being accessed. You should then use
                         the ``datasource`` helper function to retrieve both
                         the db collection/table and base query (filter), if
                         any.
        :param req: an instance of ``aerate.utils.ParsedRequest``. Contains
                    all the constraints that must be fulfilled in order to
                    satisfy the original request (where and sort parts, paging,
                    etc). Be warned that `where` and `sort` expresions will
                    need proper parsing, according to the syntax that you want
                    to support in your driver. For example ``aerate.io.Mongo``
                    supports both Python and Mongo-like query syntaxes.
        """
        raise NotImplementedError

    def retrieve_list_of_ids(self, resource, ids):
        """Retrieve a list of documents based on a list of primary keys.

        The primary key is the field defined in `ID_FIELD`.
        This is a separate function to allow us to use per-database
        optimizations for this type of query.
        :param resource: resource name.
        :param ids: a list of ids corresponding to the documents
        to retrieve
        :return: a list of documents matching the ids in `ids` from the
        collection specified in `resource`
        """
        raise NotImplementedError

    def retrieve_one(self, resource, **lookup):
        """Retrieve a single document/record.

        Consumed when a request hits an item endpoint (`/pets/{id}/`).
        :param resource: resource being accessed. You should then use the
                         ``datasource`` helper function to retrieve both the
                         db collection/table and base query (filter), if any.
        :param **lookup: the lookup fields. This will most likely be a record
                         id or, if alternate lookup is supported by the API,
                         the corresponding query.
        """
        raise NotImplementedError

    def retrieve_one_raw(self, resource, _id):
        """Retrieve a single, raw document/record.

        No projections or datasource filters are being applied here.
        Just looking up the document by unique id.
        :param resource: resource name.
        :param id: unique id.
        """
        raise NotImplementedError

    def create(self, resource, doc_or_docs):
        """Create a document into a resource collection/table.

        :param resource: resource being accessed. You should then use
                         the ``datasource`` helper function to retrieve both
                         the actual datasource name.
        :param doc_or_docs: json document or list of json documents to be added
                            to the database.
        .. versionchanged:: 0.0.6
            'document' param renamed to 'doc_or_docs', making support for bulk
            inserts apparent.
        """
        raise NotImplementedError

    def update(self, resource, id_, updates, original):
        """Update a collection/table document/row.

        :param resource: resource being accessed. You should then use
                         the ``datasource`` helper function to retrieve
                         the actual datasource name.
        :param id_: the unique id of the document.
        :param updates: json updates to be performed on the database document
                        (or row).
        :param original: definition of the json document that should be
        updated.
        :raise OriginalChangedError: raised if the database layer notices a
        change from the supplied `original` parameter.
        """
        raise NotImplementedError

    def replace(self, resource, id_, document, original):
        """Replace a collection/table document/row.

        :param resource: resource being accessed. You should then use
                         the ``datasource`` helper function to retrieve
                         the actual datasource name.
        :param id_: the unique id of the document.
        :param document: the new json document
        :param original: definition of the json document that should be
        updated.
        :raise OriginalChangedError: raised if the database layer notices a
        change from the supplied `original` parameter.
        """
        raise NotImplementedError

    def delete_one(self, resource, id_):
        """Delete a document/row from a database collection/table.

        :param resource: resource being accessed. You should then use
                         the ``datasource`` helper function to retrieve
                         the actual datasource name.
        :param id_: the unique id of the document.

        """
        raise NotImplementedError

    def delete(self, resource, lookup={}):
        """Delete a set of documents/rows from a database collection/table.

        :param resource: resource being accessed. You should then use
                         the ``datasource`` helper function to retrieve
                         the actual datasource name.
        :param lookup: a dict with the query that documents must match in order
                       to qualify for deletion. For single document deletes,
                       this is usually the unique id of the document to be
                       removed.
        """
        raise NotImplementedError
