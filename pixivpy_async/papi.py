# -*- coding:utf-8 -*-
from .bapi import BasePixivAPI
from deprecated import deprecated

# Public-API


@deprecated(version='1.2.15', reason="Public API is deprecated by Pixiv. You should use AppPixivAPI.")
class PixivAPI(BasePixivAPI):
    def __init__(self, **requests_kwargs):
        """
        initialize requests kwargs if need be
        """
        super().__init__(**requests_kwargs)

    async def works(
            self,
            illust_id: int = 121827112,
            include_sanity_level: bool = False
    ):
        method, url = self.api.works(illust_id)
        params = self.set_params(
            image_sizes=['px_128x128', 'small', 'medium', 'large', 'px_480mw'],
            include_stats=True,
            include_sanity_level=include_sanity_level
        )
        return await self.requests_(method=method, url=url, params=params, auth=True)

    async def users(
            self,
            author_id: int
    ):
        method, url = self.api.users(author_id)
        params = self.set_params(
            profile_image_sizes=['px_170x170', 'px_50x50'],
            image_sizes=['px_128x128', 'small', 'medium', 'large', 'px_480mw'],
            include_stats=1,
            include_profile=1,
            include_workspace=1,
            include_contacts=1,
        )
        return await self.requests_(method=method, url=url, params=params, auth=True)

    async def me_feeds(
            self,
            show_r18: int = 1,
            max_id: int = None
    ):
        method, url = self.api.me_feeds
        params = self.set_params(
            relation='all',
            type='touch_nottext',
            show_r18=show_r18,
        )
        if max_id:
            params['max_id'] = max_id
        return await self.requests_(method=method, url=url, params=params, auth=True)

    async def me_favorite_works(
            self,
            page: int = 1,
            per_page: int = 50,
            publicity: str = 'public',
            image_sizes: dict = None
    ):
        method, url = self.api.me_favorite_works
        params = self.set_params(
            page=page,
            per_page=per_page,
            publicity=publicity,
            image_sizes=image_sizes if image_sizes else [
                'px_128x128', 'px_480mw', 'large'],
        )
        return await self.requests_(method=method, url=url, params=params, auth=True)

    async def me_favorite_works_add(
            self,
            work_id: int,
            publicity: str = 'public'
    ):
        method, url = self.api.me_favorite_works_add
        params = self.set_params(
            work_id=work_id,
            publicity=publicity,
        )
        return await self.requests_(method=method, url=url, params=params, auth=True)

    async def me_favorite_works_delete(
            self,
            ids: list,
            publicity: str = 'public'
    ):
        method, url = self.api.me_favorite_works_delete
        params = self.set_params(
            ids=ids,
            publicity=publicity
        )
        return await self.requests_(method=method, url=url, params=params, auth=True)

    async def me_following_works(
            self,
            page: int = 1,
            per_page: int = 30,
            image_sizes: list = None,
            include_stats: bool = True,
            include_sanity_level: bool = True
    ):
        method, url = self.api.me_following_works
        params = self.set_params(
            page=page,
            per_page=per_page,
            image_sizes=image_sizes if image_sizes else [
                'px_128x128', 'px_480mw', 'large'],
            include_stats=include_stats,
            include_sanity_level=include_sanity_level,
        )
        return await self.requests_(method=method, url=url, params=params, auth=True)

    async def me_following(
            self,
            page: int = 1,
            per_page: int = 30,
            publicity: str = 'public'
    ):
        method, url = self.api.me_following
        params = self.set_params(
            page=page,
            per_page=per_page,
            publicity=publicity,
        )
        return await self.requests_(method=method, url=url, params=params, auth=True)

    async def me_favorite_users_follow(
            self,
            user_id,
            publicity='public'
    ):
        method, url = self.api.me_favorite_users_follow
        params = self.set_params(
            target_user_id=user_id,
            publicity=publicity
        )
        return await self.requests_(method=method, url=url, params=params, auth=True)

    async def me_favorite_users_unfollow(
            self,
            user_ids,
            publicity='public'
    ):
        method, url = self.api.me_favorite_users_unfollow
        params = self.set_params(
            delete_ids=user_ids,
            publicity=publicity
        )
        return await self.requests_(method=method, url=url, params=params, auth=True)

    async def users_works(
            self,
            author_id: int,
            page: int = 1,
            per_page: int = 30,
            image_sizes: list = None,
            include_stats: bool = True,
            include_sanity_level: bool = True
    ):
        method, url = self.api.users_works(author_id)
        params = self.set_params(
            page=page,
            per_page=per_page,
            include_stats=include_stats,
            include_sanity_level=include_sanity_level,
            image_sizes=image_sizes if image_sizes else [
                'px_128x128', 'px_480mw', 'large']
        )
        return await self.requests_(method=method, url=url, params=params, auth=True)

    async def users_favorite_works(
            self,
            author_id: int,
            page: int = 1,
            per_page: int = 30,
            image_sizes: list = None,
            include_sanity_level: list = True
    ):
        method, url = self.api.users_favorite_works(author_id)
        params = self.set_params(
            page=page,
            per_page=per_page,
            include_sanity_level=include_sanity_level,
            image_sizes=image_sizes if image_sizes else [
                'px_128x128', 'px_480mw', 'large']
        )
        return await self.requests_(method=method, url=url, params=params, auth=True)

    async def users_feeds(
            self,
            author_id: int,
            show_r18: int = 1,
            max_id: int = None
    ):
        method, url = self.api.users_feeds(author_id)
        params = self.set_params(
            relation='all',
            type='touch_nottext',
            show_r18=show_r18,
            max_id=max_id
        )
        return await self.requests_(method=method, url=url, params=params, auth=True)

    async def users_following(
            self,
            author_id: int,
            page: int = 1,
            per_page: int = 30
    ):
        method, url = self.api.users_following(author_id)
        params = self.set_params(
            page=page,
            per_page=per_page
        )
        return await self.requests_(method=method, url=url, params=params, auth=True)

    async def ranking(
            self,
            ranking_type: str = 'all',
            mode: str = 'daily',
            page: int = 1,
            per_page: int = 50,
            date=None,
            image_sizes: list = None,
            profile_image_sizes: list = None,
            include_stats: bool = True,
            include_sanity_level: bool = True
    ):
        method, url = self.api.ranking(ranking_type)
        params = self.set_params(
            date=date,
            mode=mode,
            page=page,
            per_page=per_page,
            include_stats=include_stats,
            include_sanity_level=include_sanity_level,
            image_sizes=image_sizes if image_sizes else [
                'px_128x128', 'px_480mw', 'large'],
            profile_image_sizes=profile_image_sizes if profile_image_sizes else [
                'px_170x170', 'px_50x50'],
        )
        return await self.requests_(method=method, url=url, params=params, auth=True)

    async def search_works(
            self,
            query,
            page: int = 1,
            per_page: int = 30,
            mode: str = 'text',
            period: str = 'all',
            order: str = 'desc',
            sort: str = 'date',
            types: list = None,
            image_sizes: list = None,
            include_stats: bool = True,
            include_sanity_level: bool = True
    ):
        method, url = self.api.search_works
        params = self.set_params(
            q=query,
            sort=sort,
            period=period,
            order=order,
            mode=mode,
            page=page,
            per_page=per_page,
            include_stats=include_stats,
            include_sanity_level=include_sanity_level,
            image_sizes=image_sizes if image_sizes else [
                'px_128x128', 'px_480mw', 'large'],
            types=types if types else ['illustration', 'manga', 'ugoira'],
        )
        return await self.requests_(method=method, url=url, params=params, auth=True)

    async def latest_works(
            self,
            page: int = 1,
            per_page: int = 30,
            image_sizes: list = None,
            profile_image_sizes: list = None,
            include_stats: bool = True,
            include_sanity_level: bool = True
    ):
        method, url = self.api.latest_works
        params = self.set_params(
            page=page,
            per_page=per_page,
            include_stats=include_stats,
            include_sanity_level=include_sanity_level,
            image_sizes=image_sizes if image_sizes else [
                'px_128x128', 'px_480mw', 'large'],
            profile_image_sizes=profile_image_sizes if profile_image_sizes else [
                'px_170x170', 'px_50x50'],
        )
        return await self.requests_(method=method, url=url, params=params, auth=True)

    def ranking_all(
            self,
            mode='daily',
            page=1,
            per_page=50,
            date=None,
            image_sizes=None,
            profile_image_sizes=None,
            include_stats=True,
            include_sanity_level=True
    ):
        return self.ranking(
            ranking_type='all',
            mode=mode,
            page=page,
            per_page=per_page,
            date=date,
            include_stats=include_stats,
            include_sanity_level=include_sanity_level,
            image_sizes=image_sizes if image_sizes else [
                'px_128x128', 'px_480mw', 'large'],
            profile_image_sizes=profile_image_sizes if profile_image_sizes else [
                'px_170x170', 'px_50x50'],
        )

    async def bad_words(self):
        method, url = self.api.bad_words
        return await self.requests_(method=method, url=url, auth=True)
