# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import sys

from pixivpy_async import AppPixivAPI

sys.dont_write_bytecode = True

_USERNAME = "userbay"
_PASSWORD = "UserPay"


async def appapi_users(aapi):
    json_result = await aapi.user_detail(275527)
    # print(json_result)
    user = json_result.user
    print("%s(@%s) region=%s" % (user.name, user.account, json_result.profile.region))

    json_result = await aapi.user_illusts(275527)
    # print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    json_result = await aapi.user_illusts(**next_qs)
    # print(json_result)
    illust = json_result.illusts[0]
    print("  > %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    json_result = await aapi.user_bookmarks_illust(2088434)
    # print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    json_result = await aapi.user_following(7314824)
    # print(json_result)
    user_preview = json_result.user_previews[0]
    print(">>> %s(@%s)" % (user_preview.user.name, user_preview.user.account))

    next_qs = aapi.parse_qs(json_result.next_url)
    json_result = await aapi.user_following(**next_qs)
    # print(json_result)
    user_preview = json_result.user_previews[0]
    print("  > %s(@%s)" % (user_preview.user.name, user_preview.user.account))

    json_result = await aapi.user_follower(275527)
    print(json_result)

    json_result = await aapi.user_mypixiv(275527)
    print(json_result)


async def _login(aapi):
    await aapi.login(_USERNAME, _PASSWORD)


async def _main(aapi):
    await _login(aapi)
    await asyncio.gather(
        appapi_users(aapi)
    )


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(AppPixivAPI()))


if __name__ == '__main__':
    main()
