class API:
    def __init__(self,
                 app_hosts="https://app-api.pixiv.net",
                 pub_hosts="https://public-api.secure.pixiv.net",
                 auth_hosts="https://oauth.secure.pixiv.net"):
        self.appv1 = '%s/v1' % app_hosts
        self.appv2 = '%s/v2' % app_hosts
        self.prefix = '%s/v1.1/' % pub_hosts
        self.apiv1 = '%s/v1' % pub_hosts
        self.auth = '%s/auth/token' % auth_hosts
        pass

    """
        App - API
    """

    @property
    def user_detail(self):
        return 'GET', '%s/user/detail' % self.appv1

    @property
    def user_illusts(self):
        return 'GET', '%s/user/illusts' % self.appv1

    @property
    def user_bookmarks_illust(self):
        return 'GET', '%s/user/bookmarks/illust' % self.appv1

    @property
    def user_related(self):
        return 'GET', '%s/user/related' % self.appv1

    @property
    def illust_follow(self):
        return 'GET', '%s/illust/follow' % self.appv2

    @property
    def illust_detail(self):
        return 'GET', '%s/illust/detail' % self.appv1

    @property
    def illust_comments(self):
        return 'GET', '%s/illust/comments' % self.appv1

    @property
    def illust_related(self):
        return 'GET', '%s/illust/related' % self.appv2

    @property
    def illust_recommended_auth(self):
        return 'GET', '%s/illust/recommended' % self.appv1

    @property
    def illust_recommended_no_auth(self):
        return 'GET', '%s/illust/recommended-nologin' % self.appv1

    @property
    def illust_ranking(self):
        return 'GET', '%s/illust/ranking' % self.appv1

    @property
    def illust_new(self):
        return 'GET', '%s/illust/new' % self.apiv1

    @property
    def trending_tags_illust(self):
        return 'GET', '%s/trending-tags/illust' % self.appv1

    @property
    def search_illust(self):
        return 'GET', '%s/search/illust' % self.appv1

    @property
    def illust_bookmark_detail(self):
        return 'GET', '%s/illust/bookmark/detail' % self.appv2

    @property
    def illust_bookmark_add(self):
        return 'POST', '%s/illust/bookmark/add' % self.appv2

    @property
    def illust_bookmark_delete(self):
        return 'POST', '%s/illust/bookmark/delete' % self.appv1

    @property
    def user_bookmark_tags_illust(self):
        return 'GET', '%s/user/bookmark-tags/illust' % self.appv1

    @property
    def user_following(self):
        return 'GET', '%s/user/following' % self.appv1

    @property
    def user_follower(self):
        return 'GET', '%s/user/follower' % self.appv1

    @property
    def user_follow_add(self):
        return 'POST', '%s/user/follow/add' % self.appv1

    @property
    def user_follow_del(self):
        return 'POST', '%s/user/follow/delete' % self.appv1

    @property
    def user_mypixiv(self):
        return 'GET', '%s/user/mypixiv' % self.appv1

    @property
    def user_list(self):
        return 'GET', '%s/user/list' % self.appv2

    @property
    def ugoira_metadata(self):
        return 'GET', '%s/ugoira/metadata' % self.appv1

    @property
    def search_user(self):
        return 'GET', '%s/search/user' % self.appv1

    @property
    def search_novel(self):
        return 'GET', '%s/search/novel' % self.appv1

    @property
    def user_novels(self):
        return 'GET', '%s/user/novels' % self.appv1

    @property
    def novel_series(self):
        return 'GET', '%s/novel/series' % self.appv2

    @property
    def novel_detail(self):
        return 'GET', '%s/novel/detail' % self.appv2

    @property
    def novel_text(self):
        return 'GET', '%s/novel/text' % self.appv1

    """
        Public API
    """

    @property
    def me_feeds(self, ):
        return 'GET', '%s/me/feeds.json' % self.apiv1

    @property
    def me_favorite_works(self):
        return 'GET', '%s/me/favorite_works.json' % self.apiv1

    @property
    def me_favorite_works_add(self):
        return 'POST', '%s/me/favorite_works.json' % self.apiv1

    @property
    def me_favorite_works_delete(self):
        return 'DELETE', '%s/me/favorite_works.json' % self.apiv1

    @property
    def me_following_works(self):
        return 'GET', '%s/me/following/works.json' % self.apiv1

    @property
    def me_following(self):
        return 'GET', '%s/me/following.json' % self.apiv1

    @property
    def me_favorite_users_follow(self):
        return 'POST', '%s/me/favorite-users.json' % self.apiv1

    @property
    def me_favorite_users_unfollow(self):
        return 'DELETE', '%s/me/favorite-users.json' % self.apiv1

    @property
    def search_works(self):
        return 'GET', '%s/search/works.json' % self.apiv1

    @property
    def latest_works(self):
        return 'GET', '%s/works.json' % self.apiv1

    @property
    def bad_words(self):
        return 'GET', '%s/bad_words.json' % self.prefix

    @property
    def showcase_article(self):
        return 'GET', 'https://www.pixiv.net/ajax/showcase/article'

    def users_works(self, author_id):
        return 'GET', '%s/users/%d/works.json' % (self.apiv1, author_id)

    def users_favorite_works(self, author_id):
        return 'GET', '%s/users/%d/favorite_works.json' % (self.apiv1,
                                                           author_id)

    def users_feeds(self, author_id):
        return 'GET', '%s/users/%d/feeds.json' % (self.apiv1, author_id)

    def users_following(self, author_id):
        return 'GET', '%s/users/%d/following.json' % (self.apiv1, author_id)

    def works(self, illust_id):
        return 'GET', '%s/works/%s.json' % (self.apiv1, illust_id)

    def users(self, author_id):
        return 'GET', '%s/users/%s.json' % (self.apiv1, author_id)

    def ranking(self, ranking_type):
        return 'GET', '%s/ranking/%s.json' % (self.apiv1, ranking_type)
