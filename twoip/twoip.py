# -*- coding: utf-8 -*-

# Import core modules
import logging as log
from typing import Optional

# Import data types to store results
from .datatypes.geo import GeoLookup, GeoLookupResult

class TwoIP(object):
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
        """Create a new TwoIP API object

        Args:
            key (str, optional): The API key to use for requests. Defaults to None.
            api (str, optional): The API endpoint. Defaults to 'https://api.2ip.ua'.
            connections (int, optional): The maximum number of concurrent connections allowed. Defaults to 10.
            http2 (bool, optional): Enable/disable HTTP2. If enabled the ht2 module must be installed. Defaults to True.

        Returns:
            object: The initialized TwoIP object
        """
        log.debug('New TwoIP object created')

        ## Set API endpoint
        log.debug(f'API endpoint: {api}')
        self._api = api

        ## Set httpx options
        self._connections = 10
        self._http2 = http2
        self.debug(f'Max connections: {connections}')
        self.debug(f'HTTP2 support: {http2}')

        ## Set API key
        if key:
            self._key = key
            log.trace(f'API key: {key}')
        else:
            log.debug(f'Not using API key; rate limits will be applied')
            self._key = None

    def __lookup_geo(self, uri: str = 'geo.json') -> object:
        pass


