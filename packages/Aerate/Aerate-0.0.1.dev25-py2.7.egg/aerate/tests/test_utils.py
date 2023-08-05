"""Test utils.py."""

from aerate.tests import TestBase
from aerate.utils import str_to_date, date_to_str, date_to_rfc1123
from aerate.utils import document_etag
import datetime
import hashlib
from aerate.io import BaseJSONEncoder
from bson.json_util import dumps


class TestUtils(TestBase):
    """Test Utility functions."""

    def setUp(self):
        """Setup Tests."""
        super(TestUtils, self).setUp()

    def test_str_to_date_returns_datetime(self):
        """Test that str_to_date returns a datetime object."""
        datestring = 'Thu, 21 Jan 2016 21:15:56 GMT'
        time = str_to_date(datestring)
        self.assertTrue(isinstance(time, datetime.datetime))

    def test_date_to_str_returns_str(self):
        """Test that date_to_str return a str object."""
        date = datetime.datetime.now()
        str_time = date_to_str(date)
        self.assertTrue(isinstance(str_time, str))

    def test_date_to_rfc1123_returns_str(self):
        """Test that date_to_rfc1123 returns a str object."""
        date = datetime.datetime.now()
        str_time = date_to_rfc1123(date)
        self.assertTrue(isinstance(str_time, str))

    def test_document_etag(self):
        """Test documents_etag function."""
        doc = {'foo': 'bar', 'meh': 'heh'}
        h = hashlib.sha1()
        json_encoder = BaseJSONEncoder
        h.update(dumps(
            doc,
            sort_keys=True,
            default=json_encoder.default
        ).encode('utf-8'))
        expected = h.hexdigest()
        result = document_etag(doc, encoder=json_encoder)
        self.assertTrue(expected == result)

    def test_document_etag_works_with_only_one_item_in_ignore_fields(self):
        """Make sure that a non-list works with ignore_field."""
        doc = {'foo': 'bar', 'meh': 'heh', 'dog': 'pluto'}
        json_encoder = BaseJSONEncoder
        tag = document_etag(
            doc, ignore_fields='dog', encoder=json_encoder)
        self.assertTrue(tag is not None)

    def test_document_etag_handles_dot_notation(self):
        """Test that we can get to sub-fields in a document."""
        doc = {
            'foo': 'bar',
            'meh': 'heh',
            'dog': {
                'name': 'pluto',
                'owner': 'mickey'
            }
        }
        h = hashlib.sha1()
        json_encoder = BaseJSONEncoder
        # Test removing a single key:
        doc_no_dog_owner = {
            'foo': 'bar',
            'meh': 'heh',
            'dog': {'name': 'pluto'}
        }
        h.update(dumps(
            doc_no_dog_owner,
            sort_keys=True,
            default=json_encoder.default
        ).encode('utf-8'))
        expected_no_dog_owner = h.hexdigest()
        result_no_dog_owner = document_etag(
            doc, ignore_fields=['dog.owner'], encoder=json_encoder)
        self.assertTrue(expected_no_dog_owner == result_no_dog_owner)

    def test_document_etag_with_ignored(self):
        """Test that document_etag can ignore fields."""
        doc = {'foo': 'bar', 'meh': 'heh', 'dog': 'pluto'}
        h = hashlib.sha1()
        json_encoder = BaseJSONEncoder
        # Test removing a single key:
        doc_no_dog = {'foo': 'bar', 'meh': 'heh'}
        h.update(dumps(
            doc_no_dog,
            sort_keys=True,
            default=json_encoder.default
        ).encode('utf-8'))
        expected_no_dog = h.hexdigest()
        result_no_dog = document_etag(
            doc, ignore_fields=['dog'], encoder=json_encoder)
        self.assertTrue(expected_no_dog == result_no_dog)
        # Test removing all keys except foo.
        doc_only_foo = {'foo': 'bar'}
        h = hashlib.sha1()
        h.update(dumps(
            doc_only_foo,
            sort_keys=True,
            default=json_encoder.default
        ).encode('utf-8'))
        expected_only_foo = h.hexdigest()
        result_only_foo = document_etag(
            doc, ignore_fields=['dog', 'meh'], encoder=json_encoder)
        self.assertTrue(expected_only_foo == result_only_foo)
