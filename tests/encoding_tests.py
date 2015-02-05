# -*- encoding: utf-8 -*-
from datetime import datetime
from decimal import Decimal
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pamqp import encode
from pamqp import PYTHON3

if PYTHON3:
    long = int


def to_bytes(value):
    if isinstance(value, bytes):
        return bytes
    if PYTHON3:
        return bytes(value, 'utf-8')
    return bytes(value)


class MarshalingTests(unittest.TestCase):

    def test_encode_bool_wrong_type(self):
        self.assertRaises(TypeError, encode.boolean, 'hi')

    def test_encode_bool_false(self):
        self.assertEqual(encode.boolean(False), b'\x00')

    def test_encode_bool_true(self):
        self.assertEqual(encode.boolean(True), b'\x01')

    def test_encode_byte_array(self):
        self.assertEqual(encode.byte_array(bytearray([65, 66, 67])),
                         b'\x00\x00\x00\x03ABC')

    def test_encode_byte_array_wrong_type(self):
        self.assertRaises(TypeError, encode.byte_array, b'ABC')

    def test_encode_decimal_wrong_type(self):
        self.assertRaises(TypeError, encode.decimal, 3.141597)

    def test_encode_decimal(self):
        self.assertEqual(encode.decimal(Decimal('3.14159')),
                         b'\x05\x00\x04\xcb/')

    def test_encode_decimal_whole(self):
        self.assertEqual(encode.decimal(Decimal('314159')),
                         b'\x00\x00\x04\xcb/')

    def test_encode_floating_point_type(self):
        self.assertRaises(TypeError, encode.floating_point, '1234')

    def test_encode_float(self):
        self.assertEqual(encode.floating_point(float(3.14159)),
                         b'@I\x0f\xd0')

    def test_encode_long_int_wrong_type(self):
        self.assertRaises(TypeError, encode.long_int, 3.141597)

    def test_encode_table_integer_bad_value_error(self):
        self.assertRaises(TypeError, encode.long_int,
                          9223372036854775808)

    def test_encode_long_int(self):
        self.assertEqual(encode.long_int(long(2147483647)),
                         b'\x7f\xff\xff\xff')

    def test_encode_long_int_error(self):
        self.assertRaises(TypeError, encode.long_int,
                          long(21474836449))

    def test_encode_long_long_int_wrong_type(self):
        self.assertRaises(TypeError, encode.long_long_int, 3.141597)

    def test_encode_long_long_int(self):
        self.assertEqual(encode.long_long_int(long(9223372036854775800)),
                         b'\x7f\xff\xff\xff\xff\xff\xff\xf8')

    def test_encode_long_long_int_error(self):
        self.assertRaises(TypeError, encode.long_long_int,
                          long(9223372036854775808))

    def test_encode_octet(self):
        self.assertEqual(encode.octet(1), b'\x01')

    def test_encode_octet_error(self):
        self.assertRaises(TypeError, encode.octet, 'hi')

    def test_encode_short_wrong_type(self):
        self.assertRaises(TypeError, encode.short_int, 3.141597)

    def test_encode_short(self):
        self.assertEqual(encode.short_int(32767),
                         b'\x7f\xff')

    def test_encode_short_error(self):
        self.assertRaises(TypeError, encode.short_int, 65536)

    def test_encode_table_integer_error(self):
        self.assertRaises(TypeError, encode.table_integer,
                          9223372036854775808)

    def test_encode_long_string(self):
        self.assertEqual(encode.long_string(b'0123456789'),
                         b'\x00\x00\x00\n0123456789')

    def test_encode_long_string_error(self):
        self.assertRaises(TypeError, encode.long_string, 100)

    def test_encode_timestamp_from_datetime(self):
        self.assertEqual(encode.timestamp(datetime(2006, 11, 21, 16, 30, 10)),
                         b'\x00\x00\x00\x00Ec)\x92')

    def test_encode_timestamp_from_struct_time(self):
        value = \
            encode.timestamp(datetime(2006, 11, 21, 16, 30, 10).timetuple())
        self.assertEqual(value, b'\x00\x00\x00\x00Ec)\x92')

    def test_encode_timestamp_error(self):
        self.assertRaises(TypeError, encode.timestamp, 'hi')


    def test_encode_field_array(self):
        expectation = (b'\x00\x00\x00<s\x00\x01I\x00\x00\xaf\xc8S'
                       b'\x00\x00\x00\x04TestT\x00\x00\x00\x00Ec)'
                       b'\x92I\xbb\x9a\xca\x00D\x02\x00\x00\x01:f@H'
                       b'\xf5\xc3l\x00\x00\x00\x00\xc4e5\xffl\x80'
                       b'\x00\x00\x00\x00\x00\x00\x08')
        data = [1, 45000, b'Test', datetime(2006, 11, 21, 16, 30, 10),
                -1147483648, Decimal('3.14'), 3.14, long(3294967295),
                -9223372036854775800]
        self.assertEqual(encode.field_array(data), expectation)

    def test_encode_field_array_error(self):
        self.assertRaises(TypeError, encode.field_array, 'hi')

    def test_encode_field_table_empty(self):
        self.assertEqual(encode.field_table(None), b'\x00\x00\x00\x00')

    def test_encode_field_table_type_error(self):
        self.assertRaises(TypeError, encode.field_table, [1, 2, 3])

    def test_encode_field_table(self):
        expectation = (b'\x00\x00\x04\x13\x08arrayvalA\x00\x00\x00\ts\x00\x01s'
                       b'\x00\x02s\x00\x03\x07boolvalt\x01\x06decvalD\x02\x00'
                       b'\x00\x01:\x07dictvalF\x00\x00\x00\x0c\x03fooS\x00\x00'
                       b'\x00\x03bar\x08floatvlaf@H\xf5\xc3\x06intvals\x00\x01'
                       b'\x07longstrS\x00\x00\x03t0000000000000000000000000000'
                       b'00000000000000000000000011111111111111111111111111111'
                       b'11111111111111111111111222222222222222222222222222222'
                       b'22222222222222222222221111111111111111111111111111111'
                       b'11111111111111111111122222222222222222222222222222222'
                       b'22222222222222222222111111111111111111111111111111111'
                       b'11111111111111111112222222222222222222222222222222222'
                       b'22222222222222222211111111111111111111111111111111111'
                       b'11111111111111111222222222222222222222222222222222222'
                       b'22222222222222221111111111111111111111111111111111111'
                       b'11111111111111122222222222222222222222222222222222222'
                       b'22222222222222111111111111111111111111111111111111111'
                       b'11111111111112222222222222222222222222222222222222222'
                       b'22222222222211111111111111111111111111111111111111111'
                       b'11111111111222222222222222222222222222222222222222222'
                       b'22222222221111111111111111111111111111111111111111111'
                       b'11111111100000000000000000000000000000000000000000000'
                       b'00000000\x07longvalI6e&U\x06strvalS\x00\x00\x00\x04'
                       b'Test\x0ctimestampvalT\x00\x00\x00\x00Ec)\x92')
        data = {'intval': 1,
                'strval': b'Test',
                'boolval': True,
                'timestampval': datetime(2006, 11, 21, 16, 30, 10),
                'decval': Decimal('3.14'),
                'floatvla': 3.14,
                'longval': long(912598613),
                'dictval': {b'foo': b'bar'},
                'arrayval': [1, 2, 3],
                'longstr': ('0000000000000000000000000000000000000000000000000'
                            '0001111111111111111111111111111111111111111111111'
                            '1111112222222222222222222222222222222222222222222'
                            '2222222221111111111111111111111111111111111111111'
                            '1111111111112222222222222222222222222222222222222'
                            '2222222222222221111111111111111111111111111111111'
                            '1111111111111111112222222222222222222222222222222'
                            '2222222222222222222221111111111111111111111111111'
                            '1111111111111111111111112222222222222222222222222'
                            '2222222222222222222222222221111111111111111111111'
                            '1111111111111111111111111111112222222222222222222'
                            '2222222222222222222222222222222221111111111111111'
                            '1111111111111111111111111111111111112222222222222'
                            '2222222222222222222222222222222222222221111111111'
                            '1111111111111111111111111111111111111111112222222'
                            '2222222222222222222222222222222222222222222221111'
                            '1111111111111111111111111111111111111111111111110'
                            '0000000000000000000000000000000000000000000000000'
                            '00')}
        self.assertEqual(encode.field_table(data), expectation)


    def test_encode_by_type_field_array(self):

        expectation = (b'\x00\x00\x00<s\x00\x01I\x00\x00\xaf\xc8S\x00\x00\x00'
                       b'\x04TestT\x00\x00\x00\x00Ec)\x92I\xbb\x9a\xca\x00D\x02'
                       b'\x00\x00\x01:f@H\xf5\xc3l\x00\x00\x00\x00\xc4e5\xffl'
                       b'\x80\x00\x00\x00\x00\x00\x00\x08')
        data = [1, 45000, b'Test', datetime(2006, 11, 21, 16, 30, 10),
                -1147483648, Decimal('3.14'), 3.14, long(3294967295),
                -9223372036854775800]
        self.assertEqual(encode.by_type(data, 'field_array'),
                         expectation)

    def test_encode_by_type_long_int(self):
        self.assertEqual(encode.by_type(long(2147483647), 'long'),
                         b'\x7f\xff\xff\xff')

    def test_encode_by_type_long_long_int(self):
        self.assertEqual(encode.by_type(long(9223372036854775800), 'longlong'),
                         b'\x7f\xff\xff\xff\xff\xff\xff\xf8')

    def test_encode_by_type_long_str(self):
        self.assertEqual(encode.by_type(b'0123456789', 'longstr'),
                         b'\x00\x00\x00\n0123456789')

    def test_encode_by_type_octet(self):
        self.assertEqual(encode.by_type(1, 'octet'), b'\x01')

    def test_encode_by_type_short(self):
        self.assertEqual(encode.by_type(32767, 'short'),
                         b'\x7f\xff')

    def test_encode_by_type_timestamp(self):
        self.assertEqual(encode.by_type(datetime(2006, 11, 21,  16, 30, 10),
                                        'timestamp'),
                         b'\x00\x00\x00\x00Ec)\x92')

    def test_encode_by_type_field_table(self):
        expectation = (b'\x00\x00\x04\x13\x08arrayvalA\x00\x00\x00\ts\x00\x01s'
                       b'\x00\x02s\x00\x03\x07boolvalt\x01\x06decvalD\x02\x00'
                       b'\x00\x01:\x07dictvalF\x00\x00\x00\x0c\x03fooS\x00\x00'
                       b'\x00\x03bar\x08floatvlaf@H\xf5\xc3\x06intvals\x00\x01'
                       b'\x07longstrS\x00\x00\x03t0000000000000000000000000000'
                       b'00000000000000000000000011111111111111111111111111111'
                       b'11111111111111111111111222222222222222222222222222222'
                       b'22222222222222222222221111111111111111111111111111111'
                       b'11111111111111111111122222222222222222222222222222222'
                       b'22222222222222222222111111111111111111111111111111111'
                       b'11111111111111111112222222222222222222222222222222222'
                       b'22222222222222222211111111111111111111111111111111111'
                       b'11111111111111111222222222222222222222222222222222222'
                       b'22222222222222221111111111111111111111111111111111111'
                       b'11111111111111122222222222222222222222222222222222222'
                       b'22222222222222111111111111111111111111111111111111111'
                       b'11111111111112222222222222222222222222222222222222222'
                       b'22222222222211111111111111111111111111111111111111111'
                       b'11111111111222222222222222222222222222222222222222222'
                       b'22222222221111111111111111111111111111111111111111111'
                       b'11111111100000000000000000000000000000000000000000000'
                       b'00000000\x07longvalI6e&U\x06strvalS\x00\x00\x00\x04'
                       b'Test\x0ctimestampvalT\x00\x00\x00\x00Ec)\x92')
        data = {'intval': 1,
                'strval': b'Test',
                'boolval': True,
                'timestampval': datetime(2006, 11, 21, 16, 30, 10),
                'decval': Decimal('3.14'),
                'floatvla': 3.14,
                'longval': long(912598613),
                'dictval': {b'foo': b'bar'},
                'arrayval': [1, 2, 3],
                'longstr': ('0000000000000000000000000000000000000000000000000'
                            '0001111111111111111111111111111111111111111111111'
                            '1111112222222222222222222222222222222222222222222'
                            '2222222221111111111111111111111111111111111111111'
                            '1111111111112222222222222222222222222222222222222'
                            '2222222222222221111111111111111111111111111111111'
                            '1111111111111111112222222222222222222222222222222'
                            '2222222222222222222221111111111111111111111111111'
                            '1111111111111111111111112222222222222222222222222'
                            '2222222222222222222222222221111111111111111111111'
                            '1111111111111111111111111111112222222222222222222'
                            '2222222222222222222222222222222221111111111111111'
                            '1111111111111111111111111111111111112222222222222'
                            '2222222222222222222222222222222222222221111111111'
                            '1111111111111111111111111111111111111111112222222'
                            '2222222222222222222222222222222222222222222221111'
                            '1111111111111111111111111111111111111111111111110'
                            '0000000000000000000000000000000000000000000000000'
                            '00')}
        self.assertEqual(encode.by_type(data, 'table'), expectation)

    def test_encode_by_type_error(self):
        self.assertRaises(TypeError, encode.by_type, 12345.12434, 'foo')
