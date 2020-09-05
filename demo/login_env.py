import asyncio

from pixivpy3 import AppPixivAPI as AAPI
from pixivpy_async import AppPixivAPI, PixivClient
from pixivpy_async.sync import AppPixivAPI as SAAPI

_USERNAME = 'userbay'
_PASSWORD = 'userpay'


def test0():
    api = AAPI()
    api.login(_USERNAME, _PASSWORD)
    print("test0 - finished")


def test2():
    api = SAAPI(env=True)
    api.login(_USERNAME, _PASSWORD)
    print("test2 - finished")


async def test1():
    client = PixivClient(env=True).start()
    api = AppPixivAPI(client=client)
    await api.login(_USERNAME, _PASSWORD)
    await client.close()
    print("test1 - finished")


if __name__ == '__main__':
    test0()
    test2()
    asyncio.run(test1())
