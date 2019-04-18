# -*- encoding: utf-8 -*-
"""AMQP Specifications and Classes"""
from pamqp.constants import PYTHON3
from pamqp.header import ContentHeader, ProtocolHeader

__author__ = 'Gavin M. Roy'
__email__ = 'gavinmroy@gmail.com'
__since__ = '2011-09-23'
__version__ = '2.3.0'
__all__ = [
    'body', 'constants', 'decode', 'encode', 'exceptions', 'frame', 'header',
    'heartbeat', 'specification', 'PYTHON3', 'ContentHeader', 'ProtocolHeader'
]
