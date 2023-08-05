from falcon import testing as test
from aerate import Aerate
from aerate.config import config


class TestBase(test.TestBase):

    def setUp(self):
        super(TestBase, self).setUp()
        # Create a mock application:
        self.srmock = test.StartResponseMock()
        self.config = config
        self.config.from_pyfile('./aerate/tests/test_settings.py')
        self.app = Aerate(
            spec_file='./aerate/tests/petstore_simple.json',
        )

    def tearDown(self):
        super(TestBase, self).tearDown()

    def simulate_request(self, path, *args, **kwargs):

        env = test.create_environ(
            path=path, **kwargs)
        return self.app(env, self.srmock)

    def simulate_get(self, *args, **kwargs):
        kwargs['method'] = 'GET'
        return self.simulate_request(*args, **kwargs)

    def simulate_post(self, *args, **kwargs):
        kwargs['method'] = 'POST'
        return self.simulate_request(*args, **kwargs)

    def simulate_delete(self, *args, **kwargs):
        kwargs['method'] = 'DELETE'
        return self.simulate_request(*args, **kwargs)
