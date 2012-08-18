
class Frame(object):
    """Base Class for AMQP Methods which specifies the encoding and decoding
    behavior.

    """
    attributes = list()
    id = 0
    index = 0
    name = 'Frame'

    def __iter__(self):
        """Iterate the attributes and values as key, value pairs.

        :rtype: tuple

        """
        for attribute in self.attributes:
            yield (attribute, getattr(self, attribute))

    def __contains__(self, item):
        """Return if the item is in the attribute list.

        :rtype: bool

        """
        return item in self.attributes

    def __getitem__(self, item):
        """Return an attribute as if it were a dict.

        :param str item: The item to look for
        :rtype: any

        """
        if item not in self.attributes:
            return None
        return getattr(self, item)

    def __len__(self):
        """Return the length of the attribute list.

        :rtype: int

        """
        return int(self.attributes)

    def __repr__(self):
        """Return the representation of the frame object

        :return: str

        """
        return '<%s.%s object at %s>' % (__name__, self.name, hex(id(self)))

    def demarshal(self, data):
        """
        Dynamically decode the frame data applying the values to the method
        object by iterating through the attributes in order and decoding them.

        :param str data: The binary encoded method data

        """
        offset = 0
        processing_bitset = False
        for argument in self.attributes:

            data_type = getattr(self.__class__, argument)

            if offset == 7 and processing_bitset:
                data = data[1:]
                offset = 0

            if processing_bitset and data_type != 'bit':
                offset = 0
                processing_bitset = False
                data = data[1:]

            consumed, value = codec.decode.by_type(data, data_type, offset)

            if data_type == 'bit':
                offset += 1
                processing_bitset = True

            setattr(self, argument, value)
            if consumed:
                data = data[consumed:]

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
        for argument in self.attributes:
            data_type = getattr(self.__class__, argument)

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
                    output.append(codec.encode.octet(byte))

                else:
                    # Apply the bit value to the byte
                    byte = codec.encode.bit(data_value, byte, offset)
                    offset += 1
                    if offset == 8:
                        # We've filled a byte for all bits, add the byte
                        output.append(codec.encode.octet(byte))
                        # Turn off processing, we'll turn on in next iteration
                        # if needed
                        processing_bitset = False

                    # Go to the next iteration
                    continue

            # Not a bit, so just process by type
            output.append(codec.encode.by_type(data_value, data_type))

        # Append the last byte if we're processing a bitset
        if processing_bitset:
            output.append(codec.encode.octet(byte))

        return ''.join(output)


class PropertiesBase(object):
    """Provide a base object that marshals and demarshals the Basic.Properties
    object values.

    """

    attributes = list()
    flags = dict()
    name = 'PropertiesBase'

    def demarshal(self, flags, data):
        """
        Dynamically decode the frame data applying the values to the method
        object by iterating through the attributes in order and decoding them.

        :param int flags: Flags that indicate if the data has the given property
        :param str data: The binary encoded method data

        """
        flag_values = getattr(self.__class__, 'flags')
        for attribute in self.attributes:
            if flags & flag_values[attribute]:
                attribute = attribute.replace('-', '_')
                data_type = getattr(self.__class__, attribute)
                consumed, value = codec.decode.by_type(data, data_type)
                setattr(self, attribute, value)
                data = data[consumed:]
