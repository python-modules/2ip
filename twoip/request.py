# -*- coding: utf-8 -*-

# Import core modules
import asyncio
import logging as log
from functools import lru_cache
from typing import Optional
from urllib import parse as urlparse

# Import third party modules
import httpx

# Import version info to add to HTTP headers
from .__version__ import __version__

class Request(object):
    """
    2ip.me API client
    """

    def __init__(self,
        ## Optional API key
        key: Optional[str] = None,
        ## The API URL
        api: str = 'https://api.2ip.ua',
        ## The maximum number of concurrent API HTTP connections allowed
        connections: int = 10,
        ## Allow the use of HTTP2 (requiring the h2 module to be installed)
        http2: bool = True,
    ) -> object:



    async def __generate_request(self, uri: str, params: dict) -> object:
        ## If the API key is configured, add it to the parameters
        if self._key and 'key' not in params:
            params['key'] = self._key

        ## Get the URL that the request needs to be made to
        url = self.__generate_url(uri = uri)

        ## Send request
        self.__request(url = url, params = params, http2 = self._http2, max_connections = self._connections)

    async def __generate_url(self, uri: str) -> str:
        parts = list(urlparse.urlparse(self._api))
        parts[2] = uri
        return urlparse.urlunparse(parts)



