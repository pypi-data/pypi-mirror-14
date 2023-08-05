"""
Connect to the pubsub engine
"""
import datetime
import logging
import math

from _ssl import SSLWantReadError

from zymbit import settings
from zymbit.exceptions import NotConnected, Disconnect
from zymbit.upstream import registration
from zymbit.upstream.ws import get_websocket
from zymbit.util.client import get_auth_token
from zymbit.util.envelope import get_envelope
from zymbit.util.statemachine import StateMachine, NO_SLEEP
from zymbit.util.time import now

NO_DELTA = datetime.timedelta(seconds=0)


class PubSubStateMachine(StateMachine):
    """
    State machine to keep connect to the pubsub engine

    This state machine handles bootstrapping a system when it's not yet
    registered and once registered, establish a persistent connection to
    the pubsub engine
    """
    def __init__(self, raise_exceptions=True, message_handler=None, subscriptions=None):
        super(PubSubStateMachine, self).__init__(raise_exceptions=raise_exceptions)

        self.message_handler = message_handler

        self.registration_retries = 0
        self.next_registration_attempt = None
        self.registration_retry_max_sleep = 3600  # sleep up to an hour

        self.subscriptions = subscriptions or []

        self.websocket = None

        # set last_read to instantiation time so that ping pong is played after
        # the connection has been established
        self.last_read = now()
        self.last_ping = self.last_read

        # play ping pong after a minute of silence
        self.ping_interval = datetime.timedelta(seconds=settings.PUBSUB_PING_INTERVAL)

    @property
    def logger(self):
        return logging.getLogger('{}.{}'.format(__name__, self.__class__.__name__))

    def send(self, envelope):
        if self.websocket is None:
            raise NotConnected()

        self.websocket.send(envelope)

    ##
    # State machine methods
    ##

    def init(self):
        if self.message_handler:
            self.message_handler(get_envelope('proxy', dict(routing_key='proxy.init')))

    def check_last_read(self):
        _now = now()

        next_ping_check = self.last_read + self.ping_interval
        if (next_ping_check - _now) < NO_DELTA:
            # only send pings once per max_silence_time
            next_ping = self.last_ping + self.ping_interval
            if (next_ping - _now) < NO_DELTA:
                self.logger.debug('sending ping')
                self.websocket.send(get_envelope('ping', {}))
                self.last_ping = _now

        # check if a re-connect is in order
        disconnect_time = self.last_read + (self.ping_interval * 3)
        if (disconnect_time - _now) < NO_DELTA:
            raise Disconnect()

    def connect(self):
        """
        Connects to the pubsub engine
        """
        self.websocket = get_websocket()

        # set last_read here so that we are not immediately disconnected by check_last_read()
        self.last_read = now()

    def disconnect(self):
        """
        Disconnects from the pubsub engine
        """
        if self.message_handler:
            self.message_handler(get_envelope('connection', dict(routing_key='connection.disconnected')))

        if self.websocket is None:
            return

        ws, self.websocket = self.websocket, None

        ws.close()

    def handle_message(self, buf):
        if self.message_handler:
            self.message_handler(buf)
        else:
            self.logger.info(repr(buf))

    def has_auth_token(self):
        """
        Checks whether this device has an auth token
        """
        return get_auth_token() is not None

    def listen(self):
        """
        Listens for upstream messages and sends up local messages
        """
        try:
            buf = self.websocket.recv()
        except SSLWantReadError:  # seems to be raised when there is no data
            buf = None

        if buf:
            self.last_read = now()
            self.handle_message(buf)

            return NO_SLEEP

        self.check_last_read()

    def register(self):
        """
        Registers the system with zymbit services
        """
        # check to see if a registration attempt should be made
        if self.next_registration_attempt:
            _now = now()
            # when there is a positive delta between now and the next registration attempt
            # simply return
            if (self.next_registration_attempt - _now) > NO_DELTA:
                return False

            self.next_registration_attempt = None

        registration.register()

        self.registration_retries = 0

    def registration_error(self):
        self.logger.exception(self.last_exception)

        self.registration_retries += 1
        sleep_time = min(math.pow(2, self.registration_retries), self.registration_retry_max_sleep)
        self.next_registration_attempt = now() + datetime.timedelta(seconds=sleep_time)

        self.logger.error('Registration error; next retry at {}'.format(self.next_registration_attempt))

    def subscribe(self):
        """
        Subscribes to desired streams
        """
        for subscription in self.subscriptions:
            if isinstance(subscription, dict):
                params = subscription
            else:
                params = dict(routing_key=subscription)

            envelope = get_envelope('subscribe', params=params)
            self.websocket.send(envelope)

    transitions = {
        StateMachine.start: {
            True: init,
        },
        init: {
            None: has_auth_token,
        },
        has_auth_token: {
            False: register,
            True: connect,
        },
        register: {
            None: connect,
            Exception: registration_error,
        },
        registration_error: {
            None: StateMachine.start,
        },
        connect: {
            None: subscribe,
            Exception: disconnect,
        },
        disconnect: {
            None: StateMachine.start,
            Exception: StateMachine.start,
        },
        subscribe: {
            None: listen,
            Exception: disconnect,
        },
        listen: {
            Exception: disconnect,
        },
    }


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    PubSubStateMachine(raise_exceptions=False).run()
