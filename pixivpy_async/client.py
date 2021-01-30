import asyncio
import aiohttp
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector


class PixivClient:
    def __init__(self, limit=30, timeout=10, env=False, internal=False, proxy=None):
        """
            When 'env' is True and 'proxy' is None, possible proxies will be
            obtained automatically (wrong proxy may be obtained).

            When 'proxy' is not None, it will force the proxy to be used and
            'env' will have no effect.

            proxy <str> is used for a single proxy with a url:
                'socks5://user:password@127.0.0.1:1080'

            proxy <dict> is used for a single proxy with a dict:
                proxy_dict = {
                    'proxy_type': ProxyType.SOCKS5,
                    'host': '127.0.0.1',
                    'port': 1080,
                    'rdns': True
                }

            proxy <list> is used for proxy chaining with a list of urls:
                [
                    'socks5://user:password@127.0.0.1:1080',
                    'socks4://127.0.0.1:1081',
                    'http://user:password@127.0.0.1:3128',
                ]

        """

        if isinstance(proxy, str):
            self.conn = ProxyConnector.from_url(proxy, limit_per_host=limit)
        elif isinstance(proxy, dict):
            self.conn = ProxyConnector(**proxy, limit_per_host=limit)
        elif isinstance(proxy, list):
            self.conn = ChainProxyConnector.from_urls(proxy, limit_per_host=limit)
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
