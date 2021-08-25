import asyncio
import aiohttp

from .bypass_sni import get_bypass_client

class PixivClient:
    def __init__(self, limit=30, timeout=10, env=False, internal=False, proxy=None, bypass=False):
        """
            When 'env' is True and 'proxy' is None, possible proxies will be
            obtained automatically (wrong proxy may be obtained).

            When 'proxy' is not None, it will force the proxy to be used and
            'env' will have no effect.

            proxy <str> is used for a single proxy with a url:
                'socks5://user:password@127.0.0.1:1080'

            If you want to use proxy chaining, read https://github.com/romis2012/aiohttp-socks.

        """

        if proxy:
            try:
                from aiohttp_socks import ProxyConnector
                self.conn = ProxyConnector.from_url(proxy, limit_per_host=limit)
                _flag = False
            except ModuleNotFoundError as e:
                if proxy.startswith('socks'):
                    raise e
                else:
                    self.conn = aiohttp.TCPConnector(limit_per_host=limit)
                    _flag = True
        else:
            self.conn = aiohttp.TCPConnector(limit_per_host=limit)

        self.internal = internal
        
        if bypass:
            self.client = get_bypass_client()
        else:
            self.client = aiohttp.ClientSession(
                connector=self.conn,
                timeout=aiohttp.ClientTimeout(total=timeout),
                trust_env=env,
            )

        if proxy and _flag:
            from functools import partial
            self.client.get = partial(self.client.get, proxy=proxy)
            self.client.post = partial(self.client.post, proxy=proxy)

    def start(self):
        return self.client

    async def close(self):
        await asyncio.sleep(0)
        await self.client.close()

    async def __aenter__(self):
        return self.client

    async def __aexit__(self, exc_type, exc, tb):
        await asyncio.sleep(0)
        await self.client.close()
