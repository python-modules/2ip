# -*- coding: utf-8 -*-

# Import core modules
import asyncio
import logging as log
from functools import lru_cache
from ipaddress import ip_address
from pprint import pformat
from typing import Optional, Union
from urllib import parse as urlparse

# Import external modules
import httpx

# Import data types to store results
from .datatypes.geo import GeoLookup, GeoLookupResult
from .datatypes.provider import ProviderLookup, ProviderLookupResult

# Import version info to add to HTTP headers
from .__version__ import __version__

## API URL
API = 'https://api.2ip.ua'
## API URI's
URI_GEO = 'geo.json'
URI_PROVIDER = 'provider.json'

class TwoIP(object):
    """
    2ip.me API client
    """

    def __init__(self,
        ## Optional API key
        key: Optional[str] = None,
        ## The API URL
        api: str = API,
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
        log.debug(f'Max connections: {connections}')
        log.debug(f'HTTP2 support: {http2}')

        ## Set API key
        if key:
            self._key = key
            log.trace(f'API key: {key}')
        else:
            log.debug(f'Not using API key; rate limits will be applied')
            self._key = None

    def lookup(self, ip: Union[str, list], lookup: str = 'geo', ignore: bool = False) -> Union[GeoLookup, ProviderLookup]:
        """Run a 2ip API lookup for the provided IP address

        Arguments:
            ip (Union[str, list]): An IP address or list of IP addresses to lookup
            lookup (str): The type of lookup to perform. Must be one of "geo" or "provider". Defaults to "geo".
            ignore (bool): Ignore invalid IP addresses. If set to False, lookups for invalid IP's will result in an exception. Defaults to False.

        Returns:
            Union[GeoLookup, ProviderLookup]: A GeoLookup or ProviderLookup object (a list of GeoLookupResult or ProviderLookupResult objects)

        Raises:
            RuntimeError: Invalid lookup type
            ValueError: IP address(es) provided are not valid (if 'ignore' is set to False)
        """
        ## Make sure type is set correctly
        if lookup not in ['geo', 'provider']:
            log.error(f'Received lookup type "{lookup}" which does not exist')
            raise RuntimeError(f'Lookup type "{lookup}" is not valid; it must be "geo" or "provider"')

        ## Convert IP to a list if it is a string
        if type(ip) is str:
            log.trace(f'Converting single IP address lookup for "{ip}" to a list')
            ip = [ip]

        ## Logging
        log.debug(f'Received {lookup} lookup for IP list: {pformat(ip)}')

        ## Normalize and validate the list of IP's
        ips = self.__normalize(ips = ip, ignore = ignore)

        ## Ensure there is something to do
        if not ips:
            log.error('No IP addresses to perform lookup on after normalization')
            return

        ## Generate the URL to send requests to
        if lookup == 'geo':
            url = self.__generate_url(api = self._api, uri = URI_GEO)
        elif lookup == 'provider':
            url = self.__generate_url(api = self._api, uri = URI_PROVIDER)
        else:
            raise RuntimeError(f'Lookup URL generator for type "{lookup}" is missing')

        ## Gather the results
        results = asyncio.run(self.__lookup(url = url, ips = ips))

        ## Parse the results
        parsed = self.__parse(results = results, lookup = lookup)

        ## Return results
        return parsed

    @staticmethod
    def __parse(results: list, lookup: str):
        """Create GeoLookupResult object from each result
        """
        ## Create list to store parsed results
        parsed = []

        ## Loop over each result
        for result in results:

            ## Parse into the appropriate dataclass
            if lookup == 'geo':
                lookup_result = GeoLookupResult(**result.json())
            elif lookup == 'provider':
                lookup_result = ProviderLookupResult(**result.json())

            ## Set the HTTP code
            lookup_result.http_code = result.status_code

            ## Add object to parsed list
            parsed.append(lookup_result)

        ## Create the parent dataclass with all results
        parent = GeoLookup(results = parsed)

        ## Return
        return parent

    @staticmethod
    def __normalize(ips: list, ignore: bool) -> list:
        """Validate and normalize a list of IP addresses

        Args:
            ips (list): The list of IP addresses to validate and normalize
            ignore (bool): Ignore invalid IP addresses. If set to False, lookups for invalid IP's will result in an exception. Defaults to False.

        Returns:
            list: The list of validated/normalized IP's
        """
        log.debug('Normalizing list of IP addresses')
        log.trace(f'Before normalization:\n{pformat(ips)}')

        ## Create list to store validated/normalized IP's
        normalized = []

        ## Loop over IP's and validate/normalize
        for ip in ips:

            ## Create IP address object which will validate/normalize the IP
            log.trace(f'Validating and normalizing IP address "{ip}"')
            try:
                ip_obj = ip_address(ip)
            except ValueError as e:
                log.error(f'Invalid IP address "{ip}"')
                if ignore:
                    log.debug(f'Skipping invalid IP address "{ip}')
                    continue
                else:
                    raise ValueError(f'The IP address "{ip}" does not appear to be valid: {e}')
            except Exception as e:
                log.error(f'Exception while validating IP address "{ip}":\n{e}')
                raise RuntimeError(f'Exception creating ipaddress object from IP "{ip}": {e}')

            ## Check if IP is already in lookup list
            if f'{ip_obj}' in normalized:
                log.warning(f'Duplicate IP "{ip_obj}" lookup request; ignoring duplicate')
                continue

            ## Add the now normalized IP to lookup list
            log.trace(f'Normalized IP: {ip_obj}')
            normalized.append(f'{ip_obj}')

        ## Return the normalized IP list
        log.trace(f'After normalization:\n{pformat(normalized)}')
        return normalized

    async def __lookup(self, url: str, ips: list) -> GeoLookup:
        """Perform a geo lookup for a list of IP's
        """
        ## Create list of tasks
        task_list = []

        ## Loop over each IP, generate params and add to tasks list
        for ip in ips:

            ## Add IP to api_param if required and encode
            if self._key:
                params = urlparse.urlencode({'key': self._key, 'ip': ip})
            else:
                params = urlparse.urlencode({'ip': ip})

            ## Generate the task for the lookup of this IP
            task_list.append(self.__request(url = url, params = params))

        ## Wait for results
        result = await asyncio.gather(*task_list)
        return result

    @staticmethod
    def __generate_url(api: str, uri: str) -> str:
        """Generate the URL to send requests to
        """
        parts = list(urlparse.urlparse(api))
        parts[2] = uri
        return urlparse.urlunparse(parts)

    @lru_cache(maxsize = 10000)
    async def __request(self, url: str, params: str) -> object:
        """Send a HTTP request to the API

        Args:
            url (str): The API URL to make the request to
            params (dict): The parameters to add to the API request
        """
        ## Create user agent header
        headers = {
            'User-Agent': f'TwoIP Python API Client/{__version__}',
        }

        ## Set maximum number of concurrent connections and keepalive connections
        limits = httpx.Limits(max_keepalive_connections = 5, max_connections = self._connections)

        ## Debug logging
        if self._http2: ver = 'HTTP2'
        else:           ver = 'HTTP1'
        log.trace(f'New API {ver} request:\n'
                    f'  - URL: {url}\n'
                    f'  - Params: {params}\n'
                    f'  - Headers: {headers}\n'
                    f'  - Max Connections: {self._connections}'
        )

        ## Make the API request
        async with httpx.AsyncClient(limits = limits, http2 = self._http2, headers = headers) as client:
            try:
                response = await client.get(url = f'{url}?{params}')
            except Exception as e:
                log.error(f'Exception while making API request:\n{e}')
                response = {'error': {e}}
            else:
                ## Log response
                log.trace(f'{response.status_code} Response from API: {response.text}')

            ## Return response
            return response