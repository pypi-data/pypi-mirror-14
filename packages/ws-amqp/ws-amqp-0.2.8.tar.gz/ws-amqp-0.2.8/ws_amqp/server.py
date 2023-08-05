import json
import logging
import threading
import time

import amqp

logger = logging.getLogger(__name__)


class Server(object):
    def __init__(self, name='', prefix='ws', threaded=False, host='localhost', user='guest', password='guest',
                 vhost='/', dumper=None):
        if not prefix.endswith('_'):
            prefix += '_'
        if len(name) > 0 and not name.endswith('_'):
            name += '_'
        self.credentials = {
            'host': host,
            'userid': user,
            'password': password,
            'virtual_host': vhost
        }
        if dumper is None:
            dumper = json
        self.dumper = dumper
        self.prefix = prefix
        self.name = name
        self.exchange_name = self.prefix + 'exchange'
        self.queue_name = self.prefix + name + 'queue'
        self.threaded = threaded
        self.connection = None
        self.channel = None
        self.endpoints = {}

    def register_endpoint(self, name, endpoint):
        self.endpoints[(self.prefix + self.name + name).replace('_', '.')] = endpoint

    def connect(self):
        self.connection = amqp.Connection(**self.credentials)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(self.exchange_name, 'topic')
        self.channel.basic_qos(0, 1, False)
        self.channel.queue_declare(self.queue_name)
        self.prepare_queues()

    def prepare_queues(self):
        for name in self.endpoints.keys():
            self.channel.queue_bind(self.queue_name, self.exchange_name, routing_key=name)
            self.channel.basic_consume(self.queue_name, callback=self.consume)
            logger.debug('Endpoint %s bound to %s', name, self.queue_name)

    def handle(self, message):
        logger.debug('Starting execution')
        endpoint = self.endpoints.get(message.delivery_info['routing_key'])
        try:
            msg = self.dumper.loads(message.body)
            result = endpoint(*msg.get('args', []), **msg.get('kwargs', {}))
        except Exception as e:
            result = e
        logger.debug('Execution ended')
        if message.properties.get('reply_to'):
            try:
                body = self.dumper.dumps(result)
            except Exception:
                body = self.dumper.dumps({'error': 'Error dump result'})
            logger.debug(
                'Sending a reply %s to %s with correlation id %s', body, message.properties['reply_to'],
                message.properties['correlation_id']
            )
            self.channel.basic_publish(
                amqp.Message(body, correlation_id=message.properties['correlation_id']),
                routing_key=message.properties['reply_to']
            )
        return result

    def consume(self, message):
        message.channel.basic_ack(message.delivery_tag)
        logger.debug('Message %s with routing key %s received', message.body, message.delivery_info['routing_key'])
        if self.threaded:
            p = threading.Thread(target=self.handle, args=(message,))
            p.daemon = True
            p.start()
        else:
            self.handle(message)

    def start(self):
        logger.debug('Start consuming')
        try:
            self.connect()
            while True:
                self.channel.wait()
        except KeyboardInterrupt:
            logger.debug('Stop consuming')
            self.channel.close()
            self.connection.close()
        except Exception as e:
            try:
                self.channel.close()
            except Exception:
                pass
            try:
                self.connection.close()
            except Exception:
                pass
            logger.error(e)
            logger.debug('Reconnect')
            time.sleep(5)
            self.start()
