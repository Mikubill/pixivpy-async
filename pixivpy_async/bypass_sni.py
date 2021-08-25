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
            pattern = re.compile(r"((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(1\d\d|2[0-4]\d|25[0-5]|[1-9]\d|\d)")
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
                *(asyncio.create_task(self.fetch(session, url, params,
                  ClientTimeout(total=timeout))) for url in URLS),
                return_exceptions=True)

        for r in results:
            if not isinstance(r, Exception):
                return r
