# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import sys

from pixivpy_async import PixivAPI

sys.dont_write_bytecode = True

_USERNAME = "userbay"
_PASSWORD = "userpay"


async def papi_me(api):
    # PAPI.me_feeds
    json_result = await api.me_feeds(show_r18=0)
    print(json_result)
    work = json_result.response[0].ref_user.works[0]
    print(work.title)

    # PAPI.me_favorite_works
    json_result = await api.me_favorite_works(publicity='private')
    print(json_result)
    illust = json_result.response[0].work
    print("[%s] %s: %s" % (illust.user.name, illust.title, illust.image_urls.px_480mw))

    # PAPI.me_following_works (New -> Follow)
    json_result = await api.me_following_works()
    print(json_result)
    illust = json_result.response[0]
    print(">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))


async def _login(aapi):
    await aapi.login(_USERNAME, _PASSWORD)


async def _main(aapi):
    await _login(aapi)
    await asyncio.gather(
        papi_me(aapi)
    )


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(PixivAPI()))


if __name__ == '__main__':
    main()
