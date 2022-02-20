# -*- coding:utf-8 -*-
import hashlib
import os
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
        self.user_agent = 'PixivAndroidApp/5.0.234 (Android 11; Pixel 5)'
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

    async def login_web(self):
        from base64 import urlsafe_b64encode
        from hashlib import sha256
        from secrets import token_urlsafe
        from urllib.parse import urlencode

        LOGIN_URL = "https://app-api.pixiv.net/web/v1/login"
        REDIRECT_URI = "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback"

        print("please visit this before continue:\n\thttps://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362")
        def s256(data):
            """S256 transformation method."""
            return urlsafe_b64encode(sha256(data).digest()).rstrip(b"=").decode("ascii")
        
        """Proof Key for Code Exchange by OAuth Public Clients (RFC7636)."""
        code_verifier = token_urlsafe(32)
        code_challenge = s256(code_verifier.encode("ascii"))
        login_params = {
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "client": "pixiv-android",
        }
        print(f"login link:\n\t{LOGIN_URL}?{urlencode(login_params)}")
        code = input("code: ").strip()


        data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "code_verifier": code_verifier,
                "grant_type": "authorization_code",
                "include_policy": "true",
                "redirect_uri": REDIRECT_URI,
             }
        headers = {
            'User-Agent': self.user_agent
        }
        
        # return auth/token response
        return await self.auth_req(self.api.auth, headers, data)
        
    async def login(self, username=None, password=None, refresh_token=None):
        """Login with password, or use the refresh_token to acquire a new bearer token"""

        url = self.api.auth
        local_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00:00')
        headers = {
            'User-Agent': self.user_agent,
            'X-Client-Time': local_time,
            'X-Client-Hash': hashlib.md5((local_time + self.hash_secret).encode('utf-8')).hexdigest(),
        }
        data = {
            'get_secure_url': 1,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        if (username is not None) and (password is not None):
            raise LoginError
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
            if auto_ext is True:
                _ = await self.down(url, referer, _request_content_type=auto_ext)
                type = await _.__anext__()
                if type in self.content_type_mapping.keys():
                    _name, _ext = os.path.splitext(img_path)
                    img_path = _name + self.content_type_mapping[type]
            if os.path.exists(img_path) and not replace:
                return False
            else:
                _ = locals().get('_', await self.down(url, referer, _request_content_type=False))
                response = await _.__anext__()
                await _.aclose()
                async with aiofiles.open(img_path, mode='wb') as out_file:
                    await out_file.write(response)
        else:
            _ = await self.down(url, referer, _request_content_type=False)
            response = await _.__anext__()
            await _.aclose()
            fname.write(response)
        del response
        return True
