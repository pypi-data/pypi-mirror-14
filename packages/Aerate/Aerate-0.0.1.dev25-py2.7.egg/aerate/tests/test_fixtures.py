"""Text Fixtures for Aerate."""
from aerate import ResourceCollection, ResourceItem
from aerate.io import DataLayer

middleware = []
app_config = {}


class TestMiddleware():
    """Define TestMiddleware class."""

    def process_request(self, req, resp, **kwargs):
        """Process request."""
        pass


class FakeDb(DataLayer):
    """Define FakeDb class."""

    def init_driver(self):
        """Initialize Db Driver."""
        pass


class PetCollection(ResourceCollection):
    """Define PetCollection object."""

    def on_get(self, req, resp):
        """Fake HTTP GET responder."""
        return 'on_get for {0}'.format(self.__class__.__name__)

    def on_post(self, req, resp):
        """Fake HTTP POST responder."""
        return 'on_post for {0}'.format(self.__class__.__name__)

    def validate_on_get(self, req, resp, **kwargs):
        """Validate GET Requests."""
        """
        Should be defined in resource with app-specific validation rules.
        Returns True if the object is validated successfully, or raises a
        ValidationError if not.
        """
        return False


class PetItem(ResourceItem):
    """Define PetItem object."""

    def on_get(self, req, resp, id):
        """Fake HTTP GET responder."""
        return 'on_get for {0} with id {1}'.format(
            self.__class__.__name__, id)

    def authorize_on_get(self, req, resp, **kwargs):
        """Authorize GET Requests."""
        return True

    def on_delete(self, req, resp, id):
        """Fake HTTP DELETE responder."""
        return 'on_delete for {0} with id {1}'.format(
            self.__class__.__name__, id)


class Foo(ResourceItem):
    """Define Foo objects."""

    def on_get(self, req, resp, id):
        """Fake HTTP GET responder."""
        return 'on_get for {0} with id {1}'.format(
            self.__class__.__name__, id)


class XXX(ResourceItem):
    """Define XXX Object."""

    def on_post(self, req, resp, id):
        """Fake HTTP POST responder."""
        return 'on_get for {0} with id {1}'.format(
            self.__class__.__name__, id)


class TestAuthorize(ResourceItem):
    """Define TestAuthorize object."""

    def on_post(self, req, resp, id):
        """Fake HTTP POST responder."""
        return 'on_get for {0} with id {1}'.format(
            self.__class__.__name__, id)

    def authorize_on_post(self):
        """Authorize POST requests."""
        return 'after_on_get for {0} with id {1}'.format(
            self.__class__.__name__, id)
