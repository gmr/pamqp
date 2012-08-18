# coding=utf-8

import decimal
import sys
import time
try:
    import unittest2 as unittest
except ImportError:
    import unittest

sys.path.insert(0, '..')
from pamqp import codec

class CodecDecodeTests(unittest.TestCase):

    FIELD_ARR_ENCODED = ('\x00\x00\x00<U\x00\x01I\x00\x00\xaf\xc8S\x00\x00'
                         '\x00\x04TestT\x00\x00\x00\x00Ec)\x92I\xbb\x9a\xca'
                         '\x00D\x02\x00\x00\x01:f@H\xf5\xc3L\x00\x00\x00\x00'
                         '\xc4e5\xffL\x80\x00\x00\x00\x00\x00\x00\x08')
    FIELD_ARR_VALUE = [1, 45000, u'Test',
                       time.struct_time((2006, 11, 21, 16, 30, 10, 1, 325, 0)),
                       -1147483648, decimal.Decimal('3.14'),
                       3.14,
                       3294967295,
                       -9223372036854775800]
    FIELD_TBL_ENCODED = ('\x00\x00\x00\x92\x07longvalI6e&U\x08floatvlaf@H\xf5'
                         '\xc3\x07boolvalt\x01\x06strvalS\x00\x00\x00\x04Test'
                         '\x06intvalU\x00\x01\x0ctimestampvalT\x00\x00\x00\x00'
                         'Ec)\x92\x06decvalD\x02\x00\x00\x01:\x08arrayvalA\x00'
                         '\x00\x00\tU\x00\x01U\x00\x02U\x00\x03\x07dictvalF'
                         '\x00\x00\x00\x0c\x03fooS\x00\x00\x00\x03bar')
    FIELD_TBL_VALUE = {'intval': 1,
                       'strval': 'Test',
                       'boolval': True,
                       'timestampval': time.struct_time((2006, 11, 21, 16, 30,
                                                         10, 1, 325, 0)),
                       'decval': decimal.Decimal('3.14'),
                       'floatvla': 3.14,
                       'longval': long(912598613),
                       'dictval': {'foo': 'bar'},
                       'arrayval': [1, 2, 3]}

    def test_decode_embedded_value_null(self):
        self.assertEqual(codec.decode._embedded_value('\00')[1], None)

    def test_decode_embedded_value_invalid_data(self):
        self.assertRaises(ValueError, codec.decode._embedded_value, 'Z\x00')

    def test_decode_by_type_invalid_data_type(self):
        self.assertRaises(ValueError, codec.decode.by_type, 'Z\x00', 'foobar')

    def test_decode_bit_bytes_consumed(self):
        self.assertEqual(codec.decode.bit('\xff', 4)[0], 0)

    def test_decode_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.bit, '\xff', None)

    def test_decode_bit_on(self):
        self.assertTrue(codec.decode.bit('\xff', 4)[1])

    def test_decode_bit_off(self):
        self.assertFalse(codec.decode.bit('\x0f', 4)[1])

    def test_decode_boolean_bytes_consumed(self):
        self.assertEqual(codec.decode.boolean('\x01')[0], 1)

    def test_decode_boolean_false(self):
        self.assertFalse(codec.decode.boolean('\x00')[1])

    def test_decode_boolean_false_data_type(self):
        self.assertIsInstance(codec.decode.boolean('\x00')[1], bool)

    def test_decode_boolean_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.boolean, None)

    def test_decode_boolean_true(self):
        self.assertTrue(codec.decode.boolean('\x01')[1])

    def test_decode_boolean_true_data_type(self):
        self.assertIsInstance(codec.decode.boolean('\x01')[1], bool)

    def test_decode_decimal_value_bytes_consumed(self):
        value = '\x05\x00\x04\xcb/'
        self.assertEqual(codec.decode.decimal(value)[0], len(value))

    def test_decode_decimal_value_data_type(self):
        self.assertIsInstance(codec.decode.decimal('\x05\x00\x04\xcb/')[1],
                              decimal.Decimal)

    def test_decode_decimal_value(self):
        self.assertEqual(round(codec.decode.decimal('\x05\x00\x04\xcb/')[1], 5),
                         round(float(decimal.Decimal('3.14159')), 5))

    def test_decode_decimal_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.decimal, False)

    def test_decode_floating_point_bytes_consumed(self):
        self.assertEqual(codec.decode.floating_point('@I\x0f\xd0')[0], 4)

    def test_decode_floating_point_data_type(self):
        self.assertIsInstance(codec.decode.floating_point('@I\x0f\xd0')[1],
                              float)

    def test_decode_floating_point_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.floating_point, False)

    def test_decode_floating_point_value(self):
        self.assertEqual(round(codec.decode.floating_point('@I\x0f\xd0')[1], 5),
                         round(float(3.14159), 5))

    def test_decode_long_int_bytes_consumed(self):
        self.assertEqual(codec.decode.long_int('\x7f\xff\xff\xff')[0], 4)

    def test_decode_long_int_data_type(self):
        self.assertIsInstance(codec.decode.long_int('\x7f\xff\xff\xff')[1],
                              int)

    def test_decode_long_int_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.long_int, None)

    def test_decode_long_int_value(self):
        self.assertEqual(codec.decode.long_int('\x7f\xff\xff\xff')[1],
                         2147483647)

    def test_decode_long_long_int_bytes_consumed(self):
        self.assertEqual(codec.decode.long_long_int('\x7f\xff\xff\xff'
                                                    '\xff\xff\xff\xf8')[0], 8)

    def test_decode_long_long_int_data_type(self):
        self.assertIsInstance(codec.decode.long_long_int('\x7f\xff\xff\xff'
                                                         '\xff\xff\xff\xf8')[1],
                              int)

    def test_decode_long_long_int_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.long_long_int, None)

    def test_decode_long_long_int_value(self):
        self.assertEqual(codec.decode.long_long_int('\x7f\xff\xff\xff'
                                                    '\xff\xff\xff\xf8')[1],
                         9223372036854775800)

    def test_decode_long_str_bytes_consumed(self):
        self.assertEqual(codec.decode.long_str('\x00\x00\x00\n0123456789')[0],
                         14)

    def test_decode_long_str_data_type(self):
        self.assertIsInstance(
            codec.decode.long_str('\x00\x00\x00\n0123456789')[1], unicode)

    def test_decode_long_str_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.long_str, None)

    def test_decode_long_str_value(self):
        self.assertEqual(codec.decode.long_str('\x00\x00\x00\n0123456789')[1],
                         '0123456789')

    def test_decode_octet_bytes_consumed(self):
        self.assertEqual(codec.decode.octet('\xff')[0], 1)

    def test_decode_octet_data_type(self):
        self.assertIsInstance(codec.decode.octet('\xff')[1], int)

    def test_decode_octet_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.octet, None)

    def test_decode_octet_value(self):
        self.assertEqual(codec.decode.octet('\xff')[1], 255)

    def test_decode_short_int_bytes_consumed(self):
        self.assertEqual(codec.decode.short_int('\x7f\xff')[0], 2)

    def test_decode_short_int_data_type(self):
        self.assertIsInstance(codec.decode.short_int('\x7f\xff')[1], int)

    def test_decode_short_int_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.short_int, None)

    def test_decode_short_int_value(self):
        self.assertEqual(codec.decode.short_int('\x7f\xff')[1], 32767)

    def test_decode_short_str_bytes_consumed(self):
        self.assertEqual(codec.decode.short_str('\n0123456789')[0], 11)

    def test_decode_short_str_data_type(self):
        self.assertIsInstance(codec.decode.short_str('\n0123456789')[1],
                              unicode)

    def test_decode_short_str_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.short_str, None)

    def test_decode_short_str_value(self):
        self.assertEqual(codec.decode.short_str('\n0123456789')[1],
                         '0123456789')

    def test_decode_timestamp_bytes_consumed(self):
        self.assertEqual(codec.decode.timestamp('\x00\x00\x00\x00Ec)\x92')[0],
                         8)

    def test_decode_timestamp_data_type(self):
        self.assertIsInstance(
            codec.decode.timestamp('\x00\x00\x00\x00Ec)\x92')[1],
            time.struct_time)

    def test_decode_timestamp_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.timestamp, None)

    def test_decode_timestamp_value(self):
        self.assertEqual(codec.decode.timestamp('\x00\x00\x00\x00Ec)\x92')[1],
                         time.struct_time((2006, 11, 21,
                                           16, 30, 10, 1, 325, 0)))

    def test_decode_field_array_bytes_consumed(self):
        self.assertEqual(codec.decode.field_array(self.FIELD_ARR_ENCODED)[0],
                         len(self.FIELD_ARR_ENCODED))

    def test_decode_field_array_data_type(self):
        self.assertIsInstance(
            codec.decode.field_array(self.FIELD_ARR_ENCODED)[1], list)

    def test_decode_field_array_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.field_array, None)

    def test_decode_field_array_value(self):
        value = codec.decode.field_array(self.FIELD_ARR_ENCODED)[1]
        for position in xrange(0, len(value)):
            if isinstance(value[position], float):
                self.assertAlmostEqual(round(value[position], 3),
                                       round(self.FIELD_ARR_VALUE[position], 3))
            else:
                self.assertEqual(value[position],
                                 self.FIELD_ARR_VALUE[position])

    def test_decode_field_table_bytes_consumed(self):
        self.assertEqual(codec.decode.field_table(self.FIELD_TBL_ENCODED)[0],
                         len(self.FIELD_TBL_ENCODED))

    def test_decode_field_table_data_type(self):
        self.assertIsInstance(
            codec.decode.field_table(self.FIELD_TBL_ENCODED)[1], dict)

    def test_decode_field_table_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.field_table, None)

    def test_decode_field_table_value(self):
        value = codec.decode.field_table(self.FIELD_TBL_ENCODED)[1]
        for key in value.keys():
            if isinstance(value[key], float):
                self.assertAlmostEqual(round(value[key], 3),
                                       round(self.FIELD_TBL_VALUE[key], 3))
            else:
                self.assertEqual(value[key], self.FIELD_TBL_VALUE[key])


    def test_decode_by_type_bit_bytes_consumed(self):
        self.assertEqual(codec.decode.by_type('\xff', 'bit', 4)[0], 0)

    def test_decode_by_type_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.by_type, '\xff', 'bit', None)

    def test_decode_by_type_bit_on(self):
        self.assertTrue(codec.decode.by_type('\xff', 'bit', 4)[1])

    def test_decode_by_type_bit_off(self):
        self.assertFalse(codec.decode.by_type('\x0f', 'bit', 4)[1])

    def test_decode_by_type_boolean_bytes_consumed(self):
        self.assertEqual(codec.decode.by_type('\x01', 'boolean')[0], 1)

    def test_decode_by_type_boolean_false(self):
        self.assertFalse(codec.decode.by_type('\x00', 'boolean')[1])

    def test_decode_by_type_boolean_false_data_type(self):
        self.assertIsInstance(codec.decode.by_type('\x00', 'boolean')[1], bool)

    def test_decode_by_type_boolean_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.by_type, None, 'boolean')

    def test_decode_by_type_boolean_true(self):
        self.assertTrue(codec.decode.by_type('\x01', 'boolean')[1])

    def test_decode_by_type_boolean_true_data_type(self):
        self.assertIsInstance(codec.decode.by_type('\x01', 'boolean')[1], bool)

    def test_decode_by_type_decimal_bytes_consumed(self):
        value = '\x05\x00\x04\xcb/'
        self.assertEqual(codec.decode.by_type(value, 'decimal')[0], len(value))

    def test_decode_by_type_decimal_data_type(self):
        self.assertIsInstance(codec.decode.by_type('\x05\x00\x04\xcb/',
                                                   'decimal')[1],
                              decimal.Decimal)

    def test_decode_by_type_decimal_value(self):
        self.assertEqual(round(codec.decode.by_type('\x05\x00\x04\xcb/',
                                                    'decimal')[1], 5),
                         round(float(decimal.Decimal('3.14159')), 5))

    def test_decode_by_type_decimal_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.by_type, False, 'decimal')

    def test_decode_by_type_floating_point_bytes_consumed(self):
        self.assertEqual(codec.decode.by_type('@I\x0f\xd0', 'float')[0], 4)

    def test_decode_by_type_floating_point_data_type(self):
        self.assertIsInstance(codec.decode.by_type('@I\x0f\xd0', 'float')[1],
                              float)

    def test_decode_by_type_floating_point_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.by_type, False, 'float')

    def test_decode_by_type_floating_point_value(self):
        self.assertEqual(round(codec.decode.by_type('@I\x0f\xd0', 'float')[1],
                               5),
                         round(float(3.14159), 5))

    def test_decode_by_type_long_bytes_consumed(self):
        self.assertEqual(codec.decode.by_type('\x7f\xff\xff\xff',
                                              'long')[0], 4)

    def test_decode_by_type_long_data_type(self):
        self.assertIsInstance(codec.decode.by_type('\x7f\xff\xff\xff',
                                                   'long')[1], int)

    def test_decode_by_type_long_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.by_type, None, 'long')

    def test_decode_by_type_long_value(self):
        self.assertEqual(codec.decode.by_type('\x7f\xff\xff\xff',
                                              'long')[1], 2147483647)

    def test_decode_by_type_long_long_bytes_consumed(self):
        self.assertEqual(codec.decode.by_type('\x7f\xff\xff\xff\xff\xff\xff'
                                              '\xf8', 'longlong')[0], 8)

    def test_decode_by_type_long_long_data_type(self):
        self.assertIsInstance(codec.decode.by_type('\x7f\xff\xff\xff\xff\xff'
                                                   '\xff\xf8',
                                                   'longlong')[1], int)

    def test_decode_by_type_long_long_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.by_type, None, 'longlong')

    def test_decode_by_type_long_long_value(self):
        self.assertEqual(codec.decode.by_type('\x7f\xff\xff\xff\xff\xff\xff'
                                              '\xf8', 'longlong')[1],
                         9223372036854775800)

    def test_decode_by_type_longstr_bytes_consumed(self):
        self.assertEqual(codec.decode.by_type('\x00\x00\x00\n0123456789',
                                              'longstr')[0], 14)

    def test_decode_by_type_longstr_data_type(self):
        self.assertIsInstance(
            codec.decode.by_type('\x00\x00\x00\n0123456789', 'longstr')[1],
            unicode)

    def test_decode_by_type_longstr_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.by_type, None, 'longstr')

    def test_decode_by_type_longstr_value(self):
        self.assertEqual(codec.decode.by_type('\x00\x00\x00\n0123456789',
                                              'longstr')[1],
                         '0123456789')

    def test_decode_by_type_octet_bytes_consumed(self):
        self.assertEqual(codec.decode.by_type('\xff', 'octet')[0], 1)

    def test_decode_by_type_octet_data_type(self):
        self.assertIsInstance(codec.decode.by_type('\xff', 'octet')[1], int)

    def test_decode_by_type_octet_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.by_type, None, 'octet')

    def test_decode_by_type_octet_value(self):
        self.assertEqual(codec.decode.by_type('\xff', 'octet')[1], 255)

    def test_decode_by_type_short_bytes_consumed(self):
        self.assertEqual(codec.decode.by_type('\x7f\xff', 'short')[0], 2)

    def test_decode_by_type_short_data_type(self):
        self.assertIsInstance(codec.decode.by_type('\x7f\xff',
                                                   'short')[1], int)

    def test_decode_by_type_short_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.by_type, None, 'short')

    def test_decode_by_type_short_value(self):
        self.assertEqual(codec.decode.by_type('\x7f\xff', 'short')[1],
                         32767)

    def test_decode_by_type_shortstr_bytes_consumed(self):
        self.assertEqual(codec.decode.by_type('\n0123456789', 'shortstr')[0],
                         11)

    def test_decode_by_type_shortstr_data_type(self):
        self.assertIsInstance(codec.decode.by_type('\n0123456789',
                                                   'shortstr')[1], unicode)

    def test_decode_by_type_shortstr_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.by_type, None, 'shortstr')

    def test_decode_by_type_shortstr_value(self):
        self.assertEqual(codec.decode.by_type('\n0123456789', 'shortstr')[1],
                         '0123456789')

    def test_decode_by_type_timestamp_bytes_consumed(self):
        self.assertEqual(codec.decode.by_type('\x00\x00\x00\x00Ec)\x92',
                                              'timestamp')[0], 8)

    def test_decode_by_type_timestamp_data_type(self):
        self.assertIsInstance(
            codec.decode.by_type('\x00\x00\x00\x00Ec)\x92', 'timestamp')[1],
            time.struct_time)

    def test_decode_by_type_timestamp_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.by_type, None, 'timestamp')

    def test_decode_by_type_timestamp_value(self):
        self.assertEqual(codec.decode.by_type('\x00\x00\x00\x00Ec)\x92',
                                              'timestamp')[1],
                         time.struct_time((2006, 11, 21,
                                           16, 30, 10, 1, 325, 0)))

    def test_decode_by_type_field_array_bytes_consumed(self):
        self.assertEqual(codec.decode.by_type(self.FIELD_ARR_ENCODED,
                                              'array')[0],
                         len(self.FIELD_ARR_ENCODED))

    def test_decode_by_type_field_array_data_type(self):
        self.assertIsInstance(codec.decode.by_type(self.FIELD_ARR_ENCODED,
                                                   'array')[1], list)

    def test_decode_by_type_field_array_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.by_type, None, 'array')

    def test_decode_by_type_field_array_value(self):
        value = codec.decode.by_type(self.FIELD_ARR_ENCODED, 'array')[1]
        for position in xrange(0, len(value)):
            if isinstance(value[position], float):
                self.assertAlmostEqual(round(value[position], 3),
                                       round(self.FIELD_ARR_VALUE[position], 3))
            else:
                self.assertEqual(value[position],
                                 self.FIELD_ARR_VALUE[position])

    def test_decode_by_type_field_table_bytes_consumed(self):
        self.assertEqual(codec.decode.by_type(self.FIELD_TBL_ENCODED,
                                              'table')[0],
                         len(self.FIELD_TBL_ENCODED))

    def test_decode_by_type_field_table_data_type(self):
        self.assertIsInstance(codec.decode.by_type(self.FIELD_TBL_ENCODED,
                                                   'table')[1], dict)

    def test_decode_by_type_field_table_invalid_value(self):
        self.assertRaises(ValueError, codec.decode.by_type, None, 'table')

    def test_decode_by_type_field_table_value(self):
        value = codec.decode.by_type(self.FIELD_TBL_ENCODED, 'table')[1]
        for key in value.keys():
            if isinstance(value[key], float):
                self.assertAlmostEqual(round(value[key], 3),
                                       round(self.FIELD_TBL_VALUE[key], 3))
            else:
                self.assertEqual(value[key], self.FIELD_TBL_VALUE[key])

    def test_decode_embedded_value_empty_bytes_consumed(self):
        self.assertEqual(codec.decode._embedded_value('')[0], 0)

    def test_decode_embedded_value_empty_value(self):
        self.assertEqual(codec.decode._embedded_value('')[1], None)

    def test_decode_embedded_value_decimal_bytes_consumed(self):
        value = 'D\x05\x00\x04\xcb/'
        self.assertEqual(codec.decode._embedded_value(value)[0], len(value))

    def test_decode_embedded_value_decimal_data_type(self):
        self.assertIsInstance(
            codec.decode._embedded_value('D\x05\x00\x04\xcb/')[1],
            decimal.Decimal)

    def test_decode_embedded_value_decimal_value(self):
        self.assertEqual(
            round(codec.decode._embedded_value('D\x05\x00\x04\xcb/')[1], 5),
            round(float(decimal.Decimal('3.14159')), 5))

    def test_decode_embeded_value_long_bytes_consumed(self):
        self.assertEqual(codec.decode._embedded_value('I\x7f\xff\xff\xff')[0],
                         5)

    def test_decode_embeded_value_long_data_type(self):
        self.assertIsInstance(
            codec.decode._embedded_value('I\x7f\xff\xff\xff')[1], int)

    def test_decode_embeded_value_long_value(self):
        self.assertEqual(codec.decode._embedded_value('I\x7f\xff\xff\xff')[1],
                         2147483647)

    def test_decode_embeded_value_long_long_bytes_consumed(self):
        self.assertEqual(
            codec.decode._embedded_value('L\x7f\xff\xff\xff'
                                         '\xff\xff\xff\xf8')[0], 9)

    def test_decode_embeded_value_long_long_data_type(self):
        self.assertIsInstance(
            codec.decode._embedded_value('L\x7f\xff\xff\xff'
                                         '\xff\xff\xff\xf8')[1], int)

    def test_decode_embeded_value_long_long_value(self):
        self.assertEqual(
            codec.decode._embedded_value('L\x7f\xff\xff\xff'
                                         '\xff\xff\xff\xf8')[1],
                         9223372036854775800)

    def test_decode_embeded_value_longstr_bytes_consumed(self):
        self.assertEqual(
            codec.decode._embedded_value('S\x00\x00\x00\n0123456789')[0], 15)

    def test_decode_embeded_value_longstr_data_type(self):
        self.assertIsInstance(
            codec.decode._embedded_value('S\x00\x00\x00\n0123456789')[1],
            unicode)

    def test_decode_embeded_value_longstr_value(self):
        self.assertEqual(
            codec.decode._embedded_value('S\x00\x00\x00\n0123456789')[1],
            '0123456789')

    def test_decode_embeded_value_short_bytes_consumed(self):
        self.assertEqual(codec.decode._embedded_value('U\x7f\xff')[0], 3)

    def test_decode_embeded_value_short_data_type(self):
        self.assertIsInstance(codec.decode._embedded_value('U\x7f\xff')[1], int)

    def test_decode_embeded_value_short_value(self):
        self.assertEqual(codec.decode._embedded_value('U\x7f\xff')[1],
                         32767)

    def test_decode_embeded_value_shortstr_bytes_consumed(self):
        self.assertEqual(codec.decode._embedded_value('s\n0123456789')[0],
                         12)

    def test_decode_embeded_value_shortstr_data_type(self):
        self.assertIsInstance(codec.decode._embedded_value('s\n0123456789')[1],
                              unicode)

    def test_decode_embeded_value_shortstr_value(self):
        self.assertEqual(codec.decode._embedded_value('s\n0123456789')[1],
                         '0123456789')

    def test_decode_embeded_value_timestamp_bytes_consumed(self):
        self.assertEqual(
            codec.decode._embedded_value('T\x00\x00\x00\x00Ec)\x92')[0], 9)

    def test_decode_embeded_value_timestamp_data_type(self):
        self.assertIsInstance(
            codec.decode._embedded_value('T\x00\x00\x00\x00Ec)\x92')[1],
            time.struct_time)

    def test_decode_embedded_value_timestamp_value(self):
        self.assertEqual(
            codec.decode._embedded_value('T\x00\x00\x00\x00Ec)\x92')[1],
            time.struct_time((2006, 11, 21, 16, 30, 10, 1, 325, 0)))

    def test_decode_embedded_value_field_array_bytes_consumed(self):
        self.assertEqual(
            codec.decode._embedded_value('A' + self.FIELD_ARR_ENCODED)[0],
            len('A' + self.FIELD_ARR_ENCODED))

    def test_decode_embedded_value_field_array_data_type(self):
        self.assertIsInstance(
            codec.decode._embedded_value('A' + self.FIELD_ARR_ENCODED)[1], list)

    def test_decode_embedded_value_field_array_value(self):
        value = codec.decode._embedded_value('A' + self.FIELD_ARR_ENCODED)[1]
        for position in xrange(0, len(value)):
            if isinstance(value[position], float):
                self.assertAlmostEqual(round(value[position], 3),
                                       round(self.FIELD_ARR_VALUE[position], 3))
            else:
                self.assertEqual(value[position],
                                 self.FIELD_ARR_VALUE[position])

    def test_decode_embedded_value_field_table_bytes_consumed(self):
        self.assertEqual(
            codec.decode._embedded_value('F' + self.FIELD_TBL_ENCODED)[0],
            len('F' + self.FIELD_TBL_ENCODED))

    def test_decode_embedded_value_field_table_data_type(self):
        self.assertIsInstance(
            codec.decode._embedded_value('F' + self.FIELD_TBL_ENCODED)[1], dict)

    def test_decode_embedded_value_field_table_value(self):
        value = codec.decode._embedded_value('F' + self.FIELD_TBL_ENCODED)[1]
        for key in value.keys():
            if isinstance(value[key], float):
                self.assertAlmostEqual(round(value[key], 3),
                                       round(self.FIELD_TBL_VALUE[key], 3))
            else:
                self.assertEqual(value[key], self.FIELD_TBL_VALUE[key])
