# -*- coding:utf-8 -*-
import json
import re
from urllib.parse import urlparse, unquote


class Utils:

    @staticmethod
    def set_headers(headers: dict, token: str):
        default_headers = {
            'App-OS': 'ios',
            'App-OS-Version': '12.2',
            'App-Version': '7.6.2',
            'User-Agent': 'PixivIOSApp/7.6.2 (iOS 12.2; iPhone9,1)'
        }
        if headers is None:
            headers = dict()
        if headers.get('User-Agent', None) is None and headers.get('user-agent', None) is None:
            headers.update(default_headers)
        if token:
            headers.update({'Authorization': 'Bearer {}'.format(token)})
        return headers

    @staticmethod
    def set_params(**kwargs):
        result = dict()
        for key, value in kwargs.items():
            if value is not None:
                if isinstance(value, str):
                    result.update(
                        {key: value}
                    )
                if isinstance(value, int):
                    result.update(
                        {key: value}
                    )
                if isinstance(value, list) and 'sizes' not in key and 'ids' not in key and 'types' not in key:
                    result.update(
                        {'%s[]' % key: ','.join(map(str, value))}
                    )
                if isinstance(value, list) and 'ids' in key:
                    result.update(
                        {'%s[]' % key: ",".join([str(pid) for pid in value])}
                    )
                if isinstance(value, list) and 'sizes' in key:
                    result.update(
                        {'%s' % key: ','.join(map(str, value))}
                    )
                if isinstance(value, list) and 'types' in key:
                    result.update(
                        {'%s' % key: ','.join(map(str, value))}
                    )
                if isinstance(value, bool):
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
    def parse_qs(next_url):
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


class JsonDict(dict):
    """general json object that allows attributes to be bound to and also behaves like a dict"""

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(r"'JsonDict' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value
