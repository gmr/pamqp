"""specification.py

Auto-generated AMQP Support Module

WARNING: DO NOT EDIT. To Generate run tools/codegen.py

"""
__since__ = '2019-04-18'

import struct
import warnings

from pamqp import decode, encode

# AMQP Protocol Version
VERSION = (0, 9, 1)

# RabbitMQ Defaults
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 5672
DEFAULT_USER = 'guest'
DEFAULT_PASS = 'guest'
DEFAULT_VHOST = '/'

# AMQP Constants
FRAME_METHOD = 1
FRAME_HEADER = 2
FRAME_BODY = 3
FRAME_HEARTBEAT = 8
FRAME_MIN_SIZE = 4096
FRAME_END = 206
# Indicates that the method completed successfully. This reply code is reserved
# for future use - the current protocol design does not use positive
# confirmation and reply codes are sent only in case of an error.
REPLY_SUCCESS = 200

# Not included in the spec XML or JSON files.
FRAME_MAX_SIZE = 131072

# AMQP data types
DATA_TYPES = [
    'bit', 'long', 'longlong', 'longstr', 'octet', 'short', 'shortstr',
    'table', 'timestamp'
]

# AMQP domains
DOMAINS = {
    'channel-id': 'longstr',
    'class-id': 'short',
    'consumer-tag': 'shortstr',
    'delivery-tag': 'longlong',
    'destination': 'shortstr',
    'duration': 'longlong',
    'exchange-name': 'shortstr',
    'method-id': 'short',
    'no-ack': 'bit',
    'no-local': 'bit',
    'offset': 'longlong',
    'path': 'shortstr',
    'peer-properties': 'table',
    'queue-name': 'shortstr',
    'redelivered': 'bit',
    'reference': 'longstr',
    'reject-code': 'short',
    'reject-text': 'shortstr',
    'reply-code': 'short',
    'reply-text': 'shortstr',
    'security-token': 'longstr'
}

# Other constants
DEPRECATION_WARNING = 'This command is deprecated in AMQP 0-9-1'


class Frame(object):
    """Base Class for AMQP Methods which specifies the encoding and decoding
    behavior.

    """
    __slots__ = []
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
        output = []
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

    __slots__ = []
    flags = {}
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
        """Take the Basic.Properties data structure and marshal it into the
        data structure needed for the ContentHeader.

        :rtype: bytes

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

    def to_dict(self):
        """Return the properties as a dict

        :rtype: dict

        """
        return dict(self)

    def unmarshal(self, flags, data):
        """
        Dynamically decode the frame data applying the values to the method
        object by iterating through the attributes in order and decoding them.

        :param int flags: Flags that indicate if the data has the property
        :param bytes data: The binary encoded method data

        """
        for property_name in self.__slots__:
            if flags & self.flags[property_name]:
                data_type = getattr(self.__class__, '_' + property_name)
                consumed, value = decode.by_type(data, data_type)
                setattr(self, property_name, value)
                data = data[consumed:]


# AMQP Errors
class AMQPContentTooLarge(Warning):
    """
    The client attempted to transfer content larger than the server could
    accept at the present time. The client may retry at a later time.

    """
    name = 'CONTENT-TOO-LARGE'
    value = 311


class AMQPNoRoute(Warning):
    """
    Undocumented AMQP Soft Error

    """
    name = 'NO-ROUTE'
    value = 312


class AMQPNoConsumers(Warning):
    """
    When the exchange cannot deliver to a consumer when the immediate flag is
    set. As a result of pending data on the queue or the absence of any
    consumers of the queue.

    """
    name = 'NO-CONSUMERS'
    value = 313


class AMQPAccessRefused(Warning):
    """
    The client attempted to work with a server entity to which it has no access
    due to security settings.

    """
    name = 'ACCESS-REFUSED'
    value = 403


class AMQPNotFound(Warning):
    """
    The client attempted to work with a server entity that does not exist.

    """
    name = 'NOT-FOUND'
    value = 404


class AMQPResourceLocked(Warning):
    """
    The client attempted to work with a server entity to which it has no access
    because another client is working with it.

    """
    name = 'RESOURCE-LOCKED'
    value = 405


class AMQPPreconditionFailed(Warning):
    """
    The client requested a method that was not allowed because some
    precondition failed.

    """
    name = 'PRECONDITION-FAILED'
    value = 406


class AMQPConnectionForced(Exception):
    """
    An operator intervened to close the connection for some reason. The client
    may retry at some later date.

    """
    name = 'CONNECTION-FORCED'
    value = 320


class AMQPInvalidPath(Exception):
    """
    The client tried to work with an unknown virtual host.

    """
    name = 'INVALID-PATH'
    value = 402


class AMQPFrameError(Exception):
    """
    The sender sent a malformed frame that the recipient could not decode. This
    strongly implies a programming error in the sending peer.

    """
    name = 'FRAME-ERROR'
    value = 501


class AMQPSyntaxError(Exception):
    """
    The sender sent a frame that contained illegal values for one or more
    fields. This strongly implies a programming error in the sending peer.

    """
    name = 'SYNTAX-ERROR'
    value = 502


class AMQPCommandInvalid(Exception):
    """
    The client sent an invalid sequence of frames, attempting to perform an
    operation that was considered invalid by the server. This usually implies a
    programming error in the client.

    """
    name = 'COMMAND-INVALID'
    value = 503


class AMQPChannelError(Exception):
    """
    The client attempted to work with a channel that had not been correctly
    opened. This most likely indicates a fault in the client layer.

    """
    name = 'CHANNEL-ERROR'
    value = 504


class AMQPUnexpectedFrame(Exception):
    """
    The peer sent a frame that was not expected, usually in the context of a
    content header and body.  This strongly indicates a fault in the peer's
    content processing.

    """
    name = 'UNEXPECTED-FRAME'
    value = 505


class AMQPResourceError(Exception):
    """
    The server could not complete the method because it lacked sufficient
    resources. This may be due to the client creating too many of some type of
    entity.

    """
    name = 'RESOURCE-ERROR'
    value = 506


class AMQPNotAllowed(Exception):
    """
    The client tried to work with some entity in a manner that is prohibited by
    the server, due to security settings or by some other criteria.

    """
    name = 'NOT-ALLOWED'
    value = 530


class AMQPNotImplemented(Exception):
    """
    The client tried to use functionality that is not implemented in the
    server.

    """
    name = 'NOT-IMPLEMENTED'
    value = 540


class AMQPInternalError(Exception):
    """
    The server could not complete the method because of an internal error. The
    server may require intervention by an operator in order to resume normal
    operations.

    """
    name = 'INTERNAL-ERROR'
    value = 541


# AMQP Error code to class mapping
ERRORS = {
    320: AMQPConnectionForced,
    505: AMQPUnexpectedFrame,
    502: AMQPSyntaxError,
    503: AMQPCommandInvalid,
    530: AMQPNotAllowed,
    504: AMQPChannelError,
    402: AMQPInvalidPath,
    403: AMQPAccessRefused,
    404: AMQPNotFound,
    405: AMQPResourceLocked,
    406: AMQPPreconditionFailed,
    311: AMQPContentTooLarge,
    312: AMQPNoRoute,
    313: AMQPNoConsumers,
    506: AMQPResourceError,
    540: AMQPNotImplemented,
    541: AMQPInternalError,
    501: AMQPFrameError
}

# AMQP Classes and Methods


class Connection(object):
    """Work with socket connections

    The connection class provides methods for a client to establish a network
    connection to a server, and for both peers to operate the connection
    thereafter.

    """
    __slots__ = []

    # AMQP Class Number and Mapping Index
    frame_id = 10
    index = 0x000A0000

    class Start(Frame):
        """Start connection negotiation

        This method starts the connection negotiation process by telling the
        client the protocol version that the server proposes, along with a list
        of security mechanisms which the client can use for authentication.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 10
        index = 0x000A000A
        name = 'Connection.Start'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Connection.StartOk']

        # AMQP Method Attributes
        __slots__ = [
            'version_major', 'version_minor', 'server_properties',
            'mechanisms', 'locales'
        ]

        # Class Attribute Types
        _version_major = 'octet'
        _version_minor = 'octet'
        _server_properties = 'table'
        _mechanisms = 'longstr'
        _locales = 'longstr'

        def __init__(self,
                     version_major=0,
                     version_minor=9,
                     server_properties=None,
                     mechanisms='PLAIN',
                     locales='en_US'):
            """Initialize the Connection.Start class

            :param int version_major: Protocol major version
            :param int version_minor: Protocol minor version
            :param dict server_properties: Server properties
            :param str mechanisms: Available security mechanisms
            :param str locales: Available message locales

            """
            # Protocol major version
            self.version_major = version_major

            # Protocol minor version
            self.version_minor = version_minor

            # Server properties
            self.server_properties = server_properties

            # Available security mechanisms
            self.mechanisms = mechanisms

            # Available message locales
            self.locales = locales

    class StartOk(Frame):
        """Select security mechanism and locale

        This method selects a SASL security mechanism.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 11
        index = 0x000A000B
        name = 'Connection.StartOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['client_properties', 'mechanism', 'response', 'locale']

        # Class Attribute Types
        _client_properties = 'table'
        _mechanism = 'shortstr'
        _response = 'longstr'
        _locale = 'shortstr'

        def __init__(self,
                     client_properties=None,
                     mechanism='PLAIN',
                     response='',
                     locale='en_US'):
            """Initialize the Connection.StartOk class

            :param dict client_properties: Client properties
            :param str mechanism: Selected security mechanism
            :param str response: Security response data
            :param str locale: Selected message locale

            """
            # Client properties
            self.client_properties = client_properties

            # Selected security mechanism
            self.mechanism = mechanism

            # Security response data
            self.response = response

            # Selected message locale
            self.locale = locale

    class Secure(Frame):
        """Security mechanism challenge

        The SASL protocol works by exchanging challenges and responses until
        both peers have received sufficient information to authenticate each
        other. This method challenges the client to provide more information.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 20
        index = 0x000A0014
        name = 'Connection.Secure'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Connection.SecureOk']

        # AMQP Method Attributes
        __slots__ = ['challenge']

        # Class Attribute Types
        _challenge = 'longstr'

        def __init__(self, challenge=''):
            """Initialize the Connection.Secure class

            :param str challenge: Security challenge data

            """
            # Security challenge data
            self.challenge = challenge

    class SecureOk(Frame):
        """Security mechanism response

        This method attempts to authenticate, passing a block of SASL data for
        the security mechanism at the server side.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 21
        index = 0x000A0015
        name = 'Connection.SecureOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['response']

        # Class Attribute Types
        _response = 'longstr'

        def __init__(self, response=''):
            """Initialize the Connection.SecureOk class

            :param str response: Security response data

            """
            # Security response data
            self.response = response

    class Tune(Frame):
        """Propose connection tuning parameters

        This method proposes a set of connection configuration values to the
        client. The client can accept and/or adjust these.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 30
        index = 0x000A001E
        name = 'Connection.Tune'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Connection.TuneOk']

        # AMQP Method Attributes
        __slots__ = ['channel_max', 'frame_max', 'heartbeat']

        # Class Attribute Types
        _channel_max = 'short'
        _frame_max = 'long'
        _heartbeat = 'short'

        def __init__(self, channel_max=0, frame_max=0, heartbeat=0):
            """Initialize the Connection.Tune class

            :param int channel_max: Proposed maximum channels
            :param int/long frame_max: Proposed maximum frame size
            :param int heartbeat: Desired heartbeat delay

            """
            # Proposed maximum channels
            self.channel_max = channel_max

            # Proposed maximum frame size
            self.frame_max = frame_max

            # Desired heartbeat delay
            self.heartbeat = heartbeat

    class TuneOk(Frame):
        """Negotiate connection tuning parameters

        This method sends the client's connection tuning parameters to the
        server. Certain fields are negotiated, others provide capability
        information.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 31
        index = 0x000A001F
        name = 'Connection.TuneOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['channel_max', 'frame_max', 'heartbeat']

        # Class Attribute Types
        _channel_max = 'short'
        _frame_max = 'long'
        _heartbeat = 'short'

        def __init__(self, channel_max=0, frame_max=0, heartbeat=0):
            """Initialize the Connection.TuneOk class

            :param int channel_max: Negotiated maximum channels
            :param int/long frame_max: Negotiated maximum frame size
            :param int heartbeat: Desired heartbeat delay

            """
            # Negotiated maximum channels
            self.channel_max = channel_max

            # Negotiated maximum frame size
            self.frame_max = frame_max

            # Desired heartbeat delay
            self.heartbeat = heartbeat

    class Open(Frame):
        """Open connection to virtual host

        This method opens a connection to a virtual host, which is a collection
        of resources, and acts to separate multiple application domains within
        a server. The server may apply arbitrary limits per virtual host, such
        as the number of each type of entity that may be used, per connection
        and/or in total.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 40
        index = 0x000A0028
        name = 'Connection.Open'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Connection.OpenOk']

        # AMQP Method Attributes
        __slots__ = ['virtual_host', 'capabilities', 'insist']

        # Class Attribute Types
        _virtual_host = 'shortstr'
        _capabilities = 'shortstr'
        _insist = 'bit'

        def __init__(self, virtual_host='/', capabilities='', insist=False):
            """Initialize the Connection.Open class

            :param str virtual_host: Virtual host name
            :param str capabilities: Deprecated
            :param bool insist: Deprecated

            """
            # Virtual host name
            self.virtual_host = virtual_host

            # Deprecated
            self.capabilities = capabilities

            # Deprecated
            self.insist = insist

    class OpenOk(Frame):
        """Signal that connection is ready

        This method signals to the client that the connection is ready for use.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 41
        index = 0x000A0029
        name = 'Connection.OpenOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['known_hosts']

        # Class Attribute Types
        _known_hosts = 'shortstr'

        def __init__(self, known_hosts=''):
            """Initialize the Connection.OpenOk class

            :param str known_hosts: Deprecated

            """
            # Deprecated
            self.known_hosts = known_hosts

    class Close(Frame):
        """Request a connection close

        This method indicates that the sender wants to close the connection.
        This may be due to internal conditions (e.g. a forced shut-down) or due
        to an error handling a specific method, i.e. an exception. When a close
        is due to an exception, the sender provides the class and method id of
        the method which caused the exception.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 50
        index = 0x000A0032
        name = 'Connection.Close'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Connection.CloseOk']

        # AMQP Method Attributes
        __slots__ = ['reply_code', 'reply_text', 'class_id', 'method_id']

        # Class Attribute Types
        _reply_code = 'short'
        _reply_text = 'shortstr'
        _class_id = 'short'
        _method_id = 'short'

        def __init__(self,
                     reply_code=0,
                     reply_text='',
                     class_id=0,
                     method_id=0):
            """Initialize the Connection.Close class

            :param int reply_code: Reply code from server
            :param str reply_text: Localised reply text
            :param int class_id: Failing method class
            :param int method_id: Failing method ID

            """
            # Reply code from server
            self.reply_code = reply_code

            # Localised reply text
            self.reply_text = reply_text

            # Failing method class
            self.class_id = class_id

            # Failing method ID
            self.method_id = method_id

    class CloseOk(Frame):
        """Confirm a connection close

        This method confirms a Connection.Close method and tells the recipient
        that it is safe to release resources for the connection and close the
        socket.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 51
        index = 0x000A0033
        name = 'Connection.CloseOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

    class Blocked(Frame):
        """Signal that connection is blocked

        This method signals to the client that the connection is blocked by
        RabbitMQ.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 60
        index = 0x000A003C
        name = 'Connection.Blocked'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['reason']

        # Class Attribute Types
        _reason = 'shortstr'

        def __init__(self, reason=''):
            """Initialize the Connection.Blocked class

            :param str reason:

            """
            self.reason = reason

    class Unblocked(Frame):
        """Signal that connection is no longer blocked

        This method signals to the client that the connection is no longer
        blocked by RabbitMQ.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 61
        index = 0x000A003D
        name = 'Connection.Unblocked'

        # Specifies if this is a synchronous AMQP method
        synchronous = False


class Channel(object):
    """Work with channels

    The channel class provides methods for a client to establish a channel to a
    server and for both peers to operate the channel thereafter.

    """
    __slots__ = []

    # AMQP Class Number and Mapping Index
    frame_id = 20
    index = 0x00140000

    class Open(Frame):
        """Open a channel for use

        This method opens a channel to the server.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 10
        index = 0x0014000A
        name = 'Channel.Open'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Channel.OpenOk']

        # AMQP Method Attributes
        __slots__ = ['out_of_band']

        # Class Attribute Types
        _out_of_band = 'shortstr'

        def __init__(self, out_of_band=''):
            """Initialize the Channel.Open class

            :param str out_of_band: Protocol level field, do not use, must be
                zero.

            """
            # Protocol level field, do not use, must be zero.
            self.out_of_band = out_of_band

    class OpenOk(Frame):
        """Signal that the channel is ready

        This method signals to the client that the channel is ready for use.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 11
        index = 0x0014000B
        name = 'Channel.OpenOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['channel_id']

        # Class Attribute Types
        _channel_id = 'longstr'

        def __init__(self, channel_id=''):
            """Initialize the Channel.OpenOk class

            :param str channel_id: Deprecated

            """
            # Deprecated
            self.channel_id = channel_id

    class Flow(Frame):
        """Enable/disable flow from peer

        This method asks the peer to pause or restart the flow of content data
        sent by a consumer. This is a simple flow-control mechanism that a peer
        can use to avoid overflowing its queues or otherwise finding itself
        receiving more messages than it can process. Note that this method is
        not intended for window control. It does not affect contents returned
        by Basic.Get-Ok methods.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 20
        index = 0x00140014
        name = 'Channel.Flow'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Channel.FlowOk']

        # AMQP Method Attributes
        __slots__ = ['active']

        # Class Attribute Types
        _active = 'bit'

        def __init__(self, active=None):
            """Initialize the Channel.Flow class

            :param bool active: Start/stop content frames

            """
            # Start/stop content frames
            self.active = active

    class FlowOk(Frame):
        """Confirm a flow method

        Confirms to the peer that a flow command was received and processed.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 21
        index = 0x00140015
        name = 'Channel.FlowOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['active']

        # Class Attribute Types
        _active = 'bit'

        def __init__(self, active=None):
            """Initialize the Channel.FlowOk class

            :param bool active: Current flow setting

            """
            # Current flow setting
            self.active = active

    class Close(Frame):
        """Request a channel close

        This method indicates that the sender wants to close the channel. This
        may be due to internal conditions (e.g. a forced shut-down) or due to
        an error handling a specific method, i.e. an exception. When a close is
        due to an exception, the sender provides the class and method id of the
        method which caused the exception.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 40
        index = 0x00140028
        name = 'Channel.Close'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Channel.CloseOk']

        # AMQP Method Attributes
        __slots__ = ['reply_code', 'reply_text', 'class_id', 'method_id']

        # Class Attribute Types
        _reply_code = 'short'
        _reply_text = 'shortstr'
        _class_id = 'short'
        _method_id = 'short'

        def __init__(self,
                     reply_code=0,
                     reply_text='',
                     class_id=0,
                     method_id=0):
            """Initialize the Channel.Close class

            :param int reply_code: Reply code from server
            :param str reply_text: Localised reply text
            :param int class_id: Failing method class
            :param int method_id: Failing method ID

            """
            # Reply code from server
            self.reply_code = reply_code

            # Localised reply text
            self.reply_text = reply_text

            # Failing method class
            self.class_id = class_id

            # Failing method ID
            self.method_id = method_id

    class CloseOk(Frame):
        """Confirm a channel close

        This method confirms a Channel.Close method and tells the recipient
        that it is safe to release resources for the channel.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 41
        index = 0x00140029
        name = 'Channel.CloseOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False


class Exchange(object):
    """Work with exchanges

    Exchanges match and distribute messages across queues. Exchanges can be
    configured in the server or declared at runtime.

    """
    __slots__ = []

    # AMQP Class Number and Mapping Index
    frame_id = 40
    index = 0x00280000

    class Declare(Frame):
        """Verify exchange exists, create if needed

        This method creates an exchange if it does not already exist, and if
        the exchange exists, verifies that it is of the correct and expected
        class.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 10
        index = 0x0028000A
        name = 'Exchange.Declare'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Exchange.DeclareOk']

        # AMQP Method Attributes
        __slots__ = [
            'ticket', 'exchange', 'exchange_type', 'passive', 'durable',
            'auto_delete', 'internal', 'nowait', 'arguments'
        ]

        # Class Attribute Types
        _ticket = 'short'
        _exchange = 'shortstr'
        _exchange_type = 'shortstr'
        _passive = 'bit'
        _durable = 'bit'
        _auto_delete = 'bit'
        _internal = 'bit'
        _nowait = 'bit'
        _arguments = 'table'

        def __init__(self,
                     ticket=0,
                     exchange='',
                     exchange_type='direct',
                     passive=False,
                     durable=False,
                     auto_delete=False,
                     internal=False,
                     nowait=False,
                     arguments=None):
            """Initialize the Exchange.Declare class

            Note that the AMQP type argument is referred to as "exchange_type"
            to not conflict with the Python type keyword.

            :param int ticket: Deprecated
            :param str exchange:
            :param str exchange_type: Exchange type
            :param bool passive: Do not create exchange
            :param bool durable: Request a durable exchange
            :param bool auto_delete: Automatically delete when not in use
            :param bool internal: Deprecated
            :param bool nowait: Do not send a reply method
            :param dict arguments: Arguments for declaration

            """
            # Deprecated
            self.ticket = ticket

            self.exchange = exchange

            # Exchange type
            self.exchange_type = exchange_type

            # Do not create exchange
            self.passive = passive

            # Request a durable exchange
            self.durable = durable

            # Automatically delete when not in use
            self.auto_delete = auto_delete

            # Deprecated
            self.internal = internal

            # Do not send a reply method
            self.nowait = nowait

            # Arguments for declaration
            self.arguments = arguments or {}

    class DeclareOk(Frame):
        """Confirm exchange declaration

        This method confirms a Declare method and confirms the name of the
        exchange, essential for automatically-named exchanges.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 11
        index = 0x0028000B
        name = 'Exchange.DeclareOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

    class Delete(Frame):
        """Delete an exchange

        This method deletes an exchange. When an exchange is deleted all queue
        bindings on the exchange are cancelled.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 20
        index = 0x00280014
        name = 'Exchange.Delete'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Exchange.DeleteOk']

        # AMQP Method Attributes
        __slots__ = ['ticket', 'exchange', 'if_unused', 'nowait']

        # Class Attribute Types
        _ticket = 'short'
        _exchange = 'shortstr'
        _if_unused = 'bit'
        _nowait = 'bit'

        def __init__(self,
                     ticket=0,
                     exchange='',
                     if_unused=False,
                     nowait=False):
            """Initialize the Exchange.Delete class

            :param int ticket: Deprecated
            :param str exchange:
            :param bool if_unused: Delete only if unused
            :param bool nowait: Do not send a reply method

            """
            # Deprecated
            self.ticket = ticket

            self.exchange = exchange

            # Delete only if unused
            self.if_unused = if_unused

            # Do not send a reply method
            self.nowait = nowait

    class DeleteOk(Frame):
        """Confirm deletion of an exchange

        This method confirms the deletion of an exchange.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 21
        index = 0x00280015
        name = 'Exchange.DeleteOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

    class Bind(Frame):
        # AMQP Method Number and Mapping Index
        frame_id = 30
        index = 0x0028001E
        name = 'Exchange.Bind'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Exchange.BindOk']

        # AMQP Method Attributes
        __slots__ = [
            'ticket', 'destination', 'source', 'routing_key', 'nowait',
            'arguments'
        ]

        # Class Attribute Types
        _ticket = 'short'
        _destination = 'shortstr'
        _source = 'shortstr'
        _routing_key = 'shortstr'
        _nowait = 'bit'
        _arguments = 'table'

        def __init__(self,
                     ticket=0,
                     destination='',
                     source='',
                     routing_key='',
                     nowait=False,
                     arguments=None):
            """Initialize the Exchange.Bind class

            :param int ticket: Deprecated
            :param str destination:
            :param str source:
            :param str routing-key:
            :param bool nowait: Do not send a reply method
            :param dict arguments:

            """
            # Deprecated
            self.ticket = ticket

            self.destination = destination

            self.source = source

            self.routing_key = routing_key

            # Do not send a reply method
            self.nowait = nowait

            self.arguments = arguments or {}

    class BindOk(Frame):
        # AMQP Method Number and Mapping Index
        frame_id = 31
        index = 0x0028001F
        name = 'Exchange.BindOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

    class Unbind(Frame):
        # AMQP Method Number and Mapping Index
        frame_id = 40
        index = 0x00280028
        name = 'Exchange.Unbind'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Exchange.UnbindOk']

        # AMQP Method Attributes
        __slots__ = [
            'ticket', 'destination', 'source', 'routing_key', 'nowait',
            'arguments'
        ]

        # Class Attribute Types
        _ticket = 'short'
        _destination = 'shortstr'
        _source = 'shortstr'
        _routing_key = 'shortstr'
        _nowait = 'bit'
        _arguments = 'table'

        def __init__(self,
                     ticket=0,
                     destination='',
                     source='',
                     routing_key='',
                     nowait=False,
                     arguments=None):
            """Initialize the Exchange.Unbind class

            :param int ticket: Deprecated
            :param str destination:
            :param str source:
            :param str routing-key:
            :param bool nowait: Do not send a reply method
            :param dict arguments:

            """
            # Deprecated
            self.ticket = ticket

            self.destination = destination

            self.source = source

            self.routing_key = routing_key

            # Do not send a reply method
            self.nowait = nowait

            self.arguments = arguments or {}

    class UnbindOk(Frame):
        # AMQP Method Number and Mapping Index
        frame_id = 51
        index = 0x00280033
        name = 'Exchange.UnbindOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False


class Queue(object):
    """Work with queues

    Queues store and forward messages. Queues can be configured in the server
    or created at runtime. Queues must be attached to at least one exchange in
    order to receive messages from publishers.

    """
    __slots__ = []

    # AMQP Class Number and Mapping Index
    frame_id = 50
    index = 0x00320000

    class Declare(Frame):
        """Declare queue, create if needed

        This method creates or checks a queue. When creating a new queue the
        client can specify various properties that control the durability of
        the queue and its contents, and the level of sharing for the queue.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 10
        index = 0x0032000A
        name = 'Queue.Declare'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Queue.DeclareOk']

        # AMQP Method Attributes
        __slots__ = [
            'ticket', 'queue', 'passive', 'durable', 'exclusive',
            'auto_delete', 'nowait', 'arguments'
        ]

        # Class Attribute Types
        _ticket = 'short'
        _queue = 'shortstr'
        _passive = 'bit'
        _durable = 'bit'
        _exclusive = 'bit'
        _auto_delete = 'bit'
        _nowait = 'bit'
        _arguments = 'table'

        def __init__(self,
                     ticket=0,
                     queue='',
                     passive=False,
                     durable=False,
                     exclusive=False,
                     auto_delete=False,
                     nowait=False,
                     arguments=None):
            """Initialize the Queue.Declare class

            :param int ticket: Deprecated
            :param str queue:
            :param bool passive: Do not create queue
            :param bool durable: Request a durable queue
            :param bool exclusive: Request an exclusive queue
            :param bool auto_delete: Auto-delete queue when unused
            :param bool nowait: Do not send a reply method
            :param dict arguments: Arguments for declaration

            """
            # Deprecated
            self.ticket = ticket

            self.queue = queue

            # Do not create queue
            self.passive = passive

            # Request a durable queue
            self.durable = durable

            # Request an exclusive queue
            self.exclusive = exclusive

            # Auto-delete queue when unused
            self.auto_delete = auto_delete

            # Do not send a reply method
            self.nowait = nowait

            # Arguments for declaration
            self.arguments = arguments or {}

    class DeclareOk(Frame):
        """Confirms a queue definition

        This method confirms a Declare method and confirms the name of the
        queue, essential for automatically-named queues.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 11
        index = 0x0032000B
        name = 'Queue.DeclareOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['queue', 'message_count', 'consumer_count']

        # Class Attribute Types
        _queue = 'shortstr'
        _message_count = 'long'
        _consumer_count = 'long'

        def __init__(self, queue='', message_count=0, consumer_count=0):
            """Initialize the Queue.DeclareOk class

            :param str queue:
            :param int/long message_count: Number of messages in queue
            :param int/long consumer_count: Number of consumers

            """
            self.queue = queue

            # Number of messages in queue
            self.message_count = message_count

            # Number of consumers
            self.consumer_count = consumer_count

    class Bind(Frame):
        """Bind queue to an exchange

        This method binds a queue to an exchange. Until a queue is bound it
        will not receive any messages. In a classic messaging model, store-and-
        forward queues are bound to a direct exchange and subscription queues
        are bound to a topic exchange.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 20
        index = 0x00320014
        name = 'Queue.Bind'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Queue.BindOk']

        # AMQP Method Attributes
        __slots__ = [
            'ticket', 'queue', 'exchange', 'routing_key', 'nowait', 'arguments'
        ]

        # Class Attribute Types
        _ticket = 'short'
        _queue = 'shortstr'
        _exchange = 'shortstr'
        _routing_key = 'shortstr'
        _nowait = 'bit'
        _arguments = 'table'

        def __init__(self,
                     ticket=0,
                     queue='',
                     exchange='',
                     routing_key='',
                     nowait=False,
                     arguments=None):
            """Initialize the Queue.Bind class

            :param int ticket: Deprecated
            :param str queue:
            :param str exchange: Name of the exchange to bind to
            :param str routing_key: Message routing key
            :param bool nowait: Do not send a reply method
            :param dict arguments: Arguments for binding

            """
            # Deprecated
            self.ticket = ticket

            self.queue = queue

            # Name of the exchange to bind to
            self.exchange = exchange

            # Message routing key
            self.routing_key = routing_key

            # Do not send a reply method
            self.nowait = nowait

            # Arguments for binding
            self.arguments = arguments or {}

    class BindOk(Frame):
        """Confirm bind successful

        This method confirms that the bind was successful.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 21
        index = 0x00320015
        name = 'Queue.BindOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

    class Purge(Frame):
        """Purge a queue

        This method removes all messages from a queue which are not awaiting
        acknowledgment.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 30
        index = 0x0032001E
        name = 'Queue.Purge'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Queue.PurgeOk']

        # AMQP Method Attributes
        __slots__ = ['ticket', 'queue', 'nowait']

        # Class Attribute Types
        _ticket = 'short'
        _queue = 'shortstr'
        _nowait = 'bit'

        def __init__(self, ticket=0, queue='', nowait=False):
            """Initialize the Queue.Purge class

            :param int ticket: Deprecated
            :param str queue:
            :param bool nowait: Do not send a reply method

            """
            # Deprecated
            self.ticket = ticket

            self.queue = queue

            # Do not send a reply method
            self.nowait = nowait

    class PurgeOk(Frame):
        """Confirms a queue purge

        This method confirms the purge of a queue.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 31
        index = 0x0032001F
        name = 'Queue.PurgeOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['message_count']

        # Class Attribute Types
        _message_count = 'long'

        def __init__(self, message_count=0):
            """Initialize the Queue.PurgeOk class

            :param int/long message-count:

            """
            self.message_count = message_count

    class Delete(Frame):
        """Delete a queue

        This method deletes a queue. When a queue is deleted any pending
        messages are sent to a dead-letter queue if this is defined in the
        server configuration, and all consumers on the queue are cancelled.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 40
        index = 0x00320028
        name = 'Queue.Delete'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Queue.DeleteOk']

        # AMQP Method Attributes
        __slots__ = ['ticket', 'queue', 'if_unused', 'if_empty', 'nowait']

        # Class Attribute Types
        _ticket = 'short'
        _queue = 'shortstr'
        _if_unused = 'bit'
        _if_empty = 'bit'
        _nowait = 'bit'

        def __init__(self,
                     ticket=0,
                     queue='',
                     if_unused=False,
                     if_empty=False,
                     nowait=False):
            """Initialize the Queue.Delete class

            :param int ticket: Deprecated
            :param str queue:
            :param bool if_unused: Delete only if unused
            :param bool if_empty: Delete only if empty
            :param bool nowait: Do not send a reply method

            """
            # Deprecated
            self.ticket = ticket

            self.queue = queue

            # Delete only if unused
            self.if_unused = if_unused

            # Delete only if empty
            self.if_empty = if_empty

            # Do not send a reply method
            self.nowait = nowait

    class DeleteOk(Frame):
        """Confirm deletion of a queue

        This method confirms the deletion of a queue.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 41
        index = 0x00320029
        name = 'Queue.DeleteOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['message_count']

        # Class Attribute Types
        _message_count = 'long'

        def __init__(self, message_count=0):
            """Initialize the Queue.DeleteOk class

            :param int/long message-count:

            """
            self.message_count = message_count

    class Unbind(Frame):
        """Unbind a queue from an exchange

        This method unbinds a queue from an exchange.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 50
        index = 0x00320032
        name = 'Queue.Unbind'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Queue.UnbindOk']

        # AMQP Method Attributes
        __slots__ = ['ticket', 'queue', 'exchange', 'routing_key', 'arguments']

        # Class Attribute Types
        _ticket = 'short'
        _queue = 'shortstr'
        _exchange = 'shortstr'
        _routing_key = 'shortstr'
        _arguments = 'table'

        def __init__(self,
                     ticket=0,
                     queue='',
                     exchange='',
                     routing_key='',
                     arguments=None):
            """Initialize the Queue.Unbind class

            :param int ticket: Deprecated
            :param str queue:
            :param str exchange:
            :param str routing_key: Routing key of binding
            :param dict arguments: Arguments of binding

            """
            # Deprecated
            self.ticket = ticket

            self.queue = queue

            self.exchange = exchange

            # Routing key of binding
            self.routing_key = routing_key

            # Arguments of binding
            self.arguments = arguments or {}

    class UnbindOk(Frame):
        """Confirm unbind successful

        This method confirms that the unbind was successful.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 51
        index = 0x00320033
        name = 'Queue.UnbindOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False


class Basic(object):
    """Work with basic content

    The Basic class provides methods that support an industry-standard
    messaging model.

    """
    __slots__ = []

    # AMQP Class Number and Mapping Index
    frame_id = 60
    index = 0x003C0000

    class Qos(Frame):
        """Specify quality of service

        This method requests a specific quality of service. The QoS can be
        specified for the current channel or for all channels on the
        connection. The particular properties and semantics of a qos method
        always depend on the content class semantics. Though the qos method
        could in principle apply to both peers, it is currently meaningful only
        for the server.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 10
        index = 0x003C000A
        name = 'Basic.Qos'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Basic.QosOk']

        # AMQP Method Attributes
        __slots__ = ['prefetch_size', 'prefetch_count', 'global_']

        # Class Attribute Types
        _prefetch_size = 'long'
        _prefetch_count = 'short'
        _global_ = 'bit'

        def __init__(self, prefetch_size=0, prefetch_count=0, global_=False):
            """Initialize the Basic.Qos class

            :param int/long prefetch_size: Prefetch window in octets
            :param int prefetch_count: Prefetch window in messages
            :param bool global_: Apply to entire connection

            """
            # Prefetch window in octets
            self.prefetch_size = prefetch_size

            # Prefetch window in messages
            self.prefetch_count = prefetch_count

            # Apply to entire connection
            self.global_ = global_

    class QosOk(Frame):
        """Confirm the requested qos

        This method tells the client that the requested QoS levels could be
        handled by the server. The requested QoS applies to all active
        consumers until a new QoS is defined.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 11
        index = 0x003C000B
        name = 'Basic.QosOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

    class Consume(Frame):
        """Start a queue consumer

        This method asks the server to start a "consumer", which is a transient
        request for messages from a specific queue. Consumers last as long as
        the channel they were declared on, or until the client cancels them.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 20
        index = 0x003C0014
        name = 'Basic.Consume'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Basic.ConsumeOk']

        # AMQP Method Attributes
        __slots__ = [
            'ticket', 'queue', 'consumer_tag', 'no_local', 'no_ack',
            'exclusive', 'nowait', 'arguments'
        ]

        # Class Attribute Types
        _ticket = 'short'
        _queue = 'shortstr'
        _consumer_tag = 'shortstr'
        _no_local = 'bit'
        _no_ack = 'bit'
        _exclusive = 'bit'
        _nowait = 'bit'
        _arguments = 'table'

        def __init__(self,
                     ticket=0,
                     queue='',
                     consumer_tag='',
                     no_local=False,
                     no_ack=False,
                     exclusive=False,
                     nowait=False,
                     arguments=None):
            """Initialize the Basic.Consume class

            :param int ticket: Deprecated
            :param str queue:
            :param str consumer-tag:
            :param bool no_local: Do not deliver own messages
            :param bool no_ack: No acknowledgement needed
            :param bool exclusive: Request exclusive access
            :param bool nowait: Do not send a reply method
            :param dict arguments: Arguments for declaration

            """
            # Deprecated
            self.ticket = ticket

            self.queue = queue

            self.consumer_tag = consumer_tag

            # Do not deliver own messages
            self.no_local = no_local

            # No acknowledgement needed
            self.no_ack = no_ack

            # Request exclusive access
            self.exclusive = exclusive

            # Do not send a reply method
            self.nowait = nowait

            # Arguments for declaration
            self.arguments = arguments or {}

    class ConsumeOk(Frame):
        """Confirm a new consumer

        The server provides the client with a consumer tag, which is used by
        the client for methods called on the consumer at a later stage.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 21
        index = 0x003C0015
        name = 'Basic.ConsumeOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['consumer_tag']

        # Class Attribute Types
        _consumer_tag = 'shortstr'

        def __init__(self, consumer_tag=''):
            """Initialize the Basic.ConsumeOk class

            :param str consumer-tag:

            """
            self.consumer_tag = consumer_tag

    class Cancel(Frame):
        """End a queue consumer

        This method cancels a consumer. This does not affect already delivered
        messages, but it does mean the server will not send any more messages
        for that consumer. The client may receive an arbitrary number of
        messages in between sending the cancel method and receiving the cancel-
        ok reply.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 30
        index = 0x003C001E
        name = 'Basic.Cancel'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Basic.CancelOk']

        # AMQP Method Attributes
        __slots__ = ['consumer_tag', 'nowait']

        # Class Attribute Types
        _consumer_tag = 'shortstr'
        _nowait = 'bit'

        def __init__(self, consumer_tag='', nowait=False):
            """Initialize the Basic.Cancel class

            :param str consumer_tag: Consumer tag
            :param bool nowait: Do not send a reply method

            """
            # Consumer tag
            self.consumer_tag = consumer_tag

            # Do not send a reply method
            self.nowait = nowait

    class CancelOk(Frame):
        """Confirm a cancelled consumer

        This method confirms that the cancellation was completed.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 31
        index = 0x003C001F
        name = 'Basic.CancelOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['consumer_tag']

        # Class Attribute Types
        _consumer_tag = 'shortstr'

        def __init__(self, consumer_tag=''):
            """Initialize the Basic.CancelOk class

            :param str consumer_tag: Consumer tag

            """
            # Consumer tag
            self.consumer_tag = consumer_tag

    class Publish(Frame):
        """Publish a message

        This method publishes a message to a specific exchange. The message
        will be routed to queues as defined by the exchange configuration and
        distributed to any active consumers when the transaction, if any, is
        committed.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 40
        index = 0x003C0028
        name = 'Basic.Publish'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = [
            'ticket', 'exchange', 'routing_key', 'mandatory', 'immediate'
        ]

        # Class Attribute Types
        _ticket = 'short'
        _exchange = 'shortstr'
        _routing_key = 'shortstr'
        _mandatory = 'bit'
        _immediate = 'bit'

        def __init__(self,
                     ticket=0,
                     exchange='',
                     routing_key='',
                     mandatory=False,
                     immediate=False):
            """Initialize the Basic.Publish class

            :param int ticket: Deprecated
            :param str exchange:
            :param str routing_key: Message routing key
            :param bool mandatory: Indicate mandatory routing
            :param bool immediate: Request immediate delivery

            """
            # Deprecated
            self.ticket = ticket

            self.exchange = exchange

            # Message routing key
            self.routing_key = routing_key

            # Indicate mandatory routing
            self.mandatory = mandatory

            # Request immediate delivery
            self.immediate = immediate

    class Return(Frame):
        """Return a failed message

        This method returns an undeliverable message that was published with
        the "immediate" flag set, or an unroutable message published with the
        "mandatory" flag set. The reply code and text provide information about
        the reason that the message was undeliverable.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 50
        index = 0x003C0032
        name = 'Basic.Return'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['reply_code', 'reply_text', 'exchange', 'routing_key']

        # Class Attribute Types
        _reply_code = 'short'
        _reply_text = 'shortstr'
        _exchange = 'shortstr'
        _routing_key = 'shortstr'

        def __init__(self,
                     reply_code=0,
                     reply_text='',
                     exchange='',
                     routing_key=''):
            """Initialize the Basic.Return class

            :param int reply_code: Reply code from server
            :param str reply_text: Localised reply text
            :param str exchange:
            :param str routing_key: Message routing key

            """
            # Reply code from server
            self.reply_code = reply_code

            # Localised reply text
            self.reply_text = reply_text

            self.exchange = exchange

            # Message routing key
            self.routing_key = routing_key

    class Deliver(Frame):
        """Notify the client of a consumer message

        This method delivers a message to the client, via a consumer. In the
        asynchronous message delivery model, the client starts a consumer using
        the Consume method, then the server responds with Deliver methods as
        and when messages arrive for that consumer.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 60
        index = 0x003C003C
        name = 'Basic.Deliver'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = [
            'consumer_tag', 'delivery_tag', 'redelivered', 'exchange',
            'routing_key'
        ]

        # Class Attribute Types
        _consumer_tag = 'shortstr'
        _delivery_tag = 'longlong'
        _redelivered = 'bit'
        _exchange = 'shortstr'
        _routing_key = 'shortstr'

        def __init__(self,
                     consumer_tag='',
                     delivery_tag=None,
                     redelivered=False,
                     exchange='',
                     routing_key=''):
            """Initialize the Basic.Deliver class

            :param str consumer_tag: Consumer tag
            :param int/long delivery_tag: Server-assigned delivery tag
            :param bool redelivered: Message is being redelivered
            :param str exchange:
            :param str routing_key: Message routing key

            """
            # Consumer tag
            self.consumer_tag = consumer_tag

            # Server-assigned delivery tag
            self.delivery_tag = delivery_tag

            # Message is being redelivered
            self.redelivered = redelivered

            self.exchange = exchange

            # Message routing key
            self.routing_key = routing_key

    class Get(Frame):
        """Direct access to a queue

        This method provides a direct access to the messages in a queue using a
        synchronous dialogue that is designed for specific types of application
        where synchronous functionality is more important than performance.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 70
        index = 0x003C0046
        name = 'Basic.Get'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Basic.GetOk', 'Basic.GetEmpty']

        # AMQP Method Attributes
        __slots__ = ['ticket', 'queue', 'no_ack']

        # Class Attribute Types
        _ticket = 'short'
        _queue = 'shortstr'
        _no_ack = 'bit'

        def __init__(self, ticket=0, queue='', no_ack=False):
            """Initialize the Basic.Get class

            :param int ticket: Deprecated
            :param str queue:
            :param bool no_ack: No acknowledgement needed

            """
            # Deprecated
            self.ticket = ticket

            self.queue = queue

            # No acknowledgement needed
            self.no_ack = no_ack

    class GetOk(Frame):
        """Provide client with a message

        This method delivers a message to the client following a get method. A
        message delivered by 'get-ok' must be acknowledged unless the no-ack
        option was set in the get method.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 71
        index = 0x003C0047
        name = 'Basic.GetOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = [
            'delivery_tag', 'redelivered', 'exchange', 'routing_key',
            'message_count'
        ]

        # Class Attribute Types
        _delivery_tag = 'longlong'
        _redelivered = 'bit'
        _exchange = 'shortstr'
        _routing_key = 'shortstr'
        _message_count = 'long'

        def __init__(self,
                     delivery_tag=None,
                     redelivered=False,
                     exchange='',
                     routing_key='',
                     message_count=0):
            """Initialize the Basic.GetOk class

            :param int/long delivery_tag: Server-assigned delivery tag
            :param bool redelivered: Message is being redelivered
            :param str exchange:
            :param str routing_key: Message routing key
            :param int/long message_count: Number of messages in queue

            """
            # Server-assigned delivery tag
            self.delivery_tag = delivery_tag

            # Message is being redelivered
            self.redelivered = redelivered

            self.exchange = exchange

            # Message routing key
            self.routing_key = routing_key

            # Number of messages in queue
            self.message_count = message_count

    class GetEmpty(Frame):
        """Indicate no messages available

        This method tells the client that the queue has no messages available
        for the client.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 72
        index = 0x003C0048
        name = 'Basic.GetEmpty'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['cluster_id']

        # Class Attribute Types
        _cluster_id = 'shortstr'

        def __init__(self, cluster_id=''):
            """Initialize the Basic.GetEmpty class

            :param str cluster_id: Deprecated

            """
            # Deprecated
            self.cluster_id = cluster_id

    class Ack(Frame):
        """Acknowledge one or more messages

        This method acknowledges one or more messages delivered via the Deliver
        or Get-Ok methods. The client can ask to confirm a single message or a
        set of messages up to and including a specific message.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 80
        index = 0x003C0050
        name = 'Basic.Ack'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['delivery_tag', 'multiple']

        # Class Attribute Types
        _delivery_tag = 'longlong'
        _multiple = 'bit'

        def __init__(self, delivery_tag=0, multiple=False):
            """Initialize the Basic.Ack class

            :param int/long delivery_tag: Server-assigned delivery tag
            :param bool multiple: Acknowledge multiple messages

            """
            # Server-assigned delivery tag
            self.delivery_tag = delivery_tag

            # Acknowledge multiple messages
            self.multiple = multiple

    class Reject(Frame):
        """Reject an incoming message

        This method allows a client to reject a message. It can be used to
        interrupt and cancel large incoming messages, or return untreatable
        messages to their original queue.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 90
        index = 0x003C005A
        name = 'Basic.Reject'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['delivery_tag', 'requeue']

        # Class Attribute Types
        _delivery_tag = 'longlong'
        _requeue = 'bit'

        def __init__(self, delivery_tag=None, requeue=True):
            """Initialize the Basic.Reject class

            :param int/long delivery_tag: Server-assigned delivery tag
            :param bool requeue: Requeue the message

            """
            # Server-assigned delivery tag
            self.delivery_tag = delivery_tag

            # Requeue the message
            self.requeue = requeue

    class RecoverAsync(Frame):
        """Redeliver unacknowledged messages

        This method asks the server to redeliver all unacknowledged messages on
        a specified channel. Zero or more messages may be redelivered.  This
        method is deprecated in favour of the synchronous Recover/Recover-Ok.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 100
        index = 0x003C0064
        name = 'Basic.RecoverAsync'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['requeue']

        # Class Attribute Types
        _requeue = 'bit'

        def __init__(self, requeue=False):
            """Initialize the Basic.RecoverAsync class

            :param bool requeue: Requeue the message

            .. deprecated:: 0-9-1
                This command is deprecated in AMQP 0-9-1

            """
            # Requeue the message
            self.requeue = requeue

            # This command is deprecated in AMQP 0-9-1
            warnings.warn(DEPRECATION_WARNING, category=DeprecationWarning)

    class Recover(Frame):
        """Redeliver unacknowledged messages

        This method asks the server to redeliver all unacknowledged messages on
        a specified channel. Zero or more messages may be redelivered.  This
        method replaces the asynchronous Recover.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 110
        index = 0x003C006E
        name = 'Basic.Recover'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Basic.RecoverOk']

        # AMQP Method Attributes
        __slots__ = ['requeue']

        # Class Attribute Types
        _requeue = 'bit'

        def __init__(self, requeue=False):
            """Initialize the Basic.Recover class

            :param bool requeue: Requeue the message

            """
            # Requeue the message
            self.requeue = requeue

    class RecoverOk(Frame):
        """Confirm recovery

        This method acknowledges a Basic.Recover method.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 111
        index = 0x003C006F
        name = 'Basic.RecoverOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

    class Nack(Frame):
        # AMQP Method Number and Mapping Index
        frame_id = 120
        index = 0x003C0078
        name = 'Basic.Nack'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

        # AMQP Method Attributes
        __slots__ = ['delivery_tag', 'multiple', 'requeue']

        # Class Attribute Types
        _delivery_tag = 'longlong'
        _multiple = 'bit'
        _requeue = 'bit'

        def __init__(self, delivery_tag=0, multiple=False, requeue=True):
            """Initialize the Basic.Nack class

            :param int/long delivery_tag: Server-assigned delivery tag
            :param bool multiple:
            :param bool requeue:

            """
            # Server-assigned delivery tag
            self.delivery_tag = delivery_tag

            self.multiple = multiple

            self.requeue = requeue

    class Properties(PropertiesBase):
        """Content Properties"""

        name = 'Basic.Properties'

        __slots__ = [
            'content_type', 'content_encoding', 'headers', 'delivery_mode',
            'priority', 'correlation_id', 'reply_to', 'expiration',
            'message_id', 'timestamp', 'message_type', 'user_id', 'app_id',
            'cluster_id'
        ]

        # Flag Values
        flags = {
            'content_type': 32768,
            'content_encoding': 16384,
            'headers': 8192,
            'delivery_mode': 4096,
            'priority': 2048,
            'correlation_id': 1024,
            'reply_to': 512,
            'expiration': 256,
            'message_id': 128,
            'timestamp': 64,
            'message_type': 32,
            'user_id': 16,
            'app_id': 8,
            'cluster_id': 4
        }

        # Class Attribute Types
        _content_type = 'shortstr'
        _content_encoding = 'shortstr'
        _headers = 'table'
        _delivery_mode = 'octet'
        _priority = 'octet'
        _correlation_id = 'shortstr'
        _reply_to = 'shortstr'
        _expiration = 'shortstr'
        _message_id = 'shortstr'
        _timestamp = 'timestamp'
        _message_type = 'shortstr'
        _user_id = 'shortstr'
        _app_id = 'shortstr'
        _cluster_id = 'shortstr'

        frame_id = 60
        index = 0x003C

        def __init__(self,
                     content_type='',
                     content_encoding='',
                     headers=None,
                     delivery_mode=None,
                     priority=None,
                     correlation_id='',
                     reply_to='',
                     expiration='',
                     message_id='',
                     timestamp=None,
                     message_type='',
                     user_id='',
                     app_id='',
                     cluster_id=''):
            """Initialize the Basic.Properties class

            Note that the AMQP property type is named message_type as to
            not conflict with the Python type keyword

            :param str content_type: MIME content type
            :param str content_encoding: MIME content encoding
            :param dict headers: Message header field table
            :param int delivery_mode: Non-persistent (1) or persistent (2)
            :param int priority: Message priority, 0 to 9
            :param str correlation_id: Application correlation identifier
            :param str reply_to: Address to reply to
            :param str expiration: Message expiration specification
            :param str message_id: Application message identifier
            :param struct_time timestamp: Message timestamp
            :param str message_type: Message type name
            :param str user_id: Creating user id
            :param str app_id: Creating application id
            :param str cluster_id: Deprecated

            """
            # MIME content type
            self.content_type = content_type

            # MIME content encoding
            self.content_encoding = content_encoding

            # Message header field table
            self.headers = headers

            # Non-persistent (1) or persistent (2)
            self.delivery_mode = delivery_mode

            # Message priority, 0 to 9
            self.priority = priority

            # Application correlation identifier
            self.correlation_id = correlation_id

            # Address to reply to
            self.reply_to = reply_to

            # Message expiration specification
            self.expiration = expiration

            # Application message identifier
            self.message_id = message_id

            # Message timestamp
            self.timestamp = timestamp

            # Message type name
            self.message_type = message_type

            # Creating user id
            self.user_id = user_id

            # Creating application id
            self.app_id = app_id

            # Deprecated
            self.cluster_id = cluster_id


class Tx(object):
    """Work with transactions

    The Tx class allows publish and ack operations to be batched into atomic
    units of work.  The intention is that all publish and ack requests issued
    within a transaction will complete successfully or none of them will.
    Servers SHOULD implement atomic transactions at least where all publish or
    ack requests affect a single queue.  Transactions that cover multiple
    queues may be non-atomic, given that queues can be created and destroyed
    asynchronously, and such events do not form part of any transaction.
    Further, the behaviour of transactions with respect to the immediate and
    mandatory flags on Basic.Publish methods is not defined.

    """
    __slots__ = []

    # AMQP Class Number and Mapping Index
    frame_id = 90
    index = 0x005A0000

    class Select(Frame):
        """Select standard transaction mode

        This method sets the channel to use standard transactions. The client
        must use this method at least once on a channel before using the Commit
        or Rollback methods.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 10
        index = 0x005A000A
        name = 'Tx.Select'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Tx.SelectOk']

    class SelectOk(Frame):
        """Confirm transaction mode

        This method confirms to the client that the channel was successfully
        set to use standard transactions.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 11
        index = 0x005A000B
        name = 'Tx.SelectOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

    class Commit(Frame):
        """Commit the current transaction

        This method commits all message publications and acknowledgments
        performed in the current transaction.  A new transaction starts
        immediately after a commit.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 20
        index = 0x005A0014
        name = 'Tx.Commit'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Tx.CommitOk']

    class CommitOk(Frame):
        """Confirm a successful commit

        This method confirms to the client that the commit succeeded. Note that
        if a commit fails, the server raises a channel exception.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 21
        index = 0x005A0015
        name = 'Tx.CommitOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False

    class Rollback(Frame):
        """Abandon the current transaction

        This method abandons all message publications and acknowledgments
        performed in the current transaction. A new transaction starts
        immediately after a rollback. Note that unacked messages will not be
        automatically redelivered by rollback; if that is required an explicit
        recover call should be issued.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 30
        index = 0x005A001E
        name = 'Tx.Rollback'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Tx.RollbackOk']

    class RollbackOk(Frame):
        """Confirm successful rollback

        This method confirms to the client that the rollback succeeded. Note
        that if an rollback fails, the server raises a channel exception.

        """
        # AMQP Method Number and Mapping Index
        frame_id = 31
        index = 0x005A001F
        name = 'Tx.RollbackOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False


class Confirm(object):
    __slots__ = []

    # AMQP Class Number and Mapping Index
    frame_id = 85
    index = 0x00550000

    class Select(Frame):
        # AMQP Method Number and Mapping Index
        frame_id = 10
        index = 0x0055000A
        name = 'Confirm.Select'

        # Specifies if this is a synchronous AMQP method
        synchronous = True

        # Valid responses to this method
        valid_responses = ['Confirm.SelectOk']

        # AMQP Method Attributes
        __slots__ = ['nowait']

        # Class Attribute Types
        _nowait = 'bit'

        def __init__(self, nowait=False):
            """Initialize the Confirm.Select class

            :param bool nowait: Do not send a reply method

            """
            # Do not send a reply method
            self.nowait = nowait

    class SelectOk(Frame):
        # AMQP Method Number and Mapping Index
        frame_id = 11
        index = 0x0055000B
        name = 'Confirm.SelectOk'

        # Specifies if this is a synchronous AMQP method
        synchronous = False


# AMQP Class.Method Index Mapping
INDEX_MAPPING = {
    0x000A000A: Connection.Start,
    0x000A000B: Connection.StartOk,
    0x000A0014: Connection.Secure,
    0x000A0015: Connection.SecureOk,
    0x000A001E: Connection.Tune,
    0x000A001F: Connection.TuneOk,
    0x000A0028: Connection.Open,
    0x000A0029: Connection.OpenOk,
    0x000A0032: Connection.Close,
    0x000A0033: Connection.CloseOk,
    0x000A003C: Connection.Blocked,
    0x000A003D: Connection.Unblocked,
    0x0014000A: Channel.Open,
    0x0014000B: Channel.OpenOk,
    0x00140014: Channel.Flow,
    0x00140015: Channel.FlowOk,
    0x00140028: Channel.Close,
    0x00140029: Channel.CloseOk,
    0x0028000A: Exchange.Declare,
    0x0028000B: Exchange.DeclareOk,
    0x00280014: Exchange.Delete,
    0x00280015: Exchange.DeleteOk,
    0x0028001E: Exchange.Bind,
    0x0028001F: Exchange.BindOk,
    0x00280028: Exchange.Unbind,
    0x00280033: Exchange.UnbindOk,
    0x0032000A: Queue.Declare,
    0x0032000B: Queue.DeclareOk,
    0x00320014: Queue.Bind,
    0x00320015: Queue.BindOk,
    0x0032001E: Queue.Purge,
    0x0032001F: Queue.PurgeOk,
    0x00320028: Queue.Delete,
    0x00320029: Queue.DeleteOk,
    0x00320032: Queue.Unbind,
    0x00320033: Queue.UnbindOk,
    0x003C000A: Basic.Qos,
    0x003C000B: Basic.QosOk,
    0x003C0014: Basic.Consume,
    0x003C0015: Basic.ConsumeOk,
    0x003C001E: Basic.Cancel,
    0x003C001F: Basic.CancelOk,
    0x003C0028: Basic.Publish,
    0x003C0032: Basic.Return,
    0x003C003C: Basic.Deliver,
    0x003C0046: Basic.Get,
    0x003C0047: Basic.GetOk,
    0x003C0048: Basic.GetEmpty,
    0x003C0050: Basic.Ack,
    0x003C005A: Basic.Reject,
    0x003C0064: Basic.RecoverAsync,
    0x003C006E: Basic.Recover,
    0x003C006F: Basic.RecoverOk,
    0x003C0078: Basic.Nack,
    0x005A000A: Tx.Select,
    0x005A000B: Tx.SelectOk,
    0x005A0014: Tx.Commit,
    0x005A0015: Tx.CommitOk,
    0x005A001E: Tx.Rollback,
    0x005A001F: Tx.RollbackOk,
    0x0055000A: Confirm.Select,
    0x0055000B: Confirm.SelectOk
}
