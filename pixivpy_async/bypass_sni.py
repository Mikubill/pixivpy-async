import asyncio
import logging
import json
import socket
from typing import List, Dict, Any
import ssl
import aiohttp
import re

from aiohttp.abc import AbstractResolver
from aiohttp import ClientTimeout


class ByPassResolver(AbstractResolver):

    async def resolve(self, host: str, port, family) -> List[Dict[str, Any]]:
        new_host = host
        if host in ["app-api.pixiv.net", "public-api.secure.pixiv.net", "www.pixiv.net", "oauth.secure.pixiv.net"]:
            new_host = "www.pixivision.net"

        ips = await self.require_appapi_hosts(new_host)
        result = []

        for i in ips:
            result.append({
                "hostname": "",
                "host": i,
                "port": port,
                "family": family,
                "proto": 0,
                "flags": socket.AI_NUMERICHOST,
            })
        return result

    async def close(self) -> None:
        pass

    async def fetch(self, client_session: aiohttp.ClientSession, url: str, params, timeout) -> list:
        async with client_session.get(url, params=params, timeout=timeout) as rsp:
            response = await rsp.text()
            obj = json.loads(response)
            pattern = re.compile(
                "((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(1\d\d|2[0-4]\d|25[0-5]|[1-9]\d|\d)")
            result = []
            for i in obj["Answer"]:
                ip = i["data"]

                if pattern.match(ip) is not None:
                    result.append(ip)
            return result

    async def require_appapi_hosts(self, hostname, timeout=3) -> List[str]:
        """
        通过 Cloudflare 的 DNS over HTTPS 请求真实的 IP 地址。
        """
        URLS = (
            "https://1.0.0.1/dns-query",
            "https://1.1.1.1/dns-query",
            "https://[2606:4700:4700::1001]/dns-query",
            "https://[2606:4700:4700::1111]/dns-query",
            "https://cloudflare-dns.com/dns-query",
        )
        params = {
            "ct": "application/dns-json",
            "name": hostname,
            "type": "A",
            "do": "false",
            "cd": "false",
        }

        async with aiohttp.ClientSession() as session:
            results = await asyncio.gather(
                *(asyncio.create_task(self.fetch(session, url, params, ClientTimeout(total=timeout))) for url in URLS),
                return_exceptions=True)

        for r in results:
            if not isinstance(r, Exception):
                return r


RESOLVER = ByPassResolver()


def get_bypass_client() -> aiohttp.ClientSession:
    ssl_ctx = ssl.SSLContext()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    connector = aiohttp.TCPConnector(ssl=ssl_ctx, resolver=RESOLVER)
    client = aiohttp.ClientSession(connector=connector)
    return client


class BypassClient:
    def __init__(self):
        self.client = get_bypass_client()

    async def __aenter__(self) -> aiohttp.ClientSession:
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.close()


async def test():
    async with BypassClient() as client:
        async with client.get(
                "https://www.pixiv.net/ajax/search/artworks/%E7%99%BE%E5%90%88?word=%E7%99%BE%E5%90%88&order=date_d&mode=all&p=99999990&s_mode=s_tag&type=all&lang=zh") as rsp:
            print(await rsp.json())


if __name__ == '__main__':
    asyncio.run(test())
