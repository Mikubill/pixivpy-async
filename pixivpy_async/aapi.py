# -*- coding:utf-8 -*-
from .bapi import BasePixivAPI


# App-API (6.x - app-api.pixiv.net)


class AppPixivAPI(BasePixivAPI):
    def __init__(self, **requests_kwargs):
        """
        initialize requests kwargs if need be
        """
        super(AppPixivAPI, self).__init__(**requests_kwargs)

    async def user_detail(
            self,
            user_id: int = 660788,
            filter: str = 'for_ios',
            req_auth: bool = True
    ) -> dict:
        """
        {
            "user": {
                "id": int,
                "name": str,
                "account": str,
                "profile_image_urls": {
                    "medium": str
                },
                "comment": str,
                "is_followed": bool
            },

            "profile": {
                "webpage": str,
                "gender": str,
                "birth": str,
                "region": str,
                "job": str,
                "total_follow_users": int,
                "total_follower": int,
                "total_mypixiv_users": int,
                "total_illusts": int, "total_manga": int,
                "total_novels": int,
                "total_illust_bookmarks_public": int,
                "background_image_url": str,
                "twitter_account": str,
                "twitter_url": str,
                "is_premium": bool
            },

            "workspace": {
                "pc": str,
                "monitor": str,
                "tool": str,
                "scanner": str,
                "tablet": str,
                "mouse": str,
                "printer": str,
                "desktop": str,
                "music": str,
                "desk": str,
                "chair": str,
                "comment": str,
                "workspace_image_url": "str"
            }
        }
        """
        method, url = self.api.user_detail
        params = self.set_params(
            user_id=user_id,
            filter=filter
        )
        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    async def user_illusts(
            self,
            user_id: int,
            type: str = 'illust',
            filter: str = 'for_ios',
            offset: int = None,
            req_auth: bool = True
    ) -> dict:
        """
        {
            "illusts": [
                {
                    "id": int,
                    "title": str,
                    "type": str,
                    "image_urls": {
                        "square_medium": str,
                        "medium": str,
                        "large": str
                    },
                    "caption": str,
                    "restrict": int,
                    "user": {
                        "id": int,
                        "name": str,
                        "account": str,
                        "profile_image_urls": {
                            "medium": str
                        },
                        "is_followed": bool
                    },
                    "tags": [
                        {
                            "name": str
                        }
                    ],
                    "tools": [str],
                    "create_date": str,
                    "page_count": int,
                    "width": int,
                    "height": int,
                    "sanity_level": int,
                    "meta_single_page": {
                        "original_image_url": str
                    },
                    "meta_pages": [],
                    "total_view": int,
                    "total_bookmarks": int,
                    "is_bookmarked": bool,
                    "visible": bool,
                    "total_comments": int
                }
            ],
            "next_url": str
        }
        """
        method, url = self.api.user_illusts
        params = self.set_params(
            user_id=user_id,
            filter=filter,
            type=type,
            offset=offset
        )
        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    async def user_bookmarks_illust(
            self,
            user_id: int,
            restrict: str = 'public',
            filter: str = 'for_ios',
            max_bookmark_id: int = None,
            tag: str = None,
            req_auth: bool = True
    ):
        """
        {
            'illusts': [
                {
                    'id': int,
                    'title': str,
                    'type': str,
                    'image_urls': {
                        'square_medium': str,
                        'medium': str,
                        'large': str
                    },
                    'caption': str,
                    'restrict': int,
                    'user': {
                        'id': int,
                        'name': str,
                        'account': str,
                        'profile_image_urls': {
                            'medium': str
                        },
                        'is_followed': bool
                    },
                    'tags': [
                        {
                            'name': str
                            'translated_name': str
                        },
                    ],
                    'tools': [
                        'SAI'
                    ],
                    'create_date': str,
                    'page_count': int,
                    'width': int,
                    'height': int,
                    'sanity_level': int,
                    'x_restrict': int,
                    'series': None,
                    'meta_single_page': {
                        'original_image_url': str
                    },
                    'meta_pages': [],
                    'total_view': int,
                    'total_bookmarks': int,
                    'is_bookmarked': bool,
                    'visible': bool,
                    'is_muted': bool
                },
            ],
            'next_url': str
        }

        """
        method, url = self.api.user_bookmarks_illust
        params = self.set_params(
            user_id=user_id,
            filter=filter,
            restrict=restrict,
            max_bookmark_id=max_bookmark_id,
            tag=tag
        )
        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    async def illust_follow(
            self,
            restrict: str = 'public',
            offset: int = None,
            req_auth: bool = True
    ):
        """
        restrict: [public, private]
        """
        method, url = self.api.illust_follow
        params = self.set_params(
            restrict=restrict,
            offset=offset
        )
        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    # 作品详情 (类似PAPI.works()，iOS中未使用)
    async def illust_detail(
            self,
            illust_id: int,
            req_auth: bool = True
    ):
        method, url = self.api.illust_detail
        params = self.set_params(
            illust_id=illust_id
        )
        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    # 作品评论
    async def illust_comments(
            self,
            illust_id,
            offset=None,
            include_total_comments=None,
            req_auth=True
    ):
        method, url = self.api.illust_comments
        params = self.set_params(
            illust_id=illust_id,
            offset=offset,
            include_total_comments=include_total_comments
        )
        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    async def illust_related(
            self,
            illust_id: int,
            filter: str = 'for_ios',
            seed_illust_ids: list = None,
            offset: int = None,
            req_auth: bool = True
    ):
        method, url = self.api.illust_related
        params = self.set_params(
            illust_id=illust_id,
            offset=offset,
            filter=filter,
            seed_illust_ids=seed_illust_ids,
        )
        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    async def illust_recommended(
            self,
            content_type: str = 'illust',
            include_ranking_label: bool = True,
            filter: str = 'for_ios',
            max_bookmark_id_for_recommend: int = None,
            min_bookmark_id_for_recent_illust: int = None,
            offset: int = None,
            include_ranking_illusts=None,
            bookmark_illust_ids: list = None,
            include_privacy_policy=None,
            req_auth: bool = True
    ) -> dict:
        if req_auth:
            method, url = self.api.illust_recommended_auth
        else:
            method, url = self.api.illust_recommended_no_auth
        params = self.set_params(
            content_type=content_type,
            offset=offset,
            filter=filter,
            bookmark_illust_ids=bookmark_illust_ids,
            include_ranking_illusts=include_ranking_illusts,
            include_ranking_label=include_ranking_label,
            include_privacy_policy=include_privacy_policy,
            max_bookmark_id_for_recommend=max_bookmark_id_for_recommend,
            min_bookmark_id_for_recent_illust=min_bookmark_id_for_recent_illust,
        )
        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    async def illust_ranking(
            self,
            mode: str = 'day',
            filter: str = 'for_ios',
            date: str = None,
            offset: int = None,
            req_auth: bool = True
    ):
        method, url = self.api.illust_ranking
        params = self.set_params(
            date=date,
            offset=offset,
            filter=filter,
            mode=mode
        )
        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    # 趋势标签 (Search - tags)
    async def trending_tags_illust(
            self,
            filter: str = 'for_ios',
            req_auth: bool = True
    ):
        method, url = self.api.trending_tags_illust
        params = self.set_params(
            filter=filter
        )
        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    async def search_illust(
            self,
            word: str,
            search_target: str = 'partial_match_for_tags',
            sort: str = 'date_desc',
            duration: str = None,
            filter: str = 'for_ios',
            offset: int = None,
            req_auth: bool = True
    ):
        method, url = self.api.search_illust
        params = self.set_params(
            word=word,
            search_target=search_target,
            sort=sort,
            filter=filter,
            duration=duration,
            offset=offset
        )
        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    async def illust_bookmark_detail(
            self,
            illust_id: int,
            req_auth: bool = True
    ):
        method, url = self.api.illust_bookmark_detail
        params = self.set_params(
            illust_id=illust_id
        )
        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    # 新增收藏
    async def illust_bookmark_add(
            self,
            illust_id: int,
            restrict: str = 'public',
            tags=None,
            req_auth: bool = True
    ):
        method, url = self.api.illust_bookmark_add
        data = self.set_params(
            illust_id=illust_id,
            restrict=restrict,
            tags=tags
        )
        return await self.requests_(method=method, url=url, data=data, auth=req_auth)

    async def illust_bookmark_delete(
            self,
            illust_id: int = None,
            req_auth: bool = True
    ):
        method, url = self.api.illust_bookmark_delete
        data = self.set_params(
            illust_id=illust_id
        )
        return await self.requests_(method=method, url=url, data=data, auth=req_auth)

    # 用户收藏标签列表
    async def user_bookmark_tags_illust(
            self,
            restrict='public',
            offset=None,
            req_auth=True
    ):
        method, url = self.api.user_bookmark_tags_illust
        params = self.set_params(
            restrict=restrict,
            offset=offset
        )
        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    async def user_following(
            self,
            user_id: int,
            restrict: str = 'public',
            offset: int = None,
            req_auth: bool = True
    ):
        method, url = self.api.user_following
        params = self.set_params(
            restrict=restrict,
            offset=offset,
            user_id=user_id
        )

        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    async def user_follower(
            self,
            user_id: int,
            filter: str = 'for_ios',
            offset: int = None,
            req_auth: bool = True
    ):
        method, url = self.api.user_follower
        params = self.set_params(
            filter=filter,
            offset=offset,
            user_id=user_id
        )

        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    async def user_mypixiv(
            self,
            user_id: int,
            offset: int = None,
            req_auth: bool = True
    ):
        method, url = self.api.user_mypixiv
        params = self.set_params(
            offset=offset,
            user_id=user_id
        )

        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    async def user_list(
            self,
            user_id: int,
            filter: str = 'for_ios',
            offset: int = None,
            req_auth: bool = True
    ):
        method, url = self.api.user_list
        params = self.set_params(
            filter=filter,
            offset=offset,
            user_id=user_id
        )
        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    async def ugoira_metadata(
            self,
            illust_id: int,
            req_auth: bool = True
    ):
        method, url = self.api.ugoira_metadata
        params = self.set_params(
            illust_id=illust_id
        )

        return await self.requests_(method=method, url=url, params=params, auth=req_auth)

    async def showcase_article(
            self,
            showcase_id: int,
            req_auth: bool = False
    ):
        method, url = self.api.showcase_article
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/63.0.3239.132 Safari/537.36',
            'Referer': 'https://www.pixiv.net',
        }
        params = self.set_params(
            showcase_id=showcase_id
        )

        return await self.requests_(method=method, url=url, headers=headers, params=params, auth=req_auth)
