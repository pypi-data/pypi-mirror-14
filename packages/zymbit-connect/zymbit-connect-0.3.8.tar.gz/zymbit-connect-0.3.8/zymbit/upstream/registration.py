import os

from zymbit import settings
from zymbit.upstream.api import ZymbitApi
from zymbit.util import get_device_meta
from zymbit.util.client import get_auth_path, get_client_info


def register():
    """
    Makes the bootstrap request upstream
    """
    post_data = {}
    post_data.update(get_device_meta())
    post_data.update(get_client_info())

    api = ZymbitApi()

    settings_dict = {}
    for item in dir(settings):
        settings_dict[item] = getattr(settings, item)

    endpoint = settings.REGISTER_ENDPOINT.format(**settings_dict)
    response = api.post(endpoint, data=post_data)
    response.raise_for_status()

    write_auth(response.json())


def write_auth(data):
    auth_token = data['grains']['zymbit']['zymbot']['auth_token']
    write_auth_token(auth_token)


def write_auth_token(auth_token):
    auth_path = get_auth_path()
    auth_root = os.path.dirname(auth_path)
    if not os.path.exists(auth_root):
        os.makedirs(auth_root)

    with open(auth_path, 'wb') as fh:
        fh.write(auth_token)
