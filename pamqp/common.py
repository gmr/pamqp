import datetime
import decimal
import struct
import time
import typing

Timestamp = typing.Union[datetime.datetime, time.struct_time]
FieldArray = typing.List['FieldValue']
FieldTable = typing.Union[None, typing.Dict[str, 'FieldValue']]
FieldValue = typing.Union[bool, bytearray, decimal.Decimal, float, int, str,
                          None, 'FieldArray', 'FieldTable', Timestamp]


class Struct:
    """Simple object for getting to the struct objects"""
    byte = struct.Struct('B')
    double = struct.Struct('>d')
    float = struct.Struct('>f')
    integer = struct.Struct('>I')
    long = struct.Struct('>l')
    long_long_int = struct.Struct('>q')
    short = struct.Struct('>h')
    short_short = struct.Struct('>B')
    timestamp = struct.Struct('>Q')
    uint = struct.Struct('>i')
    ulong = struct.Struct('>L')
    ushort = struct.Struct('>H')
