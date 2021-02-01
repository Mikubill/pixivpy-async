# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import sys

from pixivpy_async import PixivAPI

sys.dont_write_bytecode = True

_USERNAME = "userbay"
_PASSWORD = "UserPay"


async def papi_ranking(api):
    # PAPI.ranking
    json_result = await api.ranking('illust', 'weekly', 1)
    # print(json_result)
    illust = json_result.response[0].works[0].work
    print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))

    # PAPI.ranking(2015-05-01)
    json_result = await api.ranking(ranking_type='all', mode='daily', page=1, date='2015-05-01')
    # print(json_result)
    illust = json_result.response[0].works[0].work
    print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))


async def papi_search(api):
    # PAPI.search_works
    json_result = await api.search_works("五航戦 姉妹", page=1, mode='text')
    # json_result = await api.search_works("水遊び", page=1, mode='exact_tag')
    # print(json_result)
    illust = json_result.response[0]
    print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))


async def papi_others(api):
    # PAPI.latest_works (New -> Everyone)
    json_result = await api.latest_works()
    # print(json_result)
    illust = json_result.response[0]
    print(">>> %s url: %s" % (illust.title, illust.image_urls.px_480mw))


async def _login(papi):
    await papi.login(_USERNAME, _PASSWORD)


async def _main(papi):
    await _login(papi)
    await asyncio.gather(
        papi_ranking(papi),
        papi_search(papi),
        papi_others(papi)
    )


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(PixivAPI()))


if __name__ == '__main__':
    main()
