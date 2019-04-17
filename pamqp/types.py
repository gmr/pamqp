class IntBase(int):
    MIN = None
    MAX = None

    @classmethod
    def validate(cls, value):
        return cls.MIN <= value <= cls.MAX

    def __new__(cls, value):
        if not cls.validate(value):
            raise ValueError()

        return super(IntBase, cls).__new__(cls, value)

    def __repr__(self):
        return "<%s: %d>" % (self.__class__.__name__, self)


class ShortShortInt(IntBase):
    MIN = 0
    MAX = 255


class ShortInt(IntBase):
    MIN = -32768
    MAX = 32767


class ShortUInt(IntBase):
    MIN = 0
    MAX = 65535


class LongInt(IntBase):
    MIN = -2147483648
    MAX = 2147483647


class LongUInt(IntBase):
    MIN = 0
    MAX = 4294967295


class LongLongInt(IntBase):
    MIN = -9223372036854775808
    MAX = 9223372036854775807


__all__ = (
    'LongInt',
    'LongLongInt',
    'LongUInt',
    'ShortInt',
    'ShortShortInt',
    'ShortUInt',
)
