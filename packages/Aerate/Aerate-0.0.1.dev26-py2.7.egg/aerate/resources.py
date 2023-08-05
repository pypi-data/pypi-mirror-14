"""
aerate.resources.

~~~~~~~~~~~~~~~~
    Implements ResourceCollection and ResourceItem for use in
    defining Falcon routes.

    The ResourceItem must be subclassed in a user's application

    :copyright: (c) 2016 by Kelly Caylor.
    :license: BSD, see LICENSE for more details.
"""
from aerate.config import config
from aerate.utils import log
from aerate.validate import validate_object, validate_partial_object
from aerate.io.mongo import MongoJSONEncoder

METHODS = ['on_get', 'on_post', 'on_put', 'on_delete', 'on_patch', 'on_head']
VERBS = ['get', 'put', 'post', 'delete', 'patch', 'head']
METHOD_ARGS = set(['req', 'resp'])


class Resource(object):
    """Define a Resource object."""

    def __init__(
            self,
            definition=None,
            datasource=None,
            id_field=None,
            schema=None,
            json_encoder=None,
            **kwargs):
        """Initialize a resource object for use in Aerate.

        Resource objects represent entities that exist in the data layer of the
        API. Generally, each resource in the API should be defined in the
        swagger spec in the `definitions` portion of the spec. This spec-level
        definition is then used to validate resource requests to ensure
        that the request objects conform to the API specification.

        Resources will usually map to discrete collections or tables in the
        database engine.

        Static resources should not be added to the API using Resource objects,
        since these resources do not contain either swagger definitions or
        representations on the database.

        param:definition: REQUIRED. This is the name of the resource as
            defined in the swagger spec. For example, in the Swagger
            API petstore example, the definition of a PetItem or
            PetCollection would be 'Pet'

        param:datasource: REQUIRED. This is the name of the collection or
            table that stores resource objects inside the datalayer.

        param:id_field: The record field corresponding to id-based lookups.
            This field is used in the find_one implementation of datalayers,
            allowing direct querying of a resource item using the unique id
            of the resource.

        param:schema: Schema definition of resource. Generally, this should
            be set when a resource is bound to the API, using the definition
            provided in the swagger spec.

        param:json_encoder: Custom JSON encoder for this resource. Must be a
            subclass of :class:`~aerate.io.BaseJSONEncoder`. Defaults to
            :class:`~aerate.io.MongoJSONEncoder`.

        """
        self.content_type = config.CONTENT_TYPE
        self.id_field = id_field or config.ID_FIELD
        self.definition = definition
        for arg in kwargs.keys():
            setattr(self, arg, kwargs[arg])
        # Prevent user overloading of methods
        self.methods = []
        self.schema = schema
        # Set the resource encoder. The default is the MongoJSONEncoder
        self.encoder = json_encoder or MongoJSONEncoder
        self.datasource = datasource
        self.val_dict = {}
        self.auth_dict = {}
        for method in METHODS:
            val_fun = 'validate_' + method
            auth_fun = 'authorize_' + method
            verb = method.split('on_')[-1].upper()
            self.val_dict[verb] = getattr(self, val_fun)
            self.auth_dict[verb] = getattr(self, auth_fun)

    def authorize(self, method):
        """Authorize a method call for this resource."""
        log.info("called authorize in {0} with {1}".format(
            self.__class__, method.upper()))
        auth_fun = 'authorize_on_' + method.lower()
        return getattr(self, auth_fun)

    def validate(self, method):
        """Validate a method call for this resource."""
        log.info("called validate in {0} with {1}".format(
            self.__class__, method.upper()))
        val_fun = 'validate_on_' + method.lower()
        return getattr(self, val_fun)

    def filter(self, req, resp, **kwargs):
        """Filter a response object based on spec-level flags.

        Filter works in a similar fashion as validate; checking object
        fields to confirm that they are defined in the spec, and that
        they are not marked private (x-aerate-private) in the spec before
        returning response objects.
        """
        pass

    def authorize_on_get(self, req, resp, **kwargs):
        """Authorize GET requests.

        Should be defined in resource with app-specific rules
        that update req.context with method-specific authorization results
        """
        pass

    def authorize_on_post(self, req, resp, **kwargs):
        """Authorise POST requests.

        Should be defined in resource with app-specific rules
        that update req.context with method-specific authorization results
        """
        pass

    def authorize_on_patch(self, req, resp, **kwargs):
        """Authorize PATCH requests.

        Should be defined in resource with app-specific rules
        that update req.context with method-specific authorization results
        """
        pass

    def authorize_on_put(self, req, resp, **kwargs):
        """Authorize PUT requests.

        Should be defined in resource with app-specific rules
        that update req.context with method-specific authorization results
        """
        pass

    def authorize_on_delete(self, req, resp, **kwargs):
        """Authorize DELETE requests.

        Should be defined in resource with app-specific rules
        that update req.context with method-specific authorization results
        """
        pass

    def authorize_on_head(self, req, resp, **kwargs):
        """Authorize HEAD requests.

        Should be defined in resource with app-specific rules
        that update req.context with method-specific authorization results
        """
        pass

    # Validation functions. Should be over-written as needed by
    # resource-specific implementations.
    def validate_on_get(self, req, resp, **kwargs):
        """Validate GET requests.

        Should be defined in resource with app-specific validation rules.
        Returns True if the object is validated successfully, or raises a
        ValidationError if not.
        """
        return True

    def validate_on_delete(self, req, resp, **kwargs):
        """validate_on_get DELETE requests.

        Should be defined in resource with app-specific validation rules.
        Returns True if the object is validated successfully, or raises a
        ValidationError if not.
        """
        return True

    def validate_on_head(self, req, resp, **kwargs):
        """Validate HEAD requests.

        Should be defined in resource with app-specific validation rules.
        Returns True if the object is validated successfully, or raises a
        ValidationError if not.
        """
        return True

    def validate_on_post(self, req, resp, **kwargs):
        """Validate POST requests.

        Default Aerate validation for POST and PUT requests

        """
        return (
            validate_object(self.schema, *req.context['json'])
        )

    def validate_on_put(self, req, resp, **kwargs):
        """Validate PUT requests.

        Default Aerate validation for POST and PUT requests

        """
        return (
            validate_object(self.schema, *req.context['json'])
        )

    def validate_on_patch(self, req, resp, **kwargs):
        """Validate PATCH requests.

        Default Aerate validation for PATCH requests

        """
        return (
            validate_partial_object(self.schema, *req.context['json'])
        )

    # def on_get(self, req, resp, **kwargs):
    #     raise falcon.HTTPMethodNotAllowed

    # def on_post(self, req, resp, **kwargs):
    #     raise falcon.HTTPMethodNotAllowed

    # def on_put(self, req, resp, **kwargs):
    #     raise falcon.HTTPMethodNotAllowed

    # def on_delete(self, req, resp, **kwargs):
    #     raise falcon.HTTPMethodNotAllowed

    # def on_patch(self, req, resp, **kwargs):
    #     raise falcon.HTTPMethodNotAllowed

    # def _set_definition(self):
    #     return self.get_datasource().title()

    # def get_datasource(self):
    #     import re
    #     match = re.match('^.*(?=Item|Collection)', self.name())
    #     if match:
    #         return match.group(0).lower()
    #     else:
    #         return self.name().lower()

    def name(self):
        """Return a Resource name."""
        return self.__class__.__name__

    def valid_methods(self):
        """Return a list of valid methods for Resource."""
        return self._valid_methods(METHODS)

    def valid_operationIds(self):
        """Return a list of valid operationIds for Resource."""
        return list(
            [str(self.name() + '_' + method) for
                method in self.valid_methods()]
        )

    def _valid_methods(self, m):
        valid = []
        for method in m:
            if getattr(self, method, None):
                valid.append(method)
        return valid

    def _validate_function_args(self, op):
        if not op:
            raise ValueError(
                'No operation to validate {0}'.format(self.name()))
        else:
            return True


class ResourceCollection(Resource):
    """Define a ResourceCollection object.

    ResourceCollections represent groups of database objects. These can be
    either tables (MySQL) or collections (Mongo).
    """

    def __init__(self, **kwargs):
        """Initialize a ResourceCollection object."""
        super(ResourceCollection, self).__init__(**kwargs)
        self.type = 'Collection'


class ResourceItem(Resource):
    """Define a ResourceItem object.

    ResourceItems represent an individual database object. This could be
    either a row (MySQL) or document (Mongo).
    """

    def __init__(self, **kwargs):
        """Initialize a ResourceItem object."""
        super(ResourceItem, self).__init__(**kwargs)
        self.type = 'Item'


class MediaResourceCollection(ResourceCollection):
    """Define a MediaResourceCollection object.

    MediaResourceCollection objects represent groups of binary or
    file-like entities in a database.
    """

    def __init__(self, **kwargs):
        """Initialize a MediaResourceCollection object."""
        super(MediaResourceCollection, self).__init__(**kwargs)


class MediaResourceItem(ResourceItem):
    """Define a MediaResourceItem object.

    A MediaResourceItem object is an individual binary or file-like
    object stored in a database.

    """

    def __init__(self, **kwargs):
        """Initialize a MediaResourceItem object."""
        super(MediaResourceItem, self).__init__(**kwargs)
