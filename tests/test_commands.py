try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pamqp import commands


class ArgumentTypeTests(unittest.TestCase):
    def test_basic_ack_has_delivery_tag(self):
        self.assertEqual(commands.Basic.Ack.amqp_type('delivery_tag'),
                         'longlong')

    def test_basic_ack_has_multiple(self):
        self.assertEqual(commands.Basic.Ack.amqp_type('multiple'), 'bit')

    def test_basic_cancel_has_consumer_tag(self):
        self.assertEqual(commands.Basic.Cancel.amqp_type('consumer_tag'),
                         'shortstr')

    def test_basic_cancel_has_nowait(self):
        self.assertEqual(commands.Basic.Cancel.amqp_type('nowait'), 'bit')

    def test_basic_cancelok_has_consumer_tag(self):
        self.assertEqual(
            commands.Basic.CancelOk.amqp_type('consumer_tag'), 'shortstr')

    def test_basic_consume_has_ticket(self):
        self.assertEqual(commands.Basic.Consume.amqp_type('ticket'),
                         'short')

    def test_basic_consume_has_queue(self):
        self.assertEqual(commands.Basic.Consume.amqp_type('queue'),
                         'shortstr')

    def test_basic_consume_has_consumer_tag(self):
        self.assertEqual(commands.Basic.Consume.amqp_type('consumer_tag'),
                         'shortstr')

    def test_basic_consume_has_no_local(self):
        self.assertEqual(commands.Basic.Consume.amqp_type('no_local'),
                         'bit')

    def test_basic_consume_has_no_ack(self):
        self.assertEqual(commands.Basic.Consume.amqp_type('no_ack'),
                         'bit')

    def test_basic_consume_has_exclusive(self):
        self.assertEqual(commands.Basic.Consume.amqp_type('exclusive'),
                         'bit')

    def test_basic_consume_has_nowait(self):
        self.assertEqual(commands.Basic.Consume.amqp_type('nowait'),
                         'bit')

    def test_basic_consume_has_arguments(self):
        self.assertEqual(commands.Basic.Consume.amqp_type('arguments'),
                         'table')

    def test_basic_consumeok_has_consumer_tag(self):
        self.assertEqual(
            commands.Basic.ConsumeOk.amqp_type('consumer_tag'),
            'shortstr')

    def test_basic_deliver_has_consumer_tag(self):
        self.assertEqual(commands.Basic.Deliver.amqp_type('consumer_tag'),
                         'shortstr')

    def test_basic_deliver_has_delivery_tag(self):
        self.assertEqual(commands.Basic.Deliver.amqp_type('delivery_tag'),
                         'longlong')

    def test_basic_deliver_has_redelivered(self):
        self.assertEqual(commands.Basic.Deliver.amqp_type('redelivered'),
                         'bit')

    def test_basic_deliver_has_exchange(self):
        self.assertEqual(commands.Basic.Deliver.amqp_type('exchange'),
                         'shortstr')

    def test_basic_deliver_has_routing_key(self):
        self.assertEqual(commands.Basic.Deliver.amqp_type('routing_key'),
                         'shortstr')

    def test_basic_get_has_ticket(self):
        self.assertEqual(commands.Basic.Get.amqp_type('ticket'), 'short')

    def test_basic_get_has_queue(self):
        self.assertEqual(commands.Basic.Get.amqp_type('queue'),
                         'shortstr')

    def test_basic_get_has_no_ack(self):
        self.assertEqual(commands.Basic.Get.amqp_type('no_ack'), 'bit')

    def test_basic_getempty_has_cluster_id(self):
        self.assertEqual(commands.Basic.GetEmpty.amqp_type('cluster_id'),
                         'shortstr')

    def test_basic_getok_has_delivery_tag(self):
        self.assertEqual(commands.Basic.GetOk.amqp_type('delivery_tag'),
                         'longlong')

    def test_basic_getok_has_redelivered(self):
        self.assertEqual(commands.Basic.GetOk.amqp_type('redelivered'),
                         'bit')

    def test_basic_getok_has_exchange(self):
        self.assertEqual(commands.Basic.GetOk.amqp_type('exchange'),
                         'shortstr')

    def test_basic_getok_has_routing_key(self):
        self.assertEqual(commands.Basic.GetOk.amqp_type('routing_key'),
                         'shortstr')

    def test_basic_getok_has_message_count(self):
        self.assertEqual(commands.Basic.GetOk.amqp_type('message_count'),
                         'long')

    def test_basic_nack_has_delivery_tag(self):
        self.assertEqual(commands.Basic.Nack.amqp_type('delivery_tag'),
                         'longlong')

    def test_basic_nack_has_multiple(self):
        self.assertEqual(commands.Basic.Nack.amqp_type('multiple'), 'bit')

    def test_basic_nack_has_requeue(self):
        self.assertEqual(commands.Basic.Nack.amqp_type('requeue'), 'bit')

    def test_basic_publish_has_ticket(self):
        self.assertEqual(commands.Basic.Publish.amqp_type('ticket'),
                         'short')

    def test_basic_publish_has_exchange(self):
        self.assertEqual(commands.Basic.Publish.amqp_type('exchange'),
                         'shortstr')

    def test_basic_publish_has_routing_key(self):
        self.assertEqual(commands.Basic.Publish.amqp_type('routing_key'),
                         'shortstr')

    def test_basic_publish_has_mandatory(self):
        self.assertEqual(commands.Basic.Publish.amqp_type('mandatory'),
                         'bit')

    def test_basic_publish_has_immediate(self):
        self.assertEqual(commands.Basic.Publish.amqp_type('immediate'),
                         'bit')

    def test_basic_qos_has_prefetch_size(self):
        self.assertEqual(commands.Basic.Qos.amqp_type('prefetch_size'),
                         'long')

    def test_basic_qos_has_prefetch_count(self):
        self.assertEqual(commands.Basic.Qos.amqp_type('prefetch_count'),
                         'short')

    def test_basic_qos_has_global_(self):
        self.assertEqual(commands.Basic.Qos.amqp_type('global_'), 'bit')

    def test_basic_recover_has_requeue(self):
        self.assertEqual(commands.Basic.Recover.amqp_type('requeue'),
                         'bit')

    def test_basic_recoverasync_has_requeue(self):
        self.assertEqual(commands.Basic.RecoverAsync.amqp_type('requeue'),
                         'bit')

    def test_basic_reject_has_delivery_tag(self):
        self.assertEqual(commands.Basic.Reject.amqp_type('delivery_tag'),
                         'longlong')

    def test_basic_reject_has_requeue(self):
        self.assertEqual(commands.Basic.Reject.amqp_type('requeue'),
                         'bit')

    def test_basic_return_has_reply_code(self):
        self.assertEqual(commands.Basic.Return.amqp_type('reply_code'),
                         'short')

    def test_basic_return_has_reply_text(self):
        self.assertEqual(commands.Basic.Return.amqp_type('reply_text'),
                         'shortstr')

    def test_basic_return_has_exchange(self):
        self.assertEqual(commands.Basic.Return.amqp_type('exchange'),
                         'shortstr')

    def test_basic_return_has_routing_key(self):
        self.assertEqual(commands.Basic.Return.amqp_type('routing_key'),
                         'shortstr')

    def test_channel_close_has_reply_code(self):
        self.assertEqual(commands.Channel.Close.amqp_type('reply_code'),
                         'short')

    def test_channel_close_has_reply_text(self):
        self.assertEqual(commands.Channel.Close.amqp_type('reply_text'),
                         'shortstr')

    def test_channel_close_has_class_id(self):
        self.assertEqual(commands.Channel.Close.amqp_type('class_id'),
                         'short')

    def test_channel_close_has_method_id(self):
        self.assertEqual(commands.Channel.Close.amqp_type('method_id'),
                         'short')

    def test_channel_flow_has_active(self):
        self.assertEqual(commands.Channel.Flow.amqp_type('active'), 'bit')

    def test_channel_flowok_has_active(self):
        self.assertEqual(commands.Channel.FlowOk.amqp_type('active'),
                         'bit')

    def test_channel_open_has_out_of_band(self):
        self.assertEqual(commands.Channel.Open.amqp_type('out_of_band'),
                         'shortstr')

    def test_channel_openok_has_channel_id(self):
        self.assertEqual(commands.Channel.OpenOk.amqp_type('channel_id'),
                         'longstr')

    def test_confirm_select_has_nowait(self):
        self.assertEqual(commands.Confirm.Select.amqp_type('nowait'),
                         'bit')

    def test_connection_blocked_has_reason(self):
        self.assertEqual(commands.Connection.Blocked.amqp_type('reason'),
                         'shortstr')

    def test_connection_close_has_reply_code(self):
        self.assertEqual(
            commands.Connection.Close.amqp_type('reply_code'), 'short')

    def test_connection_close_has_reply_text(self):
        self.assertEqual(
            commands.Connection.Close.amqp_type('reply_text'), 'shortstr')

    def test_connection_close_has_class_id(self):
        self.assertEqual(commands.Connection.Close.amqp_type('class_id'),
                         'short')

    def test_connection_close_has_method_id(self):
        self.assertEqual(commands.Connection.Close.amqp_type('method_id'),
                         'short')

    def test_connection_open_has_virtual_host(self):
        self.assertEqual(
            commands.Connection.Open.amqp_type('virtual_host'),
            'shortstr')

    def test_connection_open_has_capabilities(self):
        self.assertEqual(
            commands.Connection.Open.amqp_type('capabilities'),
            'shortstr')

    def test_connection_open_has_insist(self):
        self.assertEqual(commands.Connection.Open.amqp_type('insist'),
                         'bit')

    def test_connection_openok_has_known_hosts(self):
        self.assertEqual(
            commands.Connection.OpenOk.amqp_type('known_hosts'),
            'shortstr')

    def test_connection_secure_has_challenge(self):
        self.assertEqual(
            commands.Connection.Secure.amqp_type('challenge'), 'longstr')

    def test_connection_secureok_has_response(self):
        self.assertEqual(
            commands.Connection.SecureOk.amqp_type('response'), 'longstr')

    def test_connection_start_has_version_major(self):
        self.assertEqual(
            commands.Connection.Start.amqp_type('version_major'), 'octet')

    def test_connection_start_has_version_minor(self):
        self.assertEqual(
            commands.Connection.Start.amqp_type('version_minor'), 'octet')

    def test_connection_start_has_server_properties(self):
        self.assertEqual(
            commands.Connection.Start.amqp_type('server_properties'),
            'table')

    def test_connection_start_has_mechanisms(self):
        self.assertEqual(
            commands.Connection.Start.amqp_type('mechanisms'), 'longstr')

    def test_connection_start_has_locales(self):
        self.assertEqual(commands.Connection.Start.amqp_type('locales'),
                         'longstr')

    def test_connection_startok_has_client_properties(self):
        self.assertEqual(
            commands.Connection.StartOk.amqp_type('client_properties'),
            'table')

    def test_connection_startok_has_mechanism(self):
        self.assertEqual(
            commands.Connection.StartOk.amqp_type('mechanism'),
            'shortstr')

    def test_connection_startok_has_response(self):
        self.assertEqual(
            commands.Connection.StartOk.amqp_type('response'), 'longstr')

    def test_connection_startok_has_locale(self):
        self.assertEqual(commands.Connection.StartOk.amqp_type('locale'),
                         'shortstr')

    def test_connection_update_secret(self):
        self.assertEqual(
            commands.Connection.UpdateSecret.amqp_type('new_secret'),
            'longstr')

    def test_connection_tune_has_channel_max(self):
        self.assertEqual(
            commands.Connection.Tune.amqp_type('channel_max'), 'short')

    def test_connection_tune_has_frame_max(self):
        self.assertEqual(commands.Connection.Tune.amqp_type('frame_max'),
                         'long')

    def test_connection_tune_has_heartbeat(self):
        self.assertEqual(commands.Connection.Tune.amqp_type('heartbeat'),
                         'short')

    def test_connection_tuneok_has_channel_max(self):
        self.assertEqual(
            commands.Connection.TuneOk.amqp_type('channel_max'), 'short')

    def test_connection_tuneok_has_frame_max(self):
        self.assertEqual(
            commands.Connection.TuneOk.amqp_type('frame_max'), 'long')

    def test_connection_tuneok_has_heartbeat(self):
        self.assertEqual(
            commands.Connection.TuneOk.amqp_type('heartbeat'), 'short')

    def test_exchange_bind_has_ticket(self):
        self.assertEqual(commands.Exchange.Bind.amqp_type('ticket'),
                         'short')

    def test_exchange_bind_has_destination(self):
        self.assertEqual(commands.Exchange.Bind.amqp_type('destination'),
                         'shortstr')

    def test_exchange_bind_has_source(self):
        self.assertEqual(commands.Exchange.Bind.amqp_type('source'),
                         'shortstr')

    def test_exchange_bind_has_routing_key(self):
        self.assertEqual(commands.Exchange.Bind.amqp_type('routing_key'),
                         'shortstr')

    def test_exchange_bind_has_nowait(self):
        self.assertEqual(commands.Exchange.Bind.amqp_type('nowait'),
                         'bit')

    def test_exchange_bind_has_arguments(self):
        self.assertEqual(commands.Exchange.Bind.amqp_type('arguments'),
                         'table')

    def test_exchange_declare_has_ticket(self):
        self.assertEqual(commands.Exchange.Declare.amqp_type('ticket'),
                         'short')

    def test_exchange_declare_has_exchange(self):
        self.assertEqual(commands.Exchange.Declare.amqp_type('exchange'),
                         'shortstr')

    def test_exchange_declare_has_exchange_type(self):
        self.assertEqual(
            commands.Exchange.Declare.amqp_type('exchange_type'),
            'shortstr')

    def test_exchange_declare_has_passive(self):
        self.assertEqual(commands.Exchange.Declare.amqp_type('passive'),
                         'bit')

    def test_exchange_declare_has_durable(self):
        self.assertEqual(commands.Exchange.Declare.amqp_type('durable'),
                         'bit')

    def test_exchange_declare_has_auto_delete(self):
        self.assertEqual(
            commands.Exchange.Declare.amqp_type('auto_delete'), 'bit')

    def test_exchange_declare_has_internal(self):
        self.assertEqual(commands.Exchange.Declare.amqp_type('internal'),
                         'bit')

    def test_exchange_declare_has_nowait(self):
        self.assertEqual(commands.Exchange.Declare.amqp_type('nowait'),
                         'bit')

    def test_exchange_declare_has_arguments(self):
        self.assertEqual(commands.Exchange.Declare.amqp_type('arguments'),
                         'table')

    def test_exchange_delete_has_ticket(self):
        self.assertEqual(commands.Exchange.Delete.amqp_type('ticket'),
                         'short')

    def test_exchange_delete_has_exchange(self):
        self.assertEqual(commands.Exchange.Delete.amqp_type('exchange'),
                         'shortstr')

    def test_exchange_delete_has_if_unused(self):
        self.assertEqual(commands.Exchange.Delete.amqp_type('if_unused'),
                         'bit')

    def test_exchange_delete_has_nowait(self):
        self.assertEqual(commands.Exchange.Delete.amqp_type('nowait'),
                         'bit')

    def test_exchange_unbind_has_ticket(self):
        self.assertEqual(commands.Exchange.Unbind.amqp_type('ticket'),
                         'short')

    def test_exchange_unbind_has_destination(self):
        self.assertEqual(
            commands.Exchange.Unbind.amqp_type('destination'), 'shortstr')

    def test_exchange_unbind_has_source(self):
        self.assertEqual(commands.Exchange.Unbind.amqp_type('source'),
                         'shortstr')

    def test_exchange_unbind_has_routing_key(self):
        self.assertEqual(
            commands.Exchange.Unbind.amqp_type('routing_key'), 'shortstr')

    def test_exchange_unbind_has_nowait(self):
        self.assertEqual(commands.Exchange.Unbind.amqp_type('nowait'),
                         'bit')

    def test_exchange_unbind_has_arguments(self):
        self.assertEqual(commands.Exchange.Unbind.amqp_type('arguments'),
                         'table')

    def test_queue_bind_has_ticket(self):
        self.assertEqual(commands.Queue.Bind.amqp_type('ticket'), 'short')

    def test_queue_bind_has_queue(self):
        self.assertEqual(commands.Queue.Bind.amqp_type('queue'),
                         'shortstr')

    def test_queue_bind_has_exchange(self):
        self.assertEqual(commands.Queue.Bind.amqp_type('exchange'),
                         'shortstr')

    def test_queue_bind_has_routing_key(self):
        self.assertEqual(commands.Queue.Bind.amqp_type('routing_key'),
                         'shortstr')

    def test_queue_bind_has_nowait(self):
        self.assertEqual(commands.Queue.Bind.amqp_type('nowait'), 'bit')

    def test_queue_bind_has_arguments(self):
        self.assertEqual(commands.Queue.Bind.amqp_type('arguments'),
                         'table')

    def test_queue_declare_has_ticket(self):
        self.assertEqual(commands.Queue.Declare.amqp_type('ticket'),
                         'short')

    def test_queue_declare_has_queue(self):
        self.assertEqual(commands.Queue.Declare.amqp_type('queue'),
                         'shortstr')

    def test_queue_declare_has_passive(self):
        self.assertEqual(commands.Queue.Declare.amqp_type('passive'),
                         'bit')

    def test_queue_declare_has_durable(self):
        self.assertEqual(commands.Queue.Declare.amqp_type('durable'),
                         'bit')

    def test_queue_declare_has_exclusive(self):
        self.assertEqual(commands.Queue.Declare.amqp_type('exclusive'),
                         'bit')

    def test_queue_declare_has_auto_delete(self):
        self.assertEqual(commands.Queue.Declare.amqp_type('auto_delete'),
                         'bit')

    def test_queue_declare_has_nowait(self):
        self.assertEqual(commands.Queue.Declare.amqp_type('nowait'),
                         'bit')

    def test_queue_declare_has_arguments(self):
        self.assertEqual(commands.Queue.Declare.amqp_type('arguments'),
                         'table')

    def test_queue_declareok_has_queue(self):
        self.assertEqual(commands.Queue.DeclareOk.amqp_type('queue'),
                         'shortstr')

    def test_queue_declareok_has_message_count(self):
        self.assertEqual(
            commands.Queue.DeclareOk.amqp_type('message_count'), 'long')

    def test_queue_declareok_has_consumer_count(self):
        self.assertEqual(
            commands.Queue.DeclareOk.amqp_type('consumer_count'), 'long')

    def test_queue_delete_has_ticket(self):
        self.assertEqual(commands.Queue.Delete.amqp_type('ticket'),
                         'short')

    def test_queue_delete_has_queue(self):
        self.assertEqual(commands.Queue.Delete.amqp_type('queue'),
                         'shortstr')

    def test_queue_delete_has_if_unused(self):
        self.assertEqual(commands.Queue.Delete.amqp_type('if_unused'),
                         'bit')

    def test_queue_delete_has_if_empty(self):
        self.assertEqual(commands.Queue.Delete.amqp_type('if_empty'),
                         'bit')

    def test_queue_delete_has_nowait(self):
        self.assertEqual(commands.Queue.Delete.amqp_type('nowait'), 'bit')

    def test_queue_deleteok_has_message_count(self):
        self.assertEqual(
            commands.Queue.DeleteOk.amqp_type('message_count'), 'long')

    def test_queue_purge_has_ticket(self):
        self.assertEqual(commands.Queue.Purge.amqp_type('ticket'),
                         'short')

    def test_queue_purge_has_queue(self):
        self.assertEqual(commands.Queue.Purge.amqp_type('queue'),
                         'shortstr')

    def test_queue_purge_has_nowait(self):
        self.assertEqual(commands.Queue.Purge.amqp_type('nowait'), 'bit')

    def test_queue_purgeok_has_message_count(self):
        self.assertEqual(
            commands.Queue.PurgeOk.amqp_type('message_count'), 'long')

    def test_queue_unbind_has_ticket(self):
        self.assertEqual(commands.Queue.Unbind.amqp_type('ticket'),
                         'short')

    def test_queue_unbind_has_queue(self):
        self.assertEqual(commands.Queue.Unbind.amqp_type('queue'),
                         'shortstr')

    def test_queue_unbind_has_exchange(self):
        self.assertEqual(commands.Queue.Unbind.amqp_type('exchange'),
                         'shortstr')

    def test_queue_unbind_has_routing_key(self):
        self.assertEqual(commands.Queue.Unbind.amqp_type('routing_key'),
                         'shortstr')

    def test_queue_unbind_has_arguments(self):
        self.assertEqual(commands.Queue.Unbind.amqp_type('arguments'),
                         'table')


class AttributeInMethodTests(unittest.TestCase):
    def test_basic_ack_has_delivery_tag(self):
        self.assertIn('delivery_tag', commands.Basic.Ack())

    def test_basic_ack_has_multiple(self):
        self.assertIn('multiple', commands.Basic.Ack())

    def test_basic_cancel_has_consumer_tag(self):
        self.assertIn('consumer_tag', commands.Basic.Cancel())

    def test_basic_cancel_has_nowait(self):
        self.assertIn('nowait', commands.Basic.Cancel())

    def test_basic_cancelok_has_consumer_tag(self):
        self.assertIn('consumer_tag', commands.Basic.CancelOk())

    def test_basic_consume_has_ticket(self):
        self.assertIn('ticket', commands.Basic.Consume())

    def test_basic_consume_has_queue(self):
        self.assertIn('queue', commands.Basic.Consume())

    def test_basic_consume_has_consumer_tag(self):
        self.assertIn('consumer_tag', commands.Basic.Consume())

    def test_basic_consume_has_no_local(self):
        self.assertIn('no_local', commands.Basic.Consume())

    def test_basic_consume_has_no_ack(self):
        self.assertIn('no_ack', commands.Basic.Consume())

    def test_basic_consume_has_exclusive(self):
        self.assertIn('exclusive', commands.Basic.Consume())

    def test_basic_consume_has_nowait(self):
        self.assertIn('nowait', commands.Basic.Consume())

    def test_basic_consume_has_arguments(self):
        self.assertIn('arguments', commands.Basic.Consume())

    def test_basic_consumeok_has_consumer_tag(self):
        self.assertIn('consumer_tag', commands.Basic.ConsumeOk())

    def test_basic_deliver_has_consumer_tag(self):
        self.assertIn('consumer_tag', commands.Basic.Deliver())

    def test_basic_deliver_has_delivery_tag(self):
        self.assertIn('delivery_tag', commands.Basic.Deliver())

    def test_basic_deliver_has_redelivered(self):
        self.assertIn('redelivered', commands.Basic.Deliver())

    def test_basic_deliver_has_exchange(self):
        self.assertIn('exchange', commands.Basic.Deliver())

    def test_basic_deliver_has_routing_key(self):
        self.assertIn('routing_key', commands.Basic.Deliver())

    def test_basic_get_has_ticket(self):
        self.assertIn('ticket', commands.Basic.Get())

    def test_basic_get_has_queue(self):
        self.assertIn('queue', commands.Basic.Get())

    def test_basic_get_has_no_ack(self):
        self.assertIn('no_ack', commands.Basic.Get())

    def test_basic_getempty_has_cluster_id(self):
        self.assertIn('cluster_id', commands.Basic.GetEmpty())

    def test_basic_getok_has_delivery_tag(self):
        self.assertIn('delivery_tag', commands.Basic.GetOk())

    def test_basic_getok_has_redelivered(self):
        self.assertIn('redelivered', commands.Basic.GetOk())

    def test_basic_getok_has_exchange(self):
        self.assertIn('exchange', commands.Basic.GetOk())

    def test_basic_getok_has_routing_key(self):
        self.assertIn('routing_key', commands.Basic.GetOk())

    def test_basic_getok_has_message_count(self):
        self.assertIn('message_count', commands.Basic.GetOk())

    def test_basic_nack_has_delivery_tag(self):
        self.assertIn('delivery_tag', commands.Basic.Nack())

    def test_basic_nack_has_multiple(self):
        self.assertIn('multiple', commands.Basic.Nack())

    def test_basic_nack_has_requeue(self):
        self.assertIn('requeue', commands.Basic.Nack())

    def test_basic_publish_has_ticket(self):
        self.assertIn('ticket', commands.Basic.Publish())

    def test_basic_publish_has_exchange(self):
        self.assertIn('exchange', commands.Basic.Publish())

    def test_basic_publish_has_routing_key(self):
        self.assertIn('routing_key', commands.Basic.Publish())

    def test_basic_publish_has_mandatory(self):
        self.assertIn('mandatory', commands.Basic.Publish())

    def test_basic_publish_has_immediate(self):
        self.assertIn('immediate', commands.Basic.Publish())

    def test_basic_qos_has_prefetch_size(self):
        self.assertIn('prefetch_size', commands.Basic.Qos())

    def test_basic_qos_has_prefetch_count(self):
        self.assertIn('prefetch_count', commands.Basic.Qos())

    def test_basic_qos_has_global_(self):
        self.assertIn('global_', commands.Basic.Qos())

    def test_basic_recover_has_requeue(self):
        self.assertIn('requeue', commands.Basic.Recover())

    def test_basic_reject_has_delivery_tag(self):
        self.assertIn('delivery_tag', commands.Basic.Reject())

    def test_basic_reject_has_requeue(self):
        self.assertIn('requeue', commands.Basic.Reject())

    def test_basic_return_has_reply_code(self):
        self.assertIn('reply_code', commands.Basic.Return())

    def test_basic_return_has_reply_text(self):
        self.assertIn('reply_text', commands.Basic.Return())

    def test_basic_return_has_exchange(self):
        self.assertIn('exchange', commands.Basic.Return())

    def test_basic_return_has_routing_key(self):
        self.assertIn('routing_key', commands.Basic.Return())

    def test_channel_close_has_reply_code(self):
        self.assertIn('reply_code', commands.Channel.Close())

    def test_channel_close_has_reply_text(self):
        self.assertIn('reply_text', commands.Channel.Close())

    def test_channel_close_has_class_id(self):
        self.assertIn('class_id', commands.Channel.Close())

    def test_channel_close_has_method_id(self):
        self.assertIn('method_id', commands.Channel.Close())

    def test_channel_flow_has_active(self):
        self.assertIn('active', commands.Channel.Flow())

    def test_channel_flowok_has_active(self):
        self.assertIn('active', commands.Channel.FlowOk())

    def test_channel_open_has_out_of_band(self):
        self.assertIn('out_of_band', commands.Channel.Open())

    def test_channel_openok_has_channel_id(self):
        self.assertIn('channel_id', commands.Channel.OpenOk())

    def test_confirm_select_has_nowait(self):
        self.assertIn('nowait', commands.Confirm.Select())

    def test_connection_blocked_has_reason(self):
        self.assertIn('reason', commands.Connection.Blocked())

    def test_connection_close_has_reply_code(self):
        self.assertIn('reply_code', commands.Connection.Close())

    def test_connection_close_has_reply_text(self):
        self.assertIn('reply_text', commands.Connection.Close())

    def test_connection_close_has_class_id(self):
        self.assertIn('class_id', commands.Connection.Close())

    def test_connection_close_has_method_id(self):
        self.assertIn('method_id', commands.Connection.Close())

    def test_connection_open_has_virtual_host(self):
        self.assertIn('virtual_host', commands.Connection.Open())

    def test_connection_open_has_capabilities(self):
        self.assertIn('capabilities', commands.Connection.Open())

    def test_connection_open_has_insist(self):
        self.assertIn('insist', commands.Connection.Open())

    def test_connection_openok_has_known_hosts(self):
        self.assertIn('known_hosts', commands.Connection.OpenOk())

    def test_connection_secure_has_challenge(self):
        self.assertIn('challenge', commands.Connection.Secure())

    def test_connection_secureok_has_response(self):
        self.assertIn('response', commands.Connection.SecureOk())

    def test_connection_start_has_version_major(self):
        self.assertIn('version_major', commands.Connection.Start())

    def test_connection_start_has_version_minor(self):
        self.assertIn('version_minor', commands.Connection.Start())

    def test_connection_start_has_server_properties(self):
        self.assertIn('server_properties', commands.Connection.Start())

    def test_connection_start_has_mechanisms(self):
        self.assertIn('mechanisms', commands.Connection.Start())

    def test_connection_start_has_locales(self):
        self.assertIn('locales', commands.Connection.Start())

    def test_connection_startok_has_mechanism(self):
        self.assertIn('mechanism', commands.Connection.StartOk())

    def test_connection_startok_has_response(self):
        self.assertIn('response', commands.Connection.StartOk())

    def test_connection_startok_has_locale(self):
        self.assertIn('locale', commands.Connection.StartOk())

    def test_connection_tune_has_channel_max(self):
        self.assertIn('channel_max', commands.Connection.Tune())

    def test_connection_tune_has_frame_max(self):
        self.assertIn('frame_max', commands.Connection.Tune())

    def test_connection_tune_has_heartbeat(self):
        self.assertIn('heartbeat', commands.Connection.Tune())

    def test_connection_tuneok_has_channel_max(self):
        self.assertIn('channel_max', commands.Connection.TuneOk())

    def test_connection_tuneok_has_frame_max(self):
        self.assertIn('frame_max', commands.Connection.TuneOk())

    def test_connection_tuneok_has_heartbeat(self):
        self.assertIn('heartbeat', commands.Connection.TuneOk())

    def test_exchange_bind_has_ticket(self):
        self.assertIn('ticket', commands.Exchange.Bind())

    def test_exchange_bind_has_destination(self):
        self.assertIn('destination', commands.Exchange.Bind())

    def test_exchange_bind_has_source(self):
        self.assertIn('source', commands.Exchange.Bind())

    def test_exchange_bind_has_routing_key(self):
        self.assertIn('routing_key', commands.Exchange.Bind())

    def test_exchange_bind_has_nowait(self):
        self.assertIn('nowait', commands.Exchange.Bind())

    def test_exchange_bind_has_arguments(self):
        self.assertIn('arguments', commands.Exchange.Bind())

    def test_exchange_declare_has_ticket(self):
        self.assertIn('ticket', commands.Exchange.Declare())

    def test_exchange_declare_has_exchange(self):
        self.assertIn('exchange', commands.Exchange.Declare())

    def test_exchange_declare_has_exchange_type(self):
        self.assertIn('exchange_type', commands.Exchange.Declare())

    def test_exchange_declare_has_passive(self):
        self.assertIn('passive', commands.Exchange.Declare())

    def test_exchange_declare_has_durable(self):
        self.assertIn('durable', commands.Exchange.Declare())

    def test_exchange_declare_has_auto_delete(self):
        self.assertIn('auto_delete', commands.Exchange.Declare())

    def test_exchange_declare_has_internal(self):
        self.assertIn('internal', commands.Exchange.Declare())

    def test_exchange_declare_has_nowait(self):
        self.assertIn('nowait', commands.Exchange.Declare())

    def test_exchange_declare_has_arguments(self):
        self.assertIn('arguments', commands.Exchange.Declare())

    def test_exchange_delete_has_ticket(self):
        self.assertIn('ticket', commands.Exchange.Delete())

    def test_exchange_delete_has_exchange(self):
        self.assertIn('exchange', commands.Exchange.Delete())

    def test_exchange_delete_has_if_unused(self):
        self.assertIn('if_unused', commands.Exchange.Delete())

    def test_exchange_delete_has_nowait(self):
        self.assertIn('nowait', commands.Exchange.Delete())

    def test_exchange_unbind_has_ticket(self):
        self.assertIn('ticket', commands.Exchange.Unbind())

    def test_exchange_unbind_has_destination(self):
        self.assertIn('destination', commands.Exchange.Unbind())

    def test_exchange_unbind_has_source(self):
        self.assertIn('source', commands.Exchange.Unbind())

    def test_exchange_unbind_has_routing_key(self):
        self.assertIn('routing_key', commands.Exchange.Unbind())

    def test_exchange_unbind_has_nowait(self):
        self.assertIn('nowait', commands.Exchange.Unbind())

    def test_exchange_unbind_has_arguments(self):
        self.assertIn('arguments', commands.Exchange.Unbind())

    def test_queue_bind_has_ticket(self):
        self.assertIn('ticket', commands.Queue.Bind())

    def test_queue_bind_has_queue(self):
        self.assertIn('queue', commands.Queue.Bind())

    def test_queue_bind_has_exchange(self):
        self.assertIn('exchange', commands.Queue.Bind())

    def test_queue_bind_has_routing_key(self):
        self.assertIn('routing_key', commands.Queue.Bind())

    def test_queue_bind_has_nowait(self):
        self.assertIn('nowait', commands.Queue.Bind())

    def test_queue_bind_has_arguments(self):
        self.assertIn('arguments', commands.Queue.Bind())

    def test_queue_declare_has_ticket(self):
        self.assertIn('ticket', commands.Queue.Declare())

    def test_queue_declare_has_queue(self):
        self.assertIn('queue', commands.Queue.Declare())

    def test_queue_declare_has_passive(self):
        self.assertIn('passive', commands.Queue.Declare())

    def test_queue_declare_has_durable(self):
        self.assertIn('durable', commands.Queue.Declare())

    def test_queue_declare_has_exclusive(self):
        self.assertIn('exclusive', commands.Queue.Declare())

    def test_queue_declare_has_auto_delete(self):
        self.assertIn('auto_delete', commands.Queue.Declare())

    def test_queue_declare_has_nowait(self):
        self.assertIn('nowait', commands.Queue.Declare())

    def test_queue_declare_has_arguments(self):
        self.assertIn('arguments', commands.Queue.Declare())

    def test_queue_declareok_has_queue(self):
        self.assertIn('queue', commands.Queue.DeclareOk())

    def test_queue_declareok_has_message_count(self):
        self.assertIn('message_count', commands.Queue.DeclareOk())

    def test_queue_declareok_has_consumer_count(self):
        self.assertIn('consumer_count', commands.Queue.DeclareOk())

    def test_queue_delete_has_ticket(self):
        self.assertIn('ticket', commands.Queue.Delete())

    def test_queue_delete_has_queue(self):
        self.assertIn('queue', commands.Queue.Delete())

    def test_queue_delete_has_if_unused(self):
        self.assertIn('if_unused', commands.Queue.Delete())

    def test_queue_delete_has_if_empty(self):
        self.assertIn('if_empty', commands.Queue.Delete())

    def test_queue_delete_has_nowait(self):
        self.assertIn('nowait', commands.Queue.Delete())

    def test_queue_deleteok_has_message_count(self):
        self.assertIn('message_count', commands.Queue.DeleteOk())

    def test_queue_purge_has_ticket(self):
        self.assertIn('ticket', commands.Queue.Purge())

    def test_queue_purge_has_queue(self):
        self.assertIn('queue', commands.Queue.Purge())

    def test_queue_purge_has_nowait(self):
        self.assertIn('nowait', commands.Queue.Purge())

    def test_queue_purgeok_has_message_count(self):
        self.assertIn('message_count', commands.Queue.PurgeOk())

    def test_queue_unbind_has_ticket(self):
        self.assertIn('ticket', commands.Queue.Unbind())

    def test_queue_unbind_has_queue(self):
        self.assertIn('queue', commands.Queue.Unbind())

    def test_queue_unbind_has_exchange(self):
        self.assertIn('exchange', commands.Queue.Unbind())

    def test_queue_unbind_has_routing_key(self):
        self.assertIn('routing_key', commands.Queue.Unbind())

    def test_queue_unbind_has_arguments(self):
        self.assertIn('arguments', commands.Queue.Unbind())

    def test_connection_update_secret_has_new_secret(self):
        self.assertIn('new_secret', commands.Connection.UpdateSecret())

    def test_connection_update_secret_has_reason(self):
        self.assertIn('reason', commands.Connection.UpdateSecret())


class DeprecationWarningTests(unittest.TestCase):
    def test_basic_recoverasync_raises_deprecation_error(self):
        with self.assertWarns(DeprecationWarning):
            commands.Basic.RecoverAsync()


class BasicPropertiesTests(unittest.TestCase):
    def test_basic_properties_has_content_type(self):
        self.assertEqual(
            commands.Basic.Properties.amqp_type('content_type'),
            'shortstr')

    def test_basic_properties_has_content_encoding(self):
        self.assertEqual(
            commands.Basic.Properties.amqp_type('content_encoding'),
            'shortstr')

    def test_basic_properties_has_headers(self):
        self.assertEqual(commands.Basic.Properties.amqp_type('headers'),
                         'table')

    def test_basic_properties_has_delivery_mode(self):
        self.assertEqual(
            commands.Basic.Properties.amqp_type('delivery_mode'), 'octet')

    def test_basic_properties_has_priority(self):
        self.assertEqual(commands.Basic.Properties.amqp_type('priority'),
                         'octet')

    def test_basic_properties_has_correlation_id(self):
        self.assertEqual(
            commands.Basic.Properties.amqp_type('correlation_id'),
            'shortstr')

    def test_basic_properties_has_reply_to(self):
        self.assertEqual(commands.Basic.Properties.amqp_type('reply_to'),
                         'shortstr')

    def test_basic_properties_has_expiration(self):
        self.assertEqual(
            commands.Basic.Properties.amqp_type('expiration'), 'shortstr')

    def test_basic_properties_has_message_id(self):
        self.assertEqual(
            commands.Basic.Properties.amqp_type('message_id'), 'shortstr')

    def test_basic_properties_has_timestamp(self):
        self.assertEqual(commands.Basic.Properties.amqp_type('timestamp'),
                         'timestamp')

    def test_basic_properties_has_message_type(self):
        self.assertEqual(
            commands.Basic.Properties.amqp_type('message_type'),
            'shortstr')

    def test_basic_properties_has_user_id(self):
        self.assertEqual(commands.Basic.Properties.amqp_type('user_id'),
                         'shortstr')

    def test_basic_properties_has_app_id(self):
        self.assertEqual(commands.Basic.Properties.amqp_type('app_id'),
                         'shortstr')

    def test_basic_properties_has_cluster_id(self):
        self.assertEqual(
            commands.Basic.Properties.amqp_type('cluster_id'), 'shortstr')


class MethodAttributeLengthTests(unittest.TestCase):
    def test_basic_ack_attribute_count(self):
        self.assertEqual(len(commands.Basic.Ack()), 2)

    def test_basic_cancel_attribute_count(self):
        self.assertEqual(len(commands.Basic.Cancel()), 2)

    def test_basic_cancelok_attribute_count(self):
        self.assertEqual(len(commands.Basic.CancelOk()), 1)

    def test_basic_consume_attribute_count(self):
        self.assertEqual(len(commands.Basic.Consume()), 8)

    def test_basic_consumeok_attribute_count(self):
        self.assertEqual(len(commands.Basic.ConsumeOk()), 1)

    def test_basic_deliver_attribute_count(self):
        self.assertEqual(len(commands.Basic.Deliver()), 5)

    def test_basic_get_attribute_count(self):
        self.assertEqual(len(commands.Basic.Get()), 3)

    def test_basic_getempty_attribute_count(self):
        self.assertEqual(len(commands.Basic.GetEmpty()), 1)

    def test_basic_getok_attribute_count(self):
        self.assertEqual(len(commands.Basic.GetOk()), 5)

    def test_basic_nack_attribute_count(self):
        self.assertEqual(len(commands.Basic.Nack()), 3)

    def test_basic_publish_attribute_count(self):
        self.assertEqual(len(commands.Basic.Publish()), 5)

    def test_basic_qos_attribute_count(self):
        self.assertEqual(len(commands.Basic.Qos()), 3)

    def test_basic_qosok_attribute_count(self):
        self.assertEqual(len(commands.Basic.QosOk()), 0)

    def test_basic_recover_attribute_count(self):
        self.assertEqual(len(commands.Basic.Recover()), 1)

    def test_basic_recoverok_attribute_count(self):
        self.assertEqual(len(commands.Basic.RecoverOk()), 0)

    def test_basic_reject_attribute_count(self):
        self.assertEqual(len(commands.Basic.Reject()), 2)

    def test_basic_return_attribute_count(self):
        self.assertEqual(len(commands.Basic.Return()), 4)

    def test_channel_close_attribute_count(self):
        self.assertEqual(len(commands.Channel.Close()), 4)

    def test_channel_closeok_attribute_count(self):
        self.assertEqual(len(commands.Channel.CloseOk()), 0)

    def test_channel_flow_attribute_count(self):
        self.assertEqual(len(commands.Channel.Flow()), 1)

    def test_channel_flowok_attribute_count(self):
        self.assertEqual(len(commands.Channel.FlowOk()), 1)

    def test_channel_open_attribute_count(self):
        self.assertEqual(len(commands.Channel.Open()), 1)

    def test_channel_openok_attribute_count(self):
        self.assertEqual(len(commands.Channel.OpenOk()), 1)

    def test_confirm_select_attribute_count(self):
        self.assertEqual(len(commands.Confirm.Select()), 1)

    def test_confirm_selectok_attribute_count(self):
        self.assertEqual(len(commands.Confirm.SelectOk()), 0)

    def test_connection_blocked_attribute_count(self):
        self.assertEqual(len(commands.Connection.Blocked()), 1)

    def test_connection_close_attribute_count(self):
        self.assertEqual(len(commands.Connection.Close()), 4)

    def test_connection_closeok_attribute_count(self):
        self.assertEqual(len(commands.Connection.CloseOk()), 0)

    def test_connection_open_attribute_count(self):
        self.assertEqual(len(commands.Connection.Open()), 3)

    def test_connection_openok_attribute_count(self):
        self.assertEqual(len(commands.Connection.OpenOk()), 1)

    def test_connection_secure_attribute_count(self):
        self.assertEqual(len(commands.Connection.Secure()), 1)

    def test_connection_secureok_attribute_count(self):
        self.assertEqual(len(commands.Connection.SecureOk()), 1)

    def test_connection_start_attribute_count(self):
        self.assertEqual(len(commands.Connection.Start()), 5)

    def test_connection_startok_attribute_count(self):
        self.assertEqual(len(commands.Connection.StartOk()), 4)

    def test_connection_tune_attribute_count(self):
        self.assertEqual(len(commands.Connection.Tune()), 3)

    def test_connection_tuneok_attribute_count(self):
        self.assertEqual(len(commands.Connection.TuneOk()), 3)

    def test_connection_unblocked_attribute_count(self):
        self.assertEqual(len(commands.Connection.Unblocked()), 0)

    def test_exchange_bind_attribute_count(self):
        self.assertEqual(len(commands.Exchange.Bind()), 6)

    def test_exchange_bindok_attribute_count(self):
        self.assertEqual(len(commands.Exchange.BindOk()), 0)

    def test_exchange_declare_attribute_count(self):
        self.assertEqual(len(commands.Exchange.Declare()), 9)

    def test_exchange_declareok_attribute_count(self):
        self.assertEqual(len(commands.Exchange.DeclareOk()), 0)

    def test_exchange_delete_attribute_count(self):
        self.assertEqual(len(commands.Exchange.Delete()), 4)

    def test_exchange_deleteok_attribute_count(self):
        self.assertEqual(len(commands.Exchange.DeleteOk()), 0)

    def test_exchange_unbind_attribute_count(self):
        self.assertEqual(len(commands.Exchange.Unbind()), 6)

    def test_exchange_unbindok_attribute_count(self):
        self.assertEqual(len(commands.Exchange.UnbindOk()), 0)

    def test_queue_bind_attribute_count(self):
        self.assertEqual(len(commands.Queue.Bind()), 6)

    def test_queue_bindok_attribute_count(self):
        self.assertEqual(len(commands.Queue.BindOk()), 0)

    def test_queue_declare_attribute_count(self):
        self.assertEqual(len(commands.Queue.Declare()), 8)

    def test_queue_declareok_attribute_count(self):
        self.assertEqual(len(commands.Queue.DeclareOk()), 3)

    def test_queue_delete_attribute_count(self):
        self.assertEqual(len(commands.Queue.Delete()), 5)

    def test_queue_deleteok_attribute_count(self):
        self.assertEqual(len(commands.Queue.DeleteOk()), 1)

    def test_queue_purge_attribute_count(self):
        self.assertEqual(len(commands.Queue.Purge()), 3)

    def test_queue_purgeok_attribute_count(self):
        self.assertEqual(len(commands.Queue.PurgeOk()), 1)

    def test_queue_unbind_attribute_count(self):
        self.assertEqual(len(commands.Queue.Unbind()), 5)

    def test_queue_unbindok_attribute_count(self):
        self.assertEqual(len(commands.Queue.UnbindOk()), 0)

    def test_tx_commit_attribute_count(self):
        self.assertEqual(len(commands.Tx.Commit()), 0)

    def test_tx_commitok_attribute_count(self):
        self.assertEqual(len(commands.Tx.CommitOk()), 0)

    def test_tx_rollback_attribute_count(self):
        self.assertEqual(len(commands.Tx.Rollback()), 0)

    def test_tx_rollbackok_attribute_count(self):
        self.assertEqual(len(commands.Tx.RollbackOk()), 0)

    def test_tx_select_attribute_count(self):
        self.assertEqual(len(commands.Tx.Select()), 0)

    def test_tx_selectok_attribute_count(self):
        self.assertEqual(len(commands.Tx.SelectOk()), 0)


class MethodAttributeDefaultTests(unittest.TestCase):
    def test_basic_ack_default_for_delivery_tag(self):
        obj = commands.Basic.Ack()
        self.assertEqual(obj['delivery_tag'], 0)

    def test_basic_ack_default_for_multiple(self):
        obj = commands.Basic.Ack()
        self.assertEqual(obj['multiple'], False)

    def test_basic_cancel_default_for_consumer_tag(self):
        obj = commands.Basic.Cancel()
        self.assertEqual(obj['consumer_tag'], None)

    def test_basic_cancel_default_for_nowait(self):
        obj = commands.Basic.Cancel()
        self.assertEqual(obj['nowait'], False)

    def test_basic_cancelok_default_for_consumer_tag(self):
        obj = commands.Basic.CancelOk()
        self.assertEqual(obj['consumer_tag'], None)

    def test_basic_consume_default_for_ticket(self):
        obj = commands.Basic.Consume()
        self.assertEqual(obj['ticket'], 0)

    def test_basic_consume_default_for_queue(self):
        obj = commands.Basic.Consume()
        self.assertEqual(obj['queue'], '')

    def test_basic_consume_default_for_consumer_tag(self):
        obj = commands.Basic.Consume()
        self.assertEqual(obj['consumer_tag'], '')

    def test_basic_consume_default_for_no_local(self):
        obj = commands.Basic.Consume()
        self.assertEqual(obj['no_local'], False)

    def test_basic_consume_default_for_no_ack(self):
        obj = commands.Basic.Consume()
        self.assertEqual(obj['no_ack'], False)

    def test_basic_consume_default_for_exclusive(self):
        obj = commands.Basic.Consume()
        self.assertEqual(obj['exclusive'], False)

    def test_basic_consume_default_for_nowait(self):
        obj = commands.Basic.Consume()
        self.assertEqual(obj['nowait'], False)

    def test_basic_consume_default_for_arguments(self):
        obj = commands.Basic.Consume()
        self.assertDictEqual(obj['arguments'], {})

    def test_basic_consumeok_default_for_consumer_tag(self):
        obj = commands.Basic.ConsumeOk()
        self.assertEqual(obj['consumer_tag'], None)

    def test_basic_deliver_default_for_consumer_tag(self):
        obj = commands.Basic.Deliver()
        self.assertEqual(obj['consumer_tag'], None)

    def test_basic_deliver_default_for_delivery_tag(self):
        obj = commands.Basic.Deliver()
        self.assertEqual(obj['delivery_tag'], None)

    def test_basic_deliver_default_for_redelivered(self):
        obj = commands.Basic.Deliver()
        self.assertEqual(obj['redelivered'], False)

    def test_basic_deliver_default_for_exchange(self):
        obj = commands.Basic.Deliver()
        self.assertEqual(obj['exchange'], None)

    def test_basic_deliver_default_for_routing_key(self):
        obj = commands.Basic.Deliver()
        self.assertEqual(obj['routing_key'], None)

    def test_basic_get_default_for_ticket(self):
        obj = commands.Basic.Get()
        self.assertEqual(obj['ticket'], 0)

    def test_basic_get_default_for_queue(self):
        obj = commands.Basic.Get()
        self.assertEqual(obj['queue'], '')

    def test_basic_get_default_for_no_ack(self):
        obj = commands.Basic.Get()
        self.assertEqual(obj['no_ack'], False)

    def test_basic_getempty_default_for_cluster_id(self):
        obj = commands.Basic.GetEmpty()
        self.assertEqual(obj['cluster_id'], '')

    def test_basic_getok_default_for_delivery_tag(self):
        obj = commands.Basic.GetOk()
        self.assertEqual(obj['delivery_tag'], None)

    def test_basic_getok_default_for_redelivered(self):
        obj = commands.Basic.GetOk()
        self.assertEqual(obj['redelivered'], False)

    def test_basic_getok_default_for_exchange(self):
        obj = commands.Basic.GetOk()
        self.assertEqual(obj['exchange'], None)

    def test_basic_getok_default_for_routing_key(self):
        obj = commands.Basic.GetOk()
        self.assertEqual(obj['routing_key'], None)

    def test_basic_getok_default_for_message_count(self):
        obj = commands.Basic.GetOk()
        self.assertEqual(obj['message_count'], None)

    def test_basic_nack_default_for_delivery_tag(self):
        obj = commands.Basic.Nack()
        self.assertEqual(obj['delivery_tag'], 0)

    def test_basic_nack_default_for_multiple(self):
        obj = commands.Basic.Nack()
        self.assertEqual(obj['multiple'], False)

    def test_basic_nack_default_for_requeue(self):
        obj = commands.Basic.Nack()
        self.assertEqual(obj['requeue'], True)

    def test_basic_publish_default_for_ticket(self):
        obj = commands.Basic.Publish()
        self.assertEqual(obj['ticket'], 0)

    def test_basic_publish_default_for_exchange(self):
        obj = commands.Basic.Publish()
        self.assertEqual(obj['exchange'], '')

    def test_basic_publish_default_for_routing_key(self):
        obj = commands.Basic.Publish()
        self.assertEqual(obj['routing_key'], '')

    def test_basic_publish_default_for_mandatory(self):
        obj = commands.Basic.Publish()
        self.assertEqual(obj['mandatory'], False)

    def test_basic_publish_default_for_immediate(self):
        obj = commands.Basic.Publish()
        self.assertEqual(obj['immediate'], False)

    def test_basic_qos_default_for_prefetch_size(self):
        obj = commands.Basic.Qos()
        self.assertEqual(obj['prefetch_size'], 0)

    def test_basic_qos_default_for_prefetch_count(self):
        obj = commands.Basic.Qos()
        self.assertEqual(obj['prefetch_count'], 0)

    def test_basic_qos_default_for_global_(self):
        obj = commands.Basic.Qos()
        self.assertEqual(obj['global_'], False)

    def test_basic_recover_default_for_requeue(self):
        obj = commands.Basic.Recover()
        self.assertEqual(obj['requeue'], False)

    def test_basic_reject_default_for_delivery_tag(self):
        obj = commands.Basic.Reject()
        self.assertEqual(obj['delivery_tag'], None)

    def test_basic_reject_default_for_requeue(self):
        obj = commands.Basic.Reject()
        self.assertEqual(obj['requeue'], True)

    def test_basic_return_default_for_reply_code(self):
        obj = commands.Basic.Return()
        self.assertEqual(obj['reply_code'], 0)

    def test_basic_return_default_for_reply_text(self):
        obj = commands.Basic.Return()
        self.assertEqual(obj['reply_text'], '')

    def test_basic_return_default_for_exchange(self):
        obj = commands.Basic.Return()
        self.assertEqual(obj['exchange'], None)

    def test_basic_return_default_for_routing_key(self):
        obj = commands.Basic.Return()
        self.assertEqual(obj['routing_key'], None)

    def test_channel_close_default_for_reply_code(self):
        obj = commands.Channel.Close()
        self.assertEqual(obj['reply_code'], 0)

    def test_channel_close_default_for_reply_text(self):
        obj = commands.Channel.Close()
        self.assertEqual(obj['reply_text'], '')

    def test_channel_close_default_for_class_id(self):
        obj = commands.Channel.Close()
        self.assertEqual(obj['class_id'], None)

    def test_channel_close_default_for_method_id(self):
        obj = commands.Channel.Close()
        self.assertEqual(obj['method_id'], None)

    def test_channel_flow_default_for_active(self):
        obj = commands.Channel.Flow()
        self.assertEqual(obj['active'], None)

    def test_channel_flowok_default_for_active(self):
        obj = commands.Channel.FlowOk()
        self.assertEqual(obj['active'], None)

    def test_channel_open_default_for_out_of_band(self):
        obj = commands.Channel.Open()
        self.assertEqual(obj['out_of_band'], '')

    def test_channel_openok_default_for_channel_id(self):
        obj = commands.Channel.OpenOk()
        self.assertEqual(obj['channel_id'], '')

    def test_confirm_select_default_for_nowait(self):
        obj = commands.Confirm.Select()
        self.assertEqual(obj['nowait'], False)

    def test_connection_blocked_default_for_reason(self):
        obj = commands.Connection.Blocked()
        self.assertEqual(obj['reason'], '')

    def test_connection_close_default_for_reply_code(self):
        obj = commands.Connection.Close()
        self.assertEqual(obj['reply_code'], 0)

    def test_connection_close_default_for_reply_text(self):
        obj = commands.Connection.Close()
        self.assertEqual(obj['reply_text'], '')

    def test_connection_close_default_for_class_id(self):
        obj = commands.Connection.Close()
        self.assertEqual(obj['class_id'], None)

    def test_connection_close_default_for_method_id(self):
        obj = commands.Connection.Close()
        self.assertEqual(obj['method_id'], None)

    def test_connection_open_default_for_virtual_host(self):
        obj = commands.Connection.Open()
        self.assertEqual(obj['virtual_host'], '/')

    def test_connection_open_default_for_capabilities(self):
        obj = commands.Connection.Open()
        self.assertEqual(obj['capabilities'], '')

    def test_connection_open_default_for_insist(self):
        obj = commands.Connection.Open()
        self.assertEqual(obj['insist'], False)

    def test_connection_openok_default_for_known_hosts(self):
        obj = commands.Connection.OpenOk()
        self.assertEqual(obj['known_hosts'], '')

    def test_connection_secure_default_for_challenge(self):
        obj = commands.Connection.Secure()
        self.assertEqual(obj['challenge'], None)

    def test_connection_secureok_default_for_response(self):
        obj = commands.Connection.SecureOk()
        self.assertEqual(obj['response'], '')

    def test_connection_start_default_for_version_major(self):
        obj = commands.Connection.Start()
        self.assertEqual(obj['version_major'], 0)

    def test_connection_start_default_for_version_minor(self):
        obj = commands.Connection.Start()
        self.assertEqual(obj['version_minor'], 9)

    def test_connection_start_default_for_mechanisms(self):
        obj = commands.Connection.Start()
        self.assertEqual(obj['mechanisms'], 'PLAIN')

    def test_connection_start_default_for_locales(self):
        obj = commands.Connection.Start()
        self.assertEqual(obj['locales'], 'en_US')

    def test_connection_startok_default_for_mechanism(self):
        obj = commands.Connection.StartOk()
        self.assertEqual(obj['mechanism'], 'PLAIN')

    def test_connection_startok_default_for_response(self):
        obj = commands.Connection.StartOk()
        self.assertEqual(obj['response'], '')

    def test_connection_startok_default_for_locale(self):
        obj = commands.Connection.StartOk()
        self.assertEqual(obj['locale'], 'en_US')

    def test_connection_tune_default_for_channel_max(self):
        obj = commands.Connection.Tune()
        self.assertEqual(obj['channel_max'], 0)

    def test_connection_tune_default_for_frame_max(self):
        obj = commands.Connection.Tune()
        self.assertEqual(obj['frame_max'], 0)

    def test_connection_tune_default_for_heartbeat(self):
        obj = commands.Connection.Tune()
        self.assertEqual(obj['heartbeat'], 0)

    def test_connection_tuneok_default_for_channel_max(self):
        obj = commands.Connection.TuneOk()
        self.assertEqual(obj['channel_max'], 0)

    def test_connection_tuneok_default_for_frame_max(self):
        obj = commands.Connection.TuneOk()
        self.assertEqual(obj['frame_max'], 0)

    def test_connection_tuneok_default_for_heartbeat(self):
        obj = commands.Connection.TuneOk()
        self.assertEqual(obj['heartbeat'], 0)

    def test_exchange_bind_default_for_ticket(self):
        obj = commands.Exchange.Bind()
        self.assertEqual(obj['ticket'], 0)

    def test_exchange_bind_default_for_destination(self):
        obj = commands.Exchange.Bind()
        self.assertEqual(obj['destination'], None)

    def test_exchange_bind_default_for_source(self):
        obj = commands.Exchange.Bind()
        self.assertEqual(obj['source'], None)

    def test_exchange_bind_default_for_routing_key(self):
        obj = commands.Exchange.Bind()
        self.assertEqual(obj['routing_key'], '')

    def test_exchange_bind_default_for_nowait(self):
        obj = commands.Exchange.Bind()
        self.assertEqual(obj['nowait'], False)

    def test_exchange_bind_default_for_arguments(self):
        obj = commands.Exchange.Bind()
        self.assertDictEqual(obj['arguments'], {})

    def test_exchange_declare_default_for_ticket(self):
        obj = commands.Exchange.Declare()
        self.assertEqual(obj['ticket'], 0)

    def test_exchange_declare_default_for_exchange(self):
        obj = commands.Exchange.Declare()
        self.assertEqual(obj['exchange'], '')

    def test_exchange_declare_default_for_exchange_type(self):
        obj = commands.Exchange.Declare()
        self.assertEqual(obj['exchange_type'], 'direct')

    def test_exchange_declare_default_for_passive(self):
        obj = commands.Exchange.Declare()
        self.assertEqual(obj['passive'], False)

    def test_exchange_declare_default_for_durable(self):
        obj = commands.Exchange.Declare()
        self.assertEqual(obj['durable'], False)

    def test_exchange_declare_default_for_auto_delete(self):
        obj = commands.Exchange.Declare()
        self.assertEqual(obj['auto_delete'], False)

    def test_exchange_declare_default_for_internal(self):
        obj = commands.Exchange.Declare()
        self.assertEqual(obj['internal'], False)

    def test_exchange_declare_default_for_nowait(self):
        obj = commands.Exchange.Declare()
        self.assertEqual(obj['nowait'], False)

    def test_exchange_declare_default_for_arguments(self):
        obj = commands.Exchange.Declare()
        self.assertDictEqual(obj['arguments'], {})

    def test_exchange_delete_default_for_ticket(self):
        obj = commands.Exchange.Delete()
        self.assertEqual(obj['ticket'], 0)

    def test_exchange_delete_default_for_exchange(self):
        obj = commands.Exchange.Delete()
        self.assertEqual(obj['exchange'], '')

    def test_exchange_delete_default_for_if_unused(self):
        obj = commands.Exchange.Delete()
        self.assertEqual(obj['if_unused'], False)

    def test_exchange_delete_default_for_nowait(self):
        obj = commands.Exchange.Delete()
        self.assertEqual(obj['nowait'], False)

    def test_exchange_unbind_default_for_ticket(self):
        obj = commands.Exchange.Unbind()
        self.assertEqual(obj['ticket'], 0)

    def test_exchange_unbind_default_for_destination(self):
        obj = commands.Exchange.Unbind()
        self.assertEqual(obj['destination'], None)

    def test_exchange_unbind_default_for_source(self):
        obj = commands.Exchange.Unbind()
        self.assertEqual(obj['source'], None)

    def test_exchange_unbind_default_for_routing_key(self):
        obj = commands.Exchange.Unbind()
        self.assertEqual(obj['routing_key'], '')

    def test_exchange_unbind_default_for_nowait(self):
        obj = commands.Exchange.Unbind()
        self.assertEqual(obj['nowait'], False)

    def test_exchange_unbind_default_for_arguments(self):
        obj = commands.Exchange.Unbind()
        self.assertDictEqual(obj['arguments'], {})

    def test_queue_bind_default_for_ticket(self):
        obj = commands.Queue.Bind()
        self.assertEqual(obj['ticket'], 0)

    def test_queue_bind_default_for_queue(self):
        obj = commands.Queue.Bind()
        self.assertEqual(obj['queue'], '')

    def test_queue_bind_default_for_exchange(self):
        obj = commands.Queue.Bind()
        self.assertEqual(obj['exchange'], None)

    def test_queue_bind_default_for_routing_key(self):
        obj = commands.Queue.Bind()
        self.assertEqual(obj['routing_key'], '')

    def test_queue_bind_default_for_nowait(self):
        obj = commands.Queue.Bind()
        self.assertEqual(obj['nowait'], False)

    def test_queue_bind_default_for_arguments(self):
        obj = commands.Queue.Bind()
        self.assertDictEqual(obj['arguments'], {})

    def test_queue_declare_default_for_ticket(self):
        obj = commands.Queue.Declare()
        self.assertEqual(obj['ticket'], 0)

    def test_queue_declare_default_for_queue(self):
        obj = commands.Queue.Declare()
        self.assertEqual(obj['queue'], '')

    def test_queue_declare_default_for_passive(self):
        obj = commands.Queue.Declare()
        self.assertEqual(obj['passive'], False)

    def test_queue_declare_default_for_durable(self):
        obj = commands.Queue.Declare()
        self.assertEqual(obj['durable'], False)

    def test_queue_declare_default_for_exclusive(self):
        obj = commands.Queue.Declare()
        self.assertEqual(obj['exclusive'], False)

    def test_queue_declare_default_for_auto_delete(self):
        obj = commands.Queue.Declare()
        self.assertEqual(obj['auto_delete'], False)

    def test_queue_declare_default_for_nowait(self):
        obj = commands.Queue.Declare()
        self.assertEqual(obj['nowait'], False)

    def test_queue_declare_default_for_arguments(self):
        obj = commands.Queue.Declare()
        self.assertDictEqual(obj['arguments'], {})

    def test_queue_declareok_default_for_queue(self):
        obj = commands.Queue.DeclareOk()
        self.assertEqual(obj['queue'], '')

    def test_queue_declareok_default_for_message_count(self):
        obj = commands.Queue.DeclareOk()
        self.assertEqual(obj['message_count'], None)

    def test_queue_declareok_default_for_consumer_count(self):
        obj = commands.Queue.DeclareOk()
        self.assertIsNone(obj['consumer_count'])

    def test_queue_delete_default_for_ticket(self):
        obj = commands.Queue.Delete()
        self.assertEqual(obj['ticket'], 0)

    def test_queue_delete_default_for_queue(self):
        obj = commands.Queue.Delete()
        self.assertEqual(obj['queue'], '')

    def test_queue_delete_default_for_if_unused(self):
        obj = commands.Queue.Delete()
        self.assertEqual(obj['if_unused'], False)

    def test_queue_delete_default_for_if_empty(self):
        obj = commands.Queue.Delete()
        self.assertEqual(obj['if_empty'], False)

    def test_queue_delete_default_for_nowait(self):
        obj = commands.Queue.Delete()
        self.assertEqual(obj['nowait'], False)

    def test_queue_deleteok_default_for_message_count(self):
        obj = commands.Queue.DeleteOk()
        self.assertIsNone(obj['message_count'])

    def test_queue_purge_default_for_ticket(self):
        obj = commands.Queue.Purge()
        self.assertEqual(obj['ticket'], 0)

    def test_queue_purge_default_for_queue(self):
        obj = commands.Queue.Purge()
        self.assertEqual(obj['queue'], '')

    def test_queue_purge_default_for_nowait(self):
        obj = commands.Queue.Purge()
        self.assertEqual(obj['nowait'], False)

    def test_queue_purgeok_default_for_message_count(self):
        obj = commands.Queue.PurgeOk()
        self.assertIsNone(obj['message_count'])

    def test_queue_unbind_default_for_ticket(self):
        obj = commands.Queue.Unbind()
        self.assertEqual(obj['ticket'], 0)

    def test_queue_unbind_default_for_queue(self):
        obj = commands.Queue.Unbind()
        self.assertEqual(obj['queue'], '')

    def test_queue_unbind_default_for_exchange(self):
        obj = commands.Queue.Unbind()
        self.assertEqual(obj['exchange'], None)

    def test_queue_unbind_default_for_routing_key(self):
        obj = commands.Queue.Unbind()
        self.assertEqual(obj['routing_key'], '')

    def test_queue_unbind_default_for_arguments(self):
        obj = commands.Queue.Unbind()
        self.assertDictEqual(obj['arguments'], {})

    def test_basic_properties_repr(self):
        self.assertTrue(repr(
            commands.Basic.Properties()).startswith(
            '<Basic.Properties object'))

    def test_basic_properties_list(self):
        self.assertEqual(
            commands.Basic.Properties.attributes(),
            [
                'content_type', 'content_encoding', 'headers', 'delivery_mode',
                'priority', 'correlation_id', 'reply_to', 'expiration',
                'message_id', 'timestamp', 'message_type', 'user_id', 'app_id',
                'cluster_id'
            ])

    def test_basic_properties_eq_error(self):
        with self.assertRaises(NotImplementedError):
            self.assertEqual(commands.Basic.Properties(), {})


class ValidationErrorTestCase(unittest.TestCase):

    def test_basic_consume_queue_length(self):
        with self.assertRaises(ValueError):
            commands.Basic.Consume(queue=str.ljust('A', 128))

    def test_basic_consume_queue_characters(self):
        with self.assertRaises(ValueError):
            commands.Basic.Consume(queue='*')

    def test_basic_deliver_exchange_length(self):
        with self.assertRaises(ValueError):
            commands.Basic.Deliver(exchange=str.ljust('A', 128))

    def test_basic_deliver_exchange_characters(self):
        with self.assertRaises(ValueError):
            commands.Basic.Deliver(exchange='*')

    def test_basic_get_queue_length(self):
        with self.assertRaises(ValueError):
            commands.Basic.Get(queue=str.ljust('A', 128))

    def test_basic_get_queue_characters(self):
        with self.assertRaises(ValueError):
            commands.Basic.Get(queue='*')

    def test_basic_getok_exchange_length(self):
        with self.assertRaises(ValueError):
            commands.Basic.GetOk(exchange=str.ljust('A', 128))

    def test_basic_getok_exchange_characters(self):
        with self.assertRaises(ValueError):
            commands.Basic.GetOk(exchange='*')

    def test_basic_publish_exchange_length(self):
        with self.assertRaises(ValueError):
            commands.Basic.Publish(exchange=str.ljust('A', 128))

    def test_basic_publish_exchange_characters(self):
        with self.assertRaises(ValueError):
            commands.Basic.Publish(exchange='*')

    def test_basic_return_exchange_length(self):
        with self.assertRaises(ValueError):
            commands.Basic.Return(exchange=str.ljust('A', 128))

    def test_basic_return_exchange_characters(self):
        with self.assertRaises(ValueError):
            commands.Basic.Return(exchange='*')

    def test_connection_open_vhost(self):
        with self.assertRaises(ValueError):
            commands.Connection.Open(str.ljust('A', 128))

    def test_exchange_declare_exchange_length(self):
        with self.assertRaises(ValueError):
            commands.Exchange.Declare(exchange=str.ljust('A', 128))

    def test_exchange_declare_exchange_characters(self):
        with self.assertRaises(ValueError):
            commands.Exchange.Declare(exchange='***')

    def test_exchange_delete_exchange_length(self):
        with self.assertRaises(ValueError):
            commands.Exchange.Delete(exchange=str.ljust('A', 128))

    def test_exchange_delete_exchange_characters(self):
        with self.assertRaises(ValueError):
            commands.Exchange.Delete(exchange='***')

    def test_queue_bind_queue_length(self):
        with self.assertRaises(ValueError):
            commands.Queue.Bind(queue=str.ljust('A', 128), exchange='B')

    def test_queue_bind_queue_characters(self):
        with self.assertRaises(ValueError):
            commands.Queue.Bind(queue='***', exchange='B')

    def test_queue_bind_exchange_length(self):
        with self.assertRaises(ValueError):
            commands.Queue.Bind(exchange=str.ljust('A', 128), queue='B')

    def test_queue_bind_exchange_characters(self):
        with self.assertRaises(ValueError):
            commands.Queue.Bind(exchange='***', queue='B')

    def test_queue_declare_queue_length(self):
        with self.assertRaises(ValueError):
            commands.Queue.Declare(queue=str.ljust('A', 128))

    def test_queue_declare_queue_characters(self):
        with self.assertRaises(ValueError):
            commands.Queue.Declare(queue='***')

    def test_queue_declareok_queue_length(self):
        with self.assertRaises(ValueError):
            commands.Queue.DeclareOk(queue=str.ljust('A', 128))

    def test_queue_declareok_queue_characters(self):
        with self.assertRaises(ValueError):
            commands.Queue.DeclareOk(queue='***')

    def test_queue_delete_queue_length(self):
        with self.assertRaises(ValueError):
            commands.Queue.Delete(queue=str.ljust('A', 128))

    def test_queue_delete_queue_characters(self):
        with self.assertRaises(ValueError):
            commands.Queue.Delete(queue='***')

    def test_queue_purge_queue_length(self):
        with self.assertRaises(ValueError):
            commands.Queue.Purge(queue=str.ljust('A', 128))

    def test_queue_purge_queue_characters(self):
        with self.assertRaises(ValueError):
            commands.Queue.Purge(queue='***')

    def test_queue_unbind_queue_length(self):
        with self.assertRaises(ValueError):
            commands.Queue.Unbind(queue=str.ljust('A', 128), exchange='B')

    def test_queue_unbind_queue_characters(self):
        with self.assertRaises(ValueError):
            commands.Queue.Unbind(queue='***', exchange='B')

    def test_queue_unbind_exchange_length(self):
        with self.assertRaises(ValueError):
            commands.Queue.Unbind(exchange=str.ljust('A', 128), queue='B')

    def test_queue_unbind_exchange_characters(self):
        with self.assertRaises(ValueError):
            commands.Queue.Unbind(exchange='***', queue='B')
