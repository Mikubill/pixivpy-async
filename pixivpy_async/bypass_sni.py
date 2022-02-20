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

    def __init__(self, endpoints=None, force_hosts=True):
        self.endpoints = [
            "https://1.0.0.1/dns-query",
            "https://1.1.1.1/dns-query",
            "https://[2606:4700:4700::1001]/dns-query",
            "https://[2606:4700:4700::1111]/dns-query",
            "https://cloudflare-dns.com/dns-query",
        ] if endpoints is None else endpoints
        self.force_hosts = force_hosts

    async def resolve(self, host: str, port, family=socket.AF_INET) -> List[Dict[str, Any]]:

        new_host = host
        if self.force_hosts and host in ["app-api.pixiv.net", "public-api.secure.pixiv.net", "www.pixiv.net", "oauth.secure.pixiv.net"]:
            new_host = "www.pixivision.net"

        done, pending = await asyncio.wait([asyncio.create_task(
            self._resolve(endpoint, new_host, family))
            for endpoint in self.endpoints], return_when=asyncio.FIRST_COMPLETED)

        ips = await self.read_result(done.union(pending))
        for future in pending:
            future.cancel()

        if len(ips) == 0:
            raise Exception("Failed to resolve {}".format(host))

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

    async def read_result(self, tasks: List[asyncio.Task]) -> List[str]:
        if len(tasks) == 0:
            return []
        task = tasks.pop()
        
        try:
            await task
            return task.result()
        except Exception as e:
            print("caught:", repr(e))
            return await self.read_result(tasks)
            
    async def close(self) -> None:
        pass

    async def parse_result(self, hostname, response) -> List[str]:
        data = json.loads(response)
        if data['Status'] != 0:
            raise Exception("Failed to resolve {}".format(hostname))

        # Pattern to match IPv4 addresses 
        pattern = re.compile(
            r"((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(1\d\d|2[0-4]\d|25[0-5]|[1-9]\d|\d)")
        result = []

        for i in data["Answer"]:
            ip = i["data"]

            if pattern.match(ip) is not None:
                result.append(ip)

        return result

    async def _resolve(self, endpoint, hostname, family, timeout=5) -> List[str]:

        params = {
            "name": hostname,
            "type": "AAAA" if family == socket.AF_INET6 else "A",
            "do": "false",
            "cd": "false",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, params=params, headers={"accept": "application/dns-json"}, timeout=ClientTimeout(total=timeout)) as resp:
                if resp.status == 200:
                    return await self.parse_result(hostname, await resp.text())
                else:
                    raise Exception("Failed to resolve {} with {}: HTTP Status {}".format(
                        hostname, endpoint, resp.status))
