# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import sys

from pixivpy_async import PixivAPI

sys.dont_write_bytecode = True

_USERNAME = "userbay"
_PASSWORD = "UserPay"


async def papi_user(api):

    # PAPI.me_following
    json_result = await api.me_following()
    print(json_result)
    user = json_result.response[0]
    print(user.name)

    # PAPI.users_works
    json_result = await api.users_works(1184799)
    print(json_result)
    illust = json_result.response[0]
    print(">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))

    # PAPI.users_favorite_works
    json_result = await api.users_favorite_works(1184799)
    print(json_result)
    illust = json_result.response[0].work
    print(">>> %s origin url: %s" % (illust.caption, illust.image_urls['large']))

    # PAPI.users_feeds
    json_result = await api.users_feeds(1184799, show_r18=0)
    print(json_result)
    ref_work = json_result.response[0].ref_work
    print(ref_work.title)

    # PAPI.users_following
    json_result = await api.users_following(4102577)
    print(json_result)
    user = json_result.response[0]
    print(user.name)


async def _login(api):
    await api.login(_USERNAME, _PASSWORD)


async def _main(api):
    await _login(api)
    await asyncio.gather(
        papi_user(api)
    )


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(PixivAPI()))


if __name__ == '__main__':
    main()
