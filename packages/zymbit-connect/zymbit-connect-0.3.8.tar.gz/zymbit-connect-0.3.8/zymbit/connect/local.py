"""
Client class for local Connect server
"""
import json
import logging
import random
import select
import socket

from zymbit import settings
from zymbit.exceptions import NotConnected
from zymbit.util.statemachine import StateMachine
from zymbit.util.time import interval


class LocalClient(StateMachine):
    buffer_size = 4096
    subscriptions = []

    def __init__(self, raise_exceptions=False, loop_sleep_time=None, subscriptions=None):
        super(LocalClient, self).__init__(raise_exceptions=raise_exceptions)

        self.socket = None

        self.loop_sleep_time = loop_sleep_time or self.loop_sleep_time
        self.subscriptions = subscriptions or self.subscriptions

    @property
    def logger(self):
        return logging.getLogger('{}.{}'.format(__name__, self.__class__.__name__))

    def connect(self):
        address = self.get_address()

        self.logger.info('address={}'.format(address))

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(address)
        self.socket.setblocking(0)

        self.logger.debug('connected to {}'.format(address))

    def disconnect(self):
        if self.socket is not None:
            self.socket.close()

    def get_address(self):
        return (settings.CONSOLE_MESSENGER_HOST, settings.CONSOLE_MESSENGER_PORT)

    def handle_buf(self, buf):
        buf_utf8 = buf.decode('utf8')

        try:
            envelope = json.loads(buf_utf8)
            if envelope.get('params', {}).get('routing_key') == 'connection.connected':
                self.subscribe()
        except ValueError:
            pass

        self.handle_message(buf_utf8)

    def handle_message(self, buf):
        self.logger.info(buf)

    def listen(self):
        r, _, _ = select.select([self.socket], [], [], 0.01)
        if self.socket in r:
            buf = self.socket.recv(self.buffer_size)

            self.handle_buf(buf)

        self.publish()

    def publish(self):
        pass

    def send(self, buf):
        if self.socket is None:
            raise NotConnected()

        if not buf.endswith('\n'):
            buf = '{}\n'.format(buf)

        self.socket.send(buf)

    def subscribe(self):
        for subscription in self.subscriptions:
            self.send('action=subscribe,routing_key={}'.format(subscription))

    transitions = {
        StateMachine.start: {
            True: connect,
        },
        connect: {
            None: listen,
            Exception: disconnect,
        },
        disconnect: {
            None: StateMachine.start,
            Exception: StateMachine.start,
        },
        listen: {
            socket.error: disconnect,
            Exception: disconnect,
        },
    }


class ExampleClient(LocalClient):
    subscriptions = [
        '#',
    ]

    @interval(30.0)
    def publish(self):
        value = int(5 * random.random())
        data = 'key=foo,value={}'.format(value)

        self.send(data)


if __name__ == '__main__':
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    client = ExampleClient()
    client.run()
