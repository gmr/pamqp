import datetime
import decimal
import os
import time
import unittest

from pamqp import encode


class MarshalingTests(unittest.TestCase):
    def test_encode_bool_wrong_type(self):
        self.assertRaises(TypeError, encode.boolean, 'hi')

    def test_encode_bool_false(self):
        self.assertEqual(encode.boolean(False), b'\x00')

    def test_encode_bool_true(self):
        self.assertEqual(encode.boolean(True), b'\x01')

    def test_encode_byte_array(self):
        self.assertEqual(
            encode.byte_array(bytearray([65, 66, 67])), b'\x00\x00\x00\x03ABC'
        )

    def test_encode_byte_array_bytes(self):
        self.assertEqual(encode.byte_array(b'ABC'), b'\x00\x00\x00\x03ABC')

    def test_encode_byte_array_wrong_type(self):
        self.assertRaises(TypeError, encode.byte_array, 'ABC')

    def test_encode_field_table_bytes_value(self):
        # Reproduction from issue #79
        self.assertEqual(
            encode.field_table({'key': b'value'}),
            b'\x00\x00\x00\x0e\x03keyx\x00\x00\x00\x05value',
        )

    def test_encode_field_array_bytes_value(self):
        self.assertEqual(
            encode.field_array([b'AB', bytearray(b'CD')]),
            b'\x00\x00\x00\x0ex\x00\x00\x00\x02ABx\x00\x00\x00\x02CD',
        )

    def test_encode_decimal_wrong_type(self):
        self.assertRaises(TypeError, encode.decimal, 3.141597)

    def test_encode_decimal(self):
        self.assertEqual(
            encode.decimal(decimal.Decimal('3.14159')), b'\x05\x00\x04\xcb/'
        )

    def test_encode_decimal_whole(self):
        self.assertEqual(
            encode.decimal(decimal.Decimal(314159)), b'\x00\x00\x04\xcb/'
        )

    def test_encode_decimal_scientific_notation(self):
        self.assertEqual(
            encode.decimal(decimal.Decimal('1E-10')), b'\n\x00\x00\x00\x01'
        )

    def test_encode_decimal_negative(self):
        self.assertEqual(
            encode.decimal(decimal.Decimal('-1.5')),
            b'\x01\xff\xff\xff\xf1',
        )

    def test_encode_decimal_positive_exponent(self):
        self.assertEqual(
            encode.decimal(decimal.Decimal('1E2')), b'\x00\x00\x00\x00d'
        )

    def test_encode_decimal_scale_out_of_range(self):
        self.assertRaises(TypeError, encode.decimal, decimal.Decimal('1E-300'))

    def test_encode_decimal_mantissa_out_of_range(self):
        self.assertRaises(
            TypeError, encode.decimal, decimal.Decimal('9999999999.9')
        )

    def test_encode_decimal_not_finite(self):
        self.assertRaises(TypeError, encode.decimal, decimal.Decimal('NaN'))

    def test_encode_double_invalid_value(self):
        self.assertRaises(TypeError, encode.double, '1234')

    def test_encode_double(self):
        self.assertEqual(encode.double(3.14159), b'@\t!\xf9\xf0\x1b\x86n')

    def test_encode_floating_point_type(self):
        self.assertRaises(TypeError, encode.floating_point, '1234')

    def test_encode_float(self):
        self.assertEqual(encode.floating_point(3.14159), b'@I\x0f\xd0')

    def test_encode_long_int_wrong_type(self):
        self.assertRaises(TypeError, encode.long_int, 3.141597)

    def test_encode_table_integer_bad_value_error(self):
        self.assertRaises(TypeError, encode.long_int, 9223372036854775808)

    def test_encode_long_int(self):
        self.assertEqual(encode.long_int(2147483647), b'\x7f\xff\xff\xff')

    def test_encode_long_int_error(self):
        self.assertRaises(TypeError, encode.long_int, 21474836449)

    def test_encode_long_uint(self):
        self.assertEqual(encode.long_uint(4294967295), b'\xff\xff\xff\xff')

    def test_encode_long_uint_error(self):
        self.assertRaises(TypeError, encode.long_uint, 4294967296)

    def test_encode_long_uint_wrong_type(self):
        self.assertRaises(TypeError, encode.long_uint, 3.141597)

    def test_encode_long_long_int_wrong_type(self):
        self.assertRaises(TypeError, encode.long_long_int, 3.141597)

    def test_encode_long_long_int_error(self):
        self.assertRaises(TypeError, encode.long_long_int, 9223372036854775808)

    def test_encode_octet(self):
        self.assertEqual(encode.octet(1), b'\x01')

    def test_encode_octet_error(self):
        self.assertRaises(TypeError, encode.octet, 'hi')

    def test_encode_short_wrong_type(self):
        self.assertRaises(TypeError, encode.short_int, 3.141597)

    def test_encode_short(self):
        self.assertEqual(encode.short_int(32767), b'\x7f\xff')

    def test_encode_short_error(self):
        self.assertRaises(TypeError, encode.short_int, 32768)

    def test_encode_short_error_message(self):
        with self.assertRaises(TypeError) as ctx:
            encode.short_int(-32769)
        self.assertEqual(
            str(ctx.exception), 'Short integer range: -32768 to 32767'
        )

    def test_encode_short_uint(self):
        self.assertEqual(encode.short_uint(65535), b'\xff\xff')

    def test_encode_short_uint_error(self):
        self.assertRaises(TypeError, encode.short_uint, 65536)

    def test_encode_short_uint_type_error(self):
        self.assertRaises(TypeError, encode.short_uint, 'hello')

    def test_encode_table_integer_error(self):
        self.assertRaises(TypeError, encode.table_integer, 9223372036854775808)

    def test_encode_short_string(self):
        self.assertEqual(encode.short_string('Hello'), b'\x05Hello')

    def test_encode_short_string_error(self):
        self.assertRaises(TypeError, encode.short_string, 32768)

    def test_encode_short_string_too_long(self):
        self.assertRaises(TypeError, encode.short_string, 'a' * 256)

    def test_encode_short_string_too_long_utf8_bytes(self):
        # 128 multi-byte chars encode to more than 255 bytes
        self.assertRaises(TypeError, encode.short_string, '🐰' * 128)

    def test_encode_short_string_utf8_python3(self):
        self.assertEqual(encode.short_string('🐰'), b'\x04\xf0\x9f\x90\xb0')

    def test_encode_long_string(self):
        self.assertEqual(
            encode.long_string('0123456789'), b'\x00\x00\x00\n0123456789'
        )

    def test_encode_long_string_bytes(self):
        self.assertEqual(
            encode.long_string('rabbitmq'), b'\x00\x00\x00\x08rabbitmq'
        )

    def test_encode_long_string_utf8_python3(self):
        self.assertEqual(
            encode.long_string('🐰'), b'\x00\x00\x00\x04\xf0\x9f\x90\xb0'
        )

    def test_encode_long_string_error(self):
        self.assertRaises(TypeError, encode.long_string, 100)

    def test_encode_timestamp_from_datetime(self):
        self.assertEqual(
            encode.timestamp(
                datetime.datetime(
                    2006, 11, 21, 16, 30, 10, tzinfo=datetime.UTC
                )
            ),
            b'\x00\x00\x00\x00Ec)\x92',
        )

    @unittest.skipUnless(hasattr(time, 'tzset'), 'needs time.tzset')
    def test_encode_timestamp_from_naive_datetime_is_utc(self):
        old_tz = os.environ.get('TZ')
        os.environ['TZ'] = 'America/New_York'
        time.tzset()
        try:
            value = encode.timestamp(
                datetime.datetime(2006, 11, 21, 16, 30, 10)
            )
        finally:
            if old_tz is None:
                del os.environ['TZ']
            else:
                os.environ['TZ'] = old_tz
            time.tzset()
        self.assertEqual(value, b'\x00\x00\x00\x00Ec)\x92')

    def test_encode_timestamp_from_struct_time(self):
        value = encode.timestamp(
            datetime.datetime(
                2006, 11, 21, 16, 30, 10, tzinfo=datetime.UTC
            ).timetuple()
        )
        self.assertEqual(value, b'\x00\x00\x00\x00Ec)\x92')

    def test_encode_timestamp_error(self):
        self.assertRaises(TypeError, encode.timestamp, 'hi')

    def test_encode_field_array(self):
        expectation = (
            b'\x00\x00\x00GI\x00\x00\x00\x01I\x00\x00\xaf\xc8I\x02bZ\x00S\x00\x00\x00\x04TestT\x00\x00\x00\x00Ec)\x92I\xbb\x9a'
            b'\xca\x00D\x02\x00\x00\x01:d@\t\x1e\xb8Q\xeb\x85\x1fl\x00\x00\x00\x00\xc4e5\xffl\x80\x00\x00\x00\x00\x00\x00\x08'
        )
        data = [
            1,
            45000,
            40000000,
            'Test',
            datetime.datetime(2006, 11, 21, 16, 30, 10, tzinfo=datetime.UTC),
            -1147483648,
            decimal.Decimal('3.14'),
            3.14,
            3294967295,
            -9223372036854775800,
        ]
        self.assertEqual(encode.field_array(data), expectation)

    def test_encode_field_array_error(self):
        self.assertRaises(TypeError, encode.field_array, 'hi')

    def test_encode_field_table_empty(self):
        self.assertEqual(encode.field_table(None), b'\x00\x00\x00\x00')

    def test_encode_field_table_type_error(self):
        self.assertRaises(TypeError, encode.field_table, [1, 2, 3])

    def test_encode_field_table_object(self):
        self.assertRaises(
            TypeError, encode.field_table, {'key': encode.field_table}
        )

    def test_encode_field_table(self):
        expectation = (
            b'\x00\x00\x047\x08arrayvalA\x00\x00\x00\x0fI\x00\x00\x00\x01I\x00\x00\x00\x02I\x00\x00\x00\x03\x07boolva'
            b'lt\x01\tbytearrayx\x00\x00\x00\x03AAA\x06decvalD\x02\x00\x00\x01:\x07dictv'
            b'alF\x00\x00\x00\x0c\x03fooS\x00\x00\x00\x03bar\x08floatvald@\t\x1e\xb8Q\xeb\x85\x1f\x06in'
            b'tvalI\x00\x00\x00\x01\x07longstrS\x00\x00\x03t000000000000000000'
            b'0000000000000000000000000000000000111111'
            b'1111111111111111111111111111111111111111'
            b'1111112222222222222222222222222222222222'
            b'2222222222222222221111111111111111111111'
            b'1111111111111111111111111111112222222222'
            b'2222222222222222222222222222222222222222'
            b'2211111111111111111111111111111111111111'
            b'1111111111111122222222222222222222222222'
            b'2222222222222222222222222211111111111111'
            b'1111111111111111111111111111111111111122'
            b'2222222222222222222222222222222222222222'
            b'2222222222111111111111111111111111111111'
            b'1111111111111111111111222222222222222222'
            b'2222222222222222222222222222222222111111'
            b'1111111111111111111111111111111111111111'
            b'1111112222222222222222222222222222222222'
            b'2222222222222222221111111111111111111111'
            b'1111111111111111111111111111112222222222'
            b'2222222222222222222222222222222222222222'
            b'2211111111111111111111111111111111111111'
            b'1111111111111100000000000000000000000000'
            b'00000000000000000000000000\x07longvalI6e&U\x04'
            b'noneV\x06strvalS\x00\x00\x00\x04Test\x0ctimestampvalT\x00\x00\x00\x00E'
            b'c)\x92'
        )
        data = {
            'intval': 1,
            'strval': 'Test',
            'boolval': True,
            'timestampval': datetime.datetime(
                2006, 11, 21, 16, 30, 10, tzinfo=datetime.UTC
            ),
            'decval': decimal.Decimal('3.14'),
            'floatval': 3.14,
            'longval': 912598613,
            'dictval': {'foo': 'bar'},
            'arrayval': [1, 2, 3],
            'none': None,
            'bytearray': bytearray((65, 65, 65)),
            'longstr': (
                '0000000000000000000000000000000000000000000000000'
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
                '00'
            ),
        }
        self.assertEqual(encode.field_table(data), expectation)

    def test_encode_by_type_field_array(self):
        expectation = (
            b'\x00\x00\x00GI\x00\x00\x00\x01I\x00\x00BhI\x00\x00\xaf\xc8S\x00\x00\x00\x04TestT\x00\x00\x00\x00Ec)\x92I\xbb\x9a'
            b'\xca\x00D\x02\x00\x00\x01:d@\t\x1e\xb8Q\xeb\x85\x1fl\x00\x00\x00\x00\xc4e5\xffl\x80\x00\x00\x00\x00\x00\x00\x08'
        )
        data = [
            1,
            17000,
            45000,
            'Test',
            datetime.datetime(2006, 11, 21, 16, 30, 10, tzinfo=datetime.UTC),
            -1147483648,
            decimal.Decimal('3.14'),
            3.14,
            3294967295,
            -9223372036854775800,
        ]
        self.assertEqual(encode.by_type(data, 'field_array'), expectation)

    def test_encode_table_with_negative_integer(self):
        data = {'x-priority': -1}
        result = encode.field_table(data)
        self.assertIn(b'x-priority', result)
        self.assertIn(b'I\xff\xff\xff\xff', result)

    def test_encode_by_type_byte_array(self):
        self.assertEqual(
            encode.by_type(bytearray((65, 66, 67)), 'bytearray'),
            b'\x00\x00\x00\x03ABC',
        )

    def test_encode_by_type_double(self):
        self.assertEqual(
            encode.by_type(float(4294967295), 'double'),
            b'A\xef\xff\xff\xff\xe0\x00\x00',
        )

    def test_encode_by_type_long_uint(self):
        self.assertEqual(
            encode.by_type(4294967295, 'long'), b'\xff\xff\xff\xff'
        )

    def test_encode_by_type_long_long_int(self):
        self.assertEqual(
            encode.by_type(9223372036854775800, 'longlong'),
            b'\x7f\xff\xff\xff\xff\xff\xff\xf8',
        )

    def test_encode_by_type_long_str(self):
        self.assertEqual(
            encode.by_type('0123456789', 'longstr'),
            b'\x00\x00\x00\n0123456789',
        )

    def test_encode_by_type_none(self):
        self.assertEqual(encode.by_type(None, 'void'), b'')

    def test_encode_by_type_octet(self):
        self.assertEqual(encode.by_type(1, 'octet'), b'\x01')

    def test_encode_by_type_short(self):
        self.assertEqual(encode.by_type(32767, 'short'), b'\x7f\xff')

    def test_encode_by_type_timestamp(self):
        self.assertEqual(
            encode.by_type(
                datetime.datetime(
                    2006, 11, 21, 16, 30, 10, tzinfo=datetime.UTC
                ),
                'timestamp',
            ),
            b'\x00\x00\x00\x00Ec)\x92',
        )

    def test_encode_by_type_field_table(self):
        expectation = (
            b'\x00\x00\x04V\x08arrayvalA\x00\x00\x00\x0fI\x00\x00\x00\x01I\x00\x00\x10`I\x00\x00\xa4\x10\x07boolva'
            b'lt\x01\x06decvalD\x02\x00\x00\x01:\x07dictvalF\x00\x00\x00\x0c\x03fooS\x00\x00\x00\x03ba'
            b'r\x08floatvald@\t\x1e\xb8Q\xeb\x85\x1f\x07longstrS\x00\x00\x03t00000000'
            b'0000000000000000000000000000000000000000'
            b'0000111111111111111111111111111111111111'
            b'1111111111111111222222222222222222222222'
            b'2222222222222222222222222222111111111111'
            b'1111111111111111111111111111111111111111'
            b'2222222222222222222222222222222222222222'
            b'2222222222221111111111111111111111111111'
            b'1111111111111111111111112222222222222222'
            b'2222222222222222222222222222222222221111'
            b'1111111111111111111111111111111111111111'
            b'1111111122222222222222222222222222222222'
            b'2222222222222222222211111111111111111111'
            b'1111111111111111111111111111111122222222'
            b'2222222222222222222222222222222222222222'
            b'2222111111111111111111111111111111111111'
            b'1111111111111111222222222222222222222222'
            b'2222222222222222222222222222111111111111'
            b'1111111111111111111111111111111111111111'
            b'2222222222222222222222222222222222222222'
            b'2222222222221111111111111111111111111111'
            b'1111111111111111111111110000000000000000'
            b'000000000000000000000000000000000000\x07lon'
            b'gvalI6e&U\x06s32intI\xc4e6\x00\x06s64intl7\x82\xda\xce\x9d\x90\x00\x00\x06st'
            b'rvalS\x00\x00\x00\x04Test\x0ctimestampvalT\x00\x00\x00\x00Ec)\x92\x06u16i'
            b'ntI\x00\x00 \x00\x06u32intl\x00\x00\x00\x00\xeek(\x00\x05u8bitI\x00\x00\x00 '
        )
        data = {
            'u8bit': 32,
            'u16int': 8192,
            's32int': -1000000000,
            'u32int': 4000000000,
            's64int': 4000000000000000000,
            'strval': 'Test',
            'boolval': True,
            'timestampval': datetime.datetime(
                2006, 11, 21, 16, 30, 10, tzinfo=datetime.UTC
            ),
            'decval': decimal.Decimal('3.14'),
            'floatval': 3.14,
            'longval': 912598613,
            'dictval': {'foo': 'bar'},
            'arrayval': [1, 4192, 42000],
            'longstr': (
                '0000000000000000000000000000000000000000000000000'
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
                '00'
            ),
        }
        self.assertEqual(encode.by_type(data, 'table'), expectation)

    def test_encode_by_type_error(self):
        self.assertRaises(TypeError, encode.by_type, 12345.12434, 'foo')


class EncodeTableIntegerTestCase(unittest.TestCase):
    def test_table_integer(self):
        tests = {
            'small': (5, b'I\x00\x00\x00\x05'),
            'negative': (-1, b'I\xff\xff\xff\xff'),
            'int32-max': (2147483647, b'I\x7f\xff\xff\xff'),
            'int32-min': (-2147483648, b'I\x80\x00\x00\x00'),
            'int32-max-plus-one': (
                2147483648,
                b'l\x00\x00\x00\x00\x80\x00\x00\x00',
            ),
            'int32-min-minus-one': (
                -2147483649,
                b'l\xff\xff\xff\xff\x7f\xff\xff\xff',
            ),
            'int64-max': (
                9223372036854775807,
                b'l\x7f\xff\xff\xff\xff\xff\xff\xff',
            ),
        }
        for key, value in tests.items():
            result = encode.table_integer(value[0])
            self.assertEqual(
                result,
                value[1],
                f'encode {key} mismatch ({result!r} != {value[1]!r})',
            )

    def test_table_float_is_double(self):
        self.assertEqual(
            encode.encode_table_value(0.1), b'd' + encode.double(0.1)
        )

    def test_too_large_int(self):
        with self.assertRaises(TypeError):
            encode.table_integer(9223372036854775809)

    def test_deprecated_rabbitmq_support_warns(self):
        with self.assertWarns(DeprecationWarning):
            encode.support_deprecated_rabbitmq(True)
        with self.assertWarns(DeprecationWarning):
            self.assertFalse(encode.DEPRECATED_RABBITMQ_SUPPORT)
        self.assertEqual(encode.table_integer(5), b'I\x00\x00\x00\x05')

    def test_unknown_module_attribute(self):
        with self.assertRaises(AttributeError):
            encode.does_not_exist  # noqa: B018
