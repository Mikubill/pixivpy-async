PixivPy-Async 
======

[![PyPI version](https://badge.fury.io/py/PixivPy-Async.svg)](https://badge.fury.io/py/PixivPy-Async)

_适用于 Python 3 的 Async Pixiv API（支持 Auth）_

_原地址: https://github.com/Mikubill/pixivpy-async_

_基于 PixivPy: https://github.com/upbit/pixivpy_

[English Version](https://github.com/Mikubill/pixivpy-async)

## 注意
 
* 你可能需要使用日本 IP（无论原生）来访问 Pixiv API，如使用其他地区 IP 可能会遇到 Cloudflare 验证。
* Pixiv API 的频率限制较为严格，请求时请适当加入等待时间

## 安装

建议安装最新版本以获得最佳支持。

```bash
pip install pixivpy-async --upgrade
```

## 或安装本库并安装 socks 代理支持

```bash
pip install pixivpy-async[socks]
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
aapi = AppPixivAPI()

# 绕过 SNI 检测
aapi = AppPixivAPI(bypass=True)
```

## 登录

```python
# For App Pixiv API
await aapi.login(username, password)

# Or
await aapi.login(refresh_token=TOKEN)

# Login with oauth (manually)
await aapi.login_web()
```

## 代理说明

Pixivpy-Async 支持多种代理模式，均需在 Init 时指定。

默认为不使用任何代理（忽略环境变量）。

使用环境变量，由 aiohttp 自动识别（暂不支持 socks5）

```python
...PixivClient(env=True)
...AppPixivAPI(env=True)
```

指定代理地址，支持 socks5/socks4/http（不支持 https）

如果使用的是 socks5/socks4 代理，请确保安装的本库拥有[socks 代理支持](#或安装本库并安装socks代理支持)

```python
...PixivClient(proxy="socks5://127.0.0.1:8080")
...AppPixivAPI(proxy="socks5://127.0.0.1:8080")
```

如果本库安装时没有安装[socks 代理支持](#或安装本库并安装socks代理支持)，并且你的应用运行在 Windows 上，请确保事件循环在运行前将策略设置为 **asyncio.WindowsSelectorEventLoopPolicy**。 [#issue4536](https://github.com/aio-libs/aiohttp/issues/4536#issuecomment-579740877)

```python
import asyncio

if __name__ == '__main__':
    policy = asyncio.WindowsSelectorEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)
    asyncio.run(...)    # use pixivpy_async with socks proxy
```

注意，指定了 proxy 后 env 会被忽略。



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
await aapi.user_related(...)
await aapi.user_follow_add(...)
await aapi.user_follow_del(...)
await aapi.user_bookmark_tags_illust(...)
await aapi.user_list(...)
await aapi.search_user(...)

await aapi.trending_tags_illust()
await aapi.search_illust(first_tag, search_target='partial_match_for_tags')
await aapi.illust_ranking('day_male')
await aapi.illust_follow(req_auth=True)
await aapi.illust_recommended(req_auth=True)
await aapi.illust_bookmark_detail(...)
await aapi.illust_bookmark_add(...)
await aapi.illust_bookmark_delete(...)

await aapi.illust_ranking('day', date='2016-08-01')
await aapi.download(image_url, path=directory, name=name)

await aapi.search_novel(...)
await aapi.user_novels(...)
await aapi.novel_series(...)
await aapi.novel_detail(...)
await aapi.novel_text(...)

# papi 已弃用，请使用 aapi
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

_查看 [样例](https://github.com/Mikubill/pixivpy-async/tree/master/demo) 来掌握 API 的使用_


## 同步支持

(源自 telethon)

每当输入以下代码时：

```python
from pixivpy_async import sync, ...
# or
from pixivpy_async.sync import ...
# or
import pixivpy_async.sync
```

sync 模块会将大多数异步方法改写成类似下面的样子：

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

这意味着您可以使用类似原始 pixivpy 的方法：

```python
aapi = AppPixivAPI()
aapi.login(username, password)
```

## 更新日志

* [2019/09/13] First Version 
