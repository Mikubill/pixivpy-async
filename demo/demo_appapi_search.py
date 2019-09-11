# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import sys

from pixivpy_async import AppPixivAPI

sys.dont_write_bytecode = True

_USERNAME = "userbay"
_PASSWORD = "userpay"


async def appapi_search(aapi):
    first_tag = None
    response = await aapi.trending_tags_illust()
    for trend_tag in response.trend_tags[:10]:
        if not first_tag:
            first_tag = trend_tag.tag
        print("%s -  %s(id=%s)" % (trend_tag.tag, trend_tag.illust.title, trend_tag.illust.id))

    json_result = await aapi.search_illust(first_tag, search_target='partial_match_for_tags')
    # print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    json_result = await aapi.search_illust(**next_qs)
    # print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))


async def _login(aapi):
    await aapi.login(_USERNAME, _PASSWORD)


async def _main(aapi):
    await _login(aapi)
    await asyncio.gather(
        appapi_search(aapi)
    )


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(AppPixivAPI()))


if __name__ == '__main__':
    main()
