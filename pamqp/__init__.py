"""AMQP Specifications and Classes"""

from importlib import metadata

from pamqp import (
    body,
    commands,
    constants,
    decode,
    encode,
    exceptions,
    frame,
    header,
    heartbeat,
)

__author__ = 'Gavin M. Roy'
__email__ = 'gavinmroy@gmail.com'
__since__ = '2011-09-23'
__version__ = version = metadata.version('pamqp')

__all__ = [
    'body',
    'commands',
    'constants',
    'decode',
    'encode',
    'exceptions',
    'frame',
    'header',
    'heartbeat',
]
