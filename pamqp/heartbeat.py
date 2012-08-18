"""
AMQP Heartbeat Frame

"""
from pamqp import specification
import struct


class Heartbeat(object):
    """
    Heartbeat frame object mapping class. AMQP Heartbeat frames are mapped on
    to this class for a common access structure to the attributes/data values.
    """
    name = 'Heartbeat'

    def marshal(self):
        """Return the binary frame content

        :rtype: str

        """
        return struct.pack('>BHI',
                           specification.FRAME_HEARTBEAT,
                           0, 0) + chr(specification.FRAME_END)
