# -*- encoding: utf-8 -*-
"""
AMQP Heartbeat Frame, used to create new Heartbeat frames for sending to a peer

"""
import struct

from pamqp import specification


class Heartbeat(object):
    """Heartbeat frame object mapping class. AMQP Heartbeat frames are mapped
    on to this class for a common access structure to the attributes/data
    values.

    """
    name: str = 'Heartbeat'
    value = struct.pack('>BHI', specification.FRAME_HEARTBEAT, 0, 0) + \
        specification.FRAME_END_CHAR

    @classmethod
    def marshal(cls) -> bytes:
        """Return the binary frame content"""
        return cls.value
