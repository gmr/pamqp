"""Manage the marshalling and demarshalling of AMQP frames

demarshal will turn a raw AMQP byte stream into the appropriate AMQP objects
from the specification file.

marshal will take an object created from the specification file and turn it
into a raw byte stream.

"""
import logging
import struct

from pamqp import body
from pamqp import codec
from pamqp import heartbeat
from pamqp import header
from pamqp import specification

DEMARSHALLING_FAILURE = 0, 0, None
FRAME_HEADER_SIZE = 7
FRAME_END_STR = '\xce'
LOGGER = logging.getLogger(__name__)


def demarshal(data_in):
    """Takes in binary data and maps builds the appropriate frame type,
    returning a frame object.

    :param str data_in: Raw byte stream data
    :rtype: tuple of  bytes consumed, channel, and a frame object
    :raises: specification.FrameError

    """
    # Look to see if it's a protocol header frame
    try:
        frame_value = _demarshal_protocol_header_frame(data_in)
        if frame_value:
            return 8, 0, frame_value
    except ValueError:
        LOGGER.warning('Demarshalling error processing a ProtocolHeader frame: '
                       '%r', data_in)
        # It was a protocol header but it didn't decode properly
        return DEMARSHALLING_FAILURE

    if FRAME_END_STR not in data_in:
        LOGGER.debug('Frame-end delimiter missing')
        return DEMARSHALLING_FAILURE

    # split the data into parts
    frame_data = data_in.split(FRAME_END_STR)[0]

    # How much data we should consume
    bytes_consumed = len(frame_data)

    # Decode the low level frame and break it into parts
    try:
        frame_type, channel_id, frame_size = _frame_parts(frame_data)
        last_byte = FRAME_HEADER_SIZE + frame_size + 1
        frame_data = frame_data[FRAME_HEADER_SIZE:last_byte]
    except ValueError:
        LOGGER.warning('Demarshalling error processing a content frame: %r',
                        data_in)
        return DEMARSHALLING_FAILURE

    # Decode a method frame
    if frame_type == specification.FRAME_METHOD:
        return bytes_consumed, channel_id, _demarshal_method_frame(frame_data)

    # Decode a header frame
    elif frame_type == specification.FRAME_HEADER:
        return bytes_consumed, channel_id, _demarshal_header_frame(frame_data)

    # Decode a body frame
    elif frame_type == specification.FRAME_BODY:
        return bytes_consumed, channel_id, frame_data

    # Decode a heartbeat frame
    elif frame_type == specification.FRAME_HEARTBEAT:
        return bytes_consumed, channel_id, heartbeat.Heartbeat()

    raise specification.FrameError("Unknown frame type: %i" % frame_type)


def marshal(frame_value, channel_id):
    """Marshal a frame to be sent over the wire.

    :param pamqp.specification.Frame frame_value: The frame object to marshal
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
    raise ValueError('Could not determine frame type: %r', frame_value)


def _demarshal_protocol_header_frame(data_in):
    """Attempt to demarshal a protocol header frame

    The ProtocolHeader is abbreviated in size and functionality compared to
    the rest of the frame types, so return DEMARSHALLING_ERROR doesn't apply
    as cleanly since we don't have all of the attributes to return even
    regardless of success or failure.

    :param str data_in: Raw byte stream data
    :rtype: header.ProtocolHeader
    :raises: ValueError

    """
    # Do the first four bytes match?
    if data_in[0:4] == 'AMQP':
        try:
            frame = header.ProtocolHeader()
            frame.demarshal(data_in)
            return frame
        except IndexError:
            raise ValueError('Frame data did not meet minimum length')


def _demarshal_method_frame(frame_data):
    """Attempt to demarshal a method frame

    :param str frame_data: Raw frame data to assign to our method frame
    :return tuple: Amount of data consumed and the frame object

    """
    # Get the Method Index from the class data
    bytes_used, method_index = codec.decode.long_int(frame_data[0:4])

    # Create an instance of the method object we're going to demarshal
    method = specification.INDEX_MAPPING[method_index]()

    # Demarshal the data
    method.demarshal(frame_data[bytes_used:])

    #  Demarshal the data in the object and return it
    return method


def _demarshal_header_frame(frame_data):
    """Attempt to demarshal a header frame

    :param str frame_data: Raw frame data to assign to our header frame
    :return tuple: Amount of data consumed and the frame object

    """
    content_header = header.ContentHeader()
    content_header.demarshal(frame_data)
    return content_header


def _demarshal_body_frame(frame_data):
    """Attempt to demarshal a body frame

    :param str frame_data: Raw frame data to assign to our body frame
    :return tuple: Amount of data consumed and the frame object

    """
    content_header = header.ContentHeader()
    content_header.demarshal(frame_data)
    return content_header


def _frame_parts(data_in):
    """Try and decode a low-level AMQP frame and return the parts of the frame.

    :param str data_in: Raw byte stream data
    :return tuple: frame type, channel number, and frame data to decode

    """
    # Get the Frame Type, Channel Number and Frame Size
    try:
        return struct.unpack('>BHI', data_in[0:FRAME_HEADER_SIZE])
    except struct.error:
        # We didn't get a full frame
        return DEMARSHALLING_FAILURE


def _marshal(frame_type, channel_id, payload):
    """Marshal the low-level AMQ frame.

    :param int frame_type: The frame type to marshal
    :param int channel_id: The channel it will be sent on
    :param str payload: The frame payload
    :rtype: str

    """
    return (struct.pack('>BHI', frame_type, channel_id, len(payload)) +
            payload + FRAME_END_STR)


def _marshal_content_body_frame(frame_value, channel_id):
    """Marshal as many content body frames as needed to transmit the content

    :param body.ContentBody frame_value: Frame object to marshal
    :param int channel_id: The channel number for the frame(s)
    :rtype: str

    """
    return _marshal(specification.FRAME_BODY, channel_id, frame_value.marshal())


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
    return _marshal(specification.FRAME_METHOD,
                    channel_id,
                    struct.pack('>I', frame_value.index) +
                    frame_value.marshal())
