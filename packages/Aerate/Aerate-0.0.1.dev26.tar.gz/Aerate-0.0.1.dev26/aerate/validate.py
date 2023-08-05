"""Validation for Aerate."""
from falcon import HTTP_400, HTTP_753, HTTPBadRequest, HTTPError
from aerate.errors import HTTPPreconditionRequired
import json
from aerate.config import config


class Validate:
    """Define Validation class."""

    def __call__(self, req, resp, res, **kwargs):
        """Set __call__ method for Validate object."""
        if validate_headers(req, resp, res, **kwargs):
            return res.validate(req.method)(req, resp, **kwargs)
        return False

    def __init__(self, req=None, resp=None, resource=None, **kwargs):
        """Initialize Validate object."""
        pass


def validate_partial_object(schema, *objects):
    """Validate a partial object against schema.

    validates partial objects against schema defintion in swagger.
    ensures that all properties in object are contained in the schema def.

    """
    properties = schema['properties'].keys()
    # Make sure all keys in this object are resource schema definition.
    # We do not need to ensure all properties are in the object because
    # PATCH is a partial update.
    msg = ''
    valid = True
    for obj in objects:
        diff = set(obj.keys()) - set(properties)
        if diff:
            valid = False
            msg += str(
                ["{0} in object, but not in schema. ".format(x)
                    for x in diff]
            )
    if msg:
        raise HTTPBadRequest('Validation error', msg)
    return valid


def validate_object(schema, *objects):
    """Validate a complete object against schema.

    validates complete objects against schema defintion in swagger.
    ensures that all properties in object are contained in the schema def,
    and that all properties in the schema def are contained in the object.

    """
    properties = schema['properties'].keys()
    # Make sure there are no differences between the properties in this object
    # and the schema definition.
    msg = ''
    valid = True
    for obj in objects:
        diff = set(obj.keys()).symmetric_difference(set(properties))
        if diff:
            valid = False
            msg += str(["{0} in schema, but not in object. ".format(x)
                        for x in set(properties) - set(obj.keys())])
            msg += str(["{0} in object, but not in schema. ".format(x)
                        for x in set(obj.keys()) - set(properties)])
    if not valid:
        raise HTTPBadRequest('Validation error', msg)
    return valid


def validate_headers(req, resp, res, **kwargs):
    """Validate Request Headers."""
    if req.method in ['GET', 'DELETE', 'HEAD']:
        return True
    if req.method in ['POST', 'PUT', 'PATCH']:
        # Check that content type is correct for this resource:
        if res.content_type not in req.get_header('Content-Type'):
            raise HTTPError(
                HTTP_400,
                'Bad Content-Type Header',
                'Content-Type must be "application/json"')
    if req.method in ['PUT', 'PATCH']:
        # Check that any necessary If-Match headers are provided:
        if config.IF_MATCH and not req.if_match:
            raise HTTPPreconditionRequired('If-Match')

    # TODO: Catch a falcon error on stream.read()
    body = req.stream.read()
    if not body:
        raise HTTPBadRequest(
            'Empty request body',
            'A valid JSON document is required.')
    try:
        req.context['json'] = json.loads(
            body.decode('utf-8'))
        # Make sure all requests are lists for validation
        if type(req.context['json']) is not list:
            req.context['json'] = [req.context['json']]

    except (ValueError, UnicodeDecodeError):
        msg = 'Could not decode the request body. '
        msg += 'The JSON was incorrect or not encoded as UTF-8.'
        raise HTTPError(
            HTTP_753,
            'Malformed JSON', msg)
    return True
