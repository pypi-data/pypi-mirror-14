"""Test Client for Aerate."""
import pytest
from aerate import Aerate
from aerate.auth import BasicAuth
from aerate.tests.test_fixtures import PetCollection, PetItem

application = Aerate(
    spec_file='./aerate/tests/petstore_simple.json',
    middleware=[],
    auth=[BasicAuth()]
)

application.add_resource(PetItem(datasource='pets', definition='Pet'))
application.add_resource(PetCollection(datasource='pets', definition='Pet'))


@pytest.fixture
def app():
    """App fixture for tests."""
    return application


def test_get(client):
    """Test the aerate client."""
    class Resource:

        def on_get(self, req, resp, **kwargs):
            resp.body = '{"foo": "bar"}'

    application.add_r('/route', Resource())

    resp = client.get('/route')
    assert resp.status == falcon.HTTP_OK
    assert resp.json['foo'] == 'bar'
