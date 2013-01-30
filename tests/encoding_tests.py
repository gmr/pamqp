# -*- encoding: utf-8 -*-
from datetime import datetime
from decimal import Decimal
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pamqp import codec
from pamqp import PYTHON3

if PYTHON3:
    long = int

def encode(value):
    if PYTHON3:
        return bytes(value, 'latin1')
    return value


class MarshalingTests(unittest.TestCase):

    def test_encode_bool_wrong_type(self):
        self.assertRaises(ValueError, codec.encode.boolean, 'hi')

    def test_encode_bool_false(self):
        self.assertEqual(codec.encode.boolean(False), encode('\x00'))

    def test_encode_bool_true(self):
        self.assertEqual(codec.encode.boolean(True), encode('\x01'))

    def test_encode_decimal_wrong_type(self):
        self.assertRaises(ValueError, codec.encode.decimal, 3.141597)

    def test_encode_decimal(self):
        self.assertEqual(codec.encode.decimal(Decimal('3.14159')),
                         encode('\x05\x00\x04\xcb/'))

    def test_encode_decimal_whole(self):
        self.assertEqual(codec.encode.decimal(Decimal('314159')),
                         encode('\x00\x00\x04\xcb/'))

    def test_encode_floating_point_type(self):
        self.assertRaises(ValueError, codec.encode.floating_point, '1234')

    def test_encode_float(self):
        self.assertEqual(codec.encode.floating_point(float(3.14159)),
                         encode('@I\x0f\xd0'))



    def test_encode_long_int_wrong_type(self):
        self.assertRaises(ValueError, codec.encode.long_int, 3.141597)

    def test_encode_table_integer_bad_value_error(self):
        self.assertRaises(ValueError, codec.encode.long_int,
                          9223372036854775808)

    def test_encode_long_int(self):
        self.assertEqual(codec.encode.long_int(long(2147483647)),
                         encode('\x7f\xff\xff\xff'))

    def test_encode_long_int_error(self):
        self.assertRaises(ValueError, codec.encode.long_int,
                          long(21474836449))

    def test_encode_long_long_int_wrong_type(self):
        self.assertRaises(ValueError, codec.encode.long_long_int, 3.141597)

    def test_encode_long_long_int(self):
        self.assertEqual(codec.encode.long_long_int(long(9223372036854775800)),
                         encode('\x7f\xff\xff\xff\xff\xff\xff\xf8'))

    def test_encode_long_long_int_error(self):
        self.assertRaises(ValueError, codec.encode.long_long_int,
                          long(9223372036854775808))

    def test_encode_octet(self):
        self.assertEqual(codec.encode.octet(1), encode('\x01'))

    def test_encode_octet_error(self):
        self.assertRaises(ValueError, codec.encode.octet, 'hi')

    def test_encode_short_wrong_type(self):
        self.assertRaises(ValueError, codec.encode.short_int, 3.141597)

    def test_encode_short(self):
        self.assertEqual(codec.encode.short_int(32767), encode('\x7f\xff'))

    def test_encode_short_error(self):
        self.assertRaises(ValueError, codec.encode.short_int, 32768)

    def test_encode_table_integer_error(self):
        self.assertRaises(ValueError, codec.encode.table_integer,
                          9223372036854775808)

    def test_encode_long_string(self):
        self.assertEqual(codec.encode.long_string('0123456789'),
                         encode('\x00\x00\x00\n0123456789'))

    def test_encode_long_string_error(self):
        self.assertRaises(ValueError, codec.encode.long_string, 100)

    def test_encode_short_string(self):
        self.assertEqual(codec.encode.short_string('0123456789'),
                         encode('\n0123456789'))

    def test_encode_python2_unicode(self):
        if not PYTHON3:
            self.assertEqual(codec.encode.short_string(u'0123456789'),
                             '\n0123456789')

    def test_encode_string_error(self):
        self.assertRaises(ValueError, codec.encode.short_string, 12345.12434)

    def test_encode_timestamp_from_datetime(self):
        self.assertEqual(codec.encode.timestamp(datetime(2006, 11, 21,
                                                         16, 30, 10)),
                         encode('\x00\x00\x00\x00Ec)\x92'))

    def test_encode_timestamp_from_struct_time(self):
        self.assertEqual(codec.encode.timestamp(datetime(2006, 11, 21, 16, 30,
                                                         10).timetuple()),
                         encode('\x00\x00\x00\x00Ec)\x92'))

    def test_encode_timestamp_error(self):
        self.assertRaises(ValueError, codec.encode.timestamp, 'hi')


    def test_encode_field_array(self):
        expectation = encode('\x00\x00\x00<U\x00\x01I\x00\x00\xaf\xc8S\x00\x00'
                             '\x00\x04TestT\x00\x00\x00\x00Ec)\x92I\xbb\x9a'
                             '\xca\x00D\x02\x00\x00\x01:f@H\xf5\xc3L\x00\x00'
                             '\x00\x00\xc4e5\xffL\x80\x00\x00\x00\x00\x00\x00'
                             '\x08')
        data = [1, 45000, 'Test', datetime(2006, 11, 21, 16, 30, 10),
                -1147483648, Decimal('3.14'), 3.14, long(3294967295),
                -9223372036854775800]
        self.assertEqual(codec.encode.field_array(data), expectation)

    def test_encode_field_array_error(self):
        self.assertRaises(ValueError, codec.encode.field_array, 'hi')

    def test_encode_field_table_empty(self):
        self.assertEqual(codec.encode.field_table(None),
                         encode('\x00\x00\x00\x00'))

    def test_encode_field_table_type_error(self):
        self.assertRaises(ValueError, codec.encode.field_table, [1, 2, 3])

    def test_encode_field_table(self):
        expectation = ('\x00\x00\x04\x13\x08arrayvalA\x00\x00\x00\tU\x00\x01U'
                       '\x00\x02U\x00\x03\x07boolvalt\x01\x06decvalD\x02\x00'
                       '\x00\x01:\x07dictvalF\x00\x00\x00\x0c\x03fooS\x00\x00'
                       '\x00\x03bar\x08floatvlaf@H\xf5\xc3\x06intvalU\x00\x01'
                       '\x07longstrS\x00\x00\x03t0000000000000000000000000000'
                       '00000000000000000000000011111111111111111111111111111'
                       '11111111111111111111111222222222222222222222222222222'
                       '22222222222222222222221111111111111111111111111111111'
                       '11111111111111111111122222222222222222222222222222222'
                       '22222222222222222222111111111111111111111111111111111'
                       '11111111111111111112222222222222222222222222222222222'
                       '22222222222222222211111111111111111111111111111111111'
                       '11111111111111111222222222222222222222222222222222222'
                       '22222222222222221111111111111111111111111111111111111'
                       '11111111111111122222222222222222222222222222222222222'
                       '22222222222222111111111111111111111111111111111111111'
                       '11111111111112222222222222222222222222222222222222222'
                       '22222222222211111111111111111111111111111111111111111'
                       '11111111111222222222222222222222222222222222222222222'
                       '22222222221111111111111111111111111111111111111111111'
                       '11111111100000000000000000000000000000000000000000000'
                       '00000000\x07longvalI6e&U\x06strvalS\x00\x00\x00\x04'
                       'Test\x0ctimestampvalT\x00\x00\x00\x00Ec)\x92')
        data = {'intval': 1,
                'strval': 'Test',
                'boolval': True,
                'timestampval': datetime(2006, 11, 21, 16, 30, 10),
                'decval': Decimal('3.14'),
                'floatvla': 3.14,
                'longval': long(912598613),
                'dictval': {'foo': 'bar'},
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
        self.assertEqual(codec.encode.field_table(data), encode(expectation))


    def test_encode_by_type_field_array(self):

        expectation = ('\x00\x00\x00<U\x00\x01I\x00\x00\xaf\xc8S\x00\x00\x00\x04'
                       'TestT\x00\x00\x00\x00Ec)\x92I\xbb\x9a\xca\x00D\x02\x00'
                       '\x00\x01:f@H\xf5\xc3L\x00\x00\x00\x00\xc4e5\xffL\x80\x00'
                       '\x00\x00\x00\x00\x00\x08')
        data = [1, 45000, 'Test', datetime(2006, 11, 21, 16, 30, 10),
                -1147483648, Decimal('3.14'), 3.14, long(3294967295),
                -9223372036854775800]
        self.assertEqual(codec.encode.by_type(data, 'field_array'),
                         encode(expectation))

    def test_encode_by_type_long_int(self):
        self.assertEqual(codec.encode.by_type(long(2147483647), 'long'),
                         encode('\x7f\xff\xff\xff'))

    def test_encode_by_type_long_long_int(self):
        self.assertEqual(codec.encode.by_type(long(9223372036854775800),
                                              'longlong'),
                         encode('\x7f\xff\xff\xff\xff\xff\xff\xf8'))

    def test_encode_by_type_long_str(self):
        self.assertEqual(codec.encode.by_type('0123456789', 'longstr'),
                         encode('\x00\x00\x00\n0123456789'))

    def test_encode_by_type_short_str(self):
        self.assertEqual(codec.encode.by_type('0123456789', 'shortstr'),
                         encode('\n0123456789'))


    def test_encode_by_type_octet(self):
        self.assertEqual(codec.encode.by_type(1, 'octet'), encode('\x01'))

    def test_encode_by_type_short(self):
        self.assertEqual(codec.encode.by_type(32767, 'short'),
                         encode('\x7f\xff'))

    def test_encode_by_type_timestamp(self):
        self.assertEqual(codec.encode.by_type(datetime(2006, 11, 21,
                                                       16, 30, 10),
                                              'timestamp'),
                         encode('\x00\x00\x00\x00Ec)\x92'))

    def test_encode_by_type_field_table(self):
        expectation = ('\x00\x00\x04\x13\x08arrayvalA\x00\x00\x00\tU\x00\x01U'
                       '\x00\x02U\x00\x03\x07boolvalt\x01\x06decvalD\x02\x00'
                       '\x00\x01:\x07dictvalF\x00\x00\x00\x0c\x03fooS\x00\x00'
                       '\x00\x03bar\x08floatvlaf@H\xf5\xc3\x06intvalU\x00\x01'
                       '\x07longstrS\x00\x00\x03t0000000000000000000000000000'
                       '00000000000000000000000011111111111111111111111111111'
                       '11111111111111111111111222222222222222222222222222222'
                       '22222222222222222222221111111111111111111111111111111'
                       '11111111111111111111122222222222222222222222222222222'
                       '22222222222222222222111111111111111111111111111111111'
                       '11111111111111111112222222222222222222222222222222222'
                       '22222222222222222211111111111111111111111111111111111'
                       '11111111111111111222222222222222222222222222222222222'
                       '22222222222222221111111111111111111111111111111111111'
                       '11111111111111122222222222222222222222222222222222222'
                       '22222222222222111111111111111111111111111111111111111'
                       '11111111111112222222222222222222222222222222222222222'
                       '22222222222211111111111111111111111111111111111111111'
                       '11111111111222222222222222222222222222222222222222222'
                       '22222222221111111111111111111111111111111111111111111'
                       '11111111100000000000000000000000000000000000000000000'
                       '00000000\x07longvalI6e&U\x06strvalS\x00\x00\x00\x04'
                       'Test\x0ctimestampvalT\x00\x00\x00\x00Ec)\x92')
        data = {'intval': 1,
                'strval': 'Test',
                'boolval': True,
                'timestampval': datetime(2006, 11, 21, 16, 30, 10),
                'decval': Decimal('3.14'),
                'floatvla': 3.14,
                'longval': long(912598613),
                'dictval': {'foo': 'bar'},
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
        self.assertEqual(codec.encode.by_type(data, 'table'),
                         encode(expectation))

    def test_encode_by_type_error(self):
        self.assertRaises(ValueError, codec.encode.by_type, 12345.12434, 'foo')
