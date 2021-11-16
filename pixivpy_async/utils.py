# -*- coding:utf-8 -*-
import json
import urllib.parse as up


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
                if isinstance(value, list):
                    if key in ["sizes", "types"]:
                        result.update(
                            {'%s' % key: ','.join(map(str, value))}
                        )
                    elif key in ["ids"]:
                        result.update(
                            {'%s[]' % key: ",".join(
                                [str(pid) for pid in value])}
                        )
                    elif key in ["viewed"]:
                        [result.update(
                            {'%s[%d]' % (key, k): value[k]}
                        ) for k in range(len(value))]
                    else:
                        result.update(
                            {'%s[]' % key: ','.join(map(str, value))}
                        )
                if isinstance(value, bool):
                    result.update(
                        {key: str(value).lower()}
                    )
        return result

    @staticmethod
    def parse_json(_):
        return json.loads(json.dumps(_), object_hook=JsonDict)

    @staticmethod
    def parse_qs(next_url):
        if not next_url:
            return None

        result_qs = {}
        query = up.urlparse(next_url).query
        for key, value in up.parse_qs(query).items():
            if '[' in key and key.endswith(']'):
                if key.split('[')[0] in result_qs:
                    result_qs[key.split('[')[0]].extend(value)
                else:
                    result_qs[key.split('[')[0]] = value
            else:
                result_qs[key] = value[-1]

        return result_qs


class JsonDict(dict):
    """general json object that allows attributes to be bound to and also behaves like a dict"""

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, attr, value):
        self[attr] = value
