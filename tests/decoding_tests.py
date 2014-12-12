# -*- encoding: utf-8 -*-
import decimal
import time
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pamqp import decode
from pamqp import PYTHON3

if PYTHON3:
    long = int
    unicode = bytes
    basestring = bytes


def utf8(value):
    if PYTHON3:
        return bytes(value, 'utf-8')
    return value.decode('utf-8')


class CodecDecodeTests(unittest.TestCase):
    FIELD_ARR = (b'\x00\x00\x00@s\x00\x01I\x00\x00\xaf\xc8S\x00\x00'
                 b'\x00\x08Test \xe2\x9c\x88T\x00\x00\x00\x00Ec)\x92'
                 b'I\xbb\x9a\xca\x00D\x02\x00\x00\x01:f@H\xf5\xc3l'
                 b'\x00\x00\x00\x00\xc4e5\xffl\x80\x00\x00\x00\x00'
                 b'\x00\x00\x08')
    FIELD_ARR_VALUE = [1, 45000, b'Test \xe2\x9c\x88',
                       time.struct_time((2006, 11, 21, 16, 30, 10, 1, 325, 0)),
                       -1147483648, decimal.Decimal('3.14'),
                       3.14,
                       3294967295,
                       -9223372036854775800]
    FIELD_TBL = (b'\x00\x00\x00\x97\x08arrayvalA\x00\x00\x00\ts\x00'
                 b'\x01s\x00\x02s\x00\x03\x07boolvalt\x01\x06decvalD'
                 b'\x02\x00\x00\x01:\x07dictvalF\x00\x00\x00\r\x04f'
                 b'\xe2\x9c\x89S\x00\x00\x00\x03\xe2\x9c\x90\x08'
                 b'floatvalf@H\xf5\xc3\x06intvals\x00\x01\x07'
                 b'longvalI6e&U\x06strvalS\x00\x00\x00\x08Test \xe2'
                 b'\x9c\x88\x0ctimestampvalT\x00\x00\x00\x00Ec)\x92')
    FIELD_TBL_VALUE = {b'intval': 1,
                       b'strval': b'Test \xe2\x9c\x88',
                       b'boolval': True,
                       b'timestampval': time.struct_time((2006, 11, 21, 16, 30,
                                                         10, 1, 325, 0)),
                       b'decval': decimal.Decimal('3.14'),
                       b'floatval': 3.14,
                       b'longval': long(912598613),
                       b'dictval': {utf8('f✉'): b'\xe2\x9c\x90'},
                       b'arrayval': [1, 2, 3]}

    def test_decode_by_type_invalid_data_type(self):
        self.assertRaises(ValueError, decode.by_type, b'Z\x00', b'foobar')

    def test_decode_bit_bytes_consumed(self):
        self.assertEqual(decode.bit(b'\xff', 4)[0], 0)

    def test_decode_invalid_value(self):
        self.assertRaises(ValueError, decode.bit, b'\xff', None)

    def test_decode_bit_on(self):
        self.assertTrue(decode.bit(b'\xff', 4)[1])

    def test_decode_bit_off(self):
        self.assertFalse(decode.bit(b'\x0f', 4)[1])

    def test_decode_boolean_bytes_consumed(self):
        self.assertEqual(decode.boolean(b'\x01')[0], 1)

    def test_decode_boolean_false(self):
        self.assertFalse(decode.boolean(b'\x00')[1])

    def test_decode_boolean_false_data_type(self):
        self.assertIsInstance(decode.boolean(b'\x00')[1], bool)

    def test_decode_boolean_invalid_value(self):
        self.assertRaises(ValueError, decode.boolean, None)

    def test_decode_boolean_true(self):
        self.assertTrue(decode.boolean(b'\x01')[1])

    def test_decode_boolean_true_data_type(self):
        self.assertIsInstance(decode.boolean(b'\x01')[1], bool)

    def test_decode_byte_array(self):
        self.assertEqual(decode.byte_array(b'\x00\x00\x00\x03ABC'),
                         (7, bytearray([65, 66, 67])))

    def test_decode_decimal_value_bytes_consumed(self):
        value = b'\x05\x00\x04\xcb/'
        self.assertEqual(decode.decimal(value)[0], len(value))

    def test_decode_decimal_value_data_type(self):
        value = b'\x05\x00\x04\xcb/'
        self.assertIsInstance(decode.decimal(value)[1], decimal.Decimal)

    def test_decode_decimal_value(self):
        value = b'\x05\x00\x04\xcb/'
        self.assertEqual(round(float(decode.decimal(value)[1]), 5),
                         round(float(decimal.Decimal('3.14159')), 5))

    def test_decode_decimal_invalid_value(self):
        self.assertRaises(ValueError, decode.decimal, False)

    def test_decode_embedded_value_null(self):
        self.assertEqual(decode._embedded_value(b'\00')[1], None)

    def test_decode_embedded_value_invalid_data(self):
        self.assertRaises(ValueError, decode._embedded_value, b'Z\x00')

    def test_decode_floating_point_bytes_consumed(self):
        value = b'@I\x0f\xd0'
        self.assertEqual(decode.floating_point(value)[0], 4)

    def test_decode_floating_point_data_type(self):
        value = b'@I\x0f\xd0'
        self.assertIsInstance(decode.floating_point(value)[1], float)

    def test_decode_floating_point_invalid_value(self):
        self.assertRaises(ValueError, decode.floating_point, False)

    def test_decode_floating_point_value(self):
        value = b'@I\x0f\xd0'
        self.assertEqual(round(decode.floating_point(value)[1], 5),
                         round(float(3.14159), 5))

    def test_decode_long_int_bytes_consumed(self):
        value = b'\x7f\xff\xff\xff'
        self.assertEqual(decode.long_int(value)[0], 4)

    def test_decode_long_int_data_type(self):
        value = b'\x7f\xff\xff\xff'
        self.assertIsInstance(decode.long_int(value)[1], int)

    def test_decode_long_int_invalid_value(self):
        self.assertRaises(ValueError, decode.long_int, None)

    def test_decode_long_int_value(self):
        value = b'\x7f\xff\xff\xff'
        self.assertEqual(decode.long_int(value)[1], 2147483647)

    def test_decode_long_long_int_bytes_consumed(self):
        value = b'\x7f\xff\xff\xff\xff\xff\xff\xf8'
        self.assertEqual(decode.long_long_int(value)[0], 8)

    def test_decode_long_long_int_data_type(self):
        value = b'\x7f\xff\xff\xff\xff\xff\xff\xf8'
        self.assertIsInstance(decode.long_long_int(value)[1], int)

    def test_decode_long_long_int_invalid_value(self):
        self.assertRaises(ValueError, decode.long_long_int, None)

    def test_decode_long_long_int_value(self):
        value = b'\x7f\xff\xff\xff\xff\xff\xff\xf8'
        self.assertEqual(decode.long_long_int(value)[1],
                         9223372036854775800)

    def test_decode_long_str_bytes_consumed(self):
        value = b'\x00\x00\x00\n0123456789'
        self.assertEqual(decode.long_str(value)[0], 14)

    def test_decode_long_str_data_type(self):
        value = b'\x00\x00\x00\n0123456789'
        self.assertIsInstance(decode.long_str(value)[1], basestring)

    def test_decode_long_str_data_type_unicode(self):
        self.assertIsInstance(decode.long_str(b'\x00\x00\x00\x0c\xd8\xa7'
                                              b'\xd8\xae\xd8\xaa\xd8\xa8'
                                              b'\xd8\xa7\xd8\xb1')[1],
                              bytes)

    def test_decode_long_str_invalid_value(self):
        self.assertRaises(ValueError, decode.long_str, None)

    def test_decode_long_str_value(self):
        value = b'\x00\x00\x00\n0123456789'
        self.assertEqual(decode.long_str(value)[1], b'0123456789')

    def test_decode_octet_bytes_consumed(self):
        value = b'\xff'
        self.assertEqual(decode.octet(value)[0], 1)

    def test_decode_octet_data_type(self):
        value = b'\xff'
        self.assertIsInstance(decode.octet(value)[1], int)

    def test_decode_octet_invalid_value(self):
        self.assertRaises(ValueError, decode.octet, None)

    def test_decode_octet_value(self):
        value = b'\xff'
        self.assertEqual(decode.octet(value)[1], 255)

    def test_decode_short_int_bytes_consumed(self):
        value = b'\x7f\xff'
        self.assertEqual(decode.short_int(value)[0], 2)

    def test_decode_short_int_data_type(self):
        value = b'\x7f\xff'
        self.assertIsInstance(decode.short_int(value)[0], int)

    def test_decode_short_int_invalid_value(self):
        self.assertRaises(ValueError, decode.short_int, None)

    def test_decode_short_int_value(self):
        value = b'\x7f\xff'
        self.assertEqual(decode.short_int(value)[1], 32767)

    def test_decode_short_str_bytes_consumed(self):
        self.assertEqual(decode.short_str(b'\n0123456789')[0], 11)

    def test_decode_short_str_data_type(self):
        self.assertIsInstance(decode.short_str(b'\n0123456789')[1], basestring)

    def test_decode_short_str_invalid_value(self):
        self.assertRaises(ValueError, decode.short_str, None)

    def test_decode_short_str_value(self):
        self.assertEqual(decode.short_str(b'\n0123456789')[1], b'0123456789')

    def test_decode_timestamp_bytes_consumed(self):
        self.assertEqual(decode.timestamp(b'\x00\x00\x00\x00Ec)\x92')[0], 8)

    def test_decode_timestamp_data_type(self):
        self.assertIsInstance(decode.timestamp(b'\x00\x00\x00\x00Ec)\x92')[1],
                              time.struct_time)

    def test_decode_timestamp_invalid_value(self):
        self.assertRaises(ValueError, decode.timestamp, None)

    def test_decode_timestamp_value(self):
        self.assertEqual(decode.timestamp(b'\x00\x00\x00\x00Ec)\x92')[1],
                         time.struct_time((2006, 11, 21,
                                           16, 30, 10, 1, 325, 0)))

    def test_decode_field_array_bytes_consumed(self):
        self.assertEqual(decode.field_array(self.FIELD_ARR)[0],
                         len(self.FIELD_ARR))

    def test_decode_field_array_data_type(self):
        self.assertIsInstance(decode.field_array(self.FIELD_ARR)[1], list)

    def test_decode_field_array_invalid_value(self):
        self.assertRaises(ValueError, decode.field_array, None)

    def test_decode_field_array_value(self):
        value = decode.field_array(self.FIELD_ARR)[1]
        for position in range(0, len(value)):
            if isinstance(value[position], float):
                self.assertAlmostEqual(round(value[position], 3),
                                       round(self.FIELD_ARR_VALUE[position],
                                             3))
            else:
                self.assertEqual(value[position],
                                 self.FIELD_ARR_VALUE[position])

    def test_decode_field_table_bytes_consumed(self):
        self.assertEqual(decode.field_table(self.FIELD_TBL)[0],
                         len(self.FIELD_TBL))

    def test_decode_field_table_data_type(self):
        self.assertIsInstance(
            decode.field_table(self.FIELD_TBL)[1], dict)

    def test_decode_field_table_invalid_value(self):
        self.assertRaises(ValueError, decode.field_table, None)

    def test_decode_field_table_value(self):
        value = decode.field_table(self.FIELD_TBL)[1]
        for key in value.keys():
            if isinstance(value[key], float):
                self.assertAlmostEqual(round(value[key], 3),
                                       round(self.FIELD_TBL_VALUE[key], 3))
            else:
                self.assertEqual(value[key], self.FIELD_TBL_VALUE[key])

    def test_decode_by_type_bit_bytes_consumed(self):
        self.assertEqual(decode.by_type(b'\xff', 'bit', 4)[0], 0)

    def test_decode_by_type_invalid_value(self):
        self.assertRaises(ValueError, decode.by_type, b'\xff', 'bit', None)

    def test_decode_by_type_bit_on(self):
        self.assertTrue(decode.by_type(b'\xff', 'bit', 4)[1])

    def test_decode_by_type_bit_off(self):
        self.assertFalse(decode.by_type(b'\x0f', 'bit', 4)[1])

    def test_decode_by_type_boolean_bytes_consumed(self):
        self.assertEqual(decode.by_type(b'\x01', 'boolean')[0], 1)

    def test_decode_by_type_boolean_false(self):
        self.assertFalse(decode.by_type(b'\x00', 'boolean')[1])

    def test_decode_by_type_boolean_false_data_type(self):
        self.assertIsInstance(decode.by_type(b'\x00', 'boolean')[1], bool)

    def test_decode_by_type_boolean_invalid_value(self):
        self.assertRaises(ValueError, decode.by_type, None, 'boolean')

    def test_decode_by_type_boolean_true(self):
        self.assertTrue(decode.by_type(b'\x01', 'boolean')[1])

    def test_decode_by_type_boolean_true_data_type(self):
        self.assertIsInstance(decode.by_type(b'\x01', 'boolean')[1], bool)

    def test_decode_by_type_decimal_bytes_consumed(self):
        value = b'\x05\x00\x04\xcb/'
        self.assertEqual(decode.by_type(value, 'decimal')[0], len(value))

    def test_decode_by_type_decimal_data_type(self):
        self.assertIsInstance(decode.by_type(b'\x05\x00\x04\xcb/',
                                             'decimal')[1],
                              decimal.Decimal)

    def test_decode_by_type_decimal_value(self):
        self.assertEqual(round(float(decode.by_type(b'\x05\x00\x04\xcb/',
                                                    'decimal')[1]), 5),
                         round(float(decimal.Decimal('3.14159')), 5))

    def test_decode_by_type_decimal_invalid_value(self):
        self.assertRaises(ValueError, decode.by_type, False, 'decimal')

    def test_decode_by_type_floating_point_bytes_consumed(self):
        self.assertEqual(decode.by_type(b'@I\x0f\xd0', 'float')[0], 4)

    def test_decode_by_type_floating_point_data_type(self):
        value = b'@I\x0f\xd0'
        self.assertIsInstance(decode.by_type(value, 'float')[1],
                              float)

    def test_decode_by_type_floating_point_invalid_value(self):
        self.assertRaises(ValueError, decode.by_type, False, 'float')

    def test_decode_by_type_floating_point_value(self):
        value = b'@I\x0f\xd0'
        self.assertEqual(round(decode.by_type(value, 'float')[1], 5),
                         round(float(3.14159), 5))

    def test_decode_by_type_long_bytes_consumed(self):
        value = b'\x7f\xff\xff\xff'
        self.assertEqual(decode.by_type(value, 'long')[0], 4)

    def test_decode_by_type_long_data_type(self):
        value = b'\x7f\xff\xff\xff'
        self.assertIsInstance(decode.by_type(value, 'long')[1], int)

    def test_decode_by_type_long_invalid_value(self):
        self.assertRaises(ValueError, decode.by_type, None, 'long')

    def test_decode_by_type_long_value(self):
        value = b'\x7f\xff\xff\xff'
        self.assertEqual(decode.by_type(value, 'long')[1], 2147483647)

    def test_decode_by_type_long_long_bytes_consumed(self):
        value = b'\x7f\xff\xff\xff\xff\xff\xff\xf8'
        self.assertEqual(decode.by_type(value, 'longlong')[0], 8)

    def test_decode_by_type_long_long_data_type(self):
        value = b'\x7f\xff\xff\xff\xff\xff\xff\xf8'
        self.assertIsInstance(decode.by_type(value, 'longlong')[1], int)

    def test_decode_by_type_long_long_invalid_value(self):
        self.assertRaises(ValueError, decode.by_type, None, 'longlong')

    def test_decode_by_type_long_long_value(self):
        value = b'\x7f\xff\xff\xff\xff\xff\xff\xf8'
        self.assertEqual(decode.by_type(value, 'longlong')[1],
                         9223372036854775800)

    def test_decode_by_type_longstr_bytes_consumed(self):
        value = b'\x00\x00\x00\n0123456789'
        self.assertEqual(decode.by_type(value, 'longstr')[0], 14)

    def test_decode_by_type_longstr_data_type_with_unicode(self):
        value = b'\x00\x00\x00\x08Test \xe2\x9c\x88'
        self.assertIsInstance(decode.by_type(value, 'longstr')[1], bytes)

    def test_decode_by_type_longstr_data_type(self):
        value = b'\x00\x00\x00\n0123456789'
        self.assertIsInstance(decode.by_type(value, 'longstr')[1], basestring)

    def test_decode_by_type_longstr_invalid_value(self):
        self.assertRaises(ValueError, decode.by_type, None, 'longstr')

    def test_decode_by_type_longstr_value(self):
        value = b'\x00\x00\x00\n0123456789'
        self.assertEqual(decode.by_type(value, 'longstr')[1], b'0123456789')

    def test_decode_by_type_octet_bytes_consumed(self):
        self.assertEqual(decode.by_type(b'\xff', 'octet')[0], 1)

    def test_decode_by_type_octet_data_type(self):
        self.assertIsInstance(decode.by_type(b'\xff', 'octet')[1], int)

    def test_decode_by_type_octet_invalid_value(self):
        self.assertRaises(ValueError, decode.by_type, None, 'octet')

    def test_decode_by_type_octet_value(self):
        self.assertEqual(decode.by_type(b'\xff', 'octet')[1], 255)

    def test_decode_by_type_short_bytes_consumed(self):
        value = b'\x7f\xff'
        self.assertEqual(decode.by_type(value, 'short')[0], 2)

    def test_decode_by_type_short_data_type(self):
        value = b'\x7f\xff'
        self.assertIsInstance(decode.by_type(value, 'short')[1], int)

    def test_decode_by_type_short_invalid_value(self):
        self.assertRaises(ValueError, decode.by_type, None, 'short')

    def test_decode_by_type_short_value(self):
        value = b'\x7f\xff'
        self.assertEqual(decode.by_type(value, 'short')[1], 32767)

    def test_decode_by_type_timestamp_bytes_consumed(self):
        value = b'\x00\x00\x00\x00Ec)\x92'
        self.assertEqual(decode.by_type(value, 'timestamp')[0], 8)

    def test_decode_by_type_timestamp_data_type(self):
        value = b'\x00\x00\x00\x00Ec)\x92'
        self.assertIsInstance(decode.by_type(value, 'timestamp')[1],
                              time.struct_time)

    def test_decode_by_type_timestamp_invalid_value(self):
        self.assertRaises(ValueError, decode.by_type, None, 'timestamp')

    def test_decode_by_type_timestamp_value(self):
        value = b'\x00\x00\x00\x00Ec)\x92'
        self.assertEqual(decode.by_type(value, 'timestamp')[1],
                         time.struct_time((2006, 11, 21,
                                           16, 30, 10, 1, 325, 0)))

    def test_decode_by_type_field_array_bytes_consumed(self):
        self.assertEqual(decode.by_type(self.FIELD_ARR, 'array')[0],
                         len(self.FIELD_ARR))

    def test_decode_by_type_field_array_data_type(self):
        self.assertIsInstance(decode.by_type(self.FIELD_ARR,
                                             'array')[1], list)

    def test_decode_by_type_field_array_invalid_value(self):
        self.assertRaises(ValueError, decode.by_type, None, 'array')

    def test_decode_by_type_field_array_value(self):
        value = decode.by_type(self.FIELD_ARR, 'array')[1]
        for position in range(0, len(value)):
            if isinstance(value[position], float):
                self.assertAlmostEqual(round(value[position], 3),
                                       round(self.FIELD_ARR_VALUE[position],
                                             3))
            else:
                self.assertEqual(value[position],
                                 self.FIELD_ARR_VALUE[position])

    def test_decode_by_type_field_table_bytes_consumed(self):
        self.assertEqual(decode.by_type(self.FIELD_TBL, 'table')[0],
                         len(self.FIELD_TBL))

    def test_decode_by_type_field_table_data_type(self):
        self.assertIsInstance(decode.by_type(self.FIELD_TBL,
                                             'table')[1], dict)

    def test_decode_by_type_field_table_invalid_value(self):
        self.assertRaises(ValueError, decode.by_type, None, 'table')

    def test_decode_by_type_field_table_value(self):
        value = decode.by_type(self.FIELD_TBL, 'table')[1]
        for key in value.keys():
            if isinstance(value[key], float):
                self.assertAlmostEqual(round(value[key], 3),
                                       round(self.FIELD_TBL_VALUE[key], 3))
            else:
                self.assertEqual(value[key], self.FIELD_TBL_VALUE[key])

    def test_decode_embedded_value_empty_bytes_consumed(self):
        self.assertEqual(decode._embedded_value(b'')[0], 0)

    def test_decode_embedded_value_empty_value(self):
        self.assertEqual(decode._embedded_value(b'')[1], None)

    def test_decode_embedded_value_decimal_bytes_consumed(self):
        value = b'D\x05\x00\x04\xcb/'
        self.assertEqual(decode._embedded_value(value)[0], len(value))

    def test_decode_embedded_value_decimal_data_type(self):
        value = b'D\x05\x00\x04\xcb/'
        self.assertIsInstance(decode._embedded_value(value)[1],
                              decimal.Decimal)

    def test_decode_embedded_value_decimal_value(self):
        value = b'D\x05\x00\x04\xcb/'
        self.assertEqual(round(float(decode._embedded_value(value)[1]), 5),
                         round(float(decimal.Decimal('3.14159')), 5))

    def test_decode_embedded_value_long_bytes_consumed(self):
        value = b'I\x7f\xff\xff\xff'
        self.assertEqual(decode._embedded_value(value)[0], 5)

    def test_decode_embedded_value_long_data_type(self):
        value = b'I\x7f\xff\xff\xff'
        self.assertIsInstance(decode._embedded_value(value)[1], int)

    def test_decode_embedded_value_long_value(self):
        value = b'I\x7f\xff\xff\xff'
        self.assertEqual(decode._embedded_value(value)[1], 2147483647)

    def test_decode_embedded_value_long_long_bytes_consumed(self):
        value = b'l\x7f\xff\xff\xff\xff\xff\xff\xf8'
        self.assertEqual(decode._embedded_value(value)[0], 9)

    def test_decode_embedded_value_long_long_data_type(self):
        value = b'l\x7f\xff\xff\xff\xff\xff\xff\xf8'
        self.assertIsInstance(decode._embedded_value(value)[1], int)

    def test_decode_embedded_value_long_long_value(self):
        value = b'l\x7f\xff\xff\xff\xff\xff\xff\xf8'
        self.assertEqual(decode._embedded_value(value)[1],
                         9223372036854775800)

    def test_decode_embedded_value_longstr_bytes_consumed(self):
        value = b'S\x00\x00\x00\n0123456789'
        self.assertEqual(decode._embedded_value(value)[0], 15)

    def test_decode_embedded_value_longstr_data_type(self):
        value = b'S\x00\x00\x00\n0123456789'
        expectation = bytes if PYTHON3 else str
        self.assertIsInstance(decode._embedded_value(value)[1],
                              expectation)

    def test_decode_embedded_value_byte_array_data(self):
        value = b'x\x00\x00\x00\x03ABC'
        self.assertEqual(decode._embedded_value(value)[1],
                         bytearray([65, 66, 67]))

    def test_decode_embedded_value_byte_array_data_type(self):
        value = b'x\x00\x00\x00\x03ABC'
        self.assertIsInstance(decode._embedded_value(value)[1], bytearray)

    def test_decode_embedded_value_longstr_data_type_unicode(self):
        value = (b'S\x00\x00\x00\x0c\xd8\xa7\xd8\xae\xd8\xaa\xd8\xa8\xd8'
                 b'\xa7\xd8\xb1')
        self.assertIsInstance(decode._embedded_value(value)[1], bytes)

    def test_decode_embedded_value_longstr_value(self):
        value = b'S\x00\x00\x00\n0123456789'
        self.assertEqual(decode._embedded_value(value)[1], b'0123456789')

    def test_decode_embedded_value_short_bytes_consumed(self):
        value = b's\x7f\xff'
        self.assertEqual(decode._embedded_value(value)[0], 3)

    def test_decode_embedded_value_short_data_type(self):
        value = b's\x7f\xff'
        self.assertIsInstance(decode._embedded_value(value)[1], int)

    def test_decode_embedded_value_short_value(self):
        self.assertEqual(decode._embedded_value(b's\x7f\xff')[1], 32767)

    def test_decode_embedded_value_timestamp_bytes_consumed(self):
        value = b'T\x00\x00\x00\x00Ec)\x92'
        self.assertEqual(decode._embedded_value(value)[0], 9)

    def test_decode_embedded_value_timestamp_data_type(self):
        value = b'T\x00\x00\x00\x00Ec)\x92'
        self.assertIsInstance(decode._embedded_value(value)[1],
                              time.struct_time)

    def test_decode_embedded_value_timestamp_value(self):
        value = b'T\x00\x00\x00\x00Ec)\x92'
        self.assertEqual(decode._embedded_value(value)[1],
                         time.struct_time((2006, 11, 21, 16, 30, 10, 1,
                                           325, 0)))

    def test_decode_embedded_value_field_array_bytes_consumed(self):
        self.assertEqual(decode._embedded_value(b'A' +
                                                self.FIELD_ARR)[0],
                         len(b'A' + self.FIELD_ARR))

    def test_decode_embedded_value_field_array_data_type(self):
        self.assertIsInstance(decode._embedded_value(b'A' +
                              self.FIELD_ARR)[1], list)

    def test_decode_embedded_value_field_array_value(self):
        value = decode._embedded_value(b'A' + self.FIELD_ARR)[1]
        for position in range(0, len(value)):
            if isinstance(value[position], float):
                self.assertAlmostEqual(round(value[position], 3),
                                       round(self.FIELD_ARR_VALUE[position],
                                             3))
            else:
                self.assertEqual(value[position],
                                 self.FIELD_ARR_VALUE[position])

    def test_decode_embedded_value_field_table_bytes_consumed(self):
        self.assertEqual(decode._embedded_value(b'F' + self.FIELD_TBL)[0],
                         len(b'F' + self.FIELD_TBL))

    def test_decode_embedded_value_field_table_data_type(self):
        self.assertIsInstance(decode._embedded_value(b'F' + self.FIELD_TBL)[1],
                              dict)

    def test_decode_embedded_value_field_table_value(self):
        value = decode._embedded_value(b'F' + self.FIELD_TBL)[1]
        for key in value.keys():
            if isinstance(value[key], float):
                self.assertAlmostEqual(round(value[key], 3),
                                       round(self.FIELD_TBL_VALUE[key], 3))
            else:
                self.assertEqual(value[key], self.FIELD_TBL_VALUE[key])
