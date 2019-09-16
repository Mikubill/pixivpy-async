"""
Pixiv API library
"""
__version__ = '1.2.5'

from .aapi import AppPixivAPI
from .papi import PixivAPI
from .client import PixivClient
from . import error


__all__ = ("PixivAPI", "AppPixivAPI", "error", "PixivClient")
