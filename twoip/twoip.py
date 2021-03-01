# -*- coding: utf-8 -*-

# Import core modules
import logging as log
from functools import lru_cache
from typing import Optional

# Import third party modules
import asyncio
import httpx

# Import version info to add to HTTP headers
from .__version__ import __version__

# Import data types to store results
from .datatypes import GeoResult

class TwoIP(object):
    """
    2ip.me API client
    """

    def __init__(self,
        ## Optional API key
        key: Optional[str] = None,
        ## The API endpoint
        api: str = 'https://api.2ip.ua',
        ## The maximum number of concurrent API HTTP connections allowed
        connections: int = 10,
        ## Allow the use of HTTP2 (requiring the h2 module to be installed)
        http2: bool = True,
    ) -> object:
        """Create a new TwoIP API object

        Args:
            key (str, optional): The API key to use for requests. Defaults to None.
            api (str, optional): The API endpoint. Defaults to 'https://api.2ip.ua'.
            connections (int, optional): The maximum number of concurrent connections allowed. Defaults to 10.
            http2 (bool, optional): Enable/disable HTTP2. If enabled the ht2 module must be installed. Defaults to True.

        Returns:
            object: The initialized TwoIP object
        """
        log.debug(f'New TwoIP object created')

        ## Set API endpoint
        log.trace(f'API endpoint: {api}')
        self._api = api

        ## Set API key
        if key:
            log.trace(f'API key: {key}')
            self._key = key

    @staticmethod
    async def request(
        ## The API URL to make the request to
        url: str,
        ## Parameters to add to the URL
        params: Optional[dict] = None,
        ## Enable/disable the use of HTTP2
        http2: bool = True,
        ## Maximum number of concurrent HTTP connections allowed
        max: int = 10
    ) -> object:

        ## Add version information to request header
        headers = {
            'User-Agent': f'TwoIP Python API Client/{__version__}',
        }

        ## Set maximum number of concurrent connections and keepalive connections
        limits = httpx.Limits(max_keepalive_connections = 5, max_connections = max)

        ## Log
        if __debug__:
            if http2:   ver = 'HTTP2'
            else:       ver = 'HTTP1'
            log.trace(f'New API {ver} request:\n'
                        f'  - URL: {url}\n'
                        f'  - Params: {params}\n'
                        f'  - Headers: {headers}\n'
                        f'  - Max Connections: {max}'
            )

        ## Make the API request
        async with httpx.AsyncClient(limits = limits, http2 = http2, headers = headers) as client:
            try:
                response = await client.get(url = url, params = params)
            except Exception as e:
                log.error(f'Exception while making API request: {e}')
                raise e
            else:
                ## Log
                if __debug__:
                    log.trace(f'{response.status_code} Response from API: {response.text}')
                ## Return result
                return response

    #@lru_cache(maxsize = 50000)


