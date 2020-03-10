# -*- coding:utf-8 -*-
import hashlib
import os
import re
from datetime import datetime
import aiofiles
from .error import *
from .utils import Utils
from .api import API
from .net import Net

try:
    basestring
except NameError:
    basestring = str


class BasePixivAPI(Net, Utils):
    def __init__(self, **requests_kwargs):
        self.additional_headers = {}
        self.client_id = 'MOBrBDS8blbauoSck0ZfDbtuzpyT'
        self.client_secret = 'lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj'
        self.hash_secret = '28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c'
        self.access_token = None
        self.user_id = 0
        self.refresh_token = None
        self.api = API()
        self.content_type_mapping = {
            'image/webp': '.webp',
            'image/jpg': '.jpg',
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
        }
        super().__init__(**requests_kwargs)

    async def requests_(
            self,
            method: str,
            url: str,
            headers: dict = None,
            params: dict = None,
            data: dict = None,
            auth: bool = True
    ):
        if auth:
            if self.access_token is None:
                raise NoTokenError
        headers = self.set_headers(headers, self.access_token)
        return await self.requests_call(method=method, url=url, headers=headers, params=params, data=data)

    def set_api_proxy(self, **kwargs):
        self.api = API(**kwargs)

    def set_auth(self, access_token, refresh_token=None):
        self.access_token = access_token
        self.refresh_token = refresh_token

    def set_additional_headers(self, headers):
        self.additional_headers = headers

    def set_client(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def set_accept_language(self, language):
        self.additional_headers['Accept-Language'] = language

    async def requests_call(self, method, url, headers=None, params=None, data=None):
        data = data if data else dict()
        params = params if params else dict()
        headers = headers if headers else dict()
        w = await self.req(method=method, url=url, headers=headers, params=params, data=data)
        return self.parse_json(w)

    async def req(self, method, url, headers=None, data=None, params=None):
        headers.update(self.additional_headers)
        if method == 'GET':
            return await self.fetch(url, headers, params)
        elif method == 'POST':
            return await self.post(url, data, headers, params)
        elif method == 'DELETE':
            return await self.delete(url, headers, params)
        else:
            raise MethodError(method)

    async def login(self, username=None, password=None, refresh_token=None):
        """Login with password, or use the refresh_token to acquire a new bearer token"""

        url = self.api.auth
        local_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00:00')
        headers = {
            'User-Agent': 'PixivAndroidApp/5.0.64 (Android 6.0)',
            'X-Client-Time': local_time,
            'X-Client-Hash': hashlib.md5((local_time + self.hash_secret).encode('utf-8')).hexdigest(),
        }
        data = {
            'get_secure_url': 1,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        if (username is not None) and (password is not None):
            data['grant_type'] = 'password'
            data['username'] = username
            data['password'] = password
        elif (refresh_token is not None) or (self.refresh_token is not None):
            data['grant_type'] = 'refresh_token'
            data['refresh_token'] = refresh_token or self.refresh_token
        else:
            raise NoLoginError

        # return auth/token response
        return await self.auth_req(url, headers, data)

    async def auth_req(self, url, headers, data):
        r, status, code = await self.auth(url, headers, data)
        if not status:
            if data['grant_type'] == 'password':
                raise AuthCredentialsError(code, r)
            else:
                raise AuthTokenError(code, r)

        token = None
        try:
            token = self.parse_json(r)
            self.access_token = token.response.access_token
            self.user_id = token.response.user.id
            self.refresh_token = token.response.refresh_token
        except Exception as e:
            raise TokenError(token, e)

        return token

    async def download(self, url, prefix='', path=os.path.curdir, fname=None, auto_ext=True,
                       name=None, replace=False, referer='https://app-api.pixiv.net/'):
        if fname is None and name is None:
            name = os.path.basename(url)
        elif isinstance(fname, basestring):
            name = fname
        if name:
            img_path = os.path.join(path, prefix + name)
            if os.path.exists(img_path) and not replace:
                return False
            else:
                response, type = await self.down(url, referer)
                if auto_ext and type in self.content_type_mapping:
                    _ext = re.findall(r'(\.\w+)$', img_path)
                    if _ext != []:
                        img_path = img_path.replace(_ext[0], self.content_type_mapping[type])
                    else:
                        img_path += self.content_type_mapping[type]
                async with aiofiles.open(img_path, mode='wb') as out_file:
                    await out_file.write(response)
        else:
            response, _ = await self.down(url, referer)
            fname.write(response)
        del response
        return True
