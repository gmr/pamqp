# coding=utf-8
import struct
import unittest

from pamqp import exceptions, frame, specification


class TestCase(unittest.TestCase):

    def test_invalid_protocol_header(self):
        try:
            frame.unmarshal(b'AMQP\x00\x00\t')
        except exceptions.UnmarshalingException as err:
            self.assertEqual(str(err),
                             "Could not unmarshal <class 'pamqp.header."
                             "ProtocolHeader'> frame: Data did not match "
                             "the ProtocolHeader format: AMQP\x00\x00\t")
        else:
            assert False, 'Failed to raise exception'

    def test_frame_with_no_length(self):
        frame_data = (b'\x01\x00\x01\x00\x00\x00\x00\x00<\x00P\x00\x00\x00\x00'
                      b'\x00\x00\x00\x01\x00\xce')
        try:
            frame.unmarshal(frame_data)
        except exceptions.UnmarshalingException as err:
            self.assertEqual(
                str(err), 'Could not unmarshal Unknown frame: No frame size')
        else:
            assert False, 'Failed to raise exception'

    def test_frame_malformed_length(self):
        frame_data = (b'\x01\x00\x01\x00\x00\x00\x0c\x00<\x00P\x00\x00\x00\x00'
                      b'\x00\x00\x00\xce')
        try:
            frame.unmarshal(frame_data)
        except exceptions.UnmarshalingException as err:
            self.assertEqual(
                str(err),
                'Could not unmarshal Unknown frame: Not all data received')
        else:
            assert False, 'Failed to raise exception'

    def test_frame_malformed_end_byte(self):
        frame_data = (b'\x01\x00\x01\x00\x00\x00\r\x00<\x00P\x00\x00\x00\x00'
                      b'\x00\x00\x00\x01\x00\x00')
        try:
            frame.unmarshal(frame_data)
        except exceptions.UnmarshalingException as err:
            self.assertEqual(
                str(err),
                'Could not unmarshal Unknown frame: Last byte error')
        else:
            assert False, 'Failed to raise exception'

    def test_malformed_frame_content(self):
        payload = struct.pack('>HxxQ', 8192, 32768)
        frame_value = b''.join([struct.pack('>BHI', 5, 0, len(payload)),
                                payload, frame.FRAME_END_CHAR])
        try:
            result = frame.unmarshal(frame_value)
        except exceptions.UnmarshalingException as err:
            self.assertEqual(
                str(err),
                'Could not unmarshal Unknown frame: Unknown frame type: 5')
        else:
            assert False, 'Failed to raise exception'
