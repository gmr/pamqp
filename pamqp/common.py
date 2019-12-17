import decimal
import struct
import typing

FieldArray = typing.List['FieldValue']
FieldTable = typing.Dict[str, 'FieldValue']
FieldValue = typing.Union[
    bool,
    bytearray,
    decimal.Decimal,
    float,
    int,
    str,
    None,
    'FieldArray',
    'FieldTable'
]


class Struct:
    """Simple object for getting to the struct objects"""

    byte = struct.Struct('B')
    double = struct.Struct('>d')
    float = struct.Struct('>f')
    integer = struct.Struct('>I')
    ulong = struct.Struct('>L')
    long = struct.Struct('>l')
    long_long_int = struct.Struct('<q')
    ushort = struct.Struct('>H')
    short = struct.Struct('>h')
    short_short = struct.Struct('>B')
    timestamp = struct.Struct('>Q')
