# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import os
import io
import sys
import time
import unittest

from pixivpy_async import utils
from pixivpy_async.net import Net
from pixivpy_async.sync import *

sys.dont_write_bytecode = True

_USERNAME = "userbay"
_PASSWORD = "UserPay"

# get your refresh_token, and replace _TOKEN
#  https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362
_TOKEN = "0zeYA-PllRYp1tfrsq_w3vHGU1rPy237JMf5oDt73c4"

aapi = AppPixivAPI()
papi = PixivAPI()
papi.login(refresh_token=_TOKEN)
aapi.login(refresh_token=_TOKEN)
t = time.time()


class TestMethods(unittest.TestCase):
    def test_login(self):
        newaapi = AppPixivAPI(bypass=True)
        # newpapi = PixivAPI()
        # self.assertIsNotNone(newaapi.login(_USERNAME, _PASSWORD))
        credential = newaapi.login(refresh_token=_TOKEN)
        self.assertIsNotNone(credential)
        self.assertIsNotNone(credential.access_token)
        self.assertIsNotNone(credential.refresh_token)
        # self.assertIsNotNone(newpapi.login(_USERNAME, _PASSWORD))

    def test_bypass(self):
        newaapi = AppPixivAPI(bypass=True)
        credential = newaapi.login(refresh_token=_TOKEN)
        self.assertIsNotNone(credential)
        self.assertIsNotNone(credential.access_token)
        self.assertIsNotNone(credential.refresh_token)

        detail = newaapi.user_detail(275527)
        self.assertIsNotNone(detail)
        self.assertIsNotNone(detail.user)
        self.assertEqual(detail.user.id, 275527)

    def test_bypass_2(self):
        newaapi = AppPixivAPI(bypass=True, proxy="socks5://127.0.0.1:9011")
        credential = newaapi.login(refresh_token=_TOKEN)
        self.assertIsNotNone(credential)
        self.assertIsNotNone(credential.access_token)
        self.assertIsNotNone(credential.refresh_token)

        detail = newaapi.user_detail(275527)
        self.assertIsNotNone(detail)
        self.assertIsNotNone(detail.user)
        self.assertEqual(detail.user.id, 275527)

    def test_socks_1(self):
        newaapi = AppPixivAPI(proxy="socks5://127.0.0.1:9011")
        credential = newaapi.login(refresh_token=_TOKEN)
        self.assertIsNotNone(credential)
        self.assertIsNotNone(credential.access_token)
        self.assertIsNotNone(credential.refresh_token)

        detail = newaapi.user_detail(275527)
        self.assertIsNotNone(detail)
        self.assertIsNotNone(detail.user)
        self.assertEqual(detail.user.id, 275527)

    def test_socks_2(self):
        os.environ['ALL_PROXY'] = "socks5://127.0.0.1:9011"
        newaapi = AppPixivAPI(env=True)
        credential = newaapi.login(refresh_token=_TOKEN)
        self.assertIsNotNone(credential)
        self.assertIsNotNone(credential.access_token)
        self.assertIsNotNone(credential.refresh_token)

        detail = newaapi.user_detail(275527)
        self.assertIsNotNone(detail)
        self.assertIsNotNone(detail.user)
        self.assertEqual(detail.user.id, 275527)

    def test_new_illusts(self):
        self.assertIsNotNone(aapi.illust_new())

    def test_illust_1(self):
        illust = aapi.illust_detail(59580629)
        self.assertIsNotNone(illust)
        self.assertIsNotNone(illust, illust)
        self.assertEqual(illust.illust.id, 59580629)
        self.assertIsNotNone(illust.illust.image_urls)

    def test_illust_2(self):
        self.assertIsNotNone(aapi.illust_comments(59580629))

    def test_illust_3(self):
        self.assertIsNotNone(aapi.ugoira_metadata(51815717))

    def test_illust_4(self):
        self.assertIsNotNone(aapi.illust_related(59580629))

    def test_illust_5(self):
        self.assertIsNotNone(aapi.illust_bookmark_detail(59580629))

    def test_page(self):
        self.assertIsNotNone(aapi.illust_recommended(
            bookmark_illust_ids=[59580629], req_auth=False))
        self.assertIsNotNone(aapi.illust_recommended(
            bookmark_illust_ids=[59580629]))
        json_result = aapi.illust_recommended(bookmark_illust_ids=[59580629])
        # page down in some case
        self.assertIsNotNone(aapi.parse_qs(json_result.next_url))
        next_qs = aapi.parse_qs(json_result.next_url)
        self.assertIsNotNone(aapi.illust_recommended(**next_qs))

    def test_user_1(self):
        self.assertIsNotNone(aapi.user_detail(275527))

    def test_user_2(self):
        self.assertIsNotNone(aapi.user_illusts(275527))

    def test_user_3(self):
        self.assertIsNotNone(aapi.user_list(2088434))

    def test_user_4(self):
        self.assertIsNotNone(aapi.user_related(7314824))

    def test_user_5(self):
        self.assertIsNotNone(aapi.search_user('ほし'))
        self.assertIsNotNone(aapi.user_bookmark_tags_illust())

    def test_bookmark(self):
        self.assertIsNotNone(aapi.user_bookmarks_illust(2088434))

    # def test_bookmark_1(self):
    #     self.assertIsNotNone(aapi.user_bookmark_tags_illust(2088434))

    # def test_showcase(self):
    #     self.assertIsNotNone(aapi.showcase_article(4616))

    def test_follow_1(self):
        self.assertIsNotNone(aapi.user_following(7314824))

    def test_follow_2(self):
        self.assertIsNotNone(aapi.user_follower(275527))

    def test_follow_3(self):
        self.assertIsNotNone(aapi.user_mypixiv(275527))

    def test_add(self):
        self.assertIsNot(aapi.user_follow_add(24687177), {})

    def test_del(self):
        self.assertIsNot(aapi.user_follow_del(24687177), {})

    def test_novel(self):
        self.assertIsNotNone(aapi.search_novel('abc'))
        self.assertIsNotNone(aapi.user_novels(2748828))
        self.assertIsNotNone(aapi.novel_series(0))
        self.assertIsNotNone(aapi.novel_detail(14588477))
        self.assertIsNotNone(aapi.novel_text(14588477))

    def test_tag(self):
        self.assertIsNotNone(aapi.trending_tags_illust())
        first_tag = None
        response = aapi.trending_tags_illust()
        for trend_tag in response.trend_tags[:10]:
            if not first_tag:
                first_tag = trend_tag.tag
        self.assertIsNotNone(aapi.search_illust(
            first_tag, search_target='partial_match_for_tags'))

    def test_ranking(self):

        self.assertIsNotNone(aapi.illust_ranking('day_male'))
        self.assertIsNotNone(aapi.illust_follow(req_auth=True))
        self.assertIsNotNone(aapi.illust_recommended(req_auth=True))

    def test_bookmark_add(self):

        illust_id = 74187223
        tags = ['Fate/GO', '50000users入り', '私服']
        self.assertIsNotNone(aapi.illust_bookmark_add(illust_id, tags=tags))
        self.assertIsNotNone(aapi.illust_bookmark_delete(illust_id))
        self.assertIsNotNone(aapi.illust_bookmark_detail(illust_id))

    def test_download(self):

        self.assertIsNotNone(aapi.illust_ranking('day', date='2016-08-01'))
        json_result = aapi.illust_ranking('day', date='2019-08-01')

        # Disabled due to Rate Limit
        for illust in json_result.illusts[:5]:
            image_url = illust.meta_single_page.get(
                'original_image_url', illust.image_urls.large)
            url_basename = os.path.basename(image_url)
            extension = os.path.splitext(url_basename)[1]
            name = "illust_id_%d_%s%s" % (illust.id, illust.title, extension)
            aapi.download(image_url, path='.', name=name)
            aapi.download(image_url, path='.', fname=io.BytesIO())
            self.assertTrue(os.path.exists(name))

    def test_papi_base(self):

        self.assertIsNotNone(papi.works(46363414))
        self.assertIsNotNone(papi.users(1184799))

    def test_papi_me(self):

        self.assertIsNotNone(papi.me_feeds(show_r18=0))
        self.assertIsNotNone(papi.me_favorite_works(publicity='private'))
        self.assertIsNotNone(papi.me_following_works())
        self.assertIsNotNone(papi.me_following())

    def test_papi_users(self):

        self.assertIsNotNone(papi.users_works(1184799))
        self.assertIsNotNone(papi.users_favorite_works(1184799))
        self.assertIsNotNone(papi.users_feeds(1184799, show_r18=0))
        self.assertIsNotNone(papi.users_following(4102577))

    def test_papi_others(self):

        self.assertIsNotNone(papi.ranking('illust', 'weekly', 1))
        self.assertIsNotNone(papi.ranking(
            ranking_type='all', mode='daily', page=1, date='2019-08-01'))
        self.assertIsNotNone(papi.search_works("しらたま", page=1, mode='text'))
        self.assertIsNotNone(papi.latest_works())
        self.assertIsNotNone(papi.ranking_all(date='2019-07-01'))

    # def test_deep(self):
    #     aapi.set_api_proxy("http://app-api.pixivlite.com")
    #     self.assertIsNotNone(aapi.illust_ranking('day'))

    def test_others(self):
        newaapi0 = AppPixivAPI()
        # self.assertIsNotNone(newaapi0.login(_USERNAME, _PASSWORD))
        self.assertIsNotNone(newaapi0.login(refresh_token=_TOKEN))
        newaapi = AppPixivAPI()
        self.assertRaises(error.NoLoginError, newaapi.login, None)
        newaapi2 = AppPixivAPI()
        self.assertRaises(error.AuthTokenError,
                          newaapi2.login, refresh_token='89urwei')
        newaapi3 = AppPixivAPI()
        self.assertRaises(error.AuthCredentialsError, newaapi3.login,
                          username='89urwei', password='97324yuieh')
        self.assertIsNone(newaapi.set_auth('None', 'None'))
        self.assertIsNone(newaapi.set_client('None', 'None'))
        self.assertIsNone(newaapi.set_accept_language('ja-jp'))
        self.assertIsNotNone(utils.Utils().set_params(fsadf=[1, 2, 3]))
        self.assertIsNone(utils.Utils().parse_qs(None))

    def test_http_methods(self):
        loop = asyncio.get_event_loop()
        self.assertIsNotNone(loop.run_until_complete(Net().post(
            'https://httpbin.org/post', None, {'accept': 'application/json'}, None)))
        self.assertIsNotNone(loop.run_until_complete(Net().delete(
            'https://httpbin.org/delete', {'accept': 'application/json'}, None)))


if __name__ == '__main__':
    unittest.main()
