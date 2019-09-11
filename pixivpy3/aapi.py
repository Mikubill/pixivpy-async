# -*- coding:utf-8 -*-
from pixivpy3 import PixivError
from .api import BasePixivAPI


# App-API (6.x - app-api.pixiv.net)


class AppPixivAPI(BasePixivAPI):
    def __init__(self, **requests_kwargs):
        """initialize requests kwargs if need be"""
        super(AppPixivAPI, self).__init__(**requests_kwargs)
        self.hosts = "https://app-api.pixiv.net"
        self.appv1 = 'https://app-api.pixiv.net/v1'
        self.appv2 = 'https://app-api.pixiv.net/v2'

    async def no_auth_requests_call(
            self,
            method: str,
            url: str,
            headers: dict = None,
            params: dict = None,
            data: dict = None,
            req_auth: bool = True
    ):
        if req_auth:
            if self.access_token is None:
                raise PixivError('No access_token Found!')
        headers = self.set_app_headers(headers, self.access_token)
        return await self.requests_call(method, url, headers, params, data)

    async def user_detail(
            self,
            user_id: int,
            filter_: str = 'for_ios',
            req_auth: bool = True
    ):
        """

        :param user_id:
        :param filter_:
        :param req_auth:
        :return:
        """
        url = '%s/user/detail' % self.appv1
        params = self.set_params(
            user_id=user_id,
            filter=filter_
        )
        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    async def user_illusts(
            self,
            user_id: int,
            type_: str = 'illust',
            filter_: str = 'for_ios',
            offset: int = None,
            req_auth: bool = True
    ):
        """

        :param user_id:
        :param type_: ['illust', 'manga']
        :param filter_:
        :param offset:
        :param req_auth:
        :return:
        """
        url = '%s/v1/user/illusts' % self.hosts
        params = self.set_params(
            user_id=user_id,
            filter=filter_,
            type=type_,
            offset=offset
        )
        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 用户收藏作品列表
    # tag: 从 user_bookmark_tags_illust 获取的收藏标签
    async def user_bookmarks_illust(
            self,
            user_id: int,
            restrict: str = 'public',
            filter_: str = 'for_ios',
            max_bookmark_id: int = None,
            tag: str = None,
            req_auth: bool = True
    ):
        """

        :param user_id:
        :param restrict:
        :param filter_:
        :param max_bookmark_id:
        :param tag:
        :param req_auth:
        :return:
        """
        url = '%s/user/bookmarks/illust' % self.appv1
        params = self.set_params(
            user_id=user_id,
            filter=filter_,
            restrict=restrict,
            max_bookmark_id=max_bookmark_id,
            tag=tag
        )
        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 关注用户的新作
    # restrict: [public, private]
    async def illust_follow(
            self,
            restrict: str = 'public',
            offset: int = None,
            req_auth: bool = True
    ):
        """

        :param restrict:
        :param offset:
        :param req_auth:
        :return:
        """
        url = '%s/illust/follow' % self.appv2
        params = self.set_params(
            restrict=restrict,
            offset=offset
        )
        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 作品详情 (类似PAPI.works()，iOS中未使用)
    async def illust_detail(
            self,
            illust_id: int,
            req_auth: bool = True
    ):
        """

        :param illust_id:
        :param req_auth:
        :return:
        """
        url = '%s/illust/detail' % self.appv1
        params = self.set_params(
            illust_id=illust_id
        )
        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 作品评论
    async def illust_comments(
            self,
            illust_id,
            offset=None,
            include_total_comments=None,
            req_auth=True
    ):
        """

        :param illust_id:
        :param offset:
        :param include_total_comments:
        :param req_auth:
        :return:
        """
        url = '%s/illust/comments' % self.appv1
        params = self.set_params(
            illust_id=illust_id,
            offset=offset,
            include_total_comments=include_total_comments
        )
        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    async def illust_related(
            self,
            illust_id: int,
            filter_: str = 'for_ios',
            seed_illust_ids: list = None,
            offset: int = None,
            req_auth: bool = True
    ):
        """

        :param illust_id:
        :param filter_:
        :param seed_illust_ids:
        :param offset:
        :param req_auth:
        :return:
        """
        url = '%s/illust/related' % self.appv2
        params = self.set_params(
            illust_id=illust_id,
            offset=offset,
            filter=filter_,
            seed_illust_ids=seed_illust_ids,
        )
        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    async def illust_recommended(
            self,
            content_type: str = 'illust',
            include_ranking_label: bool = True,
            filter_: str = 'for_ios',
            max_bookmark_id_for_recommend: int = None,
            min_bookmark_id_for_recent_illust: int = None,
            offset: int = None,
            include_ranking_illusts=None,
            bookmark_illust_ids: list = None,
            include_privacy_policy=None,
            req_auth: bool = True
    ):
        """

        :param content_type: [illust, manga]
        :param include_ranking_label:
        :param filter_:
        :param max_bookmark_id_for_recommend:
        :param min_bookmark_id_for_recent_illust:
        :param offset:
        :param include_ranking_illusts:
        :param bookmark_illust_ids:
        :param include_privacy_policy:
        :param req_auth:
        :return:
        """
        if req_auth:
            url = '%s/illust/recommended' % self.appv1
        else:
            url = '%s/illust/recommended-nologin' % self.appv1
        params = self.set_params(
            content_type=content_type,
            offset=offset,
            filter=filter_,
            bookmark_illust_ids=bookmark_illust_ids,
            include_ranking_illusts=include_ranking_illusts,
            include_ranking_label=include_ranking_label,
            include_privacy_policy=include_privacy_policy,
            max_bookmark_id_for_recommend=max_bookmark_id_for_recommend,
            min_bookmark_id_for_recent_illust=min_bookmark_id_for_recent_illust,
        )
        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    async def illust_ranking(
            self,
            mode: str = 'day',
            filter_: str = 'for_ios',
            date: str = None,
            offset: int = None,
            req_auth: bool = True
    ):
        """

        :param mode: [day, week, month, day_male, day_female, week_original, week_rookie, day_manga]
        :param filter_:
        :param date: '2016-08-01'
        :param offset:
        :param req_auth:
        :return:
        """
        url = '%s/illust/ranking' % self.appv1
        params = self.set_params(
            date=date,
            offset=offset,
            filter=filter_,
            mode=mode
        )
        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 趋势标签 (Search - tags)
    async def trending_tags_illust(
            self,
            filter_: str = 'for_ios',
            req_auth: bool = True
    ):
        """

        :param filter_:
        :param req_auth:
        :return:
        """
        url = '%s/trending-tags/illust' % self.appv1
        params = self.set_params(
            filter=filter_
        )
        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    async def search_illust(
            self,
            word: str,
            search_target: str = 'partial_match_for_tags',
            sort: str = 'date_desc',
            duration: str = None,
            filter_: str = 'for_ios',
            offset: int = None,
            req_auth: bool = True
    ):
        """

        :param word:
        :param search_target: [partial_match_for_tags, exact_match_for_tags, title_and_caption]
        :param sort: [date_desc, date_asc]
        :param duration: [within_last_day, within_last_week, within_last_month]
        :param filter_:
        :param offset:
        :param req_auth:
        :return:
        """
        url = '%s/search/illust' % self.appv1
        params = self.set_params(
            word=word,
            search_target=search_target,
            sort=sort,
            filter=filter_,
            duration=duration,
            offset=offset
        )
        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    async def illust_bookmark_detail(
            self,
            illust_id: int,
            req_auth: bool = True
    ):
        """

        :param illust_id:
        :param req_auth:
        :return:
        """
        url = '%s/illust/bookmark/detail' % self.appv2
        params = self.set_params(
            illust_id=illust_id
        )
        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 新增收藏
    async def illust_bookmark_add(
            self,
            illust_id: int,
            restrict: str = 'public',
            tags=None,
            req_auth: bool = True
    ):
        """

        :param illust_id:
        :param restrict:
        :param tags:
        :param req_auth:
        :return:
        """
        url = '%s/illust/bookmark/add' % self.appv2
        data = self.set_params(
            illust_id=illust_id,
            restrict=restrict,
            tags=tags
        )
        return await self.no_auth_requests_call('POST', url, data=data, req_auth=req_auth)

    async def illust_bookmark_delete(
            self,
            illust_id: int = None,
            req_auth: bool = True
    ):
        """

        :param illust_id:
        :param req_auth:
        :return:
        """
        url = '%s/v1/illust/bookmark/delete' % self.hosts
        data = self.set_params(
            illust_id=illust_id
        )
        return await self.no_auth_requests_call('POST', url, data=data, req_auth=req_auth)

    # 用户收藏标签列表
    async def user_bookmark_tags_illust(
            self,
            restrict='public',
            offset=None,
            req_auth=True
    ):
        """

        :param restrict:
        :param offset:
        :param req_auth:
        :return:
        """
        url = '%s/v1/user/bookmark-tags/illust' % self.hosts
        params = self.set_params(
            restrict=restrict,
            offset=offset
        )
        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    async def user_following(
            self,
            user_id: int,
            restrict: str = 'public',
            offset: int = None,
            req_auth: bool = True
    ):
        """

        :param user_id:
        :param restrict:
        :param offset:
        :param req_auth:
        :return:
        """
        url = '%s/user/following' % self.appv1
        params = self.set_params(
            restrict=restrict,
            offset=offset,
            user_id=user_id
        )

        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    async def user_follower(
            self,
            user_id: int,
            filter_: str = 'for_ios',
            offset: int = None,
            req_auth: bool = True
    ):
        """

        :param user_id:
        :param filter_:
        :param offset:
        :param req_auth:
        :return:
        """
        url = '%s/user/follower' % self.appv1
        params = self.set_params(
            filter=filter_,
            offset=offset,
            user_id=user_id
        )

        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 好P友
    async def user_mypixiv(
            self,
            user_id: int,
            offset: int = None,
            req_auth: bool = True
    ):
        """

        :param user_id:
        :param offset:
        :param req_auth:
        :return:
        """
        url = '%s/v1/user/mypixiv' % self.hosts
        params = self.set_params(
            offset=offset,
            user_id=user_id
        )

        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 黑名单用户
    async def user_list(
            self,
            user_id: int,
            filter_: str = 'for_ios',
            offset: int = None,
            req_auth: bool = True
    ):
        """
        
        :param user_id: 
        :param filter_: 
        :param offset: 
        :param req_auth: 
        :return: 
        """
        url = '%s/user/list' % self.appv2
        params = self.set_params(
            filter=filter_,
            offset=offset,
            user_id=user_id
        )
        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    # 获取ugoira信息
    async def ugoira_metadata(
            self,
            illust_id,
            req_auth=True
    ):
        """

        :param illust_id:
        :param req_auth:
        :return:
        """
        url = '%s/ugoira/metadata' % self.appv1
        params = self.set_params(
            illust_id=illust_id
        )

        return await self.no_auth_requests_call('GET', url, params=params, req_auth=req_auth)

    async def showcase_article(
            self,
            showcase_id: int
    ):
        """

        :param showcase_id:
        :return:
        """
        url = 'https://www.pixiv.net/ajax/showcase/article'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/63.0.3239.132 Safari/537.36',
            'Referer': 'https://www.pixiv.net',
        }
        params = self.set_params(
            showcase_id=showcase_id
        )

        return await self.no_auth_requests_call('GET', url, headers=headers, params=params, req_auth=False)

    def set_api_proxy(self, proxy_hosts="http://app-api.pixivlite.com"):
        """Set proxy hosts: eg pixivlite.com"""
        self.hosts = proxy_hosts
