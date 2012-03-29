# coding=utf-8

__author__ = 'Gavin M. Roy'
__email__ = 'gmr@myyearbook.com'
__date__ = '2011-09-27'

import sys
sys.path.insert(0, '..')

import test_support
import pamqp


def demarshal_protocol_header_test():

    # Decode the frame and validate lengths
    frame_data = 'AMQP\x00\x00\t\x01'
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.__class__.__name__ != 'ProtocolHeader':
        assert False, \
            ('Frame was of wrong type, expected ProtocolHeader, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 8:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (8, consumed))

    # Validate the channel
    if channel != 0:
        assert False, 'Channel number did not match the expected value'

    if frame.major_version != 0 or \
       frame.minor_version != 9 or \
       frame.revision != 1:
        assert False, 'Protocol version is incorrect'


def demarshal_basic_cancel_test():
    frame_data = '\x01\x00\x01\x00\x00\x00\r\x00<\x00\x1e\x07ctag1.0\x00\xce'
    expectation = {'consumer_tag': 'ctag1.0', 'nowait': False}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Basic.Cancel':
        assert False, \
            ('Frame was of wrong type, expected Basic.Cancel, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 20:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (20, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_basic_cancelok_test():
    frame_data = '\x01\x00\x01\x00\x00\x00\x0c\x00<\x00\x1f\x07ctag1.0\xce'
    expectation = {'consumer_tag': 'ctag1.0'}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Basic.CancelOk':
        assert False, \
            ('Frame was of wrong type, expected Basic.CancelOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 19:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (19, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_basic_consume_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00\x18\x00<\x00\x14\x00\x00\x04test'
                  '\x07ctag1.0\x00\x00\x00\x00\x00\xce')
    expectation = {'exclusive': False,
                   'nowait': False,
                   'no_local': False,
                   'consumer_tag': 'ctag1.0',
                   'queue': 'test',
                   'arguments': {},
                   'ticket': 0,
                   'no_ack': False}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Basic.Consume':
        assert False, \
            ('Frame was of wrong type, expected Basic.Consume, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 31:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (31, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_basic_consumeok_test():
    frame_data = '\x01\x00\x01\x00\x00\x00\x0c\x00<\x00\x15\x07ctag1.0\xce'
    expectation = {'consumer_tag': 'ctag1.0'}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Basic.ConsumeOk':
        assert False, \
            ('Frame was of wrong type, expected Basic.ConsumeOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 19:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (19, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_basic_deliver_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00\x1b\x00<\x00<\x07ctag1.0\x00\x00'
                  '\x00\x00\x00\x00\x00\x01\x00\x00\x04test\xce')

    expectation = {'consumer_tag': 'ctag1.0',
                   'delivery_tag': 1,
                   'redelivered': False,
                   'exchange': '',
                   'routing_key': 'test'}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Basic.Deliver':
        assert False, \
            ('Frame was of wrong type, expected Basic.Deliver, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 34:
        assert False, \
            'Bytes consumed did not match the expected value: %i/%i' % \
            (34, consumed)

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_basic_get_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00\x0c\x00<\x00F\x00\x00\x04test'
                  '\x00\xce')
    expectation = {'queue': 'test', 'ticket': 0, 'no_ack': False}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Basic.Get':
        assert False, \
            ('Frame was of wrong type, expected Basic.Get, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 19:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (19, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_basic_publish_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00\r\x00<\x00(\x00\x00\x00\x04test'
                  '\x00\xce')
    expectation = {'ticket': 0, 'mandatory': False, 'routing_key': 'test',
                   'immediate': False, 'exchange': ''}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Basic.Publish':
        assert False, \
            ('Frame was of wrong type, expected Basic.Publish, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 20:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (20, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_basic_getok_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00\x17\x00<\x00G\x00\x00\x00\x00\x00'
                  '\x00\x00\x10\x00\x00\x04test\x00\x00\x12\x06\xce')
    expectation = {'message_count': 4614,
                   'redelivered': False,
                   'routing_key': 'test',
                   'delivery_tag': 16,
                   'exchange': ''}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Basic.GetOk':
        assert False, \
            ('Frame was of wrong type, expected Basic.GetOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 30:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (30, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_basic_qos_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00\x0b\x00<\x00\n\x00\x00\x00\x00\x00'
                  '\x01\x00\xce')
    expectation = {'prefetch_count': 1, 'prefetch_size': 0, 'global_': False}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Basic.Qos':
        assert False, \
            ('Frame was of wrong type, expected Basic.Qos, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 18:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (18, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_basic_qosok_test():
    frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00<\x00\x0b\xce'
    expectation = {}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Basic.QosOk':
        assert False, \
            ('Frame was of wrong type, expected Basic.QosOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 11:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (11, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_basic_reject_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00\r\x00<\x00Z\x00\x00\x00\x00\x00'
                  '\x00\x00\x10\x01\xce')
    expectation = {'requeue': True, 'delivery_tag': 16}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Basic.Reject':
        assert False, \
            ('Frame was of wrong type, expected Basic.Reject, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 20:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (20, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_channel_close_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00\x1a\x00\x14\x00(\x00\xc8\x0f'
                  'Normal shutdown\x00\x00\x00\x00\xce')
    expectation = {'class_id': 0, 'method_id': 0, 'reply_code': 200,
                   'reply_text': 'Normal shutdown'}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Channel.Close':
        assert False, \
            ('Frame was of wrong type, expected Channel.Close, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 33:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (33, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_channel_closeok_test():
    frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00\x14\x00)\xce'
    expectation = {}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Channel.CloseOk':
        assert False, \
            ('Frame was of wrong type, expected Channel.CloseOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 11:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (11, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_channel_open_test():
    frame_data = '\x01\x00\x01\x00\x00\x00\x05\x00\x14\x00\n\x00\xce'
    expectation = {'out_of_band': ''}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Channel.Open':
        assert False, \
            ('Frame was of wrong type, expected Channel.Open, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 12:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (12, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_channel_openok_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00\x08\x00\x14\x00\x0b\x00\x00\x00'
                  '\x00\xce')
    expectation = {'channel_id': ''}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Channel.OpenOk':
        assert False, \
            ('Frame was of wrong type, expected Channel.OpenOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 15:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (15, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_confirm_select_test():
    frame_data = '\x01\x00\x01\x00\x00\x00\x05\x00U\x00\n\x00\xce'
    expectation = {'nowait': False}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Confirm.Select':
        assert False, \
            ('Frame was of wrong type, expected Confirm.Select, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 12:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (12, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_confirm_selectok_test():
    frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00U\x00\x0b\xce'
    expectation = {}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Confirm.SelectOk':
        assert False, \
            ('Frame was of wrong type, expected Confirm.SelectOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 11:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (11, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_connection_close_test():
    frame_data = ('\x01\x00\x00\x00\x00\x00\x1a\x00\n\x002\x00\xc8\x0f'
                  'Normal shutdown\x00\x00\x00\x00\xce')
    expectation = {'class_id': 0, 'method_id': 0, 'reply_code': 200,
                   'reply_text': 'Normal shutdown'}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Connection.Close':
        assert False, \
            ('Frame was of wrong type, expected Connection.Close, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 33:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (33, consumed))

    # Validate the channel
    if channel != 0:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_connection_closeok_test():
    frame_data = '\x01\x00\x00\x00\x00\x00\x04\x00\n\x003\xce'
    expectation = {}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Connection.CloseOk':
        assert False, \
            ('Frame was of wrong type, expected Connection.CloseOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 11:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (11, consumed))

    # Validate the channel
    if channel != 0:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_connection_open_test():
    frame_data = '\x01\x00\x00\x00\x00\x00\x08\x00\n\x00(\x01/\x00\x01\xce'
    expectation = {'insist': True, 'capabilities': '', 'virtual_host': '/'}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Connection.Open':
        assert False, \
            ('Frame was of wrong type, expected Connection.Open, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 15:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (15, consumed))

    # Validate the channel
    if channel != 0:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_connection_openok_test():
    frame_data = '\x01\x00\x00\x00\x00\x00\x05\x00\n\x00)\x00\xce'
    expectation = {'known_hosts': ''}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Connection.OpenOk':
        assert False, \
            ('Frame was of wrong type, expected Connection.OpenOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 12:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (12, consumed))

    # Validate the channel
    if channel != 0:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_connection_start_test():
    frame_data = ('\x01\x00\x00\x00\x00\x01G\x00\n\x00\n\x00\t\x00\x00\x01"'
                  '\x0ccapabilitiesF\x00\x00\x00X\x12publisher_confirmst\x01'
                  '\x1aexchange_exchange_bindingst\x01\nbasic.nackt\x01\x16'
                  'consumer_cancel_notifyt\x01\tcopyrightS\x00\x00\x00'
                  '$Copyright (C) 2007-2011 VMware, Inc.\x0binformationS\x00'
                  '\x00\x005Licensed under the MPL.  See http://www.rabbitmq.'
                  'com/\x08platformS\x00\x00\x00\nErlang/OTP\x07productS\x00'
                  '\x00\x00\x08RabbitMQ\x07versionS\x00\x00\x00\x052.6.1\x00'
                  '\x00\x00\x0ePLAIN AMQPLAIN\x00\x00\x00\x05en_US\xce')
    expectation = {'server_properties':
                           {'information':
                                ('Licensed under the MPL.  '
                                 'See http://www.rabbitmq.com/'),
                            'product': 'RabbitMQ',
                            'copyright':
                                'Copyright (C) 2007-2011 VMware, Inc.',
                            'capabilities':
                                    {'exchange_exchange_bindings': True,
                                     'consumer_cancel_notify': True,
                                     'publisher_confirms': True,
                                     'basic.nack': True},
                            'platform': 'Erlang/OTP',
                            'version': '2.6.1'},
                   'version_minor': 9,
                   'mechanisms': 'PLAIN AMQPLAIN',
                   'locales': 'en_US',
                   'version_major': 0}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Connection.Start':
        assert False, \
            ('Frame was of wrong type, expected Connection.Start, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 334:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (334, consumed))

    # Validate the channel
    if channel != 0:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_connection_startok_test():
    frame_data = ('\x01\x00\x00\x00\x00\x00\xf4\x00\n\x00\x0b\x00\x00\x00\xd0'
                  '\x08platformS\x00\x00\x00\x0cPython 2.7.1\x07productS\x00'
                  '\x00\x00\x1aPika Python Client Library\x07versionS\x00\x00'
                  '\x00\n0.9.6-pre0\x0ccapabilitiesF\x00\x00\x00;\x16'
                  'consumer_cancel_notifyt\x01\x12publisher_confirmst'
                  '\x01\nbasic.nackt\x01\x0binformationS\x00\x00\x00\x1a'
                  'See http://pika.github.com\x05PLAIN\x00\x00\x00\x0c\x00'
                  'guest\x00guest\x05en_US\xce')
    expectation = {'locale': 'en_US',
                   'mechanism': 'PLAIN',
                   'client_properties': {'platform': 'Python 2.7.1',
                                         'product':
                                             'Pika Python Client Library',
                                         'version': '0.9.6-pre0',
                                         'capabilities':
                                                 {'consumer_cancel_notify':
                                                      True,
                                                  'publisher_confirms': True,
                                                  'basic.nack': True},
                                         'information':
                                             'See http://pika.github.com'},
                   'response': '\x00guest\x00guest'}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Connection.StartOk':
        assert False, \
            ('Frame was of wrong type, expected Connection.StartOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 251:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (251, consumed))

    # Validate the channel
    if channel != 0:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_connection_tune_test():
    frame_data = ('\x01\x00\x00\x00\x00\x00\x0c\x00\n\x00\x1e\x00\x00\x00\x02'
                  '\x00\x00\x00\x00\xce')
    expectation = {'frame_max': 131072, 'channel_max': 0, 'heartbeat': 0}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Connection.Tune':
        assert False, \
            ('Frame was of wrong type, expected Connection.Tune, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 19:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (19, consumed))

    # Validate the channel
    if channel != 0:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_connection_tuneok_test():
    frame_data = ('\x01\x00\x00\x00\x00\x00\x0c\x00\n\x00\x1f\x00\x00\x00'
                  '\x02\x00\x00\x00\x00\xce')
    expectation = {'frame_max': 131072, 'channel_max': 0, 'heartbeat': 0}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Connection.TuneOk':
        assert False, \
            ('Frame was of wrong type, expected Connection.TuneOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 19:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (19, consumed))

    # Validate the channel
    if channel != 0:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_content_body_frame_test():
    frame_data = ('\x03\x00\x01\x00\x00\x00#Hello World #0:'
                  '1316899165.75516605\xce')

    expectation = "Hello World #0:1316899165.75516605"

    # Decode the frame and validate lengths
    consumed, channel, data = pamqp.frame.demarshal(frame_data)

    # Validate the bytes consumed
    if consumed != 41:
        assert False, \
            'Bytes consumed did not match the expected value: %i/%i' % \
            (41, consumed)

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Validate the content
    if data != expectation:
        assert False, 'Content frame data did not match the expected value'


def demarshal_exchange_declare_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00%\x00(\x00\n\x00\x00\x12'
                  'pika_test_exchange\x06direct\x00\x00\x00\x00\x00\xce')
    expectation = {'nowait': False,
                   'exchange': 'pika_test_exchange',
                   'durable': False,
                   'passive': False,
                   'internal': False,
                   'arguments': {},
                   'ticket': 0,
                   'type': 'direct',
                   'auto_delete': False}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Exchange.Declare':
        assert False, \
            ('Frame was of wrong type, expected Exchange.Declare, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 44:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (44, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_exchange_declareok_test():
    frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00(\x00\x0b\xce'
    expectation = {}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Exchange.DeclareOk':
        assert False, \
            ('Frame was of wrong type, expected Exchange.DeclareOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 11:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (11, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_exchange_delete_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00\x1a\x00(\x00\x14\x00\x00\x12'
                  'pika_test_exchange\x00\xce')
    expectation = {'ticket': 0,
                   'if_unused': False,
                   'nowait': False,
                   'exchange': 'pika_test_exchange'}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Exchange.Delete':
        assert False, \
            ('Frame was of wrong type, expected Exchange.Delete, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 33:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (33, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_exchange_deleteok_test():
    frame_data = '\x01\x00\x01\x00\x00\x00\x04\x00(\x00\x15\xce'
    expectation = {}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Exchange.DeleteOk':
        assert False, \
            ('Frame was of wrong type, expected Exchange.DeleteOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 11:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (11, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_queue_bind_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00?\x002\x00\x14\x00\x00\x0f'
                  'pika_test_queue\x12pika_test_exchange\x10test_routing_key'
                  '\x00\x00\x00\x00\x00\xce')
    expectation = {'nowait': False,
                   'exchange': 'pika_test_exchange',
                   'routing_key': 'test_routing_key',
                   'queue': 'pika_test_queue',
                   'arguments': {},
                   'ticket': 0}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Queue.Bind':
        assert False, \
            ('Frame was of wrong type, expected Queue.Bind, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 70:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (70, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_queue_bindok_test():
    frame_data = '\x01\x00\x01\x00\x00\x00\x04\x002\x00\x15\xce'
    expectation = {}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Queue.BindOk':
        assert False, \
            ('Frame was of wrong type, expected Queue.BindOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 11:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (11, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_queue_declare_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00\x10\x002\x00\n\x00\x00\x04test'
                  '\x02\x00\x00\x00\x00\xce')
    expectation = {'passive': False,
                   'nowait': False,
                   'exclusive': False,
                   'durable': True,
                   'queue': 'test',
                   'arguments': {},
                   'ticket': 0,
                   'auto_delete': False}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Queue.Declare':
        assert False, \
            ('Frame was of wrong type, expected Queue.Declare, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 23:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (23, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_queue_declareok_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00\x11\x002\x00\x0b\x04test'
                  '\x00\x00\x12\x07\x00\x00\x00\x00\xce')
    expectation = {'queue': 'test', 'message_count': 4615, 'consumer_count': 0}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Queue.DeclareOk':
        assert False, \
            ('Frame was of wrong type, expected Queue.DeclareOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 24:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (24, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_queue_delete_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00\x17\x002\x00(\x00\x00\x0f'
                  'pika_test_queue\x00\xce')
    expectation = {'queue': 'pika_test_queue',
                   'ticket': 0,
                   'if_empty': False,
                   'nowait': False,
                   'if_unused': False}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Queue.Delete':
        assert False, \
            ('Frame was of wrong type, expected Queue.Delete, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 30:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (30, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_queue_deleteok_test():
    frame_data = '\x01\x00\x01\x00\x00\x00\x08\x002\x00)\x00\x00\x00\x00\xce'
    expectation = {'message_count': 0}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Queue.DeleteOk':
        assert False, \
            ('Frame was of wrong type, expected Queue.DeleteOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 15:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (15, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_queue_purge_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00\x0c\x002\x00\x1e\x00\x00\x04test'
                  '\x00\xce')
    expectation = {'queue': 'test', 'ticket': 0, 'nowait': False}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Queue.Purge':
        assert False, \
            ('Frame was of wrong type, expected Queue.Purge, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 19:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (19, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_queue_unbind_test():
    frame_data = ('\x01\x00\x01\x00\x00\x00>\x002\x002\x00\x00\x0f'
                  'pika_test_queue\x12pika_test_exchange\x10test_routing_key'
                  '\x00\x00\x00\x00\xce')
    expectation = {'queue': 'pika_test_queue',
                   'arguments': {},
                   'ticket': 0,
                   'routing_key': 'test_routing_key',
                   'exchange': 'pika_test_exchange'}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Queue.Unbind':
        assert False, \
            ('Frame was of wrong type, expected Queue.Unbind, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 69:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (69, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)


def demarshal_queue_unbindok_test():
    frame_data = '\x01\x00\x01\x00\x00\x00\x04\x002\x003\xce'
    expectation = {}

    # Decode the frame and validate lengths
    consumed, channel, frame = pamqp.frame.demarshal(frame_data)

    # Validate the frame name
    if frame.name != 'Queue.UnbindOk':
        assert False, \
            ('Frame was of wrong type, expected Queue.UnbindOk, '
             'received %s' % frame.name)

    # Validate the bytes consumed
    if consumed != 11:
        assert False, \
            ('Bytes consumed did not match the expected value: %i/%i' %
             (11, consumed))

    # Validate the channel
    if channel != 1:
        assert False, 'Channel number did not match the expected value'

    # Run the frame check, assertions contained within
    test_support.check_frame(frame, expectation)
