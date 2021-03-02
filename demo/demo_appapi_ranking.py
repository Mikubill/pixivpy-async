# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import sys

from pixivpy_async import AppPixivAPI

sys.dont_write_bytecode = True

_USERNAME = "userbay"
_PASSWORD = "UserPay"
_TOKEN = "uXooTT7xz9v4mflnZqJUO7po9W5ciouhKrIDnI2Dv3c"

async def appapi_ranking(aapi):
    json_result = await aapi.illust_ranking('day_male')
    # print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    json_result = await aapi.illust_ranking(**next_qs)
    # print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    # 2016-07-15 日的过去一周排行
    json_result = await aapi.illust_ranking('week', date='2016-07-15')
    # print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))


async def _login(aapi):
    # await aapi.login(_USERNAME, _PASSWORD)
    await aapi.login(refresh_token=_TOKEN)


async def _main(aapi):
    await _login(aapi)
    await asyncio.gather(
        appapi_ranking(aapi)
    )


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(AppPixivAPI()))


if __name__ == '__main__':
    main()
