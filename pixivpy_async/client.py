import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector


class PixivClient:
    def __init__(self, limit=30, timeout=10, env=False, internal=False, proxy=None):
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
            self.conn = ProxyConnector.from_url(proxy, limit_per_host=limit)
        else:
            self.conn = aiohttp.TCPConnector(limit_per_host=limit)

        self.internal = internal
        self.client = aiohttp.ClientSession(
            connector=self.conn,
            timeout=aiohttp.ClientTimeout(total=timeout),
            trust_env=env,
        )

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
