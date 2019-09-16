# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import os
import sys
import time
import unittest

from pixivpy_async import utils
from pixivpy_async.net import Net
from pixivpy_async.sync import *

sys.dont_write_bytecode = True

_USERNAME = "userbay"
_PASSWORD = "userpay"

aapi = AppPixivAPI()
papi = PixivAPI()
aapi.login(_USERNAME, _PASSWORD)
papi.login(_USERNAME, _PASSWORD)
t = time.time()


async def async_func():
    from pixivpy_async import PixivClient
    from pixivpy_async import AppPixivAPI as apapi
    from pixivpy_async import PixivAPI as ppapi

    async with PixivClient() as client:
        aapid = apapi(client=client)
        await aapid.login( username=_USERNAME, password=_PASSWORD)
        await aapid.illust_detail(59580629)
        await aapid.illust_comments(59580629)
        await aapid.ugoira_metadata(51815717)
        await aapid.illust_recommended(bookmark_illust_ids=[59580629])
        await aapid.illust_related(59580629)
        await aapid.user_detail(275527)
        await aapid.user_illusts(275527)
        await aapid.user_bookmarks_illust(2088434)
        await aapid.user_following(7314824)
        await aapid.user_follower(275527)
        await aapid.user_mypixiv(275527)
        await aapid.trending_tags_illust()
        await aapid.illust_ranking('day_male')
        await aapid.illust_follow(req_auth=True)
        await aapid.illust_recommended(req_auth=True)
        await aapid.illust_ranking('day', date='2016-08-01')

        # papid = ppapi(client=client)
        # await papid.login( username=_USERNAME, password=_PASSWORD)
        # await papid.works(46363414),
        # await papid.users(1184799),
        # await papid.me_feeds(show_r18=0),
        # await papid.me_favorite_works(publicity='private'),
        # await papid.me_following_works(),
        # await papid.me_following(),
        # await papid.users_works(1184799),
        # await papid.users_favorite_works(1184799),
        # await papid.users_feeds(1184799, show_r18=0),
        # await papid.users_following(4102577),
        # await papid.ranking('illust', 'weekly', 1),
        # await papid.ranking(ranking_type='all', mode='daily', page=1, date='2015-05-01'),
        # await papid.search_works("五航戦 姉妹", page=1, mode='text'),
        # await papid.latest_works()


class TestMethods(unittest.TestCase):
    def test_login(self):
        newaapi = AppPixivAPI()
        newpapi = PixivAPI()
        self.assertIsNotNone(newaapi.login(_USERNAME, _PASSWORD))
        self.assertIsNotNone(newpapi.login(_USERNAME, _PASSWORD))

    def test_illust_0(self):

        self.assertIsNotNone(aapi.illust_detail(59580629))

    def test_illust_1(self):
        self.assertIsNotNone(aapi.illust_comments(59580629))

    def test_illust_2(self):
        self.assertIsNotNone(aapi.ugoira_metadata(51815717))

    def test_illust_3(self):
        self.assertIsNotNone(aapi.illust_related(59580629))

    def test_illust_4(self):
        self.assertIsNotNone(aapi.illust_bookmark_detail(59580629))

    def test_page(self):
        self.assertIsNotNone(aapi.illust_recommended(bookmark_illust_ids=[59580629], req_auth=False))
        self.assertIsNotNone(aapi.illust_recommended(bookmark_illust_ids=[59580629]))
        json_result = aapi.illust_recommended(bookmark_illust_ids=[59580629])
        self.assertIsNotNone(aapi.parse_qs(json_result.next_url))  # page down in some case
        next_qs = aapi.parse_qs(json_result.next_url)
        self.assertIsNotNone(aapi.illust_recommended(**next_qs))

    def test_user(self):
        self.assertIsNotNone(aapi.user_detail(275527))

    def test_user_1(self):
        self.assertIsNotNone(aapi.user_illusts(275527))

    def test_user_2(self):
        self.assertIsNotNone(aapi.user_list(2088434))

    def test_bookmark(self):
        self.assertIsNotNone(aapi.user_bookmarks_illust(2088434))

    def test_bookmark_1(self):
        self.assertIsNotNone(aapi.user_bookmark_tags_illust(2088434))

    def test_showcase(self):
        self.assertIsNotNone(aapi.showcase_article(4616))

    def test_follow(self):

        self.assertIsNotNone(aapi.user_following(7314824))

    def test_follow_1(self):
        self.assertIsNotNone(aapi.user_follower(275527))
        self.assertIsNotNone(aapi.user_mypixiv(275527))

    def test_tag(self):

        self.assertIsNotNone(aapi.trending_tags_illust())
        first_tag = None
        response = aapi.trending_tags_illust()
        for trend_tag in response.trend_tags[:10]:
            if not first_tag:
                first_tag = trend_tag.tag
        self.assertIsNotNone(aapi.search_illust(first_tag, search_target='partial_match_for_tags'))

    def test_ranking(self):

        self.assertIsNotNone(aapi.illust_ranking('day_male'))
        self.assertIsNotNone(aapi.illust_follow(req_auth=True))
        self.assertIsNotNone(aapi.illust_recommended(req_auth=True))

    def test_download(self):

        self.assertIsNotNone(aapi.illust_ranking('day', date='2016-08-01'))
        json_result = aapi.illust_ranking('day', date='2019-08-01')

        # Disabled due to Rate Limit
        for illust in json_result.illusts[:3]:
            image_url = illust.meta_single_page.get('original_image_url', illust.image_urls.large)
            url_basename = os.path.basename(image_url)
            extension = os.path.splitext(url_basename)[1]
            name = "illust_id_%d_%s%s" % (illust.id, illust.title, extension)
            aapi.download(image_url, path='.', name=name)
            self.assertTrue(os.path.exists(name))

    # def test_papi_base(self):
    #
    #     self.assertIsNotNone(papi.works(46363414))
    #     self.assertIsNotNone(papi.users(1184799))
    #
    # def test_papi_me(self):
    #
    #     self.assertIsNotNone(papi.me_feeds(show_r18=0))
    #     self.assertIsNotNone(papi.me_favorite_works(publicity='private'))
    #     self.assertIsNotNone(papi.me_following_works())
    #     self.assertIsNotNone(papi.me_following())

    # def test_papi_users(self):
    #
    #     self.assertIsNotNone(papi.users_works(1184799))
    #     self.assertIsNotNone(papi.users_favorite_works(1184799))
    #     self.assertIsNotNone(papi.users_feeds(1184799, show_r18=0))
    #     self.assertIsNotNone(papi.users_following(4102577))

    # def test_papi_others(self):
    #
    #     self.assertIsNotNone(papi.ranking('illust', 'weekly', 1))
    #     self.assertIsNotNone(papi.ranking(ranking_type='all', mode='daily', page=1, date='2019-08-01'))
    #     self.assertIsNotNone(papi.search_works("しらたま", page=1, mode='text'))
    #     self.assertIsNotNone(papi.latest_works())
    #     self.assertIsNotNone(papi.ranking_all(date='2019-07-01'))

    def test_deep(self):
        aapi.set_api_proxy("http://app-api.pixivlite.com")
        self.assertIsNotNone(aapi.illust_ranking('day'))

    def test_deep_deep(self):
        newaapi0 = AppPixivAPI()
        self.assertIsNotNone(newaapi0.login(_USERNAME, _PASSWORD))
        newaapi = AppPixivAPI()
        self.assertRaises(error.NoLoginError, newaapi.login, None)
        newaapi2 = AppPixivAPI()
        self.assertRaises(error.AuthTokenError, newaapi2.login, refresh_token='89urwei')
        newaapi3 = AppPixivAPI()
        self.assertRaises(error.AuthCredentialsError, newaapi3.login, username='89urwei', password='97324yuieh')
        self.assertIsNone(newaapi.set_auth('None', 'None'))
        self.assertIsNone(newaapi.set_client('None', 'None'))
        self.assertIsNone(newaapi.set_accept_language('ja-jp'))
        self.assertIsNotNone(utils.Utils().set_params(fsadf=[1, 2, 3]))
        self.assertIsNone(utils.Utils().parse_qs(None))

    def test_http_methods(self):
        loop = asyncio.get_event_loop()
        self.assertIsNotNone(loop.run_until_complete(Net().post('https://httpbin.org/post', None, {'accept': 'application/json'}, None)))
        self.assertIsNotNone(loop.run_until_complete(Net().delete('https://httpbin.org/delete', {'accept': 'application/json'}, None)))

    def test_async_gather(self):
        c = time.time()
        print('Sync Func: %s s' % (c - t))
        p = asyncio.gather(async_func())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(p)
        print('Async Func: %s s' % (time.time() - c))


if __name__ == '__main__':
    unittest.main()
