"""
AMQP Heartbeat Frame, used to create new Heartbeat frames for sending to a peer

"""
import struct

from pamqp import specification
from pamqp import PYTHON3


class Heartbeat(object):
    """Heartbeat frame object mapping class. AMQP Heartbeat frames are mapped
    on to this class for a common access structure to the attributes/data
    values.

    """
    name = 'Heartbeat'

    def marshal(self):
        """Return the binary frame content

        :rtype: str or bytes

        """
        value = struct.pack('>BHI', specification.FRAME_HEARTBEAT, 0, 0)
        if PYTHON3:
            return value + bytes(chr(specification.FRAME_END), 'latin1')
        return value + chr(specification.FRAME_END)
