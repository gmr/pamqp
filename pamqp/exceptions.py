# -*- encoding: utf-8 -*-
"""
pamqp specific exceptions that do not fit within the AMQP exceptions
contained in pamqp.specification

"""


class PAMQPException(Exception):
    """Base exception for all pamqp specific exceptions"""


class UnmarshalingException(PAMQPException):
    """Raised when a frame is not able to be unmarshaled."""

    def __str__(self):
        return 'Could not unmarshal {} frame: {}'.format(
            self.args[0], self.args[1])
