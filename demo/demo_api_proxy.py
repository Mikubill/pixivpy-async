#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio

from pixivpy_async import *

# change _USERNAME,_PASSWORD first!
_USERNAME = "userbay"
_PASSWORD = "userpay"


async def _cmain(aapi):

    # set API proxy to pixivlite.com
    aapi.set_api_proxy("http://app-api.pixivlite.com")

    json_result = await aapi.illust_ranking('day')
    # print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))


async def _login(aapi):
    await aapi.login(_USERNAME, _PASSWORD)


async def _main(aapi):
    await _login(aapi)
    await asyncio.gather(
        _cmain(aapi)
    )


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(AppPixivAPI()))


if __name__ == '__main__':
    main()
