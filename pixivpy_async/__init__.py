"""
Pixiv API library
"""
__version__ = '1.2.14'

from .aapi import AppPixivAPI
from .papi import PixivAPI
from .client import PixivClient
from . import error
from .error import PixivError


__all__ = ("PixivAPI", "AppPixivAPI", "error", "PixivClient", "PixivError")
