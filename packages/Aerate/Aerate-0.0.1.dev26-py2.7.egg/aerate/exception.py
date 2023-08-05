
class ValidationException(Exception):
    """ Raised when validate command cannot validate a request object.

    """
    def __init__(self, validate_exception=None):
        self.driver_exception = validate_exception

    def __str__(self):
        reason = "Unknown Reason"
        msg = ("Error validating request: {reason}. ".format(reason=reason))
        if self.driver_exception:
            msg += "Validate exception: %s" % repr(self.driver_exception)
        return msg


class AuthorizationException(Exception):
    """ Raised when authorize command cannot validate a request object.

    """
    def __init__(self, authorize_exception=None):
        self.driver_exception = authorize_exception

    def __str__(self):
        reason = "Unknown Reason"
        msg = ("Error authorizing request: {reason}. ".format(reason=reason))
        if self.driver_exception:
            msg += "Authorize exception: %s" % repr(self.driver_exception)
        return msg


class FilterException(Exception):
    """ Raised when filter command cannot validate a request object.

    """
    def __init__(self, filter_exception=None):
        self.driver_exception = filter_exception

    def __str__(self):
        reason = "Unknown Reason"
        msg = ("Error filtering request: {reason}. ".format(reason=reason))
        if self.driver_exception:
            msg += "Filter exception: %s" % repr(self.driver_exception)
        return msg
