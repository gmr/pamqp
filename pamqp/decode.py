"""AMQP Data Decoder

Functions for decoding data of various types including field tables and arrays

"""
import decimal as _decimal
import struct
import time

from pamqp import PYTHON3


class Struct(object):

    byte = struct.Struct('B')
    double = struct.Struct('>d')
    float = struct.Struct('>f')
    integer = struct.Struct('>I')
    long = struct.Struct('>l')
    short = struct.Struct('>H')
    short_short = struct.Struct('>B')
    timestamp = struct.Struct('>Q')


def bit(value, position):
    """Decode a bit value

    :param bytes value: Value to decode
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
        return 5, _decimal.Decimal(raw) * (_decimal.Decimal(10) ** -decimals)
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
        return length + 1, _maybe_utf8(value[1:length + 1])
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

    :param bytes value: Value to decode
    :return tuple: bytes used, dict
    :raises: ValueError

    """
    try:
        length = Struct.integer.unpack(value[0:4])[0]
        offset = 4
        data = dict()
        field_table_end = offset + length
        while offset < field_table_end:
            key_length = Struct.byte.unpack_from(value, offset)[0]
            offset += 1
            key = _maybe_utf8(value[offset:offset + key_length])
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

    :param bytes value: Value to decode
    :return tuple: bytes consumed, mixed

    """
    if not value:
        return 0, None

    # Determine the field type and encode it
    if value[0:1] == b't':
        bytes_consumed, value = boolean(value[1:])
    elif value[0:1] == b'b':
        bytes_consumed, value = short_short_int(value[1:])
    elif value[0:1] == b's':
        bytes_consumed, value = short_int(value[1:])
    elif value[0:1] == b'I':
        bytes_consumed, value = long_int(value[1:])
    elif value[0:1] == b'l':
        bytes_consumed, value = long_long_int(value[1:])
    elif value[0:1] == b'f':
        bytes_consumed, value = floating_point(value[1:])
    elif value[0:1] == b'd':
        bytes_consumed, value = double(value[1:])
    elif value[0:1] == b'D':
        bytes_consumed, value = decimal(value[1:])
    elif value[0:1] == b'S':
        bytes_consumed, value = long_str(value[1:])
    elif value[0:1] == b'A':
        bytes_consumed, value = field_array(value[1:])
    elif value[0:1] == b'T':
        bytes_consumed, value = timestamp(value[1:])
    elif value[0:1] == b'F':
        bytes_consumed, value = field_table(value[1:])
    elif value[0:1] == b'V':
        return 0, None
    elif value[0:1] == b'x':
        bytes_consumed, value = byte_array(value[1:])
    elif value[0:1] == b'\x00':
        return 0, None
    else:
        raise ValueError('Unknown type: %r' % value[:1])

    return bytes_consumed + 1, value


def by_type(value, data_type, offset=0):
    """Decodes values using the specified type

    :param bytes value: Value to decode
    :param str data_type: type of data to decode
    :return tuple: bytes consumed, mixed based on field type

    """
    # Determine the field type and encode it
    data_type = str(data_type)
    if data_type == 'array':
        return field_array(value)
    elif data_type == 'bit':
        return bit(value, offset)
    elif data_type == 'boolean':
        return boolean(value)
    elif data_type == 'byte_array':
        return byte_array(value)
    elif data_type == 'decimal':
        return decimal(value)
    elif data_type == 'double':
        return double(value)
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
    elif data_type == 'void':
        return None

    raise ValueError('Unknown type "%s"' % value)


def _maybe_utf8(value):
    """Try and automatically return unicode when there is UTF-8 data
    in them.

    :param bytes value: The value to try and decode to unicode
    :return: unicode or bytes or str

    """
    if PYTHON3:
        # If it's already a bytes object, cool
        if isinstance(value, bytes):
            return value

        # It might come in as a str in which case we want it to be bytes
        return bytes(value, 'utf-8')

    # Convert to unicode
    _value = value.decode('utf-8')

    try:
        # Try and force it to be a str and return the str value
        return str(_value)
    except UnicodeEncodeError:
        # Unicode obj to str with unicode data fails, return the unicode value
        return _value


# Define a data type mapping to methods
METHODS = {'array': field_array,
           'bit': bit,
           'boolean': boolean,
           'byte_array': byte_array,
           'decimal': decimal,
           'double': double,
           'float': floating_point,
           'long': long_int,
           'longlong': long_long_int,
           'longstr': long_str,
           'octet': octet,
           'short': short_int,
           'shortstr': short_str,
           'table': field_table,
           'timestamp': timestamp}
