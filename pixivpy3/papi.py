# -*- coding:utf-8 -*-
from pixivpy3 import PixivError
from .api import BasePixivAPI


# Public-API


class PixivAPI(BasePixivAPI):
    def __init__(self, **requests_kwargs):
        """
        initialize requests kwargs if need be
        """
        self.prefix = 'https://public-api.secure.pixiv.net/v1.1/'
        self.apiv1 = 'https://public-api.secure.pixiv.net/v1'
        super().__init__(**requests_kwargs)

    async def auth_requests_call(
            self,
            method: str = 'GET',
            url: str = '',
            params: dict = None,
            data: dict = None,
            headers: dict = None
    ):
        if self.access_token is None:
            raise PixivError('No access_token Found!')
        headers = self.set_public_headers(headers, self.access_token)
        return await self.requests_call(method, url, headers, params, data)

    async def works(
            self,
            illust_id: int = 121827112,
            include_sanity_level: bool = False
    ):
        """

        :param illust_id: int
        :param include_sanity_level: True, False
        :return: Coroutine
        """
        url = '%s/works/%s.json' % (self.apiv1, illust_id)
        params = self.set_params(
            image_sizes='px_128x128,small,medium,large,px_480mw',
            include_stats='true',
            include_sanity_level=include_sanity_level
        )
        return await self.auth_requests_call('GET', url, params=params)

    async def users(
            self,
            author_id: int
    ):
        """

        :param author_id: int
        :return: Coroutine
        """
        url = '%s/users/%s.json' % (self.apiv1, author_id)
        params = self.set_params(
            profile_image_sizes=['px_170x170', 'px_50x50'],
            image_sizes=['px_128x128', 'small', 'medium', 'large', 'px_480mw'],
            include_stats=1,
            include_profile=1,
            include_workspace=1,
            include_contacts=1,
        )
        return await self.auth_requests_call('GET', url, params=params)

    async def me_feeds(
            self,
            show_r18: int = 1,
            max_id: int = None
    ):
        """

        :param show_r18: int(1, 0)
        :param max_id: int
        :return: Coroutine
        """
        url = '%s/me/feeds.json' % self.apiv1
        params = self.set_params(
            relation='all',
            type='touch_nottext',
            show_r18=show_r18,
        )
        if max_id:
            params['max_id'] = max_id
        return await self.auth_requests_call('GET', url, params=params)

    async def me_favorite_works(
            self,
            page: int = 1,
            per_page: int = 50,
            publicity: str = 'public',
            image_sizes: dict = None
    ):
        """

        :param page:
        :param per_page:
        :param publicity:
        :param image_sizes:
        :return: Coroutine
        """
        url = '%s/me/favorite_works.json' % self.apiv1
        params = self.set_params(
            page=page,
            per_page=per_page,
            publicity=publicity,
            image_sizes=image_sizes if image_sizes else ['px_128x128', 'px_480mw', 'large'],
        )
        return await self.auth_requests_call('GET', url, params=params)

    async def me_favorite_works_add(
            self,
            work_id: int,
            publicity: str = 'public'
    ):
        """

        :param work_id:
        :param publicity:
        :return:
        """
        url = '%s/me/favorite_works.json' % self.apiv1
        params = self.set_params(
            work_id=work_id,
            publicity=publicity,
        )
        return await self.auth_requests_call('POST', url, params=params)

    async def me_favorite_works_delete(
            self,
            ids: list,
            publicity: str = 'public'
    ):
        """

        :param ids:
        :param publicity:
        :return:
        """
        url = '%s/me/favorite_works.json' % self.apiv1
        params = self.set_params(
            ids=ids,
            publicity=publicity
        )
        return await self.auth_requests_call('DELETE', url, params=params)

    async def me_following_works(
            self,
            page: int = 1,
            per_page: int = 30,
            image_sizes: list = None,
            include_stats: bool = True,
            include_sanity_level: bool = True
    ):
        """

        :param page:
        :param per_page:
        :param image_sizes:
        :param include_stats:
        :param include_sanity_level:
        :return:
        """
        url = '%s/me/following/works.json' % self.apiv1
        params = self.set_params(
            page=page,
            per_page=per_page,
            image_sizes=image_sizes if image_sizes else ['px_128x128', 'px_480mw', 'large'],
            include_stats=include_stats,
            include_sanity_level=include_sanity_level,
        )
        return await self.auth_requests_call('GET', url, params=params)

    async def me_following(
            self,
            page: int = 1,
            per_page: int = 30,
            publicity: str = 'public'
    ):
        """

        :param page:
        :param per_page:
        :param publicity:
        :return:
        """
        url = '%s/me/following.json' % self.apiv1
        params = self.set_params(
            page=page,
            per_page=per_page,
            publicity=publicity,
        )
        return await self.auth_requests_call('GET', url, params=params)

    async def me_favorite_users_follow(
            self,
            user_id,
            publicity='public'
    ):
        """

        :param user_id:
        :param publicity:
        :return:
        """
        url = '%s/me/favorite-users.json' % self.apiv1
        params = self.set_params(
            target_user_id=user_id,
            publicity=publicity
        )
        return await self.auth_requests_call('POST', url, params=params)

    async def me_favorite_users_unfollow(
            self,
            user_ids,
            publicity='public'
    ):
        """

        :param user_ids:
        :param publicity:
        :return:
        """
        url = '%s/me/favorite-users.json' % self.apiv1
        params = self.set_params(
            delete_ids=user_ids,
            publicity=publicity
        )
        return await self.auth_requests_call('DELETE', url, params=params)

    async def users_works(
            self,
            author_id: int,
            page: int = 1,
            per_page: int = 30,
            image_sizes: list = None,
            include_stats: bool = True,
            include_sanity_level: bool = True
    ):
        """

        :param author_id:
        :param page:
        :param per_page:
        :param image_sizes:
        :param include_stats:
        :param include_sanity_level:
        :return:
        """
        url = '%s/users/%d/works.json' % (self.apiv1, author_id)
        params = self.set_params(
            page=page,
            per_page=per_page,
            include_stats=include_stats,
            include_sanity_level=include_sanity_level,
            image_sizes=image_sizes if image_sizes else ['px_128x128', 'px_480mw', 'large']
        )
        return await self.auth_requests_call('GET', url, params=params)

    async def users_favorite_works(
            self,
            author_id: int,
            page: int = 1,
            per_page: int = 30,
            image_sizes: list = None,
            include_sanity_level: list = True
    ):
        """

        :param author_id:
        :param page:
        :param per_page:
        :param image_sizes:
        :param include_sanity_level:
        :return:
        """
        url = '%s/users/%d/favorite_works.json' % (self.apiv1, author_id)

        params = self.set_params(
            page=page,
            per_page=per_page,
            include_sanity_level=include_sanity_level,
            image_sizes=image_sizes if image_sizes else ['px_128x128', 'px_480mw', 'large']
        )
        return await self.auth_requests_call('GET', url, params=params)

    async def users_feeds(
            self,
            author_id: int,
            show_r18: int = 1,
            max_id: int = None
    ):
        """

        :param author_id:
        :param show_r18:
        :param max_id:
        :return:
        """
        url = 'https://public-api.secure.pixiv.net/v1/users/%d/feeds.json' % author_id
        params = self.set_params(
            relation='all',
            type='touch_nottext',
            show_r18=show_r18,
            max_id=max_id
        )
        return await self.auth_requests_call('GET', url, params=params)

    async def users_following(
            self,
            author_id: int,
            page: int = 1,
            per_page: int = 30
    ):
        """

        :param author_id:
        :param page:
        :param per_page:
        :return:
        """
        url = '%s/users/%d/following.json' % (self.apiv1, author_id)
        params = self.set_params(
            page=page,
            per_page=per_page
        )
        return await self.auth_requests_call('GET', url, params=params)

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
        """

        :param ranking_type:
        :param mode:
        :param page:
        :param per_page:
        :param date:
        :param image_sizes:
        :param profile_image_sizes:
        :param include_stats:
        :param include_sanity_level:
        :return:
        """
        url = '%s/ranking/%s.json' % (self.apiv1, ranking_type)
        params = self.set_params(
            date=date,
            mode=mode,
            page=page,
            per_page=per_page,
            include_stats=include_stats,
            include_sanity_level=include_sanity_level,
            image_sizes=image_sizes if image_sizes else ['px_128x128', 'px_480mw', 'large'],
            profile_image_sizes=profile_image_sizes if profile_image_sizes else ['px_170x170', 'px_50x50'],
        )
        return await self.auth_requests_call('GET', url, params=params)

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
        """

        :param query:
        :param page:
        :param per_page:
        :param mode:
        :param period:
        :param order:
        :param sort:
        :param types:
        :param image_sizes:
        :param include_stats:
        :param include_sanity_level:
        :return:
        """
        url = '%s/search/works.json' % self.apiv1
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
            image_sizes=image_sizes if image_sizes else ['px_128x128', 'px_480mw', 'large'],
            types=types if types else ['illustration', 'manga', 'ugoira'],
        )
        return await self.auth_requests_call('GET', url, params=params)

    async def latest_works(
            self,
            page: int = 1,
            per_page: int = 30,
            image_sizes: list = None,
            profile_image_sizes: list = None,
            include_stats: bool = True,
            include_sanity_level: bool = True
    ):
        """

        :param page:
        :param per_page:
        :param image_sizes:
        :param profile_image_sizes:
        :param include_stats:
        :param include_sanity_level:
        :return:
        """
        url = '%s/works.json' % self.apiv1
        params = self.set_params(
            page=page,
            per_page=per_page,
            include_stats=include_stats,
            include_sanity_level=include_sanity_level,
            image_sizes=image_sizes if image_sizes else ['px_128x128', 'px_480mw', 'large'],
            profile_image_sizes=profile_image_sizes if profile_image_sizes else ['px_170x170', 'px_50x50'],
        )
        return await self.auth_requests_call('GET', url, params=params)

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
        """

        :param mode:
        :param page:
        :param per_page:
        :param date:
        :param image_sizes:
        :param profile_image_sizes:
        :param include_stats:
        :param include_sanity_level:
        :return:
        """
        return self.ranking(
            ranking_type='all',
            mode=mode,
            page=page,
            per_page=per_page,
            date=date,
            include_stats=include_stats,
            include_sanity_level=include_sanity_level,
            image_sizes=image_sizes if image_sizes else ['px_128x128', 'px_480mw', 'large'],
            profile_image_sizes=profile_image_sizes if profile_image_sizes else ['px_170x170', 'px_50x50'],
        )

    async def bad_words(self):
        url = '%s/bad_words.json' % self.prefix
        return await self.auth_requests_call('GET', url)
