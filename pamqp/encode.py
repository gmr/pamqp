"""AMQP Data Encoder

Functions for encoding data of various types including field tables and arrays

"""
import calendar
import decimal as _decimal
import datetime
import logging
import struct
import time

LOGGER = logging.getLogger(__name__)

from pamqp import PYTHON3

if PYTHON3:
    long = int
    unicode = bytes


def bit(value, byte, position):
    """Encode a bit value

    :param int value: Value to decode
    :param int byte: The byte to apply the value to
    :param int position: The position in the byte to set the bit on
    :rtype: tuple of bytes used and a bool value

    """
    return byte | (value << position)


def boolean(value):
    """Encode a boolean value.

    :param bool value: Value to encode
    :rtype: bytes

    """
    if not isinstance(value, bool):
        raise TypeError("bool type required")
    return struct.pack('>B', int(value))


def byte_array(value):
    """Encode a bytearray

    :param bytearray value: Value to encode
    :rtype: bytes

    """
    if not isinstance(value, bytearray):
        raise TypeError("bytearray type required")
    if PYTHON3:
        return struct.pack('>I', len(value)) + value
    return bytes(struct.pack('>I', len(value)) + value)


def decimal(value):
    """Encode a decimal.Decimal value.

    :param decimal.Decimal value: Value to encode
    :rtype: bytes

    """
    if not isinstance(value, _decimal.Decimal):
        raise TypeError("decimal.Decimal type required")
    tmp = '%s' % value
    if '.' in tmp:
        decimals = len(tmp.split('.')[-1])
        value = value.normalize()
        raw = int(value * (_decimal.Decimal(10) ** decimals))
        return struct.pack('>Bi', decimals, raw)
    return struct.pack('>Bi', 0, int(value))


def double(value):
    """Encode a floating point value as a double

    :param float value: Value to encode
    :rtype: str

    """
    if not isinstance(value, float):
        raise TypeError("float type required")
    return struct.pack('>d', value)


def floating_point(value):
    """Encode a floating point value.

    :param float value: Value to encode
    :rtype: bytes

    """
    if not isinstance(value, float):
        raise TypeError("float type required")
    return struct.pack('>f', value)


def long_int(value):
    """Encode a long integer.

    :param int value: Value to encode
    :rtype: bytes

    """
    if PYTHON3 and not isinstance(value, int):
        raise TypeError("int type required")
    elif not isinstance(value, int) and not isinstance(value, long):
        raise TypeError("long type required")

    if value < -2147483648 or value > 2147483647:
        raise TypeError("Long integer range: -2147483648 to 2147483647")
    return struct.pack('>l', value)


def long_long_int(value):
    """Encode a long-long int.

    :param long or int value: Value to encode
    :rtype: bytes

    """
    if PYTHON3 and not isinstance(value, int):
        raise TypeError("int type required")
    elif not isinstance(value, long) and not isinstance(value, int):
        raise TypeError("int/long type required")
    if value < -9223372036854775808 or value > 9223372036854775807:
        raise TypeError("long-long integer range: "
                        "-9223372036854775808 to 9223372036854775807")
    return struct.pack('>q', value)


def long_string(value):
    """Encode a string.

    :param bytes value: Value to encode
    :rtype: bytes
    :raises: TypeError

    """
    if not isinstance(value, (bytes, str, unicode)):
        raise TypeError("bytes, str, or unicode required")
    if PYTHON3:
        if isinstance(value, str):
            value = bytes(value, 'ascii')
    else:
        if isinstance(value, unicode):
            value = value.encode('utf-8')
    return struct.pack('>I', len(value)) + value

def octet(value):
    """Encode an octet value.

    :param value: Value to encode
    :rtype: bytes
    :raises: TypeError

    """
    if not isinstance(value, int):
        raise TypeError("int type required")
    return struct.pack('B', value)


def short_int(value):
    """Encode a short integer.

    :param int value: Value to encode
    :rtype: bytes
    :raises: TypeError

    """
    if not isinstance(value, int):
        raise TypeError("int type required")
    if value < -65535 or value > 65535:
        raise TypeError("Short range: -65535 to 65535")
    return struct.pack('>H', value)


def short_string(value):
    """ Encode a string.

    :param str value: Value to encode
    :rtype: bytes
    :raises: TypeError

    """
    if not isinstance(value, (str, unicode, bytes)):
        raise TypeError("bytes, str, or unicode required")
    # Ensure that the value is utf-8 encoded if it's unicode
    value = _utf8_encode(value)
    return struct.pack('B', len(value)) + value


def timestamp(value):
    """Encode a datetime.datetime object or time.struct_time.

    :param datetime.datetime or time.struct_time value value: Value to encode
    :rtype: bytes
    :raises: TypeError

    """
    if isinstance(value, datetime.datetime):
        value = value.timetuple()
    if isinstance(value, time.struct_time):
        return struct.pack('>Q', calendar.timegm(value))
    raise TypeError("datetime.datetime or time.struct_time type required")


def field_array(value):
    """Encode a field array from a dictionary.

    :param list value: Value to encode
    :rtype: bytes
    :raises: TypeError

    """
    if not isinstance(value, list):
        raise TypeError("list type required")

    data = list()
    for item in value:
        data.append(encode_table_value(item))

    output = b''.join(data)
    return struct.pack('>I', len(output)) + output


def field_table(value):
    """Encode a field table from a dictionary.

    :param dict or None value: Value to encode
    :rtype: bytes
    :raises: TypeError

    """
    # If there is no value, return a standard 4 null bytes
    if not value:
        return struct.pack('>I', 0)

    if not isinstance(value, dict):
        raise TypeError("dict type required, got %s" % type(value))

    # Iterate through all of the keys and encode the data into a table
    data = list()
    for key, value in sorted(value.items()):

        # UTF-8 encode the key since it behaves like a short-string
        key = _utf8_encode(key)

        # According to the spec, field names should be 128 char max
        if len(key) > 128:
            LOGGER.warning('Truncating key %s to 128 bytes', key)
            key = key[0:128]

        # Append the field header / delimiter
        data.append(struct.pack('B', len(key)))
        data.append(key)
        try:
            data.append(encode_table_value(value))
        except TypeError as err:
            raise TypeError("%s error: %s" % (key, err))

    # Join all of the data together as a string
    output = b''.join(data)
    return struct.pack('>I', len(output)) + output


def table_integer(value):
    """Determines the best type of numeric type to encode value as, preferring
    the smallest data size first.

    :param int value: Value to encode
    :rtype: bytes
    :raises: TypeError

    """
    # Send the appropriately sized data value
    if -32768 < value < 32767:
        return b's' + short_int(value)
    elif -2147483648 < value < 2147483647:
        return b'I' + long_int(value)
    elif -9223372036854775808 < value < 9223372036854775807:
        return b'l' + long_long_int(value)

    raise TypeError("Numeric value exceeds long-long-int max: %r" % value)


def encode_table_value(value):
    """Takes a value of any type and tries to encode it with the proper encoder

    :param any value: Value to encode
    :rtype: bytes
    :raises: TypeError

    """
    # Determine the field type and encode it
    if isinstance(value, bool):
        result = b't' + boolean(value)

    elif isinstance(value, int) or isinstance(value, long):
        result = table_integer(value)

    elif isinstance(value, _decimal.Decimal):
        result = b'D' + decimal(value)

    elif isinstance(value, float):
        result = b'f' + floating_point(value)

    elif isinstance(value, (str, bytes, unicode)):
        result = b'S' + long_string(value)

    elif (isinstance(value, datetime.datetime) or
          isinstance(value, time.struct_time)):
        result = b'T' + timestamp(value)

    elif isinstance(value, dict):
        result = b'F' + field_table(value)

    elif isinstance(value, list):
        result = b'A' + field_array(value)

    elif isinstance(value, bytearray):
        result = b'x' + byte_array(value)

    elif value is None:
        result = b'V'

    else:
        raise TypeError("Unknown type: %s (%r)" % (type(value), value))

    # Return the encoded value
    return result


def by_type(value, data_type):
    """Takes a value of any type and tries to encode it with the specified
    encoder.

    :param any value: Value to encode
    :param str data_type: type of data to encode
    :rtype: bytes
    :raises: TypeError

    """
    # Determine the field type and encode it
    if data_type == 'field_array':
        return field_array(value)
    elif data_type == 'bytearray':
        return byte_array(value)
    elif data_type == 'double':
        return double(value)
    elif data_type == 'long':
        return long_int(value)
    elif data_type == 'longlong':
        return long_long_int(value)
    elif data_type == 'longstr':
        return long_string(value)
    elif data_type == 'octet':
        return octet(value)
    elif data_type == 'short':
        return short_int(value)
    elif data_type == 'shortstr':
        return short_string(value)
    elif data_type == 'table':
        return field_table(value)
    elif data_type == 'timestamp':
        return timestamp(value)
    elif data_type == 'void':
        return None
    else:
        raise TypeError("Unknown type: %s" % value)


def _utf8_encode(value):
    if PYTHON3:
        if not isinstance(value, bytes):
            return bytes(value, 'utf-8')
        return value
    if isinstance(value, unicode):
        return value.encode('utf-8')
    return value
