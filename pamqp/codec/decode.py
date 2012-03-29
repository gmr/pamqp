"""AMQP Data Decoder

Functions for decoding data of various types including field tables and arrays

"""

__author__ = 'Gavin M. Roy'
__email__ = 'gavinmroy@gmail.com'
__since__ = '2011-03-29'

import decimal as _decimal
import struct
import time


def bit(value, position):
    """Decode a bit value

    :param str value: Value to decode
    :return tuple: bytes used, bool value
    :raises: ValueError

    """
    bit_buffer = struct.unpack('B', value[0])[0]
    try:
        return 0, (bit_buffer & (1 << position)) != 0
    except TypeError:
        raise ValueError('Could not unpack data')


def boolean(value):
    """Decode a boolean value

    :param str value: Value to decode
    :return tuple: bytes used, bool
    :raises: ValueError

    """
    try:
        return 1, bool(struct.unpack_from('B', value[0])[0])
    except TypeError:
        raise ValueError('Could not unpack data')


def decimal(value):
    """Decode a decimal value

    :param str value: Value to decode
    :return tuple: bytes used, decimal.Decimal value
    :raises: ValueError

    """
    try:
        decimals = struct.unpack('B', value[0])[0]
        raw = struct.unpack('>I', value[1:5])[0]
        return 5, _decimal.Decimal(raw) * (_decimal.Decimal(10) ** -decimals)
    except TypeError:
        raise ValueError('Could not unpack data')


def floating_point(value):
    """Decode a floating point value

    :param str value: Value to decode
    :return tuple: bytes used, float
    :raises: ValueError

    """
    try:
        return 4, struct.unpack_from('>f', value)[0]
    except TypeError:
        raise ValueError('Could not unpack data')

def long_int(value):
    """Decode a long integer value

    :param str value: Value to decode
    :return tuple: bytes used, int
    :raises: ValueError

    """
    try:
        return 4, struct.unpack('>l', value[0:4])[0]
    except TypeError:
        raise ValueError('Could not unpack data')


def long_long_int(value):
    """Decode a long-long integer value

    :param str value: Value to decode
    :return tuple: bytes used, int
    :raises: ValueError

    """
    try:
        return 8, struct.unpack('>q', value[0:8])[0]
    except TypeError:
        raise ValueError('Could not unpack data')


def long_str(value):
    """Decode a string value

    :param str value: Value to decode
    :return tuple: bytes used, unicode
    :raises: ValueError

    """
    try:
        length = struct.unpack('>I', value[0:4])[0]
        return length + 4, unicode(value[4:length + 4])
    except TypeError:
        raise ValueError('Could not unpack data')


def octet(value):
    """Decode an octet value

    :param str value: Value to decode
    :return tuple: bytes used, int
    :raises: ValueError

    """
    try:
        return 1, struct.unpack('B', value[0])[0]
    except TypeError:
        raise ValueError('Could not unpack data')


def short_int(value):
    """Decode a short integer value

    :param str value: Value to decode
    :return tuple: bytes used, int
    :raises: ValueError

    """
    try:
        return 2, struct.unpack_from('>H', value[0:2])[0]
    except TypeError:
        raise ValueError('Could not unpack data')


def short_str(value):
    """Decode a string value

    :param str value: Value to decode
    :return tuple: bytes used, unicode
    :raises: ValueError

    """
    try:
        length = struct.unpack('B', value[0])[0]
        return length + 1, unicode(value[1:length + 1])
    except TypeError:
        raise ValueError('Could not unpack data')


def timestamp(value):
    """Decode a timestamp value

    :param str value: Value to decode
    :return tuple: bytes used, struct_time
    :raises: ValueError

    """
    try:
        return 8, time.gmtime(struct.unpack('>Q', value[0:8])[0])
    except TypeError:
        raise ValueError('Could not unpack data')


def field_array(value):
    """Decode a field array value

    :param str value: Value to decode
    :return tuple: bytes used, list
    :raises: ValueError

    """
    try:
        length = struct.unpack('>I', value[0:4])[0]
        offset = 4
        data = list()
        field_array_end = offset + length
        while offset < field_array_end:
            consumed, result = _embedded_value(value[offset:])
            offset += consumed
            data.append(result)
        return offset, data
    except TypeError:
        raise ValueError('Could not unpack data')


def field_table(value):
    """Decode a field array value

    :param str value: Value to decode
    :return tuple: bytes used, dict
    :raises: ValueError

    """
    try:
        length = struct.unpack('>I', value[0:4])[0]
        offset = 4
        data = dict()
        field_table_end = offset + length
        while offset < field_table_end:
            key_length = struct.unpack_from('B', value, offset)[0]
            offset += 1
            key = value[offset:offset + key_length]
            offset += key_length
            consumed, result = _embedded_value(value[offset:])
            offset += consumed
            data[key] = result
        return field_table_end, data
    except TypeError:
        raise ValueError('Could not unpack data')


def _embedded_value(value):
    """Takes in a value looking at the first byte to determine which decoder to
    use

    :param str value: Value to decode
    :return tuple: bytes consumed, mixed

    """
    if not value:
        return 0, None

    # Determine the field type and encode it
    if value[0] == 'A':
        bytes_consumed, value = field_array(value[1:])
    elif value[0] == 'D':
        bytes_consumed, value = decimal(value[1:])
    elif value[0] == 'f':
        bytes_consumed, value = floating_point(value[1:])
    elif value[0] == 'F':
        bytes_consumed, value = field_table(value[1:])
    elif value[0] == 'I':
        bytes_consumed, value = long_int(value[1:])
    elif value[0] == 'L':
        bytes_consumed, value = long_long_int(value[1:])
    elif value[0] == 't':
        bytes_consumed, value = boolean(value[1:])
    elif value[0] == 'T':
        bytes_consumed, value = timestamp(value[1:])
    elif value[0] == 's':
        bytes_consumed, value = short_str(value[1:])
    elif value[0] == 'S':
        bytes_consumed, value = long_str(value[1:])
    elif value[0] == 'U':
        bytes_consumed, value = short_int(value[1:])
    elif value[0] == '\x00':
        return 0, None
    else:
        raise ValueError('Unknown type "%s"' % value[0])

    return bytes_consumed + 1, value

def by_type(value, data_type, offset=0):
    """Decodes values using the specified type

    :param str value: Value to decode
    :param str data_type: type of data to decode
    :return tuple: bytes consumed, mixed based on field type

    """
    # Determine the field type and encode it
    if data_type == 'array':
        return field_array(value)
    elif data_type == 'bit':
        return bit(value, offset)
    elif data_type == 'boolean':
        return boolean(value)
    elif data_type == 'decimal':
        return decimal(value)
    elif data_type == 'float':
        return floating_point(value)
    elif data_type == 'long':
        return long_int(value)
    elif data_type == 'longlong':
        return long_long_int(value)
    elif data_type == 'longstr':
        return long_str(value)
    elif data_type == 'octet':
        return octet(value)
    elif data_type == 'short':
        return short_int(value)
    elif data_type == 'shortstr':
        return short_str(value)
    elif data_type == 'table':
        return field_table(value)
    elif data_type == 'timestamp':
        return timestamp(value)

    raise ValueError('Unknown type "%s"' % value)


# Define a data type mapping to methods
METHODS = {'array': field_array,
           'bit': bit,
           'boolen': boolean,
           'decimal': decimal,
           'float': floating_point,
           'long': long_int,
           'longlong': long_long_int,
           'longstr': long_str,
           'octet': octet,
           'short': short_int,
           'shortstr': short_str,
           'table': field_table,
           'timestamp': timestamp}
