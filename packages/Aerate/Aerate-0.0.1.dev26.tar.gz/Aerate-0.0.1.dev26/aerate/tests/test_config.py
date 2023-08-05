from aerate.tests import TestBase
from aerate.config import config


class TestConfig(TestBase):

    def setUp(self):
        super(TestConfig, self).setUp()
        self.config = config
        self.config.reset()
        self.settings_filename = './aerate/tests/test_settings.py'

    def test_read_settings_from_file(self):
        # Id field should not yet be set:
        self.assertTrue(self.config.get('ID_FIELD') is None)
        # Now read the test_settings.py file:
        self.config.from_pyfile(self.settings_filename)
        self.assertTrue(self.config.get('ID_FIELD') == '_id')

    def test_read_settings_from_bad_file(self):
        # Id field should not yet be set:
        # Now read the test_settings.py file:
        self.assertRaises(
            IOError,
            self.config.from_pyfile,
            'file_not_found'
        )

    def test_config_get_missing_value_is_none(self):
        self.assertTrue(
            isinstance(self.config.get('MISSING_DEFAULT_SETTING'), type(None)))

#    def test_config_keys_returns_list_from_config(self):
#        self.assertTrue(isinstance(self.config.keys(), type(list())))
