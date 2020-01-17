#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from pixivpy_async import *

_USERNAME = "userbay"
_PASSWORD = "userpay"


async def _main(aapi):
    """
    Tips: How to create a proxy for Pixiv api? Just throw the following code into a CloudFlare worker.

    ```js
    addEventListener("fetch", e => {
        let t = e.request, d = new URL(t.url);
        d.hostname = "app-api.pixiv.net"; // Or public-api.secure.pixiv.net, oauth.secure.pixiv.net
        e.respondWith(fetch(d, {body: t.body, headers: t.headers, method: t.method}))
    });
    ```
    """
    aapi.set_api_proxy()
    await aapi.login(_USERNAME, _PASSWORD)
    result = await aapi.illust_ranking('day')
    for item in result.illusts:
        print(">>> %s, origin url: %s" % (item.title, item.image_urls['large']))


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(AppPixivAPI()))


if __name__ == '__main__':
    main()
