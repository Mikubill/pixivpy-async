# -*- coding:utf-8 -*-
import json
import re
from urllib.parse import urlparse, unquote


class Utils:

    @staticmethod
    async def down_request(_session, _url, _referer):
        async with _session.get(_url, headers={'Referer': _referer}) as response:
            return await response.read()

    @staticmethod
    async def auth_request(_session, _url, _headers, _data):
        async with _session.post(_url, headers=_headers, data=_data) as response:
            await response.json(), response.status in [200, 301, 302], response.status

    @staticmethod
    async def fetch(_session, _url, _headers, _params):
        async with _session.get(_url, headers=_headers, params=_params) as response:
            return await response.json()

    @staticmethod
    async def post(_session, _url, _data, _headers, _params):
        async with _session.post(_url, data=_data, headers=_headers, params=_params) as response:
            return await response.json()

    @staticmethod
    async def delete(_session, _url, _headers, _params):
        async with _session.delete(_url, headers=_headers, params=_params) as response:
            return await response.json()

    @staticmethod
    def set_public_headers(headers, token):
        if 'Referer' not in headers or headers['Referer'] == '':
            headers.update({'Referer': 'http://spapi.pixiv.net/'})
        if 'User-Agent' not in headers or headers['User-Agent'] == '':
            headers.update({'User-Agent': 'PixivIOSApp/5.8.7'})
        headers.update({'Authorization': 'Bearer {}'.format(token)})
        return headers

    @staticmethod
    def set_app_headers(headers, token):
        default_headers = {
            'App-OS': 'ios',
            'App-OS-Version': '12.2',
            'App-Version': '7.6.2',
            'User-Agent': 'PixivIOSApp/7.6.2 (iOS 12.2; iPhone9,1)'
        }
        if headers.get('User-Agent', None) is None and headers.get('user-agent', None) is None:
            headers.update(default_headers)
        if token:
            headers.update({'Authorization': 'Bearer {}'.format(token)})
        return headers

    @staticmethod
    def set_params(**kwargs):
        result = dict()
        for key, value in kwargs:
            if value is not None:
                if isinstance(value, str) or isinstance(value, int):
                    result.update(
                        {key: value}
                    )
                elif isinstance(value, list):
                    result.update(
                        {key: ','.join(map(str, value))}
                    )
                elif isinstance(value, bool):
                    result.update(
                        {key: str(value).lower()}
                    )
        return result

    @staticmethod
    def parse_json(_):
        def _obj_hook(pairs):
            o = JsonDict()
            for k, v in pairs.items():
                o[str(k)] = v
            return o

        return json.loads(json.dumps(_), object_hook=_obj_hook)

    @staticmethod
    async def parse_qs(next_url):
        if not next_url:
            return None
        result_qs = {}
        query = urlparse(next_url).query
        for kv in query.split('&'):
            k, v = map(lambda s: unquote(s), kv.split('='))
            matched = re.match(r'(?P<key>[\w]*)\[(?P<idx>[\w]*)\]', k)
            if matched:
                mk = matched.group('key')
                marray = result_qs.get(mk, [])
                result_qs[mk] = marray + [v]
            else:
                result_qs[k] = v

        return result_qs


class PixivError(Exception):
    """Pixiv API exception"""

    def __init__(self, reason, header=None, body=None):
        self.reason = str(reason)
        self.header = header
        self.body = body
        super(Exception, self).__init__(self, reason)

    def __str__(self):
        return self.reason


class JsonDict(dict):
    """general json object that allows attributes to be bound to and also behaves like a dict"""

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(r"'JsonDict' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value
