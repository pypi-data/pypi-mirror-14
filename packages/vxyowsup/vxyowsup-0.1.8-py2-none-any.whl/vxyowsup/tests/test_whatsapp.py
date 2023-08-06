# -*- coding: UTF-8 -*-

import base64
import time

from twisted.internet.defer import inlineCallbacks, DeferredQueue
from twisted.internet import reactor

from vumi.tests.helpers import VumiTestCase
from vumi.message import TransportUserMessage
from vumi.transports.tests.helpers import TransportHelper

from vxyowsup.whatsapp import WhatsAppTransport, msisdn_to_whatsapp
from yowsup.stacks import YowStackBuilder
from yowsup.layers.logger import YowLoggerLayer
from yowsup.layers import YowLayer
from yowsup.layers.interface import YowInterfaceLayer
from yowsup.layers.protocol_messages.protocolentities import (
    TextMessageProtocolEntity)
from yowsup.layers.protocol_acks.protocolentities import AckProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import (
    IncomingReceiptProtocolEntity)
from yowsup.layers.interface.interface import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer


string_of_doom = u"Zoë the Destroyer of ASCII".encode("UTF-8")


@staticmethod
def getDummyCoreLayers():
    return (TestingLayer, YowLoggerLayer)


def TUMessage_to_PTNode(message):
    '''
    message is TransportUserMessage
    returns ProtocolTreeNode
    '''
    return TextMessageProtocolEntity(
        message['content'].encode("UTF-8"), to=message['to_addr'] +
        '@s.whatsapp.net').toProtocolTreeNode()


def PTNode_to_TUMessage(node, to_addr):
    '''
    node is ProtocolTreeNode
    returns TransportUserMessage
    '''
    message = TextMessageProtocolEntity.fromProtocolTreeNode(node)
    return TransportUserMessage(
        to_addr=to_addr, from_addr="+" + message.getFrom(False),
        content=message.getBody().decode("UTF-8"), transport_name='whatsapp',
        transport_type='whatsapp')


class TestWhatsAppTransport(VumiTestCase):

    @inlineCallbacks
    def setUp(self):
        self.patch(YowStackBuilder, 'getCoreLayers', getDummyCoreLayers)
        self.patch(
            YowInterfaceLayer, 'getLayerInterface', dummy_getLayerInterface)
        self.tx_helper = self.add_helper(TransportHelper(WhatsAppTransport))
        self.config = {
            'cc': '27',
            'phone': '27010203040',
            'password': base64.b64encode("xxx"),
            'publish_status': True,
        }

        self.transport = yield self.tx_helper.get_transport(self.config)
        self.testing_layer = self.transport.stack_client.network_layer
        self.redis = self.transport.redis

    def assert_id_format_correct(self, node):
        uuid, _sep, count = node["id"].partition('-')
        self.assertEqual(len(uuid), 10)
        self.assertTrue(int(count) > 0)

    def assert_nodes_equal(self, node1, node2):
        self.assert_id_format_correct(node1)
        self.assert_id_format_correct(node2)
        id_stub = node1["id"].split('-')[0]
        xml1 = node1.toString().replace(node1["id"], id_stub)
        xml2 = node2.toString().replace(node2["id"], id_stub)
        self.assertEqual(xml1, xml2)

    def assert_messages_equal(self, message1, message2):
        '''
        assert two instances of TransportUserMessage are equal
        '''
        self.assertEqual(message1['content'], message2['content'])
        self.assertEqual(message1['to_addr'], message2['to_addr'])
        self.assertEqual(message1['from_addr'], message2['from_addr'])

    @inlineCallbacks
    def assert_ack(self, ack, node):
        whatsapp_id = node['id']
        vumi_id = yield self.redis.get(whatsapp_id)
        self.assertEqual(ack.payload['event_type'], 'ack')
        self.assertEqual(ack.payload['user_message_id'], vumi_id)
        self.assertEqual(ack.payload['sent_message_id'], whatsapp_id)

    def assert_receipt(self, receipt, node, message_id):
        '''Assert that the receipt is valid. We need to pass in the expected
        message id, because the transport deletes the reference after it sends
        the delivery report.'''
        self.assertEqual(receipt.payload['event_type'], 'delivery_report')
        self.assertEqual(receipt.payload['user_message_id'], message_id)
        self.assertEqual(receipt.payload['delivery_status'], 'delivered')

    def add_auth_skip(self, number):
        # Layer 2 is the axolotl authentication layer
        layer = self.transport.stack_client.stack.getLayer(2)
        jid = msisdn_to_whatsapp(number)
        layer.skipEncJids.append(jid)

    @inlineCallbacks
    def test_outbound(self):
        self.add_auth_skip(self.config.get('phone'))
        message_sent = yield self.tx_helper.make_dispatch_outbound(
            content='fail!', to_addr=self.config.get('phone'),
            from_addr='vumi')
        node_received = yield self.testing_layer.data_received.get()
        self.assert_nodes_equal(
            TUMessage_to_PTNode(message_sent), node_received)

        acks = self.tx_helper.get_dispatched_events()
        self.assertFalse(acks)

        self.testing_layer.send_ack(node_received)
        [ack] = yield self.tx_helper.wait_for_dispatched_events(1)
        yield self.assert_ack(ack, node_received)

        self.tx_helper.clear_dispatched_events()

        self.testing_layer.send_receipt(node_received)
        [receipt] = yield self.tx_helper.wait_for_dispatched_events(1)
        self.assert_receipt(receipt, node_received, message_sent['message_id'])

        vumi_id = yield self.redis.get(node_received['id'])
        self.assertFalse(vumi_id)

        self.tx_helper.clear_dispatched_events()

        self.testing_layer.send_receipt(node_received, 'read')
        receipts = self.tx_helper.get_dispatched_events()
        self.assertFalse(receipts)

    @inlineCallbacks
    def test_publish(self):
        message_sent = yield self.testing_layer.send_to_transport(
            text='Hi Vumi! :)',
            from_address='123345@s.whatsapp.net')
        [message_received] = (
            yield self.tx_helper.wait_for_dispatched_inbound(1))
        self.assert_messages_equal(
            PTNode_to_TUMessage(message_sent, '+27010203040'),
            message_received)

    @inlineCallbacks
    def test_non_ascii_outbound(self):
        self.add_auth_skip(self.config.get('phone'))
        message_sent = yield self.tx_helper.make_dispatch_outbound(
            content=string_of_doom.decode("UTF-8"),
            to_addr=self.config.get('phone'), from_addr='vumi')
        node_received = yield self.testing_layer.data_received.get()
        self.assert_nodes_equal(
            TUMessage_to_PTNode(message_sent), node_received)

        acks = self.tx_helper.get_dispatched_events()
        self.assertFalse(acks)

        self.testing_layer.send_ack(node_received)
        [ack] = yield self.tx_helper.wait_for_dispatched_events(1)
        yield self.assert_ack(ack, node_received)

        self.tx_helper.clear_dispatched_events()

        self.testing_layer.send_receipt(node_received)
        [receipt] = yield self.tx_helper.wait_for_dispatched_events(1)
        self.assert_receipt(
            receipt, node_received, message_sent['message_id'])

        vumi_id = yield self.redis.get(node_received['id'])
        self.assertFalse(vumi_id)

        self.tx_helper.clear_dispatched_events()

        self.testing_layer.send_receipt(node_received, 'read')
        receipts = self.tx_helper.get_dispatched_events()
        self.assertFalse(receipts)

    @inlineCallbacks
    def test_non_ascii_publish(self):
        message_sent = self.testing_layer.send_to_transport(
            text=string_of_doom,
            from_address='123345@s.whatsapp.net')
        [message_received] = (
            yield self.tx_helper.wait_for_dispatched_inbound(1))
        self.assert_messages_equal(
            PTNode_to_TUMessage(message_sent, '+27010203040'),
            message_received)

    @inlineCallbacks
    def test_cannot_decode_message(self):
        '''When the inbound message cannot be decoded, we should send a
        degraded status message.'''
        self.testing_layer.send_to_transport(
            text=u'Hi Vumi! :)'.encode('utf-16'),
            from_address='123345@s.whatsapp.net')
        [status] = yield self.tx_helper.wait_for_dispatched_statuses(1)
        self.assertEqual(status['status'], 'degraded')
        self.assertEqual(status['component'], 'inbound')
        self.assertEqual(status['type'], 'inbound_error')
        self.assertEqual(status['message'], 'Cannot decode')

    @inlineCallbacks
    def test_status_message_for_inbound_message(self):
        '''If we are successfully able to decode the inbound message, we should
        send a successful status message.'''
        self.testing_layer.send_to_transport(
            text='Hi Vumi! :)',
            from_address='123345@s.whatsapp.net')
        [status] = yield self.tx_helper.wait_for_dispatched_statuses(1)
        self.assertEqual(status['status'], 'ok')
        self.assertEqual(status['component'], 'inbound')
        self.assertEqual(status['type'], 'inbound_success')
        self.assertEqual(
            status['message'], 'Inbound message successfully processed')

    @inlineCallbacks
    def test_repeat_status(self):
        '''If two status messages are sent for the same component with the
        same status, only one of them should go through.'''
        self.testing_layer.send_to_transport(
            text='Hi Vumi! :)',
            from_address='123345@s.whatsapp.net')
        yield self.transport.add_status(
            component='inbound', status='ok', type='inbound_success',
            message='Inbound message successfully processed')
        statuses = yield self.tx_helper.get_dispatched_statuses()
        self.assertEqual(len(statuses), 1)

    @inlineCallbacks
    def test_connect_status(self):
        '''When we get a connection, the connection component status should
        be "okay".'''
        self.testing_layer.connect()
        [status] = yield self.tx_helper.wait_for_dispatched_statuses(1)
        self.assertEqual(status['status'], 'ok')
        self.assertEqual(status['component'], 'connection')
        self.assertEqual(status['type'], 'connected')
        self.assertEqual(status['message'], 'Successfully connected to server')

    @inlineCallbacks
    def test_disconnect_status(self):
        '''When we get a disconnection, the connection component status should
        be "down".'''
        self.testing_layer.disconnect()
        [status, status_recon] = (
            yield self.tx_helper.wait_for_dispatched_statuses(1))
        self.assertEqual(status['status'], 'down')
        self.assertEqual(status['component'], 'connection')
        self.assertEqual(status['type'], 'disconnected')
        self.assertEqual(status['message'], 'Test disconnect')

        self.assertEqual(status_recon['status'], 'ok')
        self.assertEqual(status_recon['component'], 'connection')
        self.assertEqual(status_recon['type'], 'connected')
        self.assertEqual(
            status_recon['message'], 'Successfully connected to server')


def dummy_getLayerInterface(parent_interface, layer_cls):
    if layer_cls.__name__ == 'YowNetworkLayer':
        return DummyNetworkLayer()


class DummyNetworkLayer(object):
    def connect(self):
        pass


class TestingLayer(YowLayer):

    def __init__(self):
        YowLayer.__init__(self)
        self.data_received = DeferredQueue()

    def receive(self, data):
        '''
        data would've been decrypted bytes, but in the testing layer they're
        yowsup.structs.protocoltreenode.ProtocolTreeNode
        for convenience
        receive from lower (no lower in this layer)
        send to upper
        '''
        self.toUpper(data)

    def send_ack(self, node):
        # TODO: rather send IncomingAckProtocolEntity and test extra fields
        ack = AckProtocolEntity(_id=node['id'], _class='message')
        self.receive(ack.toProtocolTreeNode())

    def send_receipt(self, node, status=None):
        # status=None defualt indicates 'delivered'
        # alt: status='read'
        receipt = IncomingReceiptProtocolEntity(
            _id=node['id'], _from=node['to'],
            timestamp=str(int(time.time())), type=status)
        self.receive(receipt.toProtocolTreeNode())

    def send(self, data):
        '''
        data is yowsup.structs.protocoltreenode.ProtocolTreeNode
        receive from upper
        send to lower (no lower in this layer)
        '''
        reactor.callFromThread(self.data_received.put, data)

    def send_to_transport(self, text, from_address):
        '''method to be used in testing'''
        message = TextMessageProtocolEntity(
            text, _from=from_address).toProtocolTreeNode()
        self.receive(message)
        return message

    def connect(self):
        self.emitEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECTED))

    def disconnect(self):
        self.emitEvent(YowLayerEvent(
            YowNetworkLayer.EVENT_STATE_DISCONNECTED,
            reason='Test disconnect'))

    def onEvent(self, event):
        if event.getName() == YowNetworkLayer.EVENT_STATE_CONNECT:
            # Automatically say that we're connected for connect requests
            self.connect()
