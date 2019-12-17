# -*- encoding: utf-8 -*-
"""AMQP Specifications and Classes"""
__author__ = 'Gavin M. Roy'
__email__ = 'gavinmroy@gmail.com'
__since__ = '2011-09-23'
__version__ = '3.0.0'

DEPRECATED_RABBITMQ_SUPPORT = False
"""Toggle to support older versions of RabbitMQ."""


def support_deprecated_rabbitmq(enabled: bool = True):
    """Invoke to restrict the data types available in field-tables that are
    sent to RabbitMQ.

    """
    global DEPRECATED_RABBITMQ_SUPPORT
    DEPRECATED_RABBITMQ_SUPPORT = enabled


__all__ = [
    'body', 'decode', 'encode', 'exceptions', 'frame', 'header', 'heartbeat',
    'specification', 'support_deprecated_rabbitmq',
    'DEPRECATED_RABBITMQ_SUPPORT'
]
