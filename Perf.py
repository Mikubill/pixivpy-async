import asyncio
import sys
import time
import random

from pixivpy_async import PixivClient
from pixivpy_async import AppPixivAPI
from pixivpy_async import PixivAPI
from pixivpy3 import AppPixivAPI as Sync_aapi
from pixivpy3 import PixivAPI as Sync_papi

sys.dont_write_bytecode = True

_USERNAME = "userbay"
_PASSWORD = "UserPay"
_TOKEN = "uXooTT7xz9v4mflnZqJUO7po9W5ciouhKrIDnI2Dv3c"

saapi = Sync_aapi()
# saapi.login(_USERNAME, _PASSWORD)
saapi.login(refresh_token=_TOKEN)
spapi = Sync_papi()
# spapi.login(_USERNAME, _PASSWORD)
spapi.login(refresh_token=_TOKEN)


def gen_date():
    """201x-0x-xx"""
    year = random.randint(3, 9)
    month = random.randint(1, 9)
    day = random.randint(10, 29)
    return '201%s-0%s-%s' % (year, month, day)


def test_sync_illust(num):
    e = time.time()
    for i in range(num):
        print('%s,' % i, end="")
        sys.stdout.flush()
        saapi.illust_ranking('day', date=gen_date())
    print('\n\nsync - time: %s\n\n' % (time.time() - e))
    print(saapi.illust_ranking('day', date=gen_date()))


async def illust(aapi, i):
    print('%s,' % i, end="")
    sys.stdout.flush()
    await aapi.illust_ranking('day', date=gen_date())


async def _test_async_illust(num):
    async with PixivClient() as client:
        aapi = AppPixivAPI(client=client)
        papi = PixivAPI(client=client)
        # await aapi.login(_USERNAME, _PASSWORD)
        # await papi.login(_USERNAME, _PASSWORD)
        await papi.login(refresh_token=_TOKEN)
        await aapi.login(refresh_token=_TOKEN)
        tasks = [asyncio.ensure_future(illust(aapi, i)) for i in range(num)]
        await asyncio.wait(tasks)


def test_async_illust(num):
    e = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_test_async_illust(num))
    print('\n\nasync - time: %s\n\n' % (time.time() - e))


# ---------------------------------------


def test_sync_illust_detail(num):
    e = time.time()
    for i in range(num):
        print('%s,' % i, end="")
        sys.stdout.flush()
        saapi.illust_detail(random.randint(19180000, 19189999))
    print('\n\nsync - time: %s\n\n' % (time.time() - e))
    print(saapi.illust_detail(random.randint(19180000, 19189999)))


async def illust_detail(aapi, i):
    print('%s,' % i, end="")
    sys.stdout.flush()
    await aapi.illust_detail(random.randint(19180000, 19189999))


async def _test_async_illust_detail(num):
    async with PixivClient() as client:
        aapi = AppPixivAPI(client=client)
        papi = PixivAPI(client=client)
        await papi.login(refresh_token=_TOKEN)
        await aapi.login(refresh_token=_TOKEN)
        # await aapi.login(_USERNAME, _PASSWORD)
        # await papi.login(_USERNAME, _PASSWORD)
        tasks = [asyncio.ensure_future(illust_detail(aapi, i))
                 for i in range(num)]
        await asyncio.wait(tasks)


def test_async_illust_detail(num):
    e = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_test_async_illust(num))
    print('\n\nasync - time: %s\n\n' % (time.time() - e))


# ---------------------------------------


def test_sync_user_illusts(num):
    e = time.time()
    for i in range(num):
        print('%s,' % i, end="")
        sys.stdout.flush()
        saapi.user_illusts(random.randint(211321, 271312))
    print('\n\nsync - time: %s\n\n' % (time.time() - e))
    print(saapi.user_illusts(random.randint(211321, 271312)))


async def user_illusts(aapi, i):
    print('%s,' % i, end="")
    sys.stdout.flush()
    await aapi.user_illusts(random.randint(211321, 271312))


async def _test_async_user_illusts(num):
    async with PixivClient() as client:
        aapi = AppPixivAPI(client=client)
        papi = PixivAPI(client=client)
        await papi.login(refresh_token=_TOKEN)
        await aapi.login(refresh_token=_TOKEN)
        # await aapi.login(_USERNAME, _PASSWORD)
        # await papi.login(_USERNAME, _PASSWORD)
        tasks = [asyncio.ensure_future(user_illusts(aapi, i))
                 for i in range(num)]
        await asyncio.wait(tasks)


def test_async_user_illusts(num):
    e = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_test_async_user_illusts(num))
    print('\n\nasync - time: %s\n\n' % (time.time() - e))


# ---------------------------------------


def test_sync_user_detail(num):
    e = time.time()
    for i in range(num):
        print('%s,' % i, end="")
        sys.stdout.flush()
        saapi.user_detail(random.randint(211321, 271312))
    print('\n\nsync - time: %s\n\n' % (time.time() - e))
    print(saapi.user_detail(random.randint(211321, 271312)))


async def user_detail(aapi, i):
    print('%s,' % i, end="")
    sys.stdout.flush()
    await aapi.user_detail(random.randint(211321, 271312))


async def _test_async_user_detail(num):
    async with PixivClient() as client:
        aapi = AppPixivAPI(client=client)
        papi = PixivAPI(client=client)
        await papi.login(refresh_token=_TOKEN)
        await aapi.login(refresh_token=_TOKEN)
        # await aapi.login(_USERNAME, _PASSWORD)
        # await papi.login(_USERNAME, _PASSWORD)
        tasks = [asyncio.ensure_future(user_detail(aapi, i))
                 for i in range(num)]
        await asyncio.wait(tasks)


def test_async_user_detail(num):
    e = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_test_async_user_detail(num))
    print('\n\nasync - time: %s\n\n' % (time.time() - e))


# ---------------------------------------


def test_sync_ugoira_metadata(num):
    e = time.time()
    for i in range(num):
        print('%s,' % i, end="")
        sys.stdout.flush()
        saapi.ugoira_metadata(random.randint(19180000, 19189999))
    print('\n\nsync - time: %s\n\n' % (time.time() - e))
    print(saapi.ugoira_metadata(random.randint(19180000, 19189999)))


async def ugoira_metadata(aapi, i):
    print('%s,' % i, end="")
    sys.stdout.flush()
    await aapi.ugoira_metadata(random.randint(19180000, 19189999))


async def _test_async_ugoira_metadata(num):
    async with PixivClient() as client:
        aapi = AppPixivAPI(client=client)
        papi = PixivAPI(client=client)
        await papi.login(refresh_token=_TOKEN)
        await aapi.login(refresh_token=_TOKEN)
        # await aapi.login(_USERNAME, _PASSWORD)
        # await papi.login(_USERNAME, _PASSWORD)
        tasks = [asyncio.ensure_future(
            ugoira_metadata(aapi, i)) for i in range(num)]
        await asyncio.wait(tasks)


def test_async_ugoira_metadata(num):
    e = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_test_async_ugoira_metadata(num))
    print('\n\nasync - time: %s\n\n' % (time.time() - e))


# ---------------------------------------


def test_sync_works(num):
    e = time.time()
    for i in range(num):
        print('%s,' % i, end="")
        sys.stdout.flush()
        spapi.works(random.randint(19180000, 19189999))
    print('\n\nsync - time: %s\n\n' % (time.time() - e))
    print(spapi.works(random.randint(19180000, 19189999)))


async def works(papi, i):
    print('%s,' % i, end="")
    sys.stdout.flush()
    await papi.works(random.randint(19180000, 19189999))


async def _test_async_works(num):
    async with PixivClient() as client:
        aapi = AppPixivAPI(client=client)
        papi = PixivAPI(client=client)
        await papi.login(refresh_token=_TOKEN)
        await aapi.login(refresh_token=_TOKEN)
        # await aapi.login(_USERNAME, _PASSWORD)
        # await papi.login(_USERNAME, _PASSWORD)
        tasks = [asyncio.ensure_future(works(papi, i)) for i in range(num)]
        await asyncio.wait(tasks)


def test_async_works(num):
    e = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_test_async_works(num))
    print('\n\nasync - time: %s\n\n' % (time.time() - e))


# ---------------------------------------


def test_sync_me_following_works(num):
    e = time.time()
    for i in range(num):
        print('%s,' % i, end="")
        sys.stdout.flush()
        spapi.me_following_works()
    print('\n\nsync - time: %s\n\n' % (time.time() - e))
    print(spapi.me_following_works())


async def me_following_works(papi, i):
    print('%s,' % i, end="")
    sys.stdout.flush()
    await papi.me_following_works()


async def _test_async_me_following_works(num):
    async with PixivClient() as client:
        aapi = AppPixivAPI(client=client)
        papi = PixivAPI(client=client)
        await papi.login(refresh_token=_TOKEN)
        await aapi.login(refresh_token=_TOKEN)
        # await aapi.login(_USERNAME, _PASSWORD)
        # await papi.login(_USERNAME, _PASSWORD)
        tasks = [asyncio.ensure_future(
            me_following_works(papi, i)) for i in range(num)]
        await asyncio.wait(tasks)


def test_async_me_following_works(num):
    e = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_test_async_me_following_works(num))
    print('\n\nasync - time: %s\n\n' % (time.time() - e))


# ---------------------------------------


def test_sync_ranking(num):
    e = time.time()
    for i in range(num):
        print('%s,' % i, end="")
        sys.stdout.flush()
        spapi.ranking('illust', 'weekly', 1)
    print('\n\nsync - time: %s\n\n' % (time.time() - e))
    print(spapi.ranking('illust', 'weekly', 1))


async def ranking(papi, i):
    print('%s,' % i, end="")
    sys.stdout.flush()
    await papi.ranking('illust', 'weekly', 1)


async def _test_async_ranking(num):
    async with PixivClient() as client:
        aapi = AppPixivAPI(client=client)
        papi = PixivAPI(client=client)
        await papi.login(refresh_token=_TOKEN)
        await aapi.login(refresh_token=_TOKEN)
        # await aapi.login(_USERNAME, _PASSWORD)
        # await papi.login(_USERNAME, _PASSWORD)
        tasks = [asyncio.ensure_future(ranking(papi, i)) for i in range(num)]
        await asyncio.wait(tasks)


def test_async_ranking(num):
    e = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_test_async_ranking(num))
    print('\n\nasync - time: %s\n\n' % (time.time() - e))


# ---------------------------------------


def test_sync_latest_works(num):
    e = time.time()
    for i in range(num):
        print('%s,' % i, end="")
        sys.stdout.flush()
        spapi.latest_works()
    print('\n\nsync - time: %s\n\n' % (time.time() - e))
    print(spapi.latest_works())


async def latest_works(papi, i):
    print('%s,' % i, end="")
    sys.stdout.flush()
    await papi.latest_works()


async def _test_async_latest_works(num):
    async with PixivClient() as client:
        aapi = AppPixivAPI(client=client)
        papi = PixivAPI(client=client)
        await papi.login(refresh_token=_TOKEN)
        await aapi.login(refresh_token=_TOKEN)
        # await aapi.login(_USERNAME, _PASSWORD)
        # await papi.login(_USERNAME, _PASSWORD)
        tasks = [asyncio.ensure_future(latest_works(papi, i))
                 for i in range(num)]
        await asyncio.wait(tasks)


def test_async_latest_works(num):
    e = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_test_async_ranking(num))
    print('\n\nasync - time: %s\n\n' % (time.time() - e))


def main():
    print('\n\nStart test: AppPixivAPI - illust_detail - 350\n\n')
    test_async_illust_detail(350)

    test_sync_illust_detail(350)

    time.sleep(60)

    print('\n\nStart test: AppPixivAPI - illust_ranking - 350\n\n')
    test_async_illust(350)

    test_sync_illust(350)
    time.sleep(60)

    print('\n\nStart test: AppPixivAPI - user_illusts - 350\n\n')
    test_async_user_illusts(350)

    test_sync_user_illusts(350)
    time.sleep(60)

    print('\n\nStart test: AppPixivAPI - user_detail - 350\n\n')
    test_async_user_detail(350)

    test_sync_user_detail(350)
    time.sleep(60)

    print('\n\nStart test: AppPixivAPI - ugoira_metadata - 350\n\n')
    test_async_ugoira_metadata(350)

    test_sync_ugoira_metadata(350)
    time.sleep(60)

    print('\n\nStart test: PixivAPI - works - 350\n\n')
    test_async_works(350)

    test_sync_works(350)
    time.sleep(60)

    print('\n\nStart test: PixivAPI - me_following_works - 350\n\n')
    test_async_me_following_works(350)

    test_sync_me_following_works(350)
    time.sleep(60)

    print('\n\nStart test: PixivAPI - ranking - 350\n\n')
    test_async_ranking(350)

    test_sync_ranking(350)
    time.sleep(60)

    print('\n\nStart test: PixivAPI - latest_works - 350\n\n')
    test_async_latest_works(350)

    test_sync_latest_works(350)


if __name__ == '__main__':
    main()
