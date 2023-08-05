import websocket

from zymbit.settings import CHECK_HOSTNAME, WEBSOCKET_ENDPOINT, WEBSOCKET_SEND_CLIENT_INFO
from zymbit.upstream.api import ZymbitApi
from zymbit.util.client import get_client_info


def get_websocket():
    sslopt = {"check_hostname": CHECK_HOSTNAME}
    url = get_websocket_url()

    ws = websocket.create_connection(url, sslopt=sslopt)
    ws.settimeout(0)

    return ws


def get_websocket_url():
    params = {}

    if WEBSOCKET_SEND_CLIENT_INFO:
        params.update(get_client_info())

    api = ZymbitApi()
    response = api.get(WEBSOCKET_ENDPOINT, params=params)

    return response.json()
