# -*- encoding: utf-8 -*-
"""Manage the marshaling and unmarshaling of AMQP frames

unmarshal will turn a raw AMQP byte stream into the appropriate AMQP objects
from the specification file.

marshal will take an object created from the specification file and turn it
into a raw byte stream.

"""
import logging
import struct

from pamqp import (body, decode, exceptions, header, heartbeat, PYTHON3,
                   specification)

AMQP = b'AMQP'
FRAME_HEADER_SIZE = 7
FRAME_END_CHAR = chr(specification.FRAME_END)
DECODE_FRAME_END_CHAR = FRAME_END_CHAR
if PYTHON3:
    FRAME_END_CHAR = bytes((specification.FRAME_END, ))
    DECODE_FRAME_END_CHAR = specification.FRAME_END
LOGGER = logging.getLogger(__name__)
UNMARSHAL_FAILURE = 0, 0, None


def unmarshal(data_in):
    """Takes in binary data and maps builds the appropriate frame type,
    returning a frame object.

    :param bytes data_in: Raw byte stream data
    :rtype: tuple of  bytes consumed, channel, and a frame object
    :raises: specification.FrameError

    """
    # Look to see if it's a protocol header frame
    try:
        frame_value = _unmarshal_protocol_header_frame(data_in)
        if frame_value:
            return 8, 0, frame_value
    except ValueError as error:
        raise exceptions.UnmarshalingException(header.ProtocolHeader, error)

    # Decode the low level frame and break it into parts
    frame_type, channel_id, frame_size = frame_parts(data_in)

    # Heartbeats do not have frame length indicators
    if frame_type == specification.FRAME_HEARTBEAT and frame_size == 0:
        return 8, channel_id, heartbeat.Heartbeat()

    if not frame_size:
        raise exceptions.UnmarshalingException('Unknown', 'No frame size')

    byte_count = FRAME_HEADER_SIZE + frame_size + 1
    if byte_count > len(data_in):
        raise exceptions.UnmarshalingException('Unknown',
                                               'Not all data received')
    if data_in[byte_count - 1] != DECODE_FRAME_END_CHAR:
        raise exceptions.UnmarshalingException('Unknown', 'Last byte error')

    frame_data = data_in[FRAME_HEADER_SIZE:byte_count - 1]

    # Decode a method frame
    if frame_type == specification.FRAME_METHOD:
        return byte_count, channel_id, _unmarshal_method_frame(frame_data)

    # Decode a header frame
    elif frame_type == specification.FRAME_HEADER:
        return byte_count, channel_id, _unmarshal_header_frame(frame_data)

    # Decode a body frame
    elif frame_type == specification.FRAME_BODY:
        return byte_count, channel_id, _unmarshal_body_frame(frame_data)

    raise exceptions.UnmarshalingException(
        'Unknown', 'Unknown frame type: {}'.format(frame_type))


def marshal(frame_value, channel_id):
    """Marshal a frame to be sent over the wire.

    :param frame_value: The frame object to marshal
    :type frame_value: pamqp.specification.Frame or pamqp.heartbeat.Heartbeat
    :param int channel_id: The channel number to send the frame on
    :rtype: str
    :raises: ValueError

    """
    if isinstance(frame_value, header.ProtocolHeader):
        return frame_value.marshal()
    elif isinstance(frame_value, specification.Frame):
        return _marshal_method_frame(frame_value, channel_id)
    elif isinstance(frame_value, header.ContentHeader):
        return _marshal_content_header_frame(frame_value, channel_id)
    elif isinstance(frame_value, body.ContentBody):
        return _marshal_content_body_frame(frame_value, channel_id)
    elif isinstance(frame_value, heartbeat.Heartbeat):
        return frame_value.marshal()
    raise ValueError('Could not determine frame type: {}'.format(frame_value))


def _unmarshal_protocol_header_frame(data_in):
    """Attempt to unmarshal a protocol header frame

    The ProtocolHeader is abbreviated in size and functionality compared to
    the rest of the frame types, so return UNMARSHAL_ERROR doesn't apply
    as cleanly since we don't have all of the attributes to return even
    regardless of success or failure.

    :param bytes data_in: Raw byte stream data
    :rtype: header.ProtocolHeader
    :raises: ValueError

    """
    # Do the first four bytes match?
    if data_in[0:4] == AMQP:
        frame = header.ProtocolHeader()
        frame.unmarshal(data_in)
        return frame


def _unmarshal_method_frame(frame_data):
    """Attempt to unmarshal a method frame

    :param bytes frame_data: Raw frame data to assign to our method frame
    :return tuple: Amount of data consumed and the frame object

    """
    # Get the Method Index from the class data
    bytes_used, method_index = decode.long_int(frame_data[0:4])

    # Create an instance of the method object we're going to unmarshal
    try:
        method = specification.INDEX_MAPPING[method_index]()
    except KeyError:
        raise exceptions.UnmarshalingException(
            'Unknown', 'Unknown method index: {}'.format(str(method_index)))

    # Unmarshal the data
    try:
        method.unmarshal(frame_data[bytes_used:])
    except struct.error as error:
        raise exceptions.UnmarshalingException(method, error)

    #  Unmarshal the data in the object and return it
    return method


def _unmarshal_header_frame(frame_data):
    """Attempt to unmarshal a header frame

    :param bytes frame_data: Raw frame data to assign to our header frame
    :return tuple: Amount of data consumed and the frame object

    """
    content_header = header.ContentHeader()
    try:
        content_header.unmarshal(frame_data)
    except struct.error as error:
        raise exceptions.UnmarshalingException('ContentHeader', error)
    return content_header


def _unmarshal_body_frame(frame_data):
    """Attempt to unmarshal a body frame

    :param bytes frame_data: Raw frame data to assign to our body frame
    :return tuple: Amount of data consumed and the frame object

    """
    content_body = body.ContentBody()
    content_body.unmarshal(frame_data)
    return content_body


def frame_parts(data_in):
    """Try and decode a low-level AMQP frame and return the parts of the frame.

    :param bytes data_in: Raw byte stream data
    :return tuple: frame type, channel number, and frame data to decode

    """
    # Get the Frame Type, Channel Number and Frame Size
    try:
        return struct.unpack('>BHI', data_in[0:FRAME_HEADER_SIZE])
    except struct.error:
        # We didn't get a full frame
        return UNMARSHAL_FAILURE


def _marshal(frame_type, channel_id, payload):
    """Marshal the low-level AMQ frame.

    :param int frame_type: The frame type to marshal
    :param int channel_id: The channel it will be sent on
    :param bytes|bytes payload: The frame payload
    :rtype: str or bytes

    """
    return b''.join([
        struct.pack('>BHI', frame_type, channel_id, len(payload)), payload,
        FRAME_END_CHAR
    ])


def _marshal_content_body_frame(frame_value, channel_id):
    """Marshal as many content body frames as needed to transmit the content

    :param body.ContentBody frame_value: Frame object to marshal
    :param int channel_id: The channel number for the frame(s)
    :rtype: str

    """
    return _marshal(specification.FRAME_BODY, channel_id,
                    frame_value.marshal())


def _marshal_content_header_frame(frame_value, channel_id):
    """Marshal a content header frame

    :param header.ContentHeader frame_value: Frame object to marshal
    :param int channel_id: The channel number for the frame
    :rtype: str

    """
    return _marshal(specification.FRAME_HEADER, channel_id,
                    frame_value.marshal())


def _marshal_method_frame(frame_value, channel_id):
    """Marshal a method frame

    :param specification.Frame frame_value: Frame object to marshal
    :param int channel_id: The channel number for the frame
    :rtype: str

    """
    return _marshal(
        specification.FRAME_METHOD, channel_id,
        struct.pack('>I', frame_value.index) + frame_value.marshal())
