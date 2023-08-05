import logging
import socket

from select import select

from zymbit import settings
from zymbit.util.envelope import get_envelope

BUFSIZE = 4096


class BaseServer(object):
    def __init__(self, host, port, message_handler=None):
        self.addr = (host, port)

        self._tcp_sock = None
        self._udp_sock = None

        self.connections = {}

        self.message_handler = message_handler

        self._run = True

    @property
    def logger(self):
        logger_name = '{}.{}'.format(__name__, self.__class__.__name__)
        return logging.getLogger(logger_name)

    @property
    def tcp_sock(self):
        if self._tcp_sock:
            return self._tcp_sock

        try:
            self._tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self._tcp_sock.setblocking(0)
            self._tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._tcp_sock.bind(self.addr)
            self._tcp_sock.listen(128)  # max 128 clients
        except socket.error:
            self.logger.warning('Unable to bind TCP socket at addr={}'.format(self.addr))
        else:
            self.logger.info("Listening on TCP addr={}".format(self.addr))

        return self._tcp_sock

    @property
    def udp_sock(self):
        if self._udp_sock:
            return self._udp_sock

        try:
            self._udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            self._udp_sock.setblocking(0)
            self._udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._udp_sock.bind(self.addr)
        except socket.error:
            self.logger.warning('Unable to bind UDP socket at addr={}'.format(self.addr))
        else:
            self.logger.info("Listening on UDP addr={}".format(self.addr))

        return self._udp_sock

    def broadcast(self, message):
        for connection in self.connections:
            self.send(connection, message)

    def close_tcp(self):
        self._tcp_sock = None

    def close_udp(self):
        self._udp_sock = None

    def connect(self, info):
        message = get_envelope('connection', dict(routing_key='connection.connected'))

        conn, addr = info
        self.logger.info('%s, %s %s' % (conn, addr, message))

        self.connections[conn] = addr

        self.handle_message(conn, message)

    def disconnect(self, connection):
        message = get_envelope('connection', dict(routing_key='connection.disconnected'))

        addr = self.connections.pop(connection)
        self.logger.info('%s, %s %s' % (connection, addr, message))

        self.handle_message(connection, message)

    def fileno(self):
        return self.tcp_sock.fileno()

    def handle_message(self, client, buf):
        if self.message_handler:
            self.message_handler(client, buf)
        else:
            self.logger.info('client={}, buf={}'.format(client, buf))

    def loop(self, select_timeout=1.0):
        handled = None

        # check UDP
        try:
            buf, client = self.udp_sock.recvfrom(1024)
        except socket.error as exc:
            # (11, 'Resource temporarily unavailable')
            # [Errno 35] Resource temporarily unavailable
            error_number = exc[0]
            if error_number not in (11, 35):
                self.logger.exception(exc)
                self.logger.warning('got socket error_number={}'.format(error_number))

                self.close_udp()
        else:
            if buf:
                self.handle_message(client, buf)
                handled = True

        try:
            self.connect(self.tcp_sock.accept())
        except socket.error as exc:
            # (11, 'Resource temporarily unavailable')
            # [Errno 35] Resource temporarily unavailable
            error_number = exc[0]
            if error_number not in (11, 35):
                self.logger.exception(exc)
                self.logger.warning('got socket error_number={}'.format(error_number))

                self.close_tcp()

        ready, _, _ = select(self.connections, [], [], select_timeout)

        for client in ready:
            try:
                buf = client.recv(BUFSIZE)
                if buf == '':
                    self.disconnect(client)
                    continue
            except socket.error as exc:
                # [Errno 54] Connection reset by peer
                # [Errno 104] Connection reset by peer -- raspbian
                error_number = exc[0]
                if error_number not in (54, 104):
                    self.logger.exception(exc)
                    self.logger.warning('got socket error_number={}'.format(error_number))

                self.disconnect(client)
                continue

            self.handle_message(client, buf)
            handled = True

        return handled

    def quit(self):
        self.tcp_sock.close()
        self.udp_sock.close()

        # prevent getting exception where dictionary changes while looping
        connections = list(self.connections.keys())
        for connection in connections:
            self.disconnect(connection)

    def run(self):
        while self._run:
            self.loop()

    def send(self, connection, buf):
        try:
            connection.send(buf)
        except Exception as exc:
            self.logger.exception(exc)
            self.logger.error('error sending connection={}, buf={}'.format(connection, buf))


class ConsoleMessengerServer(BaseServer):
    def __init__(self, message_handler):
        super(ConsoleMessengerServer, self).__init__(
                settings.CONSOLE_MESSENGER_HOST,
                settings.CONSOLE_MESSENGER_PORT,
                message_handler=message_handler
        )
