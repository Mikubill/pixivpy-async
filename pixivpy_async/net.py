import aiohttp
import random
import asyncio
from .retry import retry
from .client import PixivClient

retryable_error = asyncio.TimeoutError, aiohttp.ClientError, aiohttp.ServerTimeoutError, \
    aiohttp.ServerConnectionError, aiohttp.ServerDisconnectedError


class ClientManager:
    def __init__(self, s, **opt):
        if s is None:
            self.session = PixivClient(internal=True, **opt)
        else:
            self.session = s

    async def __aenter__(self):
        if isinstance(self.session, PixivClient):
            return self.session.start()
        if isinstance(self.session, aiohttp.ClientSession):
            return self.session

    async def __aexit__(self, exception_type, exception_value, traceback):
        if isinstance(self.session, PixivClient):
            if self.session.internal:
                await self.session.close()


class Net(object):
    def __init__(self, client=None, env=False, proxy=None, bypass=False, **requests_kwargs):
        self.session = client
        self.conn_opt = {'env': env, 'proxy': proxy, 'bypass': bypass}
        self.requests_kwargs = requests_kwargs

    @retry(*retryable_error, retries=10, cooldown=random.randint(1, 3))
    async def down(self, _url, _referer, _request_content_type: bool = False):
        async with ClientManager(self.session, **self.conn_opt) as session:
            if _request_content_type is True:
                async with session.head(_url, headers={'Referer': _referer}, **self.requests_kwargs) as head:
                    yield head.content_type
            async with session.get(_url, headers={'Referer': _referer}, **self.requests_kwargs) as res:
                yield await res.read()

    @retry(*retryable_error, retries=10, cooldown=random.randint(1, 3))
    async def auth(self, _url, _headers, _data):
        async with ClientManager(self.session, **self.conn_opt) as session:
            async with session.post(_url, headers=_headers, data=_data, **self.requests_kwargs) as res:
                r, b, q = await res.json(), res.status in [200, 301, 302], res.status

        await asyncio.sleep(0)
        return r, b, q

    @retry(*retryable_error, retries=10, cooldown=random.randint(1, 3))
    async def fetch(self, _url, _headers, _params):
        async with ClientManager(self.session, **self.conn_opt) as session:
            async with session.get(_url, headers=_headers, params=_params, **self.requests_kwargs) as res:
                q = await res.json()

        await asyncio.sleep(0)
        return q

    @retry(*retryable_error, retries=10, cooldown=random.randint(1, 3))
    async def post(self, _url, _data, _headers, _params):
        async with ClientManager(self.session, **self.conn_opt) as session:
            async with session.post(_url, data=_data, headers=_headers, params=_params, **self.requests_kwargs) as res:
                r = await res.json()

        await asyncio.sleep(0)
        return r

    @retry(*retryable_error, retries=10, cooldown=random.randint(1, 3))
    async def delete(self, _url, _headers, _params):
        async with ClientManager(self.session, **self.conn_opt) as session:
            async with session.delete(_url, headers=_headers, params=_params, **self.requests_kwargs) as res:
                q = await res.json()

        await asyncio.sleep(0)
        return q
