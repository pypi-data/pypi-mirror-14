"""
aerate.utils.

Utility functions for the Aerate module.

"""
from datetime import datetime
from aerate.config import config
import hashlib
import logging
from copy import copy
from bson.json_util import dumps
from aerate import RFC1123_DATE_FORMAT


def date_to_rfc1123(date):
    """Convert a datetime value to the corresponding RFC-1123 string.

    :param date: the datetime value to convert.
    """
    return datetime.strftime(date, RFC1123_DATE_FORMAT) if date else None


def date_to_str(date):
    """Convert a datetime object into the configuration file format.

    :param date: the datetime value to convert.
    """
    return datetime.strftime(date, config.DATE_FORMAT) if date else None


def str_to_date(string):
    """Convert a date string to datetime.

    date string must be formatted as defined in the configuration
    to the corresponding datetime value.
    :param string: the RFC-1123 string to convert to datetime value.
    """
    return datetime.strptime(string, config.DATE_FORMAT) if string else None


def document_etag(value, ignore_fields=None, encoder=None):
    """Compute and return a valid ETag for the input value.

    :param value: the value to compute the ETag with.

    :param ignore_fields: `ignore_fields` list of fields to skip to
                          compute the ETag value.

    :param encoder: JSON encoder to use. Defaults to config.json_encoder
    """
    from aerate.io import BaseJSONEncoder
    json_encoder_class = encoder or BaseJSONEncoder
    if ignore_fields:
        if not isinstance(ignore_fields, list):
            ignore_fields = [ignore_fields]

        def filter_ignore_fields(d, fields):
            # recursive function to remove the fields that they are in d,
            # field is a list of fields to skip or dotted fields to look up
            # to nested keys such as  ["foo", "dict.bar", "dict.joe"]
            for field in fields:
                key, _, value = field.partition(".")
                if value:
                    filter_ignore_fields(d[key], [value])
                elif field in d:
                    d.pop(field)
                else:
                    # not required fields can be not present
                    pass

        value_ = copy(value)
        filter_ignore_fields(value_, ignore_fields)
    else:
        value_ = value

    h = hashlib.sha1()
    json_encoder = json_encoder_class()
    h.update(dumps(value_, sort_keys=True,
                   default=json_encoder.default).encode('utf-8'))
    return h.hexdigest()

log = logging.getLogger(__name__)

# TODO: Set logging level based on config
log.setLevel(logging.ERROR)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
log.addHandler(handler)
