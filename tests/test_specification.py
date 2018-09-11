try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pamqp import specification


class ArgumentTypeTests(unittest.TestCase):
    def test_basic_ack_has_delivery_tag(self):
        self.assertEqual(specification.Basic.Ack.type('delivery_tag'),
                         'longlong')

    def test_basic_ack_has_multiple(self):
        self.assertEqual(specification.Basic.Ack.type('multiple'), 'bit')

    def test_basic_cancel_has_consumer_tag(self):
        self.assertEqual(specification.Basic.Cancel.type('consumer_tag'),
                         'shortstr')

    def test_basic_cancel_has_nowait(self):
        self.assertEqual(specification.Basic.Cancel.type('nowait'), 'bit')

    def test_basic_cancelok_has_consumer_tag(self):
        self.assertEqual(specification.Basic.CancelOk.type('consumer_tag'),
                         'shortstr')

    def test_basic_consume_has_ticket(self):
        self.assertEqual(specification.Basic.Consume.type('ticket'), 'short')

    def test_basic_consume_has_queue(self):
        self.assertEqual(specification.Basic.Consume.type('queue'), 'shortstr')

    def test_basic_consume_has_consumer_tag(self):
        self.assertEqual(specification.Basic.Consume.type('consumer_tag'),
                         'shortstr')

    def test_basic_consume_has_no_local(self):
        self.assertEqual(specification.Basic.Consume.type('no_local'), 'bit')

    def test_basic_consume_has_no_ack(self):
        self.assertEqual(specification.Basic.Consume.type('no_ack'), 'bit')

    def test_basic_consume_has_exclusive(self):
        self.assertEqual(specification.Basic.Consume.type('exclusive'), 'bit')

    def test_basic_consume_has_nowait(self):
        self.assertEqual(specification.Basic.Consume.type('nowait'), 'bit')

    def test_basic_consume_has_arguments(self):
        self.assertEqual(specification.Basic.Consume.type('arguments'), 'table')

    def test_basic_consumeok_has_consumer_tag(self):
        self.assertEqual(specification.Basic.ConsumeOk.type('consumer_tag'),
                         'shortstr')

    def test_basic_deliver_has_consumer_tag(self):
        self.assertEqual(specification.Basic.Deliver.type('consumer_tag'),
                         'shortstr')

    def test_basic_deliver_has_delivery_tag(self):
        self.assertEqual(specification.Basic.Deliver.type('delivery_tag'),
                         'longlong')

    def test_basic_deliver_has_redelivered(self):
        self.assertEqual(specification.Basic.Deliver.type('redelivered'), 'bit')

    def test_basic_deliver_has_exchange(self):
        self.assertEqual(specification.Basic.Deliver.type('exchange'),
                         'shortstr')

    def test_basic_deliver_has_routing_key(self):
        self.assertEqual(specification.Basic.Deliver.type('routing_key'),
                         'shortstr')

    def test_basic_get_has_ticket(self):
        self.assertEqual(specification.Basic.Get.type('ticket'), 'short')

    def test_basic_get_has_queue(self):
        self.assertEqual(specification.Basic.Get.type('queue'), 'shortstr')

    def test_basic_get_has_no_ack(self):
        self.assertEqual(specification.Basic.Get.type('no_ack'), 'bit')

    def test_basic_getempty_has_cluster_id(self):
        self.assertEqual(specification.Basic.GetEmpty.type('cluster_id'),
                         'shortstr')

    def test_basic_getok_has_delivery_tag(self):
        self.assertEqual(specification.Basic.GetOk.type('delivery_tag'),
                         'longlong')

    def test_basic_getok_has_redelivered(self):
        self.assertEqual(specification.Basic.GetOk.type('redelivered'), 'bit')

    def test_basic_getok_has_exchange(self):
        self.assertEqual(specification.Basic.GetOk.type('exchange'), 'shortstr')

    def test_basic_getok_has_routing_key(self):
        self.assertEqual(specification.Basic.GetOk.type('routing_key'),
                         'shortstr')

    def test_basic_getok_has_message_count(self):
        self.assertEqual(specification.Basic.GetOk.type('message_count'),
                         'long')

    def test_basic_nack_has_delivery_tag(self):
        self.assertEqual(specification.Basic.Nack.type('delivery_tag'),
                         'longlong')

    def test_basic_nack_has_multiple(self):
        self.assertEqual(specification.Basic.Nack.type('multiple'), 'bit')

    def test_basic_nack_has_requeue(self):
        self.assertEqual(specification.Basic.Nack.type('requeue'), 'bit')

    def test_basic_publish_has_ticket(self):
        self.assertEqual(specification.Basic.Publish.type('ticket'), 'short')

    def test_basic_publish_has_exchange(self):
        self.assertEqual(specification.Basic.Publish.type('exchange'),
                         'shortstr')

    def test_basic_publish_has_routing_key(self):
        self.assertEqual(specification.Basic.Publish.type('routing_key'),
                         'shortstr')

    def test_basic_publish_has_mandatory(self):
        self.assertEqual(specification.Basic.Publish.type('mandatory'), 'bit')

    def test_basic_publish_has_immediate(self):
        self.assertEqual(specification.Basic.Publish.type('immediate'), 'bit')

    def test_basic_qos_has_prefetch_size(self):
        self.assertEqual(specification.Basic.Qos.type('prefetch_size'), 'long')

    def test_basic_qos_has_prefetch_count(self):
        self.assertEqual(specification.Basic.Qos.type('prefetch_count'),
                         'short')

    def test_basic_qos_has_global_(self):
        self.assertEqual(specification.Basic.Qos.type('global_'), 'bit')

    def test_basic_recover_has_requeue(self):
        self.assertEqual(specification.Basic.Recover.type('requeue'), 'bit')

    def test_basic_recoverasync_has_requeue(self):
        self.assertEqual(specification.Basic.RecoverAsync.type('requeue'),
                         'bit')

    def test_basic_reject_has_delivery_tag(self):
        self.assertEqual(specification.Basic.Reject.type('delivery_tag'),
                         'longlong')

    def test_basic_reject_has_requeue(self):
        self.assertEqual(specification.Basic.Reject.type('requeue'), 'bit')

    def test_basic_return_has_reply_code(self):
        self.assertEqual(specification.Basic.Return.type('reply_code'), 'short')

    def test_basic_return_has_reply_text(self):
        self.assertEqual(specification.Basic.Return.type('reply_text'),
                         'shortstr')

    def test_basic_return_has_exchange(self):
        self.assertEqual(specification.Basic.Return.type('exchange'),
                         'shortstr')

    def test_basic_return_has_routing_key(self):
        self.assertEqual(specification.Basic.Return.type('routing_key'),
                         'shortstr')

    def test_channel_close_has_reply_code(self):
        self.assertEqual(specification.Channel.Close.type('reply_code'),
                         'short')

    def test_channel_close_has_reply_text(self):
        self.assertEqual(specification.Channel.Close.type('reply_text'),
                         'shortstr')

    def test_channel_close_has_class_id(self):
        self.assertEqual(specification.Channel.Close.type('class_id'), 'short')

    def test_channel_close_has_method_id(self):
        self.assertEqual(specification.Channel.Close.type('method_id'), 'short')

    def test_channel_flow_has_active(self):
        self.assertEqual(specification.Channel.Flow.type('active'), 'bit')

    def test_channel_flowok_has_active(self):
        self.assertEqual(specification.Channel.FlowOk.type('active'), 'bit')

    def test_channel_open_has_out_of_band(self):
        self.assertEqual(specification.Channel.Open.type('out_of_band'),
                         'shortstr')

    def test_channel_openok_has_channel_id(self):
        self.assertEqual(specification.Channel.OpenOk.type('channel_id'),
                         'longstr')

    def test_confirm_select_has_nowait(self):
        self.assertEqual(specification.Confirm.Select.type('nowait'), 'bit')

    def test_connection_blocked_has_reason(self):
        self.assertEqual(specification.Connection.Blocked.type('reason'),
                         'shortstr')

    def test_connection_close_has_reply_code(self):
        self.assertEqual(specification.Connection.Close.type('reply_code'),
                         'short')

    def test_connection_close_has_reply_text(self):
        self.assertEqual(specification.Connection.Close.type('reply_text'),
                         'shortstr')

    def test_connection_close_has_class_id(self):
        self.assertEqual(specification.Connection.Close.type('class_id'),
                         'short')

    def test_connection_close_has_method_id(self):
        self.assertEqual(specification.Connection.Close.type('method_id'),
                         'short')

    def test_connection_open_has_virtual_host(self):
        self.assertEqual(specification.Connection.Open.type('virtual_host'),
                         'shortstr')

    def test_connection_open_has_capabilities(self):
        self.assertEqual(specification.Connection.Open.type('capabilities'),
                         'shortstr')

    def test_connection_open_has_insist(self):
        self.assertEqual(specification.Connection.Open.type('insist'), 'bit')

    def test_connection_openok_has_known_hosts(self):
        self.assertEqual(specification.Connection.OpenOk.type('known_hosts'),
                         'shortstr')

    def test_connection_secure_has_challenge(self):
        self.assertEqual(specification.Connection.Secure.type('challenge'),
                         'longstr')

    def test_connection_secureok_has_response(self):
        self.assertEqual(specification.Connection.SecureOk.type('response'),
                         'longstr')

    def test_connection_start_has_version_major(self):
        self.assertEqual(specification.Connection.Start.type('version_major'),
                         'octet')

    def test_connection_start_has_version_minor(self):
        self.assertEqual(specification.Connection.Start.type('version_minor'),
                         'octet')

    def test_connection_start_has_server_properties(self):
        self.assertEqual(
            specification.Connection.Start.type('server_properties'), 'table')

    def test_connection_start_has_mechanisms(self):
        self.assertEqual(specification.Connection.Start.type('mechanisms'),
                         'longstr')

    def test_connection_start_has_locales(self):
        self.assertEqual(specification.Connection.Start.type('locales'),
                         'longstr')

    def test_connection_startok_has_client_properties(self):
        self.assertEqual(
            specification.Connection.StartOk.type('client_properties'), 'table')

    def test_connection_startok_has_mechanism(self):
        self.assertEqual(specification.Connection.StartOk.type('mechanism'),
                         'shortstr')

    def test_connection_startok_has_response(self):
        self.assertEqual(specification.Connection.StartOk.type('response'),
                         'longstr')

    def test_connection_startok_has_locale(self):
        self.assertEqual(specification.Connection.StartOk.type('locale'),
                         'shortstr')

    def test_connection_tune_has_channel_max(self):
        self.assertEqual(specification.Connection.Tune.type('channel_max'),
                         'short')

    def test_connection_tune_has_frame_max(self):
        self.assertEqual(specification.Connection.Tune.type('frame_max'),
                         'long')

    def test_connection_tune_has_heartbeat(self):
        self.assertEqual(specification.Connection.Tune.type('heartbeat'),
                         'short')

    def test_connection_tuneok_has_channel_max(self):
        self.assertEqual(specification.Connection.TuneOk.type('channel_max'),
                         'short')

    def test_connection_tuneok_has_frame_max(self):
        self.assertEqual(specification.Connection.TuneOk.type('frame_max'),
                         'long')

    def test_connection_tuneok_has_heartbeat(self):
        self.assertEqual(specification.Connection.TuneOk.type('heartbeat'),
                         'short')

    def test_exchange_bind_has_ticket(self):
        self.assertEqual(specification.Exchange.Bind.type('ticket'), 'short')

    def test_exchange_bind_has_destination(self):
        self.assertEqual(specification.Exchange.Bind.type('destination'),
                         'shortstr')

    def test_exchange_bind_has_source(self):
        self.assertEqual(specification.Exchange.Bind.type('source'), 'shortstr')

    def test_exchange_bind_has_routing_key(self):
        self.assertEqual(specification.Exchange.Bind.type('routing_key'),
                         'shortstr')

    def test_exchange_bind_has_nowait(self):
        self.assertEqual(specification.Exchange.Bind.type('nowait'), 'bit')

    def test_exchange_bind_has_arguments(self):
        self.assertEqual(specification.Exchange.Bind.type('arguments'), 'table')

    def test_exchange_declare_has_ticket(self):
        self.assertEqual(specification.Exchange.Declare.type('ticket'), 'short')

    def test_exchange_declare_has_exchange(self):
        self.assertEqual(specification.Exchange.Declare.type('exchange'),
                         'shortstr')

    def test_exchange_declare_has_exchange_type(self):
        self.assertEqual(specification.Exchange.Declare.type('exchange_type'),
                         'shortstr')

    def test_exchange_declare_has_passive(self):
        self.assertEqual(specification.Exchange.Declare.type('passive'), 'bit')

    def test_exchange_declare_has_durable(self):
        self.assertEqual(specification.Exchange.Declare.type('durable'), 'bit')

    def test_exchange_declare_has_auto_delete(self):
        self.assertEqual(specification.Exchange.Declare.type('auto_delete'),
                         'bit')

    def test_exchange_declare_has_internal(self):
        self.assertEqual(specification.Exchange.Declare.type('internal'), 'bit')

    def test_exchange_declare_has_nowait(self):
        self.assertEqual(specification.Exchange.Declare.type('nowait'), 'bit')

    def test_exchange_declare_has_arguments(self):
        self.assertEqual(specification.Exchange.Declare.type('arguments'),
                         'table')

    def test_exchange_delete_has_ticket(self):
        self.assertEqual(specification.Exchange.Delete.type('ticket'), 'short')

    def test_exchange_delete_has_exchange(self):
        self.assertEqual(specification.Exchange.Delete.type('exchange'),
                         'shortstr')

    def test_exchange_delete_has_if_unused(self):
        self.assertEqual(specification.Exchange.Delete.type('if_unused'), 'bit')

    def test_exchange_delete_has_nowait(self):
        self.assertEqual(specification.Exchange.Delete.type('nowait'), 'bit')

    def test_exchange_unbind_has_ticket(self):
        self.assertEqual(specification.Exchange.Unbind.type('ticket'), 'short')

    def test_exchange_unbind_has_destination(self):
        self.assertEqual(specification.Exchange.Unbind.type('destination'),
                         'shortstr')

    def test_exchange_unbind_has_source(self):
        self.assertEqual(specification.Exchange.Unbind.type('source'),
                         'shortstr')

    def test_exchange_unbind_has_routing_key(self):
        self.assertEqual(specification.Exchange.Unbind.type('routing_key'),
                         'shortstr')

    def test_exchange_unbind_has_nowait(self):
        self.assertEqual(specification.Exchange.Unbind.type('nowait'), 'bit')

    def test_exchange_unbind_has_arguments(self):
        self.assertEqual(specification.Exchange.Unbind.type('arguments'),
                         'table')

    def test_queue_bind_has_ticket(self):
        self.assertEqual(specification.Queue.Bind.type('ticket'), 'short')

    def test_queue_bind_has_queue(self):
        self.assertEqual(specification.Queue.Bind.type('queue'), 'shortstr')

    def test_queue_bind_has_exchange(self):
        self.assertEqual(specification.Queue.Bind.type('exchange'), 'shortstr')

    def test_queue_bind_has_routing_key(self):
        self.assertEqual(specification.Queue.Bind.type('routing_key'),
                         'shortstr')

    def test_queue_bind_has_nowait(self):
        self.assertEqual(specification.Queue.Bind.type('nowait'), 'bit')

    def test_queue_bind_has_arguments(self):
        self.assertEqual(specification.Queue.Bind.type('arguments'), 'table')

    def test_queue_declare_has_ticket(self):
        self.assertEqual(specification.Queue.Declare.type('ticket'), 'short')

    def test_queue_declare_has_queue(self):
        self.assertEqual(specification.Queue.Declare.type('queue'), 'shortstr')

    def test_queue_declare_has_passive(self):
        self.assertEqual(specification.Queue.Declare.type('passive'), 'bit')

    def test_queue_declare_has_durable(self):
        self.assertEqual(specification.Queue.Declare.type('durable'), 'bit')

    def test_queue_declare_has_exclusive(self):
        self.assertEqual(specification.Queue.Declare.type('exclusive'), 'bit')

    def test_queue_declare_has_auto_delete(self):
        self.assertEqual(specification.Queue.Declare.type('auto_delete'), 'bit')

    def test_queue_declare_has_nowait(self):
        self.assertEqual(specification.Queue.Declare.type('nowait'), 'bit')

    def test_queue_declare_has_arguments(self):
        self.assertEqual(specification.Queue.Declare.type('arguments'), 'table')

    def test_queue_declareok_has_queue(self):
        self.assertEqual(specification.Queue.DeclareOk.type('queue'),
                         'shortstr')

    def test_queue_declareok_has_message_count(self):
        self.assertEqual(specification.Queue.DeclareOk.type('message_count'),
                         'long')

    def test_queue_declareok_has_consumer_count(self):
        self.assertEqual(specification.Queue.DeclareOk.type('consumer_count'),
                         'long')

    def test_queue_delete_has_ticket(self):
        self.assertEqual(specification.Queue.Delete.type('ticket'), 'short')

    def test_queue_delete_has_queue(self):
        self.assertEqual(specification.Queue.Delete.type('queue'), 'shortstr')

    def test_queue_delete_has_if_unused(self):
        self.assertEqual(specification.Queue.Delete.type('if_unused'), 'bit')

    def test_queue_delete_has_if_empty(self):
        self.assertEqual(specification.Queue.Delete.type('if_empty'), 'bit')

    def test_queue_delete_has_nowait(self):
        self.assertEqual(specification.Queue.Delete.type('nowait'), 'bit')

    def test_queue_deleteok_has_message_count(self):
        self.assertEqual(specification.Queue.DeleteOk.type('message_count'),
                         'long')

    def test_queue_purge_has_ticket(self):
        self.assertEqual(specification.Queue.Purge.type('ticket'), 'short')

    def test_queue_purge_has_queue(self):
        self.assertEqual(specification.Queue.Purge.type('queue'), 'shortstr')

    def test_queue_purge_has_nowait(self):
        self.assertEqual(specification.Queue.Purge.type('nowait'), 'bit')

    def test_queue_purgeok_has_message_count(self):
        self.assertEqual(specification.Queue.PurgeOk.type('message_count'),
                         'long')

    def test_queue_unbind_has_ticket(self):
        self.assertEqual(specification.Queue.Unbind.type('ticket'), 'short')

    def test_queue_unbind_has_queue(self):
        self.assertEqual(specification.Queue.Unbind.type('queue'), 'shortstr')

    def test_queue_unbind_has_exchange(self):
        self.assertEqual(specification.Queue.Unbind.type('exchange'),
                         'shortstr')

    def test_queue_unbind_has_routing_key(self):
        self.assertEqual(specification.Queue.Unbind.type('routing_key'),
                         'shortstr')

    def test_queue_unbind_has_arguments(self):
        self.assertEqual(specification.Queue.Unbind.type('arguments'), 'table')


class AttributeInMethodTests(unittest.TestCase):

    def test_basic_ack_has_delivery_tag(self):
        self.assertIn('delivery_tag', specification.Basic.Ack())

    def test_basic_ack_has_multiple(self):
        self.assertIn('multiple', specification.Basic.Ack())

    def test_basic_cancel_has_consumer_tag(self):
        self.assertIn('consumer_tag', specification.Basic.Cancel())

    def test_basic_cancel_has_nowait(self):
        self.assertIn('nowait', specification.Basic.Cancel())

    def test_basic_cancelok_has_consumer_tag(self):
        self.assertIn('consumer_tag', specification.Basic.CancelOk())

    def test_basic_consume_has_ticket(self):
        self.assertIn('ticket', specification.Basic.Consume())

    def test_basic_consume_has_queue(self):
        self.assertIn('queue', specification.Basic.Consume())

    def test_basic_consume_has_consumer_tag(self):
        self.assertIn('consumer_tag', specification.Basic.Consume())

    def test_basic_consume_has_no_local(self):
        self.assertIn('no_local', specification.Basic.Consume())

    def test_basic_consume_has_no_ack(self):
        self.assertIn('no_ack', specification.Basic.Consume())

    def test_basic_consume_has_exclusive(self):
        self.assertIn('exclusive', specification.Basic.Consume())

    def test_basic_consume_has_nowait(self):
        self.assertIn('nowait', specification.Basic.Consume())

    def test_basic_consume_has_arguments(self):
        self.assertIn('arguments', specification.Basic.Consume())

    def test_basic_consumeok_has_consumer_tag(self):
        self.assertIn('consumer_tag', specification.Basic.ConsumeOk())

    def test_basic_deliver_has_consumer_tag(self):
        self.assertIn('consumer_tag', specification.Basic.Deliver())

    def test_basic_deliver_has_delivery_tag(self):
        self.assertIn('delivery_tag', specification.Basic.Deliver())

    def test_basic_deliver_has_redelivered(self):
        self.assertIn('redelivered', specification.Basic.Deliver())

    def test_basic_deliver_has_exchange(self):
        self.assertIn('exchange', specification.Basic.Deliver())

    def test_basic_deliver_has_routing_key(self):
        self.assertIn('routing_key', specification.Basic.Deliver())

    def test_basic_get_has_ticket(self):
        self.assertIn('ticket', specification.Basic.Get())

    def test_basic_get_has_queue(self):
        self.assertIn('queue', specification.Basic.Get())

    def test_basic_get_has_no_ack(self):
        self.assertIn('no_ack', specification.Basic.Get())

    def test_basic_getempty_has_cluster_id(self):
        self.assertIn('cluster_id', specification.Basic.GetEmpty())

    def test_basic_getok_has_delivery_tag(self):
        self.assertIn('delivery_tag', specification.Basic.GetOk())

    def test_basic_getok_has_redelivered(self):
        self.assertIn('redelivered', specification.Basic.GetOk())

    def test_basic_getok_has_exchange(self):
        self.assertIn('exchange', specification.Basic.GetOk())

    def test_basic_getok_has_routing_key(self):
        self.assertIn('routing_key', specification.Basic.GetOk())

    def test_basic_getok_has_message_count(self):
        self.assertIn('message_count', specification.Basic.GetOk())

    def test_basic_nack_has_delivery_tag(self):
        self.assertIn('delivery_tag', specification.Basic.Nack())

    def test_basic_nack_has_multiple(self):
        self.assertIn('multiple', specification.Basic.Nack())

    def test_basic_nack_has_requeue(self):
        self.assertIn('requeue', specification.Basic.Nack())

    def test_basic_publish_has_ticket(self):
        self.assertIn('ticket', specification.Basic.Publish())

    def test_basic_publish_has_exchange(self):
        self.assertIn('exchange', specification.Basic.Publish())

    def test_basic_publish_has_routing_key(self):
        self.assertIn('routing_key', specification.Basic.Publish())

    def test_basic_publish_has_mandatory(self):
        self.assertIn('mandatory', specification.Basic.Publish())

    def test_basic_publish_has_immediate(self):
        self.assertIn('immediate', specification.Basic.Publish())

    def test_basic_qos_has_prefetch_size(self):
        self.assertIn('prefetch_size', specification.Basic.Qos())

    def test_basic_qos_has_prefetch_count(self):
        self.assertIn('prefetch_count', specification.Basic.Qos())

    def test_basic_qos_has_global_(self):
        self.assertIn('global_', specification.Basic.Qos())

    def test_basic_recover_has_requeue(self):
        self.assertIn('requeue', specification.Basic.Recover())

    def test_basic_reject_has_delivery_tag(self):
        self.assertIn('delivery_tag', specification.Basic.Reject())

    def test_basic_reject_has_requeue(self):
        self.assertIn('requeue', specification.Basic.Reject())

    def test_basic_return_has_reply_code(self):
        self.assertIn('reply_code', specification.Basic.Return())

    def test_basic_return_has_reply_text(self):
        self.assertIn('reply_text', specification.Basic.Return())

    def test_basic_return_has_exchange(self):
        self.assertIn('exchange', specification.Basic.Return())

    def test_basic_return_has_routing_key(self):
        self.assertIn('routing_key', specification.Basic.Return())

    def test_channel_close_has_reply_code(self):
        self.assertIn('reply_code', specification.Channel.Close())

    def test_channel_close_has_reply_text(self):
        self.assertIn('reply_text', specification.Channel.Close())

    def test_channel_close_has_class_id(self):
        self.assertIn('class_id', specification.Channel.Close())

    def test_channel_close_has_method_id(self):
        self.assertIn('method_id', specification.Channel.Close())

    def test_channel_flow_has_active(self):
        self.assertIn('active', specification.Channel.Flow())

    def test_channel_flowok_has_active(self):
        self.assertIn('active', specification.Channel.FlowOk())

    def test_channel_open_has_out_of_band(self):
        self.assertIn('out_of_band', specification.Channel.Open())

    def test_channel_openok_has_channel_id(self):
        self.assertIn('channel_id', specification.Channel.OpenOk())

    def test_confirm_select_has_nowait(self):
        self.assertIn('nowait', specification.Confirm.Select())

    def test_connection_blocked_has_reason(self):
        self.assertIn('reason', specification.Connection.Blocked())

    def test_connection_close_has_reply_code(self):
        self.assertIn('reply_code', specification.Connection.Close())

    def test_connection_close_has_reply_text(self):
        self.assertIn('reply_text', specification.Connection.Close())

    def test_connection_close_has_class_id(self):
        self.assertIn('class_id', specification.Connection.Close())

    def test_connection_close_has_method_id(self):
        self.assertIn('method_id', specification.Connection.Close())

    def test_connection_open_has_virtual_host(self):
        self.assertIn('virtual_host', specification.Connection.Open())

    def test_connection_open_has_capabilities(self):
        self.assertIn('capabilities', specification.Connection.Open())

    def test_connection_open_has_insist(self):
        self.assertIn('insist', specification.Connection.Open())

    def test_connection_openok_has_known_hosts(self):
        self.assertIn('known_hosts', specification.Connection.OpenOk())

    def test_connection_secure_has_challenge(self):
        self.assertIn('challenge', specification.Connection.Secure())

    def test_connection_secureok_has_response(self):
        self.assertIn('response', specification.Connection.SecureOk())

    def test_connection_start_has_version_major(self):
        self.assertIn('version_major', specification.Connection.Start())

    def test_connection_start_has_version_minor(self):
        self.assertIn('version_minor', specification.Connection.Start())

    def test_connection_start_has_server_properties(self):
        self.assertIn('server_properties', specification.Connection.Start())

    def test_connection_start_has_mechanisms(self):
        self.assertIn('mechanisms', specification.Connection.Start())

    def test_connection_start_has_locales(self):
        self.assertIn('locales', specification.Connection.Start())

    def test_connection_startok_has_mechanism(self):
        self.assertIn('mechanism', specification.Connection.StartOk())

    def test_connection_startok_has_response(self):
        self.assertIn('response', specification.Connection.StartOk())

    def test_connection_startok_has_locale(self):
        self.assertIn('locale', specification.Connection.StartOk())

    def test_connection_tune_has_channel_max(self):
        self.assertIn('channel_max', specification.Connection.Tune())

    def test_connection_tune_has_frame_max(self):
        self.assertIn('frame_max', specification.Connection.Tune())

    def test_connection_tune_has_heartbeat(self):
        self.assertIn('heartbeat', specification.Connection.Tune())

    def test_connection_tuneok_has_channel_max(self):
        self.assertIn('channel_max', specification.Connection.TuneOk())

    def test_connection_tuneok_has_frame_max(self):
        self.assertIn('frame_max', specification.Connection.TuneOk())

    def test_connection_tuneok_has_heartbeat(self):
        self.assertIn('heartbeat', specification.Connection.TuneOk())

    def test_exchange_bind_has_ticket(self):
        self.assertIn('ticket', specification.Exchange.Bind())

    def test_exchange_bind_has_destination(self):
        self.assertIn('destination', specification.Exchange.Bind())

    def test_exchange_bind_has_source(self):
        self.assertIn('source', specification.Exchange.Bind())

    def test_exchange_bind_has_routing_key(self):
        self.assertIn('routing_key', specification.Exchange.Bind())

    def test_exchange_bind_has_nowait(self):
        self.assertIn('nowait', specification.Exchange.Bind())

    def test_exchange_bind_has_arguments(self):
        self.assertIn('arguments', specification.Exchange.Bind())

    def test_exchange_declare_has_ticket(self):
        self.assertIn('ticket', specification.Exchange.Declare())

    def test_exchange_declare_has_exchange(self):
        self.assertIn('exchange', specification.Exchange.Declare())

    def test_exchange_declare_has_exchange_type(self):
        self.assertIn('exchange_type', specification.Exchange.Declare())

    def test_exchange_declare_has_passive(self):
        self.assertIn('passive', specification.Exchange.Declare())

    def test_exchange_declare_has_durable(self):
        self.assertIn('durable', specification.Exchange.Declare())

    def test_exchange_declare_has_auto_delete(self):
        self.assertIn('auto_delete', specification.Exchange.Declare())

    def test_exchange_declare_has_internal(self):
        self.assertIn('internal', specification.Exchange.Declare())

    def test_exchange_declare_has_nowait(self):
        self.assertIn('nowait', specification.Exchange.Declare())

    def test_exchange_declare_has_arguments(self):
        self.assertIn('arguments', specification.Exchange.Declare())

    def test_exchange_delete_has_ticket(self):
        self.assertIn('ticket', specification.Exchange.Delete())

    def test_exchange_delete_has_exchange(self):
        self.assertIn('exchange', specification.Exchange.Delete())

    def test_exchange_delete_has_if_unused(self):
        self.assertIn('if_unused', specification.Exchange.Delete())

    def test_exchange_delete_has_nowait(self):
        self.assertIn('nowait', specification.Exchange.Delete())

    def test_exchange_unbind_has_ticket(self):
        self.assertIn('ticket', specification.Exchange.Unbind())

    def test_exchange_unbind_has_destination(self):
        self.assertIn('destination', specification.Exchange.Unbind())

    def test_exchange_unbind_has_source(self):
        self.assertIn('source', specification.Exchange.Unbind())

    def test_exchange_unbind_has_routing_key(self):
        self.assertIn('routing_key', specification.Exchange.Unbind())

    def test_exchange_unbind_has_nowait(self):
        self.assertIn('nowait', specification.Exchange.Unbind())

    def test_exchange_unbind_has_arguments(self):
        self.assertIn('arguments', specification.Exchange.Unbind())

    def test_queue_bind_has_ticket(self):
        self.assertIn('ticket', specification.Queue.Bind())

    def test_queue_bind_has_queue(self):
        self.assertIn('queue', specification.Queue.Bind())

    def test_queue_bind_has_exchange(self):
        self.assertIn('exchange', specification.Queue.Bind())

    def test_queue_bind_has_routing_key(self):
        self.assertIn('routing_key', specification.Queue.Bind())

    def test_queue_bind_has_nowait(self):
        self.assertIn('nowait', specification.Queue.Bind())

    def test_queue_bind_has_arguments(self):
        self.assertIn('arguments', specification.Queue.Bind())

    def test_queue_declare_has_ticket(self):
        self.assertIn('ticket', specification.Queue.Declare())

    def test_queue_declare_has_queue(self):
        self.assertIn('queue', specification.Queue.Declare())

    def test_queue_declare_has_passive(self):
        self.assertIn('passive', specification.Queue.Declare())

    def test_queue_declare_has_durable(self):
        self.assertIn('durable', specification.Queue.Declare())

    def test_queue_declare_has_exclusive(self):
        self.assertIn('exclusive', specification.Queue.Declare())

    def test_queue_declare_has_auto_delete(self):
        self.assertIn('auto_delete', specification.Queue.Declare())

    def test_queue_declare_has_nowait(self):
        self.assertIn('nowait', specification.Queue.Declare())

    def test_queue_declare_has_arguments(self):
        self.assertIn('arguments', specification.Queue.Declare())

    def test_queue_declareok_has_queue(self):
        self.assertIn('queue', specification.Queue.DeclareOk())

    def test_queue_declareok_has_message_count(self):
        self.assertIn('message_count', specification.Queue.DeclareOk())

    def test_queue_declareok_has_consumer_count(self):
        self.assertIn('consumer_count', specification.Queue.DeclareOk())

    def test_queue_delete_has_ticket(self):
        self.assertIn('ticket', specification.Queue.Delete())

    def test_queue_delete_has_queue(self):
        self.assertIn('queue', specification.Queue.Delete())

    def test_queue_delete_has_if_unused(self):
        self.assertIn('if_unused', specification.Queue.Delete())

    def test_queue_delete_has_if_empty(self):
        self.assertIn('if_empty', specification.Queue.Delete())

    def test_queue_delete_has_nowait(self):
        self.assertIn('nowait', specification.Queue.Delete())

    def test_queue_deleteok_has_message_count(self):
        self.assertIn('message_count', specification.Queue.DeleteOk())

    def test_queue_purge_has_ticket(self):
        self.assertIn('ticket', specification.Queue.Purge())

    def test_queue_purge_has_queue(self):
        self.assertIn('queue', specification.Queue.Purge())

    def test_queue_purge_has_nowait(self):
        self.assertIn('nowait', specification.Queue.Purge())

    def test_queue_purgeok_has_message_count(self):
        self.assertIn('message_count', specification.Queue.PurgeOk())

    def test_queue_unbind_has_ticket(self):
        self.assertIn('ticket', specification.Queue.Unbind())

    def test_queue_unbind_has_queue(self):
        self.assertIn('queue', specification.Queue.Unbind())

    def test_queue_unbind_has_exchange(self):
        self.assertIn('exchange', specification.Queue.Unbind())

    def test_queue_unbind_has_routing_key(self):
        self.assertIn('routing_key', specification.Queue.Unbind())

    def test_queue_unbind_has_arguments(self):
        self.assertIn('arguments', specification.Queue.Unbind())


class DeprecationWarningTests(unittest.TestCase):
    def test_basic_recoverasync_raises_deprecation_error(self):
        self.assertRaises(DeprecationWarning, specification.Basic.RecoverAsync)


class BasicPropertiesTests(unittest.TestCase):
    def test_basic_properties_has_content_type(self):
        self.assertEqual(specification.Basic.Properties.type('content_type'),
                         'shortstr')

    def test_basic_properties_has_content_encoding(self):
        self.assertEqual(
            specification.Basic.Properties.type('content_encoding'), 'shortstr')

    def test_basic_properties_has_headers(self):
        self.assertEqual(specification.Basic.Properties.type('headers'),
                         'table')

    def test_basic_properties_has_delivery_mode(self):
        self.assertEqual(specification.Basic.Properties.type('delivery_mode'),
                         'octet')

    def test_basic_properties_has_priority(self):
        self.assertEqual(specification.Basic.Properties.type('priority'),
                         'octet')

    def test_basic_properties_has_correlation_id(self):
        self.assertEqual(specification.Basic.Properties.type('correlation_id'),
                         'shortstr')

    def test_basic_properties_has_reply_to(self):
        self.assertEqual(specification.Basic.Properties.type('reply_to'),
                         'shortstr')

    def test_basic_properties_has_expiration(self):
        self.assertEqual(specification.Basic.Properties.type('expiration'),
                         'shortstr')

    def test_basic_properties_has_message_id(self):
        self.assertEqual(specification.Basic.Properties.type('message_id'),
                         'shortstr')

    def test_basic_properties_has_timestamp(self):
        self.assertEqual(specification.Basic.Properties.type('timestamp'),
                         'timestamp')

    def test_basic_properties_has_message_type(self):
        self.assertEqual(specification.Basic.Properties.type('message_type'),
                         'shortstr')

    def test_basic_properties_has_user_id(self):
        self.assertEqual(specification.Basic.Properties.type('user_id'),
                         'shortstr')

    def test_basic_properties_has_app_id(self):
        self.assertEqual(specification.Basic.Properties.type('app_id'),
                         'shortstr')

    def test_basic_properties_has_cluster_id(self):
        self.assertEqual(specification.Basic.Properties.type('cluster_id'),
                         'shortstr')


class MethodAttributeLengthTests(unittest.TestCase):

    def test_basic_ack_attribute_count(self):
        self.assertEqual(len(specification.Basic.Ack()), 2)

    def test_basic_cancel_attribute_count(self):
        self.assertEqual(len(specification.Basic.Cancel()), 2)

    def test_basic_cancelok_attribute_count(self):
        self.assertEqual(len(specification.Basic.CancelOk()), 1)

    def test_basic_consume_attribute_count(self):
        self.assertEqual(len(specification.Basic.Consume()), 8)

    def test_basic_consumeok_attribute_count(self):
        self.assertEqual(len(specification.Basic.ConsumeOk()), 1)

    def test_basic_deliver_attribute_count(self):
        self.assertEqual(len(specification.Basic.Deliver()), 5)

    def test_basic_get_attribute_count(self):
        self.assertEqual(len(specification.Basic.Get()), 3)

    def test_basic_getempty_attribute_count(self):
        self.assertEqual(len(specification.Basic.GetEmpty()), 1)

    def test_basic_getok_attribute_count(self):
        self.assertEqual(len(specification.Basic.GetOk()), 5)

    def test_basic_nack_attribute_count(self):
        self.assertEqual(len(specification.Basic.Nack()), 3)

    def test_basic_publish_attribute_count(self):
        self.assertEqual(len(specification.Basic.Publish()), 5)

    def test_basic_qos_attribute_count(self):
        self.assertEqual(len(specification.Basic.Qos()), 3)

    def test_basic_qosok_attribute_count(self):
        self.assertEqual(len(specification.Basic.QosOk()), 0)

    def test_basic_recover_attribute_count(self):
        self.assertEqual(len(specification.Basic.Recover()), 1)

    def test_basic_recoverok_attribute_count(self):
        self.assertEqual(len(specification.Basic.RecoverOk()), 0)

    def test_basic_reject_attribute_count(self):
        self.assertEqual(len(specification.Basic.Reject()), 2)

    def test_basic_return_attribute_count(self):
        self.assertEqual(len(specification.Basic.Return()), 4)

    def test_channel_close_attribute_count(self):
        self.assertEqual(len(specification.Channel.Close()), 4)

    def test_channel_closeok_attribute_count(self):
        self.assertEqual(len(specification.Channel.CloseOk()), 0)

    def test_channel_flow_attribute_count(self):
        self.assertEqual(len(specification.Channel.Flow()), 1)

    def test_channel_flowok_attribute_count(self):
        self.assertEqual(len(specification.Channel.FlowOk()), 1)

    def test_channel_open_attribute_count(self):
        self.assertEqual(len(specification.Channel.Open()), 1)

    def test_channel_openok_attribute_count(self):
        self.assertEqual(len(specification.Channel.OpenOk()), 1)

    def test_confirm_select_attribute_count(self):
        self.assertEqual(len(specification.Confirm.Select()), 1)

    def test_confirm_selectok_attribute_count(self):
        self.assertEqual(len(specification.Confirm.SelectOk()), 0)

    def test_connection_blocked_attribute_count(self):
        self.assertEqual(len(specification.Connection.Blocked()), 1)

    def test_connection_close_attribute_count(self):
        self.assertEqual(len(specification.Connection.Close()), 4)

    def test_connection_closeok_attribute_count(self):
        self.assertEqual(len(specification.Connection.CloseOk()), 0)

    def test_connection_open_attribute_count(self):
        self.assertEqual(len(specification.Connection.Open()), 3)

    def test_connection_openok_attribute_count(self):
        self.assertEqual(len(specification.Connection.OpenOk()), 1)

    def test_connection_secure_attribute_count(self):
        self.assertEqual(len(specification.Connection.Secure()), 1)

    def test_connection_secureok_attribute_count(self):
        self.assertEqual(len(specification.Connection.SecureOk()), 1)

    def test_connection_start_attribute_count(self):
        self.assertEqual(len(specification.Connection.Start()), 5)

    def test_connection_startok_attribute_count(self):
        self.assertEqual(len(specification.Connection.StartOk()), 4)

    def test_connection_tune_attribute_count(self):
        self.assertEqual(len(specification.Connection.Tune()), 3)

    def test_connection_tuneok_attribute_count(self):
        self.assertEqual(len(specification.Connection.TuneOk()), 3)

    def test_connection_unblocked_attribute_count(self):
        self.assertEqual(len(specification.Connection.Unblocked()), 0)

    def test_exchange_bind_attribute_count(self):
        self.assertEqual(len(specification.Exchange.Bind()), 6)

    def test_exchange_bindok_attribute_count(self):
        self.assertEqual(len(specification.Exchange.BindOk()), 0)

    def test_exchange_declare_attribute_count(self):
        self.assertEqual(len(specification.Exchange.Declare()), 9)

    def test_exchange_declareok_attribute_count(self):
        self.assertEqual(len(specification.Exchange.DeclareOk()), 0)

    def test_exchange_delete_attribute_count(self):
        self.assertEqual(len(specification.Exchange.Delete()), 4)

    def test_exchange_deleteok_attribute_count(self):
        self.assertEqual(len(specification.Exchange.DeleteOk()), 0)

    def test_exchange_unbind_attribute_count(self):
        self.assertEqual(len(specification.Exchange.Unbind()), 6)

    def test_exchange_unbindok_attribute_count(self):
        self.assertEqual(len(specification.Exchange.UnbindOk()), 0)

    def test_queue_bind_attribute_count(self):
        self.assertEqual(len(specification.Queue.Bind()), 6)

    def test_queue_bindok_attribute_count(self):
        self.assertEqual(len(specification.Queue.BindOk()), 0)

    def test_queue_declare_attribute_count(self):
        self.assertEqual(len(specification.Queue.Declare()), 8)

    def test_queue_declareok_attribute_count(self):
        self.assertEqual(len(specification.Queue.DeclareOk()), 3)

    def test_queue_delete_attribute_count(self):
        self.assertEqual(len(specification.Queue.Delete()), 5)

    def test_queue_deleteok_attribute_count(self):
        self.assertEqual(len(specification.Queue.DeleteOk()), 1)

    def test_queue_purge_attribute_count(self):
        self.assertEqual(len(specification.Queue.Purge()), 3)

    def test_queue_purgeok_attribute_count(self):
        self.assertEqual(len(specification.Queue.PurgeOk()), 1)

    def test_queue_unbind_attribute_count(self):
        self.assertEqual(len(specification.Queue.Unbind()), 5)

    def test_queue_unbindok_attribute_count(self):
        self.assertEqual(len(specification.Queue.UnbindOk()), 0)

    def test_tx_commit_attribute_count(self):
        self.assertEqual(len(specification.Tx.Commit()), 0)

    def test_tx_commitok_attribute_count(self):
        self.assertEqual(len(specification.Tx.CommitOk()), 0)

    def test_tx_rollback_attribute_count(self):
        self.assertEqual(len(specification.Tx.Rollback()), 0)

    def test_tx_rollbackok_attribute_count(self):
        self.assertEqual(len(specification.Tx.RollbackOk()), 0)

    def test_tx_select_attribute_count(self):
        self.assertEqual(len(specification.Tx.Select()), 0)

    def test_tx_selectok_attribute_count(self):
        self.assertEqual(len(specification.Tx.SelectOk()), 0)


class MethodAttributeDefaultTests(unittest.TestCase):
    def test_basic_ack_default_for_delivery_tag(self):
        obj = specification.Basic.Ack()
        self.assertEqual(obj['delivery_tag'], 0)

    def test_basic_ack_default_for_multiple(self):
        obj = specification.Basic.Ack()
        self.assertEqual(obj['multiple'], False)

    def test_basic_cancel_default_for_consumer_tag(self):
        obj = specification.Basic.Cancel()
        self.assertEqual(obj['consumer_tag'], '')

    def test_basic_cancel_default_for_nowait(self):
        obj = specification.Basic.Cancel()
        self.assertEqual(obj['nowait'], False)

    def test_basic_cancelok_default_for_consumer_tag(self):
        obj = specification.Basic.CancelOk()
        self.assertEqual(obj['consumer_tag'], '')

    def test_basic_consume_default_for_ticket(self):
        obj = specification.Basic.Consume()
        self.assertEqual(obj['ticket'], 0)

    def test_basic_consume_default_for_queue(self):
        obj = specification.Basic.Consume()
        self.assertEqual(obj['queue'], '')

    def test_basic_consume_default_for_consumer_tag(self):
        obj = specification.Basic.Consume()
        self.assertEqual(obj['consumer_tag'], '')

    def test_basic_consume_default_for_no_local(self):
        obj = specification.Basic.Consume()
        self.assertEqual(obj['no_local'], False)

    def test_basic_consume_default_for_no_ack(self):
        obj = specification.Basic.Consume()
        self.assertEqual(obj['no_ack'], False)

    def test_basic_consume_default_for_exclusive(self):
        obj = specification.Basic.Consume()
        self.assertEqual(obj['exclusive'], False)

    def test_basic_consume_default_for_nowait(self):
        obj = specification.Basic.Consume()
        self.assertEqual(obj['nowait'], False)

    def test_basic_consume_default_for_arguments(self):
        obj = specification.Basic.Consume()
        self.assertDictEqual(obj['arguments'], {})

    def test_basic_consumeok_default_for_consumer_tag(self):
        obj = specification.Basic.ConsumeOk()
        self.assertEqual(obj['consumer_tag'], '')

    def test_basic_deliver_default_for_consumer_tag(self):
        obj = specification.Basic.Deliver()
        self.assertEqual(obj['consumer_tag'], '')

    def test_basic_deliver_default_for_delivery_tag(self):
        obj = specification.Basic.Deliver()
        self.assertEqual(obj['delivery_tag'], None)

    def test_basic_deliver_default_for_redelivered(self):
        obj = specification.Basic.Deliver()
        self.assertEqual(obj['redelivered'], False)

    def test_basic_deliver_default_for_exchange(self):
        obj = specification.Basic.Deliver()
        self.assertEqual(obj['exchange'], '')

    def test_basic_deliver_default_for_routing_key(self):
        obj = specification.Basic.Deliver()
        self.assertEqual(obj['routing_key'], '')

    def test_basic_get_default_for_ticket(self):
        obj = specification.Basic.Get()
        self.assertEqual(obj['ticket'], 0)

    def test_basic_get_default_for_queue(self):
        obj = specification.Basic.Get()
        self.assertEqual(obj['queue'], '')

    def test_basic_get_default_for_no_ack(self):
        obj = specification.Basic.Get()
        self.assertEqual(obj['no_ack'], False)

    def test_basic_getempty_default_for_cluster_id(self):
        obj = specification.Basic.GetEmpty()
        self.assertEqual(obj['cluster_id'], '')

    def test_basic_getok_default_for_delivery_tag(self):
        obj = specification.Basic.GetOk()
        self.assertEqual(obj['delivery_tag'], None)

    def test_basic_getok_default_for_redelivered(self):
        obj = specification.Basic.GetOk()
        self.assertEqual(obj['redelivered'], False)

    def test_basic_getok_default_for_exchange(self):
        obj = specification.Basic.GetOk()
        self.assertEqual(obj['exchange'], '')

    def test_basic_getok_default_for_routing_key(self):
        obj = specification.Basic.GetOk()
        self.assertEqual(obj['routing_key'], '')

    def test_basic_getok_default_for_message_count(self):
        obj = specification.Basic.GetOk()
        self.assertEqual(obj['message_count'], 0)

    def test_basic_nack_default_for_delivery_tag(self):
        obj = specification.Basic.Nack()
        self.assertEqual(obj['delivery_tag'], 0)

    def test_basic_nack_default_for_multiple(self):
        obj = specification.Basic.Nack()
        self.assertEqual(obj['multiple'], False)

    def test_basic_nack_default_for_requeue(self):
        obj = specification.Basic.Nack()
        self.assertEqual(obj['requeue'], True)

    def test_basic_publish_default_for_ticket(self):
        obj = specification.Basic.Publish()
        self.assertEqual(obj['ticket'], 0)

    def test_basic_publish_default_for_exchange(self):
        obj = specification.Basic.Publish()
        self.assertEqual(obj['exchange'], '')

    def test_basic_publish_default_for_routing_key(self):
        obj = specification.Basic.Publish()
        self.assertEqual(obj['routing_key'], '')

    def test_basic_publish_default_for_mandatory(self):
        obj = specification.Basic.Publish()
        self.assertEqual(obj['mandatory'], False)

    def test_basic_publish_default_for_immediate(self):
        obj = specification.Basic.Publish()
        self.assertEqual(obj['immediate'], False)

    def test_basic_qos_default_for_prefetch_size(self):
        obj = specification.Basic.Qos()
        self.assertEqual(obj['prefetch_size'], 0)

    def test_basic_qos_default_for_prefetch_count(self):
        obj = specification.Basic.Qos()
        self.assertEqual(obj['prefetch_count'], 0)

    def test_basic_qos_default_for_global_(self):
        obj = specification.Basic.Qos()
        self.assertEqual(obj['global_'], False)

    def test_basic_recover_default_for_requeue(self):
        obj = specification.Basic.Recover()
        self.assertEqual(obj['requeue'], False)

    def test_basic_reject_default_for_delivery_tag(self):
        obj = specification.Basic.Reject()
        self.assertEqual(obj['delivery_tag'], None)

    def test_basic_reject_default_for_requeue(self):
        obj = specification.Basic.Reject()
        self.assertEqual(obj['requeue'], True)

    def test_basic_return_default_for_reply_code(self):
        obj = specification.Basic.Return()
        self.assertEqual(obj['reply_code'], 0)

    def test_basic_return_default_for_reply_text(self):
        obj = specification.Basic.Return()
        self.assertEqual(obj['reply_text'], '')

    def test_basic_return_default_for_exchange(self):
        obj = specification.Basic.Return()
        self.assertEqual(obj['exchange'], '')

    def test_basic_return_default_for_routing_key(self):
        obj = specification.Basic.Return()
        self.assertEqual(obj['routing_key'], '')

    def test_channel_close_default_for_reply_code(self):
        obj = specification.Channel.Close()
        self.assertEqual(obj['reply_code'], 0)

    def test_channel_close_default_for_reply_text(self):
        obj = specification.Channel.Close()
        self.assertEqual(obj['reply_text'], '')

    def test_channel_close_default_for_class_id(self):
        obj = specification.Channel.Close()
        self.assertEqual(obj['class_id'], 0)

    def test_channel_close_default_for_method_id(self):
        obj = specification.Channel.Close()
        self.assertEqual(obj['method_id'], 0)

    def test_channel_flow_default_for_active(self):
        obj = specification.Channel.Flow()
        self.assertEqual(obj['active'], None)

    def test_channel_flowok_default_for_active(self):
        obj = specification.Channel.FlowOk()
        self.assertEqual(obj['active'], None)

    def test_channel_open_default_for_out_of_band(self):
        obj = specification.Channel.Open()
        self.assertEqual(obj['out_of_band'], '')

    def test_channel_openok_default_for_channel_id(self):
        obj = specification.Channel.OpenOk()
        self.assertEqual(obj['channel_id'], '')

    def test_confirm_select_default_for_nowait(self):
        obj = specification.Confirm.Select()
        self.assertEqual(obj['nowait'], False)

    def test_connection_blocked_default_for_reason(self):
        obj = specification.Connection.Blocked()
        self.assertEqual(obj['reason'], '')

    def test_connection_close_default_for_reply_code(self):
        obj = specification.Connection.Close()
        self.assertEqual(obj['reply_code'], 0)

    def test_connection_close_default_for_reply_text(self):
        obj = specification.Connection.Close()
        self.assertEqual(obj['reply_text'], '')

    def test_connection_close_default_for_class_id(self):
        obj = specification.Connection.Close()
        self.assertEqual(obj['class_id'], 0)

    def test_connection_close_default_for_method_id(self):
        obj = specification.Connection.Close()
        self.assertEqual(obj['method_id'], 0)

    def test_connection_open_default_for_virtual_host(self):
        obj = specification.Connection.Open()
        self.assertEqual(obj['virtual_host'], '/')

    def test_connection_open_default_for_capabilities(self):
        obj = specification.Connection.Open()
        self.assertEqual(obj['capabilities'], '')

    def test_connection_open_default_for_insist(self):
        obj = specification.Connection.Open()
        self.assertEqual(obj['insist'], False)

    def test_connection_openok_default_for_known_hosts(self):
        obj = specification.Connection.OpenOk()
        self.assertEqual(obj['known_hosts'], '')

    def test_connection_secure_default_for_challenge(self):
        obj = specification.Connection.Secure()
        self.assertEqual(obj['challenge'], '')

    def test_connection_secureok_default_for_response(self):
        obj = specification.Connection.SecureOk()
        self.assertEqual(obj['response'], '')

    def test_connection_start_default_for_version_major(self):
        obj = specification.Connection.Start()
        self.assertEqual(obj['version_major'], 0)

    def test_connection_start_default_for_version_minor(self):
        obj = specification.Connection.Start()
        self.assertEqual(obj['version_minor'], 9)

    def test_connection_start_default_for_mechanisms(self):
        obj = specification.Connection.Start()
        self.assertEqual(obj['mechanisms'], 'PLAIN')

    def test_connection_start_default_for_locales(self):
        obj = specification.Connection.Start()
        self.assertEqual(obj['locales'], 'en_US')

    def test_connection_startok_default_for_mechanism(self):
        obj = specification.Connection.StartOk()
        self.assertEqual(obj['mechanism'], 'PLAIN')

    def test_connection_startok_default_for_response(self):
        obj = specification.Connection.StartOk()
        self.assertEqual(obj['response'], '')

    def test_connection_startok_default_for_locale(self):
        obj = specification.Connection.StartOk()
        self.assertEqual(obj['locale'], 'en_US')

    def test_connection_tune_default_for_channel_max(self):
        obj = specification.Connection.Tune()
        self.assertEqual(obj['channel_max'], 0)

    def test_connection_tune_default_for_frame_max(self):
        obj = specification.Connection.Tune()
        self.assertEqual(obj['frame_max'], 0)

    def test_connection_tune_default_for_heartbeat(self):
        obj = specification.Connection.Tune()
        self.assertEqual(obj['heartbeat'], 0)

    def test_connection_tuneok_default_for_channel_max(self):
        obj = specification.Connection.TuneOk()
        self.assertEqual(obj['channel_max'], 0)

    def test_connection_tuneok_default_for_frame_max(self):
        obj = specification.Connection.TuneOk()
        self.assertEqual(obj['frame_max'], 0)

    def test_connection_tuneok_default_for_heartbeat(self):
        obj = specification.Connection.TuneOk()
        self.assertEqual(obj['heartbeat'], 0)

    def test_exchange_bind_default_for_ticket(self):
        obj = specification.Exchange.Bind()
        self.assertEqual(obj['ticket'], 0)

    def test_exchange_bind_default_for_destination(self):
        obj = specification.Exchange.Bind()
        self.assertEqual(obj['destination'], '')

    def test_exchange_bind_default_for_source(self):
        obj = specification.Exchange.Bind()
        self.assertEqual(obj['source'], '')

    def test_exchange_bind_default_for_routing_key(self):
        obj = specification.Exchange.Bind()
        self.assertEqual(obj['routing_key'], '')

    def test_exchange_bind_default_for_nowait(self):
        obj = specification.Exchange.Bind()
        self.assertEqual(obj['nowait'], False)

    def test_exchange_bind_default_for_arguments(self):
        obj = specification.Exchange.Bind()
        self.assertDictEqual(obj['arguments'], {})

    def test_exchange_declare_default_for_ticket(self):
        obj = specification.Exchange.Declare()
        self.assertEqual(obj['ticket'], 0)

    def test_exchange_declare_default_for_exchange(self):
        obj = specification.Exchange.Declare()
        self.assertEqual(obj['exchange'], '')

    def test_exchange_declare_default_for_exchange_type(self):
        obj = specification.Exchange.Declare()
        self.assertEqual(obj['exchange_type'], 'direct')

    def test_exchange_declare_default_for_passive(self):
        obj = specification.Exchange.Declare()
        self.assertEqual(obj['passive'], False)

    def test_exchange_declare_default_for_durable(self):
        obj = specification.Exchange.Declare()
        self.assertEqual(obj['durable'], False)

    def test_exchange_declare_default_for_auto_delete(self):
        obj = specification.Exchange.Declare()
        self.assertEqual(obj['auto_delete'], False)

    def test_exchange_declare_default_for_internal(self):
        obj = specification.Exchange.Declare()
        self.assertEqual(obj['internal'], False)

    def test_exchange_declare_default_for_nowait(self):
        obj = specification.Exchange.Declare()
        self.assertEqual(obj['nowait'], False)

    def test_exchange_declare_default_for_arguments(self):
        obj = specification.Exchange.Declare()
        self.assertDictEqual(obj['arguments'], {})

    def test_exchange_delete_default_for_ticket(self):
        obj = specification.Exchange.Delete()
        self.assertEqual(obj['ticket'], 0)

    def test_exchange_delete_default_for_exchange(self):
        obj = specification.Exchange.Delete()
        self.assertEqual(obj['exchange'], '')

    def test_exchange_delete_default_for_if_unused(self):
        obj = specification.Exchange.Delete()
        self.assertEqual(obj['if_unused'], False)

    def test_exchange_delete_default_for_nowait(self):
        obj = specification.Exchange.Delete()
        self.assertEqual(obj['nowait'], False)

    def test_exchange_unbind_default_for_ticket(self):
        obj = specification.Exchange.Unbind()
        self.assertEqual(obj['ticket'], 0)

    def test_exchange_unbind_default_for_destination(self):
        obj = specification.Exchange.Unbind()
        self.assertEqual(obj['destination'], '')

    def test_exchange_unbind_default_for_source(self):
        obj = specification.Exchange.Unbind()
        self.assertEqual(obj['source'], '')

    def test_exchange_unbind_default_for_routing_key(self):
        obj = specification.Exchange.Unbind()
        self.assertEqual(obj['routing_key'], '')

    def test_exchange_unbind_default_for_nowait(self):
        obj = specification.Exchange.Unbind()
        self.assertEqual(obj['nowait'], False)

    def test_exchange_unbind_default_for_arguments(self):
        obj = specification.Exchange.Unbind()
        self.assertDictEqual(obj['arguments'], {})

    def test_queue_bind_default_for_ticket(self):
        obj = specification.Queue.Bind()
        self.assertEqual(obj['ticket'], 0)

    def test_queue_bind_default_for_queue(self):
        obj = specification.Queue.Bind()
        self.assertEqual(obj['queue'], '')

    def test_queue_bind_default_for_exchange(self):
        obj = specification.Queue.Bind()
        self.assertEqual(obj['exchange'], '')

    def test_queue_bind_default_for_routing_key(self):
        obj = specification.Queue.Bind()
        self.assertEqual(obj['routing_key'], '')

    def test_queue_bind_default_for_nowait(self):
        obj = specification.Queue.Bind()
        self.assertEqual(obj['nowait'], False)

    def test_queue_bind_default_for_arguments(self):
        obj = specification.Queue.Bind()
        self.assertDictEqual(obj['arguments'], {})

    def test_queue_declare_default_for_ticket(self):
        obj = specification.Queue.Declare()
        self.assertEqual(obj['ticket'], 0)

    def test_queue_declare_default_for_queue(self):
        obj = specification.Queue.Declare()
        self.assertEqual(obj['queue'], '')

    def test_queue_declare_default_for_passive(self):
        obj = specification.Queue.Declare()
        self.assertEqual(obj['passive'], False)

    def test_queue_declare_default_for_durable(self):
        obj = specification.Queue.Declare()
        self.assertEqual(obj['durable'], False)

    def test_queue_declare_default_for_exclusive(self):
        obj = specification.Queue.Declare()
        self.assertEqual(obj['exclusive'], False)

    def test_queue_declare_default_for_auto_delete(self):
        obj = specification.Queue.Declare()
        self.assertEqual(obj['auto_delete'], False)

    def test_queue_declare_default_for_nowait(self):
        obj = specification.Queue.Declare()
        self.assertEqual(obj['nowait'], False)

    def test_queue_declare_default_for_arguments(self):
        obj = specification.Queue.Declare()
        self.assertDictEqual(obj['arguments'], {})

    def test_queue_declareok_default_for_queue(self):
        obj = specification.Queue.DeclareOk()
        self.assertEqual(obj['queue'], '')

    def test_queue_declareok_default_for_message_count(self):
        obj = specification.Queue.DeclareOk()
        self.assertEqual(obj['message_count'], 0)

    def test_queue_declareok_default_for_consumer_count(self):
        obj = specification.Queue.DeclareOk()
        self.assertEqual(obj['consumer_count'], 0)

    def test_queue_delete_default_for_ticket(self):
        obj = specification.Queue.Delete()
        self.assertEqual(obj['ticket'], 0)

    def test_queue_delete_default_for_queue(self):
        obj = specification.Queue.Delete()
        self.assertEqual(obj['queue'], '')

    def test_queue_delete_default_for_if_unused(self):
        obj = specification.Queue.Delete()
        self.assertEqual(obj['if_unused'], False)

    def test_queue_delete_default_for_if_empty(self):
        obj = specification.Queue.Delete()
        self.assertEqual(obj['if_empty'], False)

    def test_queue_delete_default_for_nowait(self):
        obj = specification.Queue.Delete()
        self.assertEqual(obj['nowait'], False)

    def test_queue_deleteok_default_for_message_count(self):
        obj = specification.Queue.DeleteOk()
        self.assertEqual(obj['message_count'], 0)

    def test_queue_purge_default_for_ticket(self):
        obj = specification.Queue.Purge()
        self.assertEqual(obj['ticket'], 0)

    def test_queue_purge_default_for_queue(self):
        obj = specification.Queue.Purge()
        self.assertEqual(obj['queue'], '')

    def test_queue_purge_default_for_nowait(self):
        obj = specification.Queue.Purge()
        self.assertEqual(obj['nowait'], False)

    def test_queue_purgeok_default_for_message_count(self):
        obj = specification.Queue.PurgeOk()
        self.assertEqual(obj['message_count'], 0)

    def test_queue_unbind_default_for_ticket(self):
        obj = specification.Queue.Unbind()
        self.assertEqual(obj['ticket'], 0)

    def test_queue_unbind_default_for_queue(self):
        obj = specification.Queue.Unbind()
        self.assertEqual(obj['queue'], '')

    def test_queue_unbind_default_for_exchange(self):
        obj = specification.Queue.Unbind()
        self.assertEqual(obj['exchange'], '')

    def test_queue_unbind_default_for_routing_key(self):
        obj = specification.Queue.Unbind()
        self.assertEqual(obj['routing_key'], '')

    def test_queue_unbind_default_for_arguments(self):
        obj = specification.Queue.Unbind()
        self.assertDictEqual(obj['arguments'], {})
