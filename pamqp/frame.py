# -*- encoding: utf-8 -*-
"""Manage the marshaling and unmarshaling of AMQP frames

unmarshal will turn a raw AMQP byte stream into the appropriate AMQP objects
from the specification file.

marshal will take an object created from the specification file and turn it
into a raw byte stream.

"""
from __future__ import annotations

import logging
import struct
import typing

from pamqp import (body, common, decode, encode, exceptions, header, heartbeat,
                   specification)

LOGGER = logging.getLogger(__name__)
UNMARSHAL_FAILURE = 0, 0, None

FrameTypes = typing.Union[body.ContentBody, 'Frame', header.ContentHeader,
                          header.ProtocolHeader, heartbeat.Heartbeat, ]


def marshal(frame_value: FrameTypes, channel_id: int) -> bytes:
    """Marshal a frame to be sent over the wire.

    :raises: ValueError

    """
    if isinstance(frame_value, header.ProtocolHeader):
        return frame_value.marshal()
    elif isinstance(frame_value, Frame):
        return _marshal_method_frame(frame_value, channel_id)
    elif isinstance(frame_value, header.ContentHeader):
        return _marshal_content_header_frame(frame_value, channel_id)
    elif isinstance(frame_value, body.ContentBody):
        return _marshal_content_body_frame(frame_value, channel_id)
    elif isinstance(frame_value, heartbeat.Heartbeat):
        return frame_value.marshal()
    raise ValueError('Could not determine frame type: {}'.format(frame_value))


def unmarshal(data_in: bytes) -> typing.Tuple[int, int, FrameTypes]:
    """Takes in binary data and maps builds the appropriate frame type,
    returning a frame object.

    :returns: tuple of  bytes consumed, channel, and a frame object
    :raises: specification.FrameError

    """
    try:  # Look to see if it's a protocol header frame
        value = _unmarshal_protocol_header_frame(data_in)
    except ValueError as error:
        raise exceptions.UnmarshalingException(header.ProtocolHeader, error)
    else:
        if value:
            return 8, 0, value

    frame_type, channel_id, frame_size = _frame_parts(data_in)

    # Heartbeats do not have frame length indicators
    if frame_type == specification.FRAME_HEARTBEAT and frame_size == 0:
        return 8, channel_id, heartbeat.Heartbeat()

    if not frame_size:
        raise exceptions.UnmarshalingException('Unknown', 'No frame size')

    byte_count = specification.FRAME_HEADER_SIZE + frame_size + 1
    if byte_count > len(data_in):
        raise exceptions.UnmarshalingException('Unknown',
                                               'Not all data received')
    if data_in[byte_count - 1] != specification.FRAME_END_CHAR:
        raise exceptions.UnmarshalingException('Unknown', 'Last byte error')
    frame_data = data_in[specification.FRAME_HEADER_SIZE:byte_count - 1]
    if frame_type == specification.FRAME_METHOD:
        return byte_count, channel_id, _unmarshal_method_frame(frame_data)
    elif frame_type == specification.FRAME_HEADER:
        return byte_count, channel_id, _unmarshal_header_frame(frame_data)
    elif frame_type == specification.FRAME_BODY:
        return byte_count, channel_id, _unmarshal_body_frame(frame_data)
    raise exceptions.UnmarshalingException(
        'Unknown', 'Unknown frame type: {}'.format(frame_type))


def _frame_parts(data: bytes) -> typing.Tuple[int, int, typing.Optional[int]]:
    """Attempt to decode a low-level frame, returning frame parts"""
    try:  # Get the Frame Type, Channel Number and Frame Size
        return struct.unpack('>BHI', data[0:specification.FRAME_HEADER_SIZE])
    except struct.error:  # Did not receive a full frame
        return UNMARSHAL_FAILURE


def _marshal(frame_type: int, channel_id: int, payload: bytes) -> bytes:
    """Marshal the low-level AMQ frame"""
    return b''.join([
        struct.pack('>BHI', frame_type, channel_id, len(payload)), payload,
        specification.FRAME_END_CHAR
    ])


def _marshal_content_body_frame(value: body.ContentBody,
                                channel_id: int) -> bytes:
    """Marshal as many content body frames as needed to transmit the content"""
    return _marshal(specification.FRAME_BODY, channel_id, value.marshal())


def _marshal_content_header_frame(value: header.ContentHeader,
                                  channel_id: int) -> bytes:
    """Marshal a content header frame"""
    return _marshal(specification.FRAME_HEADER, channel_id, value.marshal())


def _marshal_method_frame(value: Frame, channel_id: int) -> bytes:
    """Marshal a method frame"""
    return _marshal(specification.FRAME_METHOD, channel_id,
                    common.Struct.integer.pack(value.index) + value.marshal())


def _unmarshal_protocol_header_frame(data_in: bytes) \
        -> typing.Optional[header.ProtocolHeader]:
    """Attempt to unmarshal a protocol header frame

    The ProtocolHeader is abbreviated in size and functionality compared to
    the rest of the frame types, so return UNMARSHAL_ERROR doesn't apply
    as cleanly since we don't have all of the attributes to return even
    regardless of success or failure.

    :raises: ValueError

    """
    if data_in[0:4] == specification.AMQP:  # Do the first four bytes match?
        frame = header.ProtocolHeader()
        frame.unmarshal(data_in)
        return frame


def _unmarshal_method_frame(frame_data: bytes) -> Frame:
    """Attempt to unmarshal a method frame

    :raises: pamqp.exceptions.UnmarshalingException

    """
    bytes_used, method_index = decode.long_int(frame_data[0:4])
    try:
        method = specification.INDEX_MAPPING[method_index]()
    except KeyError:
        raise exceptions.UnmarshalingException(
            'Unknown', 'Unknown method index: {}'.format(str(method_index)))
    try:
        method.unmarshal(frame_data[bytes_used:])
    except struct.error as error:
        raise exceptions.UnmarshalingException(method, error)
    return method


def _unmarshal_header_frame(frame_data: bytes) -> header.ContentHeader:
    """Attempt to unmarshal a header frame

    :raises: pamqp.exceptions.UnmarshalingException

    """
    content_header = header.ContentHeader()
    try:
        content_header.unmarshal(frame_data)
    except struct.error as error:
        raise exceptions.UnmarshalingException('ContentHeader', error)
    return content_header


def _unmarshal_body_frame(frame_data: bytes) -> body.ContentBody:
    """Attempt to unmarshal a body frame"""
    content_body = body.ContentBody()
    content_body.unmarshal(frame_data)
    return content_body


class _AMQData:
    """Base class for AMQ methods and properties for encoding and decoding"""
    __annotations__ = {}
    __slots__ = []
    name = '_AMQData'

    def __contains__(self, item: str) -> bool:
        """Return if the item is in the attribute list"""
        return item in self.__slots__

    def __delattr__(self, item: str):
        setattr(self, item, None)

    def __getitem__(self, item: str) -> common.FieldValue:
        """Return an attribute as if it were a dict

        :raises: KeyError

        """
        return getattr(self, item)

    def __iter__(self) -> typing.Tuple[str, common.FieldValue]:
        """Iterate the attributes and values as key, value pairs"""
        for attribute in self.__slots__:
            yield attribute, getattr(self, attribute)

    def __len__(self) -> int:
        """Return the length of the attribute list"""
        return len(self.__slots__)

    def __repr__(self) -> str:
        """Return the representation of the frame object"""
        return '<{}.{} object at {}>'.format(self.__class__.__name__,
                                             self.name, hex(id(self)))

    @classmethod
    def amqp_type(cls, attr: str) -> str:
        """Return the AMQP data type for an attribute"""
        return getattr(cls, '_' + attr)

    @classmethod
    def attributes(cls: _AMQData) -> list:
        """Return the list of attributes"""
        return cls.__slots__


class Frame(_AMQData):
    """Base Class for AMQ Methods for encoding and decoding"""
    frame_id = 0
    index = 0
    synchronous = False
    valid_responses = []

    def marshal(self) -> bytes:
        """Dynamically encode the frame by taking the list of attributes and
        encode them item by item getting the value form the object attribute
        and the data type from the class attribute.

        """
        byte, offset, output, processing_bitset = None, 0, [], False
        for argument in self.__slots__:
            data_type = self.amqp_type(argument)
            if not processing_bitset and data_type == 'bit':
                byte = 0
                offset = 0
                processing_bitset = True
            data_value = getattr(self, argument)
            if processing_bitset:
                if data_type != 'bit':
                    processing_bitset = False
                    output.append(encode.octet(byte))
                else:
                    byte = encode.bit(data_value, byte, offset)
                    offset += 1
                    if offset == 8:
                        output.append(encode.octet(byte))
                        processing_bitset = False
                    continue
            output.append(encode.by_type(data_value, data_type))
        if processing_bitset:
            output.append(encode.octet(byte))
        return b''.join(output)

    def unmarshal(self, data: bytes) -> typing.NoReturn:
        """Dynamically decode the frame data applying the values to the method
        object by iterating through the attributes in order and decoding them.

        """
        offset, processing_bitset = 0, False
        for argument in self.__slots__:
            data_type = self.amqp_type(argument)
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


class BasicProperties(_AMQData):
    """Provide a base object that marshals and unmarshals the Basic.Properties
    object values.

    """
    flags = {}
    name = 'BasicProperties'

    def encode_property(self, name: str, value: common.FieldValue) -> bytes:
        """Encode a single property value

        :raises: TypeError

        """
        return encode.by_type(value, self.amqp_type(name))

    def marshal(self) -> bytes:
        """Take the Basic.Properties data structure and marshal it into the
        data structure needed for the ContentHeader.

        """
        flags = 0
        parts = []
        for property_name in self.__slots__:
            property_value = getattr(self, property_name)
            if property_value is not None and property_value != '':
                flags = flags | self.flags[property_name]
                parts.append(
                    self.encode_property(property_name, property_value))
        flag_pieces = []
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

    def unmarshal(self, flags: int, data: bytes) -> typing.NoReturn:
        """Dynamically decode the frame data applying the values to the method
        object by iterating through the attributes in order and decoding them.

        """
        for property_name in self.__slots__:
            if flags & self.flags[property_name]:
                data_type = getattr(self.__class__, '_' + property_name)
                consumed, value = decode.by_type(data, data_type)
                setattr(self, property_name, value)
                data = data[consumed:]
