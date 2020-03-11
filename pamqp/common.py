import datetime
import decimal
import struct
import typing

FieldValue = typing.Union[bool,
                          bytearray,
                          decimal.Decimal,
                          'FieldArray',
                          'FieldTable',
                          float,
                          int,
                          None,
                          str,
                          datetime.datetime]
FieldArray = typing.List[FieldValue]
FieldTable = typing.Dict[str, FieldValue]


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
