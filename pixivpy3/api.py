# -*- coding:utf-8 -*-
import asyncio
import hashlib
import logging
import os
import random
from datetime import datetime

import aiohttp

from .utils import PixivError, Utils


class BasePixivAPI(Utils):
    def __init__(self, **requests_kwargs):
        self.session = aiohttp.ClientSession()
        self.requests_kwargs = requests_kwargs
        self.additional_headers = {}
        self.client_id = 'MOBrBDS8blbauoSck0ZfDbtuzpyT'
        self.client_secret = 'lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj'
        self.hash_secret = '28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c'
        self.access_token = None
        self.user_id = 0
        self.refresh_token = None

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
        w = await self.req(method, url, headers, params, data)
        return self.parse_json(w)

    async def req(self, method, url, headers=None, data=None, params=None, retr=0):
        headers.update(self.additional_headers)
        try:
            if method == 'GET':
                return await self.fetch(self.session, url, headers, params)
            elif method == 'POST':
                return await self.post(self.session, url, data, headers, params)
            elif method == 'DELETE':
                return await self.delete(self.session, url, headers, params)
            else:
                raise PixivError('Unknow method: %s' % method)
        except asyncio.TimeoutError:
            """Retry for timeout"""
            logging.warning('requests %s %s  timeout. retrying %s time(s)...' % (method, url, retr + 1))
            await asyncio.sleep(random.randint(1, 3))
            if retr < 5:
                return await self.req(method, url, headers=headers, params=params,
                                      data=data, retr=retr + 1)
            else:
                raise PixivError('requests %s %s timeout error' % (method, url))
        except Exception as e:
            raise PixivError('requests %s %s error: %s' % (method, url, e))

    async def login(self, username=None, password=None, refresh_token=None):
        """Login with password, or use the refresh_token to acquire a new bearer token"""

        url = 'https://oauth.secure.pixiv.net/auth/token'
        local_time = datetime.now().isoformat()
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
            raise PixivError(
                '[ERROR] auth() but no password or refresh_token is set.'
            )

        # return auth/token response
        return self.auth_req(url, headers, data)

    async def auth_req(self, url, headers, data):
        r, status, code = await self.auth_request(self.session, url, headers, data)
        if not status:
            if data['grant_type'] == 'password':
                raise PixivError(
                    '[ERROR] auth() failed! check username and password.'
                    '\nHTTP %s: %s' % (code, r)
                )
            else:
                raise PixivError(
                    '[ERROR] auth() failed! check refresh_token.'
                    '\nHTTP %s: %s' % (code, r)
                )

        token = None
        try:
            token = self.parse_json(r)
            self.access_token = token.response.access_token
            self.user_id = token.response.user.id
            self.refresh_token = token.response.refresh_token
        except Exception as e:
            raise PixivError('Get access_token error! \nResponse: %s\nError: %s' % (token, e))

        return token

    async def download(self, url, prefix='', path=os.path.curdir,
                       name=None, replace=False, referer='https://app-api.pixiv.net/'):

        name = prefix + name if name else prefix + os.path.basename(url)
        img_path = os.path.join(path, name)
        if not os.path.exists(img_path) or replace:
            e = await self.down_request(self.session, url, referer)
            with open(img_path, 'wb') as out_file:
                out_file.write(e)
