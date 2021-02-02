#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import uuid
from pixivpy_async import *

_USERNAME = "userbay"
_PASSWORD = "UserPay"


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
    aapi.set_api_proxy(app_hosts="", auth_hosts="", pub_hosts="")
    await aapi.login(_USERNAME, _PASSWORD)
    result = await aapi.illust_ranking('day')
    for item in result.illusts:
        print(item.image_urls['large'])
        await aapi.download(item.image_urls['large'])


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main(AppPixivAPI()))


if __name__ == '__main__':
    main()
