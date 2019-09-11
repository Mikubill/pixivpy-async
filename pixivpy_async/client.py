import asyncio
import aiohttp


class PixivClient:
    def __init__(self, limit=30, timeout=10):
        self.conn = aiohttp.TCPConnector(limit_per_host=limit)
        self.client = aiohttp.ClientSession(
            connector=self.conn,
            timeout=aiohttp.ClientTimeout(total=timeout)
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