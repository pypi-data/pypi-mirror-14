

class SimpleFilter():
    """ A simple spec-based filter for object responses
    """
    def __call__(self, res, req, resp, **kwargs):
        pass


class SimpleValidate():
    """ A simple spec-based validation for requests and responses
    """
    def __call__(self, res, req, resp, **kwargs):
        pass


class SimpleAuthenticate():
    """ A simple spec-based authentication for requests and responses
    """
    def __call__(self, res, req, resp, **kwargs):
        pass
