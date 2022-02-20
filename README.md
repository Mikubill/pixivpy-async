PixivPy-Async 
======

[![PyPI version](https://badge.fury.io/py/PixivPy-Async.svg)](https://badge.fury.io/py/PixivPy-Async) 

_Async Pixiv API for Python 3(with Auth supported)_

PixivPy-Async is an async Python 3 library of Pixiv API(with Auth supported).

_Source: https://github.com/Mikubill/pixivpy-async_

_Based on PixivPy: https://github.com/upbit/pixivpy_

[中文说明](https://github.com/Mikubill/pixivpy-async/blob/master/README.zh-cn.md)

## Note

* You may need to use a Japanese IP (no matter native) to access the Pixiv API. IP from other regions may encounter Cloudflare verification.
* Pixiv API has a strict policy on access frequency. Recommended to add some waiting time when requesting

## Install

```bash
pip install pixivpy-async
```

## Or install with socks proxy support:
```bash
pip install pixivpy-async[socks]
```

## Import Package

Import **async** pixivpy:

```python
from pixivpy_async import *
```

...or **sync** pixivpy([Sync Support](https://github.com/Mikubill/pixivpy-async#sync-support)):
```python
from pixivpy_async.sync import *

```

## API Init

```python
# Use Context Manager (Recommended)
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

## Login

```python
# For App Pixiv API
await aapi.login(username, password)

# Or
await aapi.login(refresh_token=TOKEN)

# Login with oauth (manually)
await aapi.login_web()
```

## Proxy

The default is not to use any proxy (ignoring environment variables).

Use environment variables, automatically recognized by aiohttp (not support socks5)

```python
...PixivClient(env=True)
...AppPixivAPI(env=True)
```

Specify the proxy address, support socks5/socks4/http (not support https)

If use the socks5/socks4 proxy, make sure the package is installed with [socks proxy support](#or-install-with-socks-proxy-support).

```python
...PixivClient(proxy="socks5://127.0.0.1:8080")
...AppPixivAPI(proxy="socks5://127.0.0.1:8080")
```

If the package is not installed with [socks proxy support](#or-install-with-socks-proxy-support), and your application runs on Windows, please make sure that event loop uses the policy **asyncio.WindowsSelectorEventLoopPolicy** before loop runs. [#issue4536](https://github.com/aio-libs/aiohttp/issues/4536#issuecomment-579740877)

```python
import asyncio

if __name__ == '__main__':
    policy = asyncio.WindowsSelectorEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)
    asyncio.run(...)    # use pixivpy_async with socks proxy
```

Note that env will be ignored when a proxy is specified.


## Doing stuff

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
await aapi.illust_ranking('day', date='2016-08-01')
await aapi.illust_bookmark_detail(...)
await aapi.illust_bookmark_add(...)
await aapi.illust_bookmark_delete(...)
await aapi.download(image_url, path=directory, name=name)
await aapi.search_novel(...)
await aapi.user_novels(...)
await aapi.novel_series(...)
await aapi.novel_detail(...)
await aapi.novel_text(...)

# papi is deprecated
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

## Nest steps

_Read [docs](https://github.com/upbit/pixivpy/wiki) for more information_

_Read [demos](https://github.com/Mikubill/pixivpy-async/tree/master/demo) for more usage_


## Sync support

(Inspired by telethon)

The moment you import any of these:

```python
from pixivpy_async import sync, ...
# or
from pixivpy_async.sync import ...
# or
import pixivpy_async.sync
```

The sync module rewrites most async def methods in pixivpy_async to something similar to this:

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

That means you can do thing like this:

```python
aapi = AppPixivAPI()
aapi.login(username, password)
```

## Update

* [2019/09/13] First Version 

## Performance Testing

Warning: The rate limit was hit multiple times during the test, so the result may not be informative.

Script: https://github.com/Mikubill/pixivpy-async/blob/master/Perf.py


| Method | Sync(10,sg)  |  Async(10,sg)   |  Sync(200,sg)  |  Async(200,sg)   |
| ----  | ----  |  ----  | ----  |  ----  | 
|  illust_detail  | 1.1209 | 0.8641 | 31.7041 | 2.4580 |
| illust_ranking  | 1.0697 | 0.7936 | 28.4539 | 2.0693 |
|   user_illusts  | 0.8824 | 0.7505 | 28.3981 | 1.8199 |
|    user_detail  | 0.9628 | 0.7550 | 28.3055 | 1.7738 |
| ugoira_metadata | 0.8509 | 0.7459 | 29.5566 | 2.2331 |
| works           | 1.1204 | 0.8912 | 32.2068 | 2.8513 |
| me_following_works | 1.1253 | 0.7845 | 39.3142 | 2.2785 |
| ranking             | 1.0946 | 0.7944 | 39.6509 | 2.6548 |
| latest_works        | 1.0483 | 0.8667 | 36.1992 | 2.5066 |


| Method |  Sync(500,jp)  |  Async(500,jp)   |  
| ----  |  ----  |  ----  | 
|  illust_detail  |6.2178 | 0.6400 |
| illust_ranking  |6.4046 | 0.6119 |
|   user_illusts  |7.6093 | 1.5266 |
|    user_detail  |6.6759 | 0.5952 |
| ugoira_metadata |6.5155 | 0.7577 |
| works           | 13.3074| 0.8619|
| me_following_works | 24.2693|2.0835|
| ranking             | 21.4119|3.2805|
| latest_works        | 17.3502|2.7029|


<!-- 

(10,sg): https://img.vim-cn.com/4d/58f39562561685b4f8f930a5fb1f07f2318158 

(200,sg): https://img.vim-cn.com/d7/65f1f5989ad348af668c6da15c2abd9b1e65ca

(500,jp): https://cfp.vim-cn.com/cbf2y

-->

## License

Feel free to use, reuse and abuse the code in this project.
