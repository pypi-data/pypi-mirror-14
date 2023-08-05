"""HTTP Error Codes for Aerate."""
from falcon.errors import HTTPBadRequest


class HTTPPreconditionRequired(HTTPBadRequest):
    """A precondition is missing from the request.

    Inherits from ``HTTPBadRequest``.
    This error may refer to a required pre-condition, for example the
    need to match and If-Match header with an object ETag prior to updates.

    Args:
        condition_name (str): The name of the pre-condition.
        kwargs (optional): Same as for ``HTTPError``.
    """

    def __init__(self, condition_name, **kwargs):
        """Initialize the error."""
        description = 'The "{0}" precondition is required.'
        description = description.format(condition_name)

        super(HTTPPreconditionRequired, self).__init__(
            'Missing precondition',
            description, **kwargs
        )


class HTTPPreconditionFailed(HTTPBadRequest):
    """A precondition failed in the request.

    Inherits from ``HTTPBadRequest``.
    This error refers to a required pre-condition, for example the
    need to match and If-Match header with an object ETag prior to updates.

    Args:
        condition_name (str): The name of the pre-condition that failed.
        kwargs (optional): Same as for ``HTTPError``.
    """

    def __init__(self, condition_name, **kwargs):
        """Initialize the error."""
        description = 'The "{0}" precondition failed.'
        description = description.format(condition_name)

        super(HTTPPreconditionFailed, self).__init__(
            'Failed precondition',
            description, **kwargs
        )
