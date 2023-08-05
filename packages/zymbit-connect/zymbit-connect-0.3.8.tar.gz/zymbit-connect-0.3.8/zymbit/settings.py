import os

from conversion import convert_bool

API_URL = os.environ.get('API_URL', 'https://zymbit.com/api/v1')
AUTH_ROOT = '/etc/zymbit/auth'
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
BOOTSTRAP_KEY = os.environ.get('BOOTSTRAP_KEY')
CHECK_HOSTNAME = convert_bool(os.environ.get('CHECK_HOSTNAME', 'true'))
CLIENT_ID_VERSION = os.environ.get('CLIENT_ID_VERSION')
PUBSUB_PING_INTERVAL = int(os.environ.get('PUBSUB_PING_INTERVAL', 300))
REGISTER_ENDPOINT = '/zymbots/register?key={BOOTSTRAP_KEY}'
WEBSOCKET_ENDPOINT = '/websocket_url'
WEBSOCKET_SEND_CLIENT_INFO = convert_bool(os.environ.get('WEBSOCKET_SEND_CLIENT_INFO', 'true'))
ZYMBIT_RUN_PATH = '/run/zymbit'
ZYMBIT_HOST_INFO_PATH = os.path.join(ZYMBIT_RUN_PATH, 'host_info')

CONNECT_PORT_9628_TCP_ADDR = os.environ.get('CONNECT_PORT_9628_TCP_ADDR', '0.0.0.0')
CONNECT_PORT_9628_TCP_PORT = int(os.environ.get('CONNECT_PORT_9628_TCP_PORT', 9628))

CONSOLE_MESSENGER_HOST = os.environ.get('CONSOLE_MESSENGER_HOST', CONNECT_PORT_9628_TCP_ADDR)
CONSOLE_MESSENGER_PORT = int(os.environ.get('CONSOLE_MESSENGER_PORT', CONNECT_PORT_9628_TCP_PORT))
