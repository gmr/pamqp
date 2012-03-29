# coding=utf-8

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-09-23'

import sys
sys.path.insert(0, '..')

from pamqp import codec

from datetime import datetime
from decimal import Decimal


def test_encode_bool_wrong_type():
    try:
        codec.encode.boolean('Hi')
    except ValueError:
        return
    assert False, 'encode.boolean did not raise a ValueError Exception'


def test_encode_bool_false():
    expectation = '\x00'
    value = codec.encode.boolean(False)
    if value != expectation:
        assert False, ('Encoded value does not match expectation value: %r' %
                       value)


def test_encode_bool_true():
    expectation = '\x01'
    value = codec.encode.boolean(True)
    if value != expectation:
        assert False, ('Encoded value does not match expectation value: %r' %
                       value)


def test_encode_decimal_wrong_type():
    try:
        codec.encode.decimal(3.141597)
    except ValueError:
        return
    assert False, 'encode.decimal did not raise a ValueError Exception'


def test_encode_decimal():
    expectation = '\x05\x00\x04\xcb/'
    value = codec.encode.decimal(Decimal('3.14159'))
    if value != expectation:
        assert False, ('Encoded value does not match expectation value: %r' %
                       value)


def test_encode_decimal_whole():
    expectation = '\x00\x00\x04\xcb/'
    value = codec.encode.decimal(Decimal('314159'))
    if value != expectation:
        assert False, ('Encoded value does not match expectation value: %r' %
                       value)


def test_encode_floating_point_type():
    try:
        codec.encode.floating_point('1234')
    except ValueError:
        return
    assert False, 'encode.float did not raise a ValueError Exception'


def test_encode_float():
    expectation = '@I\x0f\xd0'
    value = codec.encode.floating_point(float(3.14159))
    if value != expectation:
        assert False, \
            'Encoded value does not match expectation value: %r' % value


def test_encode_long_int_wrong_type():
    try:
        codec.encode.long_int(3.141597)
    except ValueError:
        return
    assert False, 'encode.long_int did not raise a ValueError Exception'


def test_encode_table_integer_bad_value_error():
    try:
        codec.encode.table_integer(9223372036854775808)
    except ValueError:
        return
    assert False, 'encode.table_integer did not raise a ValueError Exception'


def test_encode_long_int():
    expectation = '\x7f\xff\xff\xff'
    value = codec.encode.long_int(long(2147483647))
    if value != expectation:
        assert False, \
            'Encoded value does not match expectation value: %r' % value


def test_encode_long_int_error():
    try:
        codec.encode.long_int(long(21474836449))
    except ValueError:
        return
    assert False, 'encode.long_int did not raise a ValueError Exception'


def test_encode_long_long_int_wrong_type():
    try:
        codec.encode.long_long_int(3.141597)
    except ValueError:
        return
    assert False, 'encode.long_long_int did not raise a ValueError Exception'


def test_encode_long_long_int():
    expectation = '\x7f\xff\xff\xff\xff\xff\xff\xf8'
    value = codec.encode.long_long_int(long(9223372036854775800))
    if value != expectation:
        assert False, \
            'Encoded value does not match expectation value: %r' % value


def test_encode_long_long_int_error():
    try:
        codec.encode.long_long_int(long(9223372036854775808))
    except ValueError:
        return
    assert False, 'encode.long_long_int did not raise a ValueError Exception'


def test_encode_octet():
    expectation = '\x01'
    value = codec.encode.octet(1)
    if value != expectation:
        assert False, \
            'Encoded value does not match expectation value: %r' % value


def test_encode_octet_error():
    try:
        codec.encode.octet('hi')
    except ValueError:
        return
    assert False, 'encode.octet did not raise a ValueError Exception'


def test_encode_short_wrong_type():
    try:
        codec.encode.short_int(3.141597)
    except ValueError:
        return
    assert False, 'encode.short_int did not raise a ValueError Exception'


def test_encode_short():
    expectation = '\x7f\xff'
    value = codec.encode.short_int(32767)
    if value != expectation:
        assert False, ('Encoded value does not match expectation value: %r' %
                       value)


def test_encode_integer_error():
    try:
        codec.encode.table_integer(9223372036854775808)
    except ValueError:
        return
    assert False, 'encode.table_integer did not raise a ValueError Exception'


def test_encode_short_error():
    try:
        codec.encode.short_int(32768)
    except ValueError:
        return
    assert False, 'encode.short_int did not raise a ValueError Exception'


def test_encode_long_string():
    expectation = '\x00\x00\x00\n0123456789'
    value = codec.encode.long_string('0123456789')
    if value != expectation:
        assert False, ('Encoded value does not match expectation value: %r' %
                       value)


def test_encode_long_string_error():
    try:
        codec.encode.long_string(100)
    except ValueError:
        return
    assert False, 'encode.long_string failed to raise a ValueError Exception'


def test_encode_short_string():
    expectation = '\n0123456789'
    value = codec.encode.short_string('0123456789')
    if value != expectation:
        assert False, ('Encoded value does not match expectation value: %r' %
                       value)


def test_encode_unicode():
    expectation = '\n0123456789'
    value = codec.encode.short_string(unicode('0123456789'))
    if value != expectation:
        assert False, ('Encoded value does not match expectation value: %r' %
                       value)


def test_encode_string_error():
    try:
        codec.encode.short_string(12345.12434)
    except ValueError:
        return
    assert False, 'encode.string did not raise a ValueError Exception'


def test_encode_long_string_error():
    try:
        codec.encode.long_string(12345.12434)
    except ValueError:
        return
    assert False, 'encode.long_string did not raise a ValueError Exception'


def test_encode_timestamp_from_datetime():
    expectation = '\x00\x00\x00\x00Ec)\x92'
    value = datetime(2006, 11, 21, 16, 30, 10)
    value = codec.encode.timestamp(value)
    if value != expectation:
        assert False, ('Encoded value does not match expectation value: %r' %
                       value)


def test_encode_timestamp_from_struct_time():
    expectation = '\x00\x00\x00\x00Ec)\x92'
    value = datetime(2006, 11, 21, 16, 30, 10).timetuple()
    value = codec.encode.timestamp(value)
    if value != expectation:
        assert False, ('Encoded value does not match expectation value: %r' %
                       value)


def test_encode_timestamp_error():
    try:
        codec.encode.timestamp('hi')
    except ValueError:
        return
    assert False, 'encode.timestamp did not raise a ValueError Exception'


def test_encode_field_array_error():
    try:
        codec.encode.field_array('hi')
    except ValueError:
        return
    assert False, 'encode.field_array did not raise a ValueError Exception'


def test_encode_field_array():
    expectation = ('\x00\x00\x009U\x00\x01I\x00\x00\xaf\xc8s\x04TestT\x00\x00'
                   '\x00\x00Ec)\x92I\xbb\x9a\xca\x00D\x02\x00\x00\x01:f@H\xf5'
                   '\xc3L\x00\x00\x00\x00\xc4e5\xffL\x80\x00\x00\x00\x00\x00'
                   '\x00\x08')
    data = [1, 45000, 'Test', datetime(2006, 11, 21, 16, 30, 10),
            -1147483648, Decimal('3.14'), 3.14, long(3294967295),
            -9223372036854775800]
    value = codec.encode.field_array(data)
    if value != expectation:
        assert False, \
                ('Encoded value does not match expectation value:\n%r\n%r' %
                 (expectation, value))


def test_encode_field_table_value_type_error():
    try:
        codec.encode.field_table({'test': object()})
    except ValueError:
        return
    assert False, 'encode.field_table did not raise a ValueError Exception'


def test_encode_field_table_empty():
    value = codec.encode.field_table(None)
    if value != '\x00\x00\x00\x00':
        assert False, \
            'Encoded value does not match expectation value: %r' % value


def test_encode_field_table_type_error():
    try:
        codec.encode.field_table([1, 2, 3])
    except ValueError:
        return
    assert False, 'encode.field_table did not raise a ValueError Exception'


def test_encode_field_table():
    expectation = ('\x00\x00\x04\r\x07longvalI6e&U\x08floatvlaf@H\xf5\xc3\x07'
                   'boolvalt\x01\x06strvals\x04Test\x06intvalU\x00\x01\x07'
                   'longstrS\x00\x00\x03t000000000000000000000000000000000'
                   '000000000000000000011111111111111111111111111111111111'
                   '111111111111111112222222222222222222222222222222222222'
                   '222222222222222111111111111111111111111111111111111111'
                   '111111111111122222222222222222222222222222222222222222'
                   '222222222221111111111111111111111111111111111111111111'
                   '111111111222222222222222222222222222222222222222222222'
                   '222222211111111111111111111111111111111111111111111111'
                   '111112222222222222222222222222222222222222222222222222'
                   '222111111111111111111111111111111111111111111111111111'
                   '122222222222222222222222222222222222222222222222222221'
                   '111111111111111111111111111111111111111111111111111222'
                   '222222222222222222222222222222222222222222222222211111'
                   '111111111111111111111111111111111111111111111112222222'
                   '222222222222222222222222222222222222222222222111111111'
                   '111111111111111111111111111111111111111111100000000000'
                   '00000000000000000000000000000000000000000\x0ctimestampval'
                   'T\x00\x00\x00\x00Ec)\x92\x06decvalD\x02\x00\x00\x01:\x08'
                   'arrayvalA\x00\x00\x00\tU\x00\x01U\x00\x02U\x00\x03\x07'
                   'dictvalF\x00\x00\x00\t\x03foos\x03bar')
    data = {'intval': 1,
            'strval': 'Test',
            'boolval': True,
            'timestampval': datetime(2006, 11, 21, 16, 30, 10),
            'decval': Decimal('3.14'),
            'floatvla': 3.14,
            'longval': long(912598613),
            'dictval': {'foo': 'bar'},
            'arrayval': [1, 2, 3],
            'longstr': ('0000000000000000000000000000000000000000000000000000'
                        '1111111111111111111111111111111111111111111111111111'
                        '2222222222222222222222222222222222222222222222222222'
                        '1111111111111111111111111111111111111111111111111111'
                        '2222222222222222222222222222222222222222222222222222'
                        '1111111111111111111111111111111111111111111111111111'
                        '2222222222222222222222222222222222222222222222222222'
                        '1111111111111111111111111111111111111111111111111111'
                        '2222222222222222222222222222222222222222222222222222'
                        '1111111111111111111111111111111111111111111111111111'
                        '2222222222222222222222222222222222222222222222222222'
                        '1111111111111111111111111111111111111111111111111111'
                        '2222222222222222222222222222222222222222222222222222'
                        '1111111111111111111111111111111111111111111111111111'
                        '2222222222222222222222222222222222222222222222222222'
                        '1111111111111111111111111111111111111111111111111111'
                        '0000000000000000000000000000000000000000000000000000')}
    value = codec.encode.field_table(data)
    if value != expectation:
        assert False,\
                ('Encoded value does not match expectation value:\n%r\n%r' %
                 (value, expectation))


def test_encode_by_type_field_array():

    expectation = ('\x00\x00\x009U\x00\x01I\x00\x00\xaf\xc8s\x04TestT\x00\x00'
                   '\x00\x00Ec)\x92I\xbb\x9a\xca\x00D\x02\x00\x00\x01:f@H\xf5'
                   '\xc3L\x00\x00\x00\x00\xc4e5\xffL\x80\x00\x00\x00\x00\x00'
                   '\x00\x08')
    data = [1, 45000, 'Test', datetime(2006, 11, 21, 16, 30, 10),
            -1147483648, Decimal('3.14'), 3.14, long(3294967295),
            -9223372036854775800]
    value = codec.encode.by_type(data, 'field_array')
    if value != expectation:
        assert False, \
                ('Encoded value does not match expectation value:\n%r\n%r' %
                 (expectation, value))


def test_encode_by_type_long_int():
    expectation = '\x7f\xff\xff\xff'
    value = codec.encode.by_type(long(2147483647), 'long')
    if value != expectation:
        assert False, \
            'Encoded value does not match expectation value: %r' % value


def test_encode_by_type_long_long_int():
    expectation = '\x7f\xff\xff\xff\xff\xff\xff\xf8'
    value = codec.encode.by_type(long(9223372036854775800), 'longlong')
    if value != expectation:
        assert False, \
            'Encoded value does not match expectation value: %r' % value


def test_encode_by_type_long_str():
    expectation = '\x00\x00\x00\n0123456789'
    value = codec.encode.by_type('0123456789', 'longstr')
    if value != expectation:
        assert False, ('Encoded value does not match expectation value: %r' %
                       value)


def test_encode_by_type_short_str():
    expectation = '\n0123456789'
    value = codec.encode.by_type('0123456789', 'shortstr')
    if value != expectation:
        assert False, ('Encoded value does not match expectation value: %r' %
                       value)


def test_encode_by_type_octet():
    expectation = '\x01'
    value = codec.encode.by_type(1, 'octet')
    if value != expectation:
        assert False, \
            'Encoded value does not match expectation value: %r' % value


def test_encode_by_type_short():
    expectation = '\x7f\xff'
    value = codec.encode.by_type(32767, 'short')
    if value != expectation:
        assert False, ('Encoded value does not match expectation value: %r' %
                       value)

def test_encode_by_type_timestamp():
    expectation = '\x00\x00\x00\x00Ec)\x92'
    value = datetime(2006, 11, 21, 16, 30, 10)
    value = codec.encode.by_type(value, 'timestamp')
    if value != expectation:
        assert False, ('Encoded value does not match expectation value: %r' %
                       value)

def test_encode_by_type_field_table():
    expectation = ('\x00\x00\x04\r\x07longvalI6e&U\x08floatvlaf@H\xf5\xc3\x07'
                   'boolvalt\x01\x06strvals\x04Test\x06intvalU\x00\x01\x07'
                   'longstrS\x00\x00\x03t000000000000000000000000000000000'
                   '000000000000000000011111111111111111111111111111111111'
                   '111111111111111112222222222222222222222222222222222222'
                   '222222222222222111111111111111111111111111111111111111'
                   '111111111111122222222222222222222222222222222222222222'
                   '222222222221111111111111111111111111111111111111111111'
                   '111111111222222222222222222222222222222222222222222222'
                   '222222211111111111111111111111111111111111111111111111'
                   '111112222222222222222222222222222222222222222222222222'
                   '222111111111111111111111111111111111111111111111111111'
                   '122222222222222222222222222222222222222222222222222221'
                   '111111111111111111111111111111111111111111111111111222'
                   '222222222222222222222222222222222222222222222222211111'
                   '111111111111111111111111111111111111111111111112222222'
                   '222222222222222222222222222222222222222222222111111111'
                   '111111111111111111111111111111111111111111100000000000'
                   '00000000000000000000000000000000000000000\x0ctimestampval'
                   'T\x00\x00\x00\x00Ec)\x92\x06decvalD\x02\x00\x00\x01:\x08'
                   'arrayvalA\x00\x00\x00\tU\x00\x01U\x00\x02U\x00\x03\x07'
                   'dictvalF\x00\x00\x00\t\x03foos\x03bar')
    data = {'intval': 1,
            'strval': 'Test',
            'boolval': True,
            'timestampval': datetime(2006, 11, 21, 16, 30, 10),
            'decval': Decimal('3.14'),
            'floatvla': 3.14,
            'longval': long(912598613),
            'dictval': {'foo': 'bar'},
            'arrayval': [1, 2, 3],
            'longstr': ('0000000000000000000000000000000000000000000000000000'
                        '1111111111111111111111111111111111111111111111111111'
                        '2222222222222222222222222222222222222222222222222222'
                        '1111111111111111111111111111111111111111111111111111'
                        '2222222222222222222222222222222222222222222222222222'
                        '1111111111111111111111111111111111111111111111111111'
                        '2222222222222222222222222222222222222222222222222222'
                        '1111111111111111111111111111111111111111111111111111'
                        '2222222222222222222222222222222222222222222222222222'
                        '1111111111111111111111111111111111111111111111111111'
                        '2222222222222222222222222222222222222222222222222222'
                        '1111111111111111111111111111111111111111111111111111'
                        '2222222222222222222222222222222222222222222222222222'
                        '1111111111111111111111111111111111111111111111111111'
                        '2222222222222222222222222222222222222222222222222222'
                        '1111111111111111111111111111111111111111111111111111'
                        '0000000000000000000000000000000000000000000000000000')}
    value = codec.encode.by_type(data, 'table')
    if value != expectation:
        assert False,\
                ('Encoded value does not match expectation value:\n%r\n%r' %
                 (value, expectation))


def test_encode_by_type_error():
    try:
        codec.encode.by_type(12345.12434, 'foo')
    except ValueError:
        return
    assert False, 'encode.by_type did not raise a ValueError Exception'
