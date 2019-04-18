# -*- encoding: utf-8 -*-
"""
AMQP Heartbeat Frame, used to create new Heartbeat frames for sending to a peer

"""
import struct

from pamqp import PYTHON3, specification


class Heartbeat(object):
    """Heartbeat frame object mapping class. AMQP Heartbeat frames are mapped
    on to this class for a common access structure to the attributes/data
    values.

    """
    name = 'Heartbeat'

    @staticmethod
    def marshal():
        """Return the binary frame content

        :rtype: str or bytes

        """
        value = struct.pack('>BHI', specification.FRAME_HEARTBEAT, 0, 0)
        if PYTHON3:
            return value + bytes((specification.FRAME_END, ))
        return value + chr(specification.FRAME_END)
