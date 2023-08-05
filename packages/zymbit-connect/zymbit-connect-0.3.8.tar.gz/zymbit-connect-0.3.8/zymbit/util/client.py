import hashlib
import json
import os
import re

from zymbit.settings import AUTH_ROOT, AUTH_TOKEN, CLIENT_ID_VERSION, ZYMBIT_HOST_INFO_PATH

MAC_RE = re.compile(r'.*HWaddr (?P<hwaddr>[^ ]+)')
SDCARD_ATTRS_RE = re.compile(r'ATTRS{(?P<key>[^}]+)}=="(?P<value>[^"]+)"')


def get_auth_path():
    client_id = get_client_id()
    return os.path.join(AUTH_ROOT, client_id)


def get_auth_token():
    auth_token = AUTH_TOKEN
    if auth_token is not None:
        return auth_token

    auth_path = get_auth_path()

    if os.path.exists(auth_path):
        with open(auth_path, 'rb') as fh:
            auth_token = fh.read().strip()

    return auth_token


def get_cpu_info():
    """
    Returns CPU identification information
    :return:
    """
    info = {
        'cpu_hardware': None,
        'cpu_revision': None,
        'cpu_serial': None,
    }

    with open(os.path.join(ZYMBIT_HOST_INFO_PATH, 'cpu')) as fh:
        content = fh.read()

    for line in content.splitlines():
        line = line.strip()
        if line == '':
            continue

        line_split = line.split(':', 1)
        key = 'cpu_{}'.format(line_split[0].strip().replace(' ', '_').lower())

        if key not in list(info.keys()):
            continue

        info[key] = line_split[1].strip()

    return info


def get_eth0_info():
    """
    Returns eth0 identification information
    :return:
    """
    info = {
        'eth0_hwaddr': None
    }

    with open(os.path.join(ZYMBIT_HOST_INFO_PATH, 'eth0')) as fh:
        content = fh.read()

    for line in content.splitlines():
        matches = MAC_RE.match(line)
        if not matches:
            continue

        info['eth0_hwaddr'] = matches.group('hwaddr')

    return info


def get_sdcard_info():
    """
    Returns sdcard identification information
    :return dict: sdcard information
    """
    info = {
        'sdcard_manfid': None,
        'sdcard_serial': None,
    }

    with open(os.path.join(ZYMBIT_HOST_INFO_PATH, 'sdcard')) as fh:
        content = fh.read()

    for line in content.splitlines():
        matches = SDCARD_ATTRS_RE.match(line.strip())
        if not matches:
            continue

        key = 'sdcard_{}'.format(matches.group('key'))
        if key not in list(info.keys()):
            continue

        info[key] = matches.group('value')

    return info


def get_client_id():
    if CLIENT_ID_VERSION is None:
        return get_client_id_latest()

    return globals()['get_client_id_v{}'.format(CLIENT_ID_VERSION)]()


def get_client_id_v0():
    info = get_eth0_info()

    return info['eth0_hwaddr']


def get_client_id_v1():
    info = get_client_info()

    # the client_id is the hash of a JSON representation of an array of (key, value) 2-tuples
    data = json.dumps(sorted(list(info.items()), key=lambda a: a[0]))
    sha = hashlib.sha1(data)

    return sha.hexdigest()


# alias the default get_client_id to v1
get_client_id_latest = get_client_id_v1


def get_client_info():
    info = {}

    info.update(get_cpu_info())
    info.update(get_eth0_info())
    info.update(get_sdcard_info())

    return info
