# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import sys

from pixivpy_async import AppPixivAPI

sys.dont_write_bytecode = True

_USERNAME = "userbay"
_PASSWORD = "UserPay"


async def appapi_illust(aapi):
    json_result = await aapi.illust_detail(59580629)
    # print(json_result)
    illust = json_result.illust
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    json_result = await aapi.illust_comments(59580629)
    # print(json_result)

    json_result = await aapi.ugoira_metadata(51815717)
    # print(json_result)
    metadata = json_result.ugoira_metadata
    print(">>> frames=%d %s" % (len(metadata.frames), metadata.zip_urls.medium))


async def _login(aapi):
    await aapi.login(_USERNAME, _PASSWORD)


async def _main(aapi):
    await _login(aapi)
    await asyncio.gather(
        appapi_illust(aapi)
    )


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(AppPixivAPI()))


if __name__ == '__main__':
    main()
