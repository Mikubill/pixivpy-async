import aiohttp
import random
import asyncio
from .retry import retry


class Net(object):
    def __init__(self, client=None, **requests_kwargs):
        self.gen = True
        if client:
            self.session = client
            self.gen = False
        self.requests_kwargs = requests_kwargs

    @retry(asyncio.TimeoutError, aiohttp.ClientError, aiohttp.ServerTimeoutError,
           aiohttp.ServerConnectionError, aiohttp.ServerDisconnectedError,
           retries=10, cooldown=random.randint(1, 3))
    async def down(self, _url, _referer):
        if self.gen:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(_url, headers={'Referer': _referer}, **self.requests_kwargs) as response:
                    c = await response.read()
                    t = response.content_type
        else:
            async with self.session.get(_url, headers={'Referer': _referer}, **self.requests_kwargs) as response:
                c = await response.read()
                t = response.content_type
        await asyncio.sleep(0)
        return c, t

    @retry(asyncio.TimeoutError, aiohttp.ClientError, aiohttp.ServerTimeoutError,
           aiohttp.ServerConnectionError, aiohttp.ServerDisconnectedError,
           retries=10, cooldown=random.randint(1, 3))
    async def auth(self, _url, _headers, _data):
        if self.gen:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.post(_url, headers=_headers, data=_data, **self.requests_kwargs) as response:
                    r, b, q = await response.json(), response.status in [200, 301, 302], response.status
        else:
            async with self.session.post(_url, headers=_headers, data=_data, **self.requests_kwargs) as response:
                r, b, q = await response.json(), response.status in [200, 301, 302], response.status

        await asyncio.sleep(0)
        return r, b, q

    @retry(asyncio.TimeoutError, aiohttp.ClientError, aiohttp.ServerTimeoutError,
           aiohttp.ServerConnectionError, aiohttp.ServerDisconnectedError,
           retries=10, cooldown=random.randint(1, 3))
    async def fetch(self, _url, _headers, _params):
        if self.gen:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(_url, headers=_headers, params=_params,
                                       **self.requests_kwargs) as response:
                    q = await response.json()
        else:
            async with self.session.get(_url, headers=_headers, params=_params,
                                        **self.requests_kwargs) as response:
                q = await response.json()

        await asyncio.sleep(0)
        return q

    @retry(asyncio.TimeoutError, aiohttp.ClientError, aiohttp.ServerTimeoutError,
           aiohttp.ServerConnectionError, aiohttp.ServerDisconnectedError,
           retries=10, cooldown=random.randint(1, 3))
    async def post(self, _url, _data, _headers, _params):
        if self.gen:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.post(_url, data=_data, headers=_headers,
                                        params=_params, **self.requests_kwargs) as response:
                    r = await response.json()
        else:
            async with self.session.post(_url, data=_data, headers=_headers,
                                         params=_params, **self.requests_kwargs) as response:
                r = await response.json()

        await asyncio.sleep(0)
        return r

    @retry(asyncio.TimeoutError, aiohttp.ClientError, aiohttp.ServerTimeoutError,
           aiohttp.ServerConnectionError, aiohttp.ServerDisconnectedError,
           retries=10, cooldown=random.randint(1, 3))
    async def delete(self, _url, _headers, _params):
        if self.gen:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.delete(_url, headers=_headers, params=_params,
                                          **self.requests_kwargs) as response:
                    q = await response.json()
        else:
            async with self.session.delete(_url, headers=_headers, params=_params,
                                           **self.requests_kwargs) as response:
                q = await response.json()

        await asyncio.sleep(0)
        return q
