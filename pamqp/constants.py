"""
AMQP Constants
==============

Auto-generated, do not edit. To Generate run `.tools/codegen.py`

"""
# AMQP Protocol Frame Prefix
AMQP = b'AMQP'

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
FRAME_END_CHAR = b'\xce'
FRAME_HEADER_SIZE = 7
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
