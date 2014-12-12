
class Frame(object):
    """Base Class for AMQP Methods which specifies the encoding and decoding
    behavior.

    """
    __slots__ = list()
    frame_id = 0
    index = 0
    name = 'Frame'
    synchronous = False
    valid_responses = []

    def __iter__(self):
        """Iterate the attributes and values as key, value pairs.

        :rtype: tuple

        """
        for attribute in self.__slots__:
            yield (attribute, getattr(self, attribute))

    def __contains__(self, item):
        """Return if the item is in the attribute list.

        :rtype: bool

        """
        return item in self.__slots__

    def __getitem__(self, item):
        """Return an attribute as if it were a dict.

        :param str item: The item to look for
        :raises: KeyError
        :rtype: any

        """
        return getattr(self, item)

    def __len__(self):
        """Return the length of the attribute list.

        :rtype: int

        """
        return len(self.__slots__)

    def __repr__(self):
        """Return the representation of the frame object

        :return: str

        """
        return '<%s.%s object at %s>' % (__name__, self.name, hex(id(self)))

    @classmethod
    def type(cls, attr):
        """Return the data type for an attribute.

        :rtype: str

        """
        return getattr(cls, '_' + attr)

    def marshal(self):
        """
        Dynamically encode the frame by taking the list of attributes and
        encode them item by item getting the value form the object attribute
        and the data type from the class attribute.

        :rtype: str

        """
        output = list()
        processing_bitset = False
        byte = None
        offset = 0
        for argument in self.__slots__:
            data_type = self.type(argument)

            # Check if we need to turn on bit processing
            if not processing_bitset and data_type == 'bit':
                byte = 0
                offset = 0
                processing_bitset = True

            # Get the data value
            data_value = getattr(self, argument)

            # If we're processing a bitset, apply special rules
            if processing_bitset:

                # Is this value not a bit? turn off bitset processing and
                # append the byte value as an octet
                if data_type != 'bit':
                    processing_bitset = False
                    output.append(encode.octet(byte))

                else:
                    # Apply the bit value to the byte
                    byte = encode.bit(data_value, byte, offset)
                    offset += 1
                    if offset == 8:
                        # We've filled a byte for all bits, add the byte
                        output.append(encode.octet(byte))
                        # Turn off processing, we'll turn on in next iteration
                        # if needed
                        processing_bitset = False

                    # Go to the next iteration
                    continue

            # Not a bit, so just process by type
            output.append(encode.by_type(data_value, data_type))

        # Append the last byte if we're processing a bitset
        if processing_bitset:
            output.append(encode.octet(byte))

        return b''.join(output)

    def unmarshal(self, data):
        """
        Dynamically decode the frame data applying the values to the method
        object by iterating through the attributes in order and decoding them.

        :param str data: The binary encoded method data

        """
        offset = 0
        processing_bitset = False
        for argument in self.__slots__:
            data_type = self.type(argument)

            if offset == 7 and processing_bitset:
                data = data[1:]
                offset = 0

            if processing_bitset and data_type != 'bit':
                offset = 0
                processing_bitset = False
                data = data[1:]

            consumed, value = decode.by_type(data, data_type, offset)

            if data_type == 'bit':
                offset += 1
                processing_bitset = True
                consumed = 0

            setattr(self, argument, value)
            if consumed:
                data = data[consumed:]


class PropertiesBase(object):
    """Provide a base object that marshals and unmarshals the Basic.Properties
    object values.

    """

    __slots__ = list()
    flags = dict()
    name = 'PropertiesBase'

    def __contains__(self, item):
        return item in self.__slots__

    def __delattr__(self, item):
        setattr(self, item, None)

    def __iter__(self):
        """Iterate the attributes and values as key, value pairs.

        :rtype: tuple

        """
        for attribute in self.__slots__:
            yield (attribute, getattr(self, attribute))

    @classmethod
    def attributes(cls):
        """Return the list of attributes

        :rtype: list

        """
        return [attr for attr in cls.__slots__]

    @classmethod
    def type(cls, attr):
        """Return the data type for an attribute.

        :rtype: str

        """
        return getattr(cls, '_' + attr)

    def encode_property(self, property_name, property_value):
        """Encode a single property value

        :param str property_name: The property name to encode
        :param any property_value: The value to encode

        """
        return encode.by_type(property_value, self.type(property_name))

    def marshal(self):
        """Take the Basic.Properties data structure and marshal it into the data
        structure needed for the ContentHeader.

        :rtype: bytes

        """
        flags = 0
        parts = list()
        for property_name in self.__slots__:
            property_value = getattr(self, property_name)
            if property_value is not None and property_value != '':
                flags = flags | self.flags[property_name]
                parts.append(self.encode_property(property_name,
                                                  property_value))
        flag_pieces = list()
        while True:
            remainder = flags >> 16
            partial_flags = flags & 0xFFFE
            if remainder != 0:
                partial_flags |= 1
            flag_pieces.append(struct.pack('>H', partial_flags))
            flags = remainder
            if not flags:
                break
        return b''.join(flag_pieces + parts)

    def to_dict(self):
        """Return the properties as a dict

        :rtype: dict

        """
        return dict(self)

    def unmarshal(self, flags, data):
        """
        Dynamically decode the frame data applying the values to the method
        object by iterating through the attributes in order and decoding them.

        :param int flags: Flags that indicate if the data has the given property
        :param bytes data: The binary encoded method data

        """
        for property_name in self.__slots__:
            if flags & self.flags[property_name]:
                data_type = getattr(self.__class__, '_' + property_name)
                consumed, value = decode.by_type(data, data_type)
                setattr(self, property_name, value)
                data = data[consumed:]
