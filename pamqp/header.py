# -*- encoding: utf-8 -*-
"""
AMQP Header Class Definitions

For encoding AMQP Header frames into binary AMQP stream data and decoding AMQP
binary data into AMQP Header frames.

"""
import struct

from pamqp import decode, specification

AMQP = b'AMQP'


class ProtocolHeader(object):
    """Class that represents the AMQP Protocol Header"""
    name = 'ProtocolHeader'

    def __init__(self, major_version=None, minor_version=None, revision=None):
        """Construct a Protocol Header frame object for the specified AMQP
        version.

        :param int major_version: Major version number
        :param int minor_version: Minor version number
        :param int revision: Revision number

        """
        self.major_version = major_version or specification.VERSION[0]
        self.minor_version = minor_version or specification.VERSION[1]
        self.revision = revision or specification.VERSION[2]

    def marshal(self):
        """Return the full AMQP wire protocol frame data representation of the
        ProtocolHeader frame.

        :rtype: str or bytes

        """
        return AMQP + struct.pack('BBBB', 0, self.major_version,
                                  self.minor_version, self.revision)

    def unmarshal(self, data):
        """Dynamically decode the frame data applying the values to the method
        object by iterating through the attributes in order and decoding them.

        :param bytes data: The binary encoded method data
        :rtype: int byte count of data used to unmarshal the frame
        :raises: ValueError

        """
        try:
            (self.major_version, self.minor_version,
             self.revision) = struct.unpack('BBB', data[5:8])
        except struct.error:
            raise ValueError('Data did not match the ProtocolHeader '
                             'format: {}'.format(data))
        # All in we consume 8 bytes
        return 8


class ContentHeader(object):
    """Represent a content header frame

    A Content Header frame is received after a Basic.Deliver or Basic.GetOk
    frame and has the data and properties for the Content Body frames that
    follow.

    """
    name = 'ContentHeader'

    def __init__(self, weight=0, body_size=0, properties=None):
        """Initialize the Exchange.DeleteOk class

        :param int weight: Unused, must be 0
        :param long body_size: The size of the body for the message across all
                               received AMQP frames
        :param specification.Basic.Properties properties: Message properties

        """
        self.class_id = None
        self.weight = weight
        self.body_size = body_size
        self.properties = properties or specification.Basic.Properties()

    def marshal(self):
        """Return the AMQP binary encoded value of the frame

        """
        return struct.pack('>HxxQ', specification.Basic.frame_id,
                           self.body_size) + self.properties.marshal()

    def unmarshal(self, data):
        """Dynamically decode the frame data applying the values to the method
        object by iterating through the attributes in order and decoding them.

        :param bytes data: The binary encoded method data
        :rtype: int byte count of data used to unmarshal the frame
        :raises: ValueError

        """
        # Get the class, weight and body size
        (self.class_id, self.weight,
         self.body_size) = struct.unpack('>HHQ', data[0:12])

        # Get the flags for what properties we have available
        offset, flags = self._get_flags(data[12:])

        # Demarshal the properties
        self.properties.unmarshal(flags, data[12 + offset:])

    def _get_flags(self, data):
        """Decode the flags from the data returning the bytes consumed and
        flags

        :param bytes data: The data to pull flags out of
        :rtype: int, int

        """
        # Defaults
        bytes_consumed, flags, flagword_index = 0, 0, 0

        # Read until we don't have a value pulled out of the flags
        while True:
            consumed, partial_flags = decode.short_int(data)
            bytes_consumed += consumed
            flags |= (partial_flags << (flagword_index * 16))
            if not partial_flags & 1:
                break
            flagword_index += 1

        # Return the bytes consumed and the flags
        return bytes_consumed, flags
