# -*- encoding: utf-8 -*-
import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest
from pamqp import frame
from pamqp import header
from pamqp import heartbeat
from pamqp import specification

PYTHON3 = True if sys.version_info > (3, 0, 0) else False

def encode(value):
    if PYTHON3:
        return bytes(value, 'latin1')
    return value


class MarshalingTests(unittest.TestCase):

    def protocol_header_test(self):
        expectation = encode('AMQP\x00\x00\t\x01')
        response = header.ProtocolHeader().marshal()
        self.assertEqual(response,
                         expectation,
                         "ProtocolHeader did not match expectation")

    def basic_ack_test(self):
        expectation = encode('\x01\x00\x01\x00\x00\x00\r\x00<\x00P\x00\x00\x00'
                             '\x00\x00\x00\x00\x01\x00\xce')
        frame_obj = specification.Basic.Ack(1, False)
        response = frame.marshal(frame_obj, 1)
        self.assertEqual(response, expectation,
                         "Basic.Ack did not match expectation")

    def basic_cancel_test(self):
        expectation = encode('\x01\x00\x01\x00\x00\x00\r\x00<\x00\x1e\x07'
                             'ctag1.0\x00\xce')
        frame_obj = specification.Basic.Cancel(consumer_tag='ctag1.0')
        response = frame.marshal(frame_obj, 1)
        self.assertEqual(response, expectation,
                         "Basic.Cancel did not match expectation")

    def basic_cancelok_test(self):
        expectation = encode('\x01\x00\x01\x00\x00\x00\x0c\x00<\x00\x1f\x07'
                             'ctag1.0\xce')
        frame_obj = specification.Basic.CancelOk(consumer_tag='ctag1.0')
        response = frame.marshal(frame_obj, 1)
        self.assertEqual(response, expectation,
                         "Basic.Cancel did not match expectation")

    def basic_consume_test(self):
        expectation = encode('\x01\x00\x01\x00\x00\x00\x15\x00<\x00\x14\x00'
                             '\x00\x03bar\x05ctag0\x00\x00\x00\x00\x00\xce')
        frame_obj = specification.Basic.Consume(0, 'bar', 'ctag0',
                                                False, False, False, False)
        response = frame.marshal(frame_obj, 1)
        self.assertEqual(response, expectation,
                         "Basic.Consume did not match expectation")

    def heartbeat_test(self):
        expectation = encode('\x08\x00\x00\x00\x00\x00\x00\xce')
        response = frame.marshal(heartbeat.Heartbeat(), 0)
        self.assertEqual(response, expectation,
                         "Heartbeat did not match expectation")
