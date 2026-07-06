import datetime
import decimal
import unittest

from pamqp import decode, encode


class EncodeDecodeTests(unittest.TestCase):
    def test_encode_decode_negative_decimal(self):
        data = decimal.Decimal('-1.5')
        encoded = encode.decimal(data)
        decoded = decode.decimal(encoded)[1]
        self.assertEqual(decoded, data)

    def test_encode_decode_field_table_long_keys(self):
        """Encoding and decoding a field_table with too long keys."""
        # second key is 126 A's + \N{PILE OF POO}
        data = {
            'A' * 256: 1,
            ((b'A' * 128) + b'\xf0\x9f\x92\xa9').decode('utf-8'): 2,
        }
        encoded = encode.field_table(data)
        decoded = decode.field_table(encoded)[1]
        self.assertIn('A' * 128, decoded)

    def test_timestamp_with_dst(self):
        # this test assumes the system is set up using a northern hemisphere
        # timesone with DST (America/New_York as per github CI is fine)
        data = datetime.datetime(2006, 5, 21, 16, 30, 10, tzinfo=datetime.UTC)
        encoded = encode.timestamp(data)
        decoded = decode.timestamp(encoded)[1]
        self.assertEqual(decoded, data)

    def test_timestamp_without_timezone(self):
        naive = datetime.datetime(2006, 5, 21, 16, 30, 10)
        aware = datetime.datetime(2006, 5, 21, 16, 30, 10, tzinfo=datetime.UTC)
        encoded = encode.timestamp(naive)
        decoded = decode.timestamp(encoded)[1]
        self.assertEqual(decoded, aware)
