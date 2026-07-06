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

    def test_encode_decode_field_table_multibyte_key(self):
        """A multibyte key over 128 bytes must not raise struct.error."""
        # 128 \N{PILE OF POO} chars encode to 512 bytes
        key = '\U0001f4a9' * 128
        encoded = encode.field_table({key: 1})
        decoded = decode.field_table(encoded)[1]
        self.assertEqual(list(decoded.values()), [1])
        # the truncated key must round-trip cleanly (no split characters)
        (decoded_key,) = decoded
        self.assertTrue(key.startswith(decoded_key))
        self.assertLessEqual(len(decoded_key.encode('utf-8')), 128)

    def test_encode_decode_decimal_scientific_notation(self):
        encoded = encode.decimal(decimal.Decimal('1E-10'))
        decoded = decode.decimal(encoded)[1]
        self.assertEqual(decoded, decimal.Decimal('1E-10'))

    def test_encode_decode_decimal(self):
        value = decimal.Decimal('3.14159')
        decoded = decode.decimal(encode.decimal(value))[1]
        self.assertEqual(decoded, value)

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
