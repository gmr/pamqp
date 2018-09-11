# -*- encoding: utf-8 -*-
from datetime import datetime
from decimal import Decimal
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pamqp import encode, decode
from pamqp import PYTHON3

if PYTHON3:
    long = int


def to_bytes(value):
    if isinstance(value, bytes):
        return bytes
    if PYTHON3:
        return bytes(value, 'utf-8')
    return bytes(value)


class EncodeDecodeTests(unittest.TestCase):

    def test_encode_decode_field_table_long_keys(self):
        """Encoding and decoding a field_table with too long keys."""
        # second key is 126 A's + \N{PILE OF POO}
        data = {'A' * 256: 1,
                ((b'A' * 128) + b'\xf0\x9f\x92\xa9').decode('utf-8'): 2}
        encoded = encode.field_table(data)
        decoded = decode.field_table(encoded)[1]
        self.assertIn(b'A' * 128, decoded)
