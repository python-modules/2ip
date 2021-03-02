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

    @staticmethod
    @lru_cache(maxsize = 10000)
    async def __request(
        ## The API URL to make the request to
        url: str,
        ## Parameters to add to the URL
        params: dict,
        ## Enable/disable the use of HTTP2
        http2: bool = True,
        ## Maximum connections default value
        max_connections: int = 10,
    ) -> object:
        """Send a HTTP request to the API

        Args:
            url (str): The API URL to make the request to
            params (dict): The parameters to add to the API request
            http2 (bool, optional): Enable HTTP2 support. Defaults to True.
            max_connections (int, optional): The maximum number of concurrent connections to the API. Defaults to 10.

        Raises:
            e: [description]

        Returns:
            object: [description]
        """

        ## Add version information to request header
        headers = {
            'User-Agent': f'TwoIP Python API Client/{__version__}',
        }

        ## Set maximum number of concurrent connections and keepalive connections
        limits = httpx.Limits(max_keepalive_connections = 5, max_connections = max_connections)

        ## Debug logging; skip if running optimized
        if __debug__:
            if http2:   ver = 'HTTP2'
            else:       ver = 'HTTP1'
            log.trace(f'New API {ver} request:\n'
                        f'  - URL: {url}\n'
                        f'  - Params: {params}\n'
                        f'  - Headers: {headers}\n'
                        f'  - Max Connections: {max_connections}'
            )

        ## Make the API request
        async with httpx.AsyncClient(limits = limits, http2 = http2, headers = headers) as client:
            try:
                response = await client.get(url = url, params = params)
            except Exception as e:
                log.error(f'Exception while making API request:\n{e}')
                raise e
            else:
                ## Log
                if __debug__:
                    log.trace(f'{response.status_code} Response from API: {response.text}')
                ## Return result
                return response

