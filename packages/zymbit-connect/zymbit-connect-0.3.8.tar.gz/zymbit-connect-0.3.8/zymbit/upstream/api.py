import functools
import requests

from zymbit import settings
from zymbit.util.client import get_auth_token
from zymbit.util.version import get_version


class ZymbitApi(object):
    ConnectionError = requests.ConnectionError
    HTTPError = requests.HTTPError

    def __init__(self, auth_token=None):
        self._auth_token = auth_token

        self.session = requests.session()
        self.response = None

    def __getattribute__(self, item):
        if item in ('delete', 'get', 'patch', 'post', 'put'):
            request = super(ZymbitApi, self).__getattribute__('request')
            return functools.partial(request, item)

        return super(ZymbitApi, self).__getattribute__(item)

    @property
    def auth_token(self):
        if self._auth_token:
            return self._auth_token

        self._auth_token = get_auth_token()

        return self._auth_token

    def request(self, method, endpoint, **kwargs):
        headers = kwargs.pop('headers', {})
        headers['User-Agent'] = 'Zymbit Connect {}'.format(get_version())

        if 'Authorization' not in headers:
            if self.auth_token:
                headers['Authorization'] = 'Token {}'.format(self.auth_token)

        kwargs['headers'] = headers

        if 'verify' not in kwargs:
            kwargs['verify'] = settings.CHECK_HOSTNAME

        api_url = settings.API_URL
        url = '{}{}'.format(api_url, endpoint)

        method_fn = getattr(self.session, method)
        try:
            self.response = method_fn(url, **kwargs)
        except requests.ConnectionError as exc:
            raise requests.ConnectionError('Unable to connect to url={}'.format(url))
        else:
            self.response.raise_for_status()

        return self.response
