# -*- encoding: utf-8 -*-
"""
AMQP Data Decoder
=================

Functions for decoding data of various types including field tables and arrays

"""
import decimal as _decimal
import struct
import time

from pamqp import PYTHON3


class Struct(object):
    """Simple object for getting to the struct objects"""

    byte = struct.Struct('B')
    double = struct.Struct('>d')
    float = struct.Struct('>f')
    integer = struct.Struct('>I')
    ulong = struct.Struct('>L')
    long = struct.Struct('>l')
    ushort = struct.Struct('>H')
    short = struct.Struct('>h')
    short_short = struct.Struct('>B')
    timestamp = struct.Struct('>Q')


def bit(value, position):
    """Decode a bit value

    :param bytes value: Value to decode
    :param int position: The bit position to retrieve
    :return tuple: bytes used, bool value
    :raises: ValueError

    """
    bit_buffer = Struct.byte.unpack_from(value)[0]
    try:
        return 0, (bit_buffer & (1 << position)) != 0
    except TypeError:
        raise ValueError('Could not unpack data')


def boolean(value):
    """Decode a boolean value

    :param bytes value: Value to decode
    :return tuple: bytes used, bool
    :raises: ValueError

    """
    try:
        return 1, bool(Struct.byte.unpack_from(value[0:1])[0])
    except TypeError:
        raise ValueError('Could not unpack data')


def byte_array(value):
    """Decode a byte_array value

    :param bytes value: Value to decode
    :return tuple: bytes used, bool
    :raises: ValueError

    """
    try:
        length = Struct.integer.unpack(value[0:4])[0]
        return length + 4, bytearray(value[4:length + 4])
    except TypeError:
        raise ValueError('Could not unpack data')


def decimal(value):
    """Decode a decimal value

    :param bytes value: Value to decode
    :return tuple: bytes used, decimal.Decimal value
    :raises: ValueError

    """
    try:
        decimals = Struct.byte.unpack(value[0:1])[0]
        raw = Struct.integer.unpack(value[1:5])[0]
        return 5, _decimal.Decimal(raw) * (_decimal.Decimal(10)**-decimals)
    except TypeError:
        raise ValueError('Could not unpack data')


def double(value):
    """Decode a double value

    :param bytes value: Value to decode
    :return tuple: bytes used, float
    :raises: ValueError

    """
    try:
        return 8, Struct.double.unpack_from(value)[0]
    except TypeError:
        raise ValueError('Could not unpack data')


def floating_point(value):
    """Decode a floating point value

    :param bytes value: Value to decode
    :return tuple: bytes used, float
    :raises: ValueError

    """
    try:
        return 4, Struct.float.unpack_from(value)[0]
    except TypeError:
        raise ValueError('Could not unpack data')


def long_int(value):
    """Decode a long integer value

    :param bytes value: Value to decode
    :return tuple: bytes used, int
    :raises: ValueError

    """
    try:
        return 4, Struct.long.unpack(value[0:4])[0]
    except TypeError:
        raise ValueError('Could not unpack data')


def long_uint(value):
    """Decode an unsigned long integer value

    :param bytes value: Value to decode
    :return tuple: bytes used, int
    :raises: ValueError

    """
    try:
        return 4, Struct.ulong.unpack(value[0:4])[0]
    except TypeError:
        raise ValueError('Could not unpack data')


def long_long_int(value):
    """Decode a long-long integer value

    :param bytes value: Value to decode
    :return tuple: bytes used, int
    :raises: ValueError

    """
    try:
        return 8, struct.unpack('>q', value[0:8])[0]
    except TypeError:
        raise ValueError('Could not unpack data')


def long_str(value):
    """Decode a string value

    :param bytes value: Value to decode
    :return tuple: bytes used, bytes|str
    :raises: ValueError

    """
    try:
        length = Struct.integer.unpack(value[0:4])[0]
        return length + 4, value[4:length + 4]
    except TypeError:
        raise ValueError('Could not unpack data')


def octet(value):
    """Decode an octet value

    :param bytes value: Value to decode
    :return tuple: bytes used, int
    :raises: ValueError

    """
    try:
        return 1, Struct.byte.unpack(value[0:1])[0]
    except TypeError:
        raise ValueError('Could not unpack data')


def short_int(value):
    """Decode a short integer value

    :param bytes value: Value to decode
    :return tuple: bytes used, int
    :raises: ValueError

    """
    try:
        return 2, Struct.short.unpack_from(value[0:2])[0]
    except TypeError:
        raise ValueError('Could not unpack data')


def short_uint(value):
    """Decode an unsigned short integer value

    :param bytes value: Value to decode
    :return tuple: bytes used, int
    :raises: ValueError

    """
    try:
        return 2, Struct.ushort.unpack_from(value[0:2])[0]
    except TypeError:
        raise ValueError('Could not unpack data')


def short_short_int(value):
    """Decode a short, short integer value

    :param bytes value: Value to decode
    :return tuple: bytes used, int
    :raises: ValueError

    """
    try:
        return 1, Struct.short_short.unpack_from(value[0:1])[0]
    except TypeError:
        raise ValueError('Could not unpack data')


def short_str(value):
    """Decode a string value

    :param bytes value: Value to decode
    :return tuple: bytes used, unicode|str
    :raises: ValueError

    """
    try:
        length = Struct.byte.unpack(value[0:1])[0]
        return length + 1, _to_str(value[1:length + 1])
    except TypeError:
        raise ValueError('Could not unpack data')


def timestamp(value):
    """Decode a timestamp value

    :param bytes value: Value to decode
    :return tuple: bytes used, struct_time
    :raises: ValueError

    """
    try:
        value = Struct.timestamp.unpack(value[0:8])
        return 8, time.gmtime(value[0])
    except TypeError:
        raise ValueError('Could not unpack data')


def field_array(value):
    """Decode a field array value

    :param bytes value: Value to decode
    :return tuple: bytes used, list
    :raises: ValueError

    """
    try:
        length = Struct.integer.unpack(value[0:4])[0]
        offset = 4
        data = []
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

    :param bytes value: Value to decode
    :return tuple: bytes used, dict
    :raises: ValueError

    """
    try:
        length = Struct.integer.unpack(value[0:4])[0]
        offset = 4
        data = {}
        field_table_end = offset + length
        while offset < field_table_end:
            key_length = Struct.byte.unpack_from(value, offset)[0]
            offset += 1
            key = _to_str(value[offset:offset + key_length])
            offset += key_length
            consumed, result = _embedded_value(value[offset:])
            offset += consumed
            data[key] = result
        return field_table_end, data
    except TypeError:
        raise ValueError('Could not unpack data')


def _void(_):
    return 0, None


TABLE_MAPPING = {
    b'\x00': _void,
    b'A': field_array,
    b'b': short_short_int,
    b'D': decimal,
    b'd': double,
    b'F': field_table,
    b'f': floating_point,
    b'I': long_int,
    b'i': long_uint,
    b'l': long_long_int,
    b'S': long_str,
    b's': short_int,
    b't': boolean,
    b'T': timestamp,
    b'u': short_uint,
    b'V': _void,
    b'x': byte_array,
}


def _embedded_value(value):
    """Takes in a value looking at the first byte to determine which decoder to
    use

    :param bytes value: Value to decode
    :return tuple: bytes consumed, mixed

    """
    if not value:
        return 0, None

    hdr, payload = value[0:1], value[1:]
    try:
        bytes_consumed, value = TABLE_MAPPING[hdr](payload)
    except KeyError:
        raise ValueError('Unknown type: {!r}'.format(value[:1]))
    return bytes_consumed + 1, value


def by_type(value, data_type, offset=0):
    """Decodes values using the specified type

    :param bytes value: Value to decode
    :param str data_type: type of data to decode
    :return tuple: bytes consumed, mixed based on field type

    """
    # Determine the field type and encode it
    data_type = str(data_type)

    if data_type == 'bit':
        return bit(value, offset)

    decoder = METHODS.get(data_type)
    if decoder is None:
        raise ValueError('Unknown type: {}'.format(data_type))

    return decoder(value)


def _to_str(value):
    """Ensure the field table keys are strings (unicode or otherwise)

    :param bytes value: The value to try and decode to unicode
    :rtype: unicode or str

    """
    if PYTHON3:
        return value.decode('utf-8')

    try:
        return str(value.decode('utf-8'))
    except UnicodeEncodeError:
        return value.decode('utf-8')


# Define a data type mapping to methods
METHODS = {
    'array': field_array,
    'bit': bit,
    'boolean': boolean,
    'byte_array': byte_array,
    'decimal': decimal,
    'double': double,
    'float': floating_point,
    'long': long_uint,
    'longlong': long_long_int,
    'longstr': long_str,
    'octet': octet,
    'short': short_uint,
    'shortstr': short_str,
    'table': field_table,
    'timestamp': timestamp,
    'void': lambda _: None,
}
