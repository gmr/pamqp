# coding=utf-8

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-09-28'

import sys
sys.path.insert(0, '..')

import pamqp


def marshal_protocol_header_test():
    expectation = 'AMQP\x00\x00\t\x01'
    frame = pamqp.ProtocolHeader()
    data = frame.marshal()
    if data != expectation:
        assert False, \
            "marshalling did not return the expectation: %r/%r" % \
            (data, expectation)


def demarshal_basic_cancel_test():
    expectation = '\x01\x00\x01\x00\x00\x00\r\x00<\x00\x1e\x07ctag1.0\x00\xce'
    frame = pamqp.specification.Basic.Cancel(consumer_tag='ctag1.0')
    data = pamqp.frame.marshal(frame, 1)
    if data != expectation:
        assert False, \
            "marshalling did not return the expectation:\n%r\n%r" % \
            (expectation, data)


def demarshal_basic_cancelok_test():
    expectation = '\x01\x00\x01\x00\x00\x00\x0c\x00<\x00\x1f\x07ctag1.0\xce'
    frame = pamqp.specification.Basic.CancelOk(consumer_tag='ctag1.0')
    data = pamqp.frame.marshal(frame, 1)
    if data != expectation:
        assert False, \
            "marshalling did not return the expectation:\n%r\n%r" % \
            (expectation, data)

