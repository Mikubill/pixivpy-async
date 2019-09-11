PixivPy-Async 
======

[![Build Status](https://travis-ci.org/Mikubill/pixivpy-async.svg)](https://travis-ci.org/Mikubill/pixivpy-async) [![PyPI version](https://badge.fury.io/py/PixivPy-Async.svg)](https://badge.fury.io/py/PixivPy-Async) [![codecov](https://codecov.io/gh/Mikubill/pixivpy-async/branch/master/graph/badge.svg)](https://codecov.io/gh/Mikubill/pixivpy-async)

_适用于Python 3的Async Pixiv API（支持Auth）_

_原地址: https://github.com/Mikubill/pixivpy-async_

_基于PixivPy: https://github.com/upbit/pixivpy_

[English Version](https://github.com/Mikubill/pixivpy-async)

## 安装

建议安装最新版本以获得最佳支持。

```bash
pip install pixivpy-async --upgrade
```

## 导入

导入 pixivpy-async:

```python
from pixivpy_async import *
```

...或者也可以选择 **同步化版本** ([同步支持](https://github.com/Mikubill/pixivpy-async/blob/master/README.zh-cn.md#同步支持)):
```python
from pixivpy_async.sync import *
```

## API Init

```python
# 使用 Context Manager (推荐)
async with PixivClient() as client:
    aapi = AppPixivAPI(client=client)
    # Doing stuff...
    
# Or
client = PixivClient()
aapi = AppPixivAPI(client=client.start())
# Doing stuff...
await client.close()

# Or Following Standard Usage
papi = PixivAPI()
aapi = AppPixivAPI()
```

## 登录

```python
# For Public Pixiv API
await papi.login(username, password)

# For App Pixiv API
await papi.login(username, password)
```

## 尽情地使用

```python
await aapi.illust_detail(59580629)
await aapi.illust_comments(59580629)
await aapi.ugoira_metadata(51815717)

await aapi.illust_recommended(bookmark_illust_ids=[59580629])
aapi.parse_qs(json_result.next_url) # page down in some case
await aapi.illust_recommended(**next_qs)

await aapi.illust_related(59580629)
await aapi.user_detail(275527)
await aapi.user_illusts(275527)
await aapi.user_bookmarks_illust(2088434)
await aapi.user_following(7314824)
await aapi.user_follower(275527)
await aapi.user_mypixiv(275527)

await aapi.trending_tags_illust()
await aapi.search_illust(first_tag, search_target='partial_match_for_tags')
await aapi.illust_ranking('day_male')
await aapi.illust_follow(req_auth=True)
await aapi.illust_recommended(req_auth=True)

await aapi.illust_ranking('day', date='2016-08-01')
await aapi.download(image_url, path=directory, name=name)

await papi.works(46363414)
await papi.users(1184799)
await papi.me_feeds(show_r18=0)
await papi.me_favorite_works(publicity='private')
await papi.me_following_works()
await papi.me_following()

await papi.users_works(1184799)
await papi.users_favorite_works(1184799)
await papi.users_feeds(1184799, show_r18=0)
await papi.users_following(4102577)
await papi.ranking('illust', 'weekly', 1)
await papi.ranking(ranking_type='all', mode='daily', page=1, date='2015-05-01')

await papi.search_works("五航戦 姉妹", page=1, mode='text')
await papi.latest_works()
```

## 更进一步...

_阅读 [文档](https://github.com/upbit/pixivpy/wiki) 来了解更多信息_

_查看 [样例](https://github.com/Mikubill/pixivpy-async/tree/master/demo) 来掌握API的使用_


## 同步支持

(源自telethon)

每当输入以下代码时:

```python
from pixivpy_async import sync, ...
# or
from pixivpy_async.sync import ...
# or
import pixivpy_async.sync
```

sync模块会将大多数异步方法改写成类似下面的样子:

```python
def new_method():
    result = original_method()
    if loop.is_running():
        # the loop is already running, return the await-able to the user
        return result
    else:
        # the loop is not running yet, so we can run it for the user
        return loop.run_until_complete(result)
```

这意味着您可以使用类似原始pixivpy的方法:

```python
aapi = AppPixivAPI()
aapi.login(username, password)
```

## 更新日志

* [2019/09/13] First Version 
