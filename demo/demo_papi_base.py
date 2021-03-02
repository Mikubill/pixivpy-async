# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import sys

from pixivpy_async import PixivAPI

sys.dont_write_bytecode = True

_USERNAME = "userbay"
_PASSWORD = "UserPay"
_TOKEN = "uXooTT7xz9v4mflnZqJUO7po9W5ciouhKrIDnI2Dv3c"

async def papi_base(api):
    # PAPI.works
    json_result = await api.works(46363414)
    # print(json_result)
    illust = json_result.response[0]
    print(">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))

    # PAPI.users
    json_result = await api.users(1184799)
    # print(json_result)
    user = json_result.response[0]
    print(user.profile.introduction)


async def _login(papi):
    # await aapi.login(_USERNAME, _PASSWORD)
    await papi.login(refresh_token=_TOKEN)


async def _main(papi):
    await _login(papi)
    await asyncio.gather(
        papi_base(papi)
    )


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(PixivAPI()))


if __name__ == '__main__':
    main()
