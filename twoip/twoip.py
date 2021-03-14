# -*- coding: utf-8 -*-

# Import core modules
import asyncio
import logging
from ipaddress import ip_address, IPv4Address, IPv6Address
from pprint import pformat
from typing import Optional, Union, Literal, List
from urllib import parse as urlparse

# Import external modules
import httpx

# Import data types to store results
from twoip.datatypes.apiresponse import APIResponse
from .datatypes.geo import Geo
from .datatypes.provider import Provider

# Import version info to add to HTTP headers
from .__version__ import __version__

# Get logger
log = logging.getLogger('twoip')

## API base URL
API = 'https://api.2ip.ua'
## API URI's
URI_GEO = 'geo.json'
URI_PROVIDER = 'provider.json'

class TwoIP(object):
    """
    2ip.me API module
    """

    def __init__(self,
        ## Optional API key
        key: Optional[str] = None,
        ## The API base URL
        api: str = API,
        ## The maximum number of concurrent API HTTP connections allowed
        connections: int = 10,
        ## Allow the use of HTTP2 (requiring the h2 module to be installed)
        http2: bool = True,
        ## Strict mode; any errors result in an exception being raised
        strict: bool = False,
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
        ## Don't allow more than 100 connections
        if connections < 1 or connections > 100:
            log.fatal(f'A minimum of 1 connection and a maximum of 100 connections must be used')

        log.info('New TwoIP object created')

        ## Set API endpoint
        log.debug(f'API endpoint: {api}')
        self._api = api

        ## Set httpx options
        self._connections = connections
        self._http2 = http2
        log.debug(f'Max connections: {connections}')
        log.debug(f'HTTP2 support: {http2}')

        ## Set API key
        if key:
            self._key = f'{key}'
            log.debug(f'API key has been provided')
            log.trace(f'API key: {key}')
        else:
            log.debug(f'Not using API key; rate limits will be applied')
            self._key = None

        ## Set strict mode
        self._strict = strict
        log.debug(f'Strict mode: {strict}')

        ## Generate the user agent
        user_agent = f'TwoIP Python API Client/{__version__}'
        log.debug(f'HTTP User-Agent: {user_agent}')

        ## Add User-Agent to headers
        self._headers = { 'User-Agent': user_agent }

        ## Create httpx limits object
        self.limits = httpx.Limits(max_keepalive_connections = 5, max_connections = self._connections)

    def geo(self, ip: Union[List[Union[IPv4Address, IPv6Address, str]], IPv4Address, IPv6Address, str]) -> Geo:
        """Perform a geo lookup for one or more IP addresses

        Args:
            ip (Union[List[Union[IPv4Address, IPv6Address, str]], str]): A list or string of IP addresses or ip_address objects to lookup

        Returns:
            Geo: The results of the lookup as a Geo object
        """
        ## Logging
        log.info('Attempting geo lookup')

        ## Call the Geo lookup function
        return self.__lookup(ip = ip, lookup_type = 'geo')

    def provider(self, ip: Union[List[Union[IPv4Address, IPv6Address, str]], IPv4Address, IPv6Address, str]) -> Provider:
        """Perform a provider lookup for one or more IP addresses

        Args:
            ip (Union[List[Union[IPv4Address, IPv6Address, str]], str]): A list or string of IP addresses or ip_address objects to lookup

        Returns:
            Provider: The results of the lookup as a Provider object
        """
        ## Logging
        log.info('Attempting provider lookup')

        ## Call the provider lookup function
        return self.__lookup(ip = ip, lookup_type = 'provider')

    def __lookup(self, ip: Union[List[Union[IPv4Address, IPv6Address, str]], IPv4Address, IPv6Address, str], lookup_type: Literal['geo', 'provider']) -> Union[Geo, Provider]:
        ## If a string was provided, convert to list
        if type(ip) == str:
            log.verbose('Lookup for single IP address; converting to list with single entry')
            ip = [ip]

        ## Logging
        log.trace(f'IP list to lookup:\n{pformat(ip, compact = False)}')

        ## Normalize list of IP's to lookup
        log.verbose('Requesting normalization of all IP addresses')
        ips: List[Union[IPv4Address, IPv6Address]] = self.__normalize_ip(ip = ip, strict = self._strict)

        ## Ensure there is something to do
        log.debug('Checking for work to do')
        if not ips:
            log.warn('No IP addresses to perform lookup on after normalization; returning empty result')
            if lookup_type == 'geo':
                return Geo()
            elif lookup_type == 'provider':
                return Provider()
            else:
                raise ValueError(f'Lookup return type does not exist: {lookup_type}')
        else:
            log.info(f'{len(ips)} IP addresses to lookup after normalization')

        ## Generate the API URL
        if lookup_type == 'geo':
            url: str = self.__generate_url(api = self._api, uri = URI_GEO)
        elif lookup_type == 'provider':
            url: str = self.__generate_url(api = self._api, uri = URI_PROVIDER)
        else:
            raise RuntimeError(f'Lookup URL generator for type "{lookup_type}" is missing')

        ## Generate and run the list of tasks
        log.info('Running asyncio function to generate and send API requests')
        results: List[dict] = asyncio.run(self.__generate_tasks(ips = ips, url = url))

        ## Parse the results
        log.info('HTTP requests finished, parsing results')
        parsed_results = self.__parse_results(results = results, lookup_type = lookup_type)

        ## Return the results
        log.info('Finished parsing, returning results')
        return parsed_results

    @staticmethod
    def __normalize_ip(ip: List[Union[IPv4Address, IPv6Address, str]], strict: bool) -> List[Union[IPv4Address, IPv6Address]]:
        """Validate, normalize and deduplicate list of IP addresses

        Args:
            ip (List[Union[IPv4Address, IPv6Address, str]]): The list of IP addresses to validate and normalize

        Returns:
            List[Union[IPv4Address, IPv6Address]]: The validated/normalized list of IP addresses
        """
        ## Logging
        log.debug('Normalizing list of IP addresses')

        ## Create empty list to store IP's
        ips = []

        ## Loop over each IP provided
        for address in ip:

            ## Skip if the address is already an ipaddress object
            if type(address) in [IPv4Address, IPv6Address]:
                log.debug(f'IP address "{address}" has already been validated and normalized')
                ips.append(address)
                continue

            ## Logging
            log.debug(f'Normalizing IP address "{address}"')

            ## Try to create ip address object for IP and add to IP list to return
            try:
                ipaddress = ip_address(address)
            except Exception as e:
                ## IP could not be validated, raise exception or warn and skip
                if strict:
                    log.fatal(f'Could not validate IP address "{address}":\n{e}')
                else:
                    log.warning(f'Could not validate IP address "{address}", it will be skipped:\n{e}')
                    continue
            else:
                log.debug(f'Validated and normalized IP address "{address}" as "{ipaddress}"')

            ## Make sure IP is not a duplicate
            if ipaddress in ips:
                log.warning(f'Skipping duplicate IP address "{address}"')
                continue

            ## Append IP to ips list
            ips.append(ipaddress)

        log.debug('Returning validated IP list')
        log.trace(f'Validated IP list:\n{pformat(ips, compact = False)}')
        return ips

    @staticmethod
    def __generate_url(api: str, uri: str) -> str:
        """Generate the API URL to send requests to

        Args:
            api (str): The base API URL
            uri (str): The URI to the provider that the lookup will be ran against

        Returns:
            str: The full API URL
        """
        ## Logging
        log.debug(f'Generating API URL from API address "{api}" and URI "{uri}"')

        ## Parse API URL
        try:
            parts = list(urlparse.urlparse(api))
        except Exception as e:
            log.fatal(f'API URL could not be generated:\n{e}')

        ## Add URI
        parts[2] = uri

        ## Generate the full URL
        url = urlparse.urlunparse(parts)

        ## Return
        log.verbose(f'Generated API URL: {url}')
        return url

    @staticmethod
    def __generate_params(key: Optional[str], ip: Union[IPv4Address, IPv6Address]) -> str:
        ## Create params for the HTTP request
        log.debug(f'Generating URL params for IP "{ip}"')
        if key:
            params = urlparse.urlencode({'key': key, 'ip': f'{ip}'})
        else:
            params = urlparse.urlencode({'ip': f'{ip}'})

        ## Return
        log.trace(f'Generated params: {params}')
        return params

    async def __generate_tasks(self, ips: List[Union[IPv4Address, IPv6Address]], url: str) -> List[dict]:
        """Generate and execute a list of tasks (lookups)

        Args:
            ips (List[Union[IPv4Address, IPv6Address]]): The list of IP addresses to lookup
            url (str): The API URL to make the request to

        Returns:
            List (object): List of response objects
        """
        ## Logging
        log.debug('Generating list of tasks to execute')

        ## Create empty task list
        tasks = []

        ## Create the httpx client
        client = httpx.AsyncClient(limits = self.limits, http2 = self._http2, headers = self._headers)

        ## Loop over each IP
        for ip in ips:

            ## Generate params from API key and IP
            params = self.__generate_params(key = self._key, ip = ip)

            ## Append task to task list
            log.debug(f'Adding task for IP "{ip}" to tasks list and executing')
            tasks.append(self.__request(client = client, url = url, params = params, ip = ip))

        ## Wait for results
        log.debug('Waiting for API requests to finish')
        results = await asyncio.gather(*tasks)

        ## Close async client
        log.debug('API requests finished, closing HTTP connections')
        await client.aclose()

        ## Return results
        log.debug('Returning results from API')
        return results

    @staticmethod
    async def __request(client: httpx.AsyncClient, url: str, params: str, ip = Union[IPv4Address, IPv6Address]) -> APIResponse:

        ## Logging
        log.trace(f'Making HTTP request to URL "{url}?{params}" for IP address {ip}')

        ## Make the HTTP request
        try:
            response = await client.get(url = f'{url}?{params}')
        except httpx.RequestError as e:
            log.error(f'RequestError while making API request for IP address {ip}:\n{e}')
            error = f'RequestError: {e}'
        except httpx.TransportError as e:
            log.error(f'TransportError while making API request for IP address {ip}:\n{e}')
            error = f'TransportError: {e}'
        except Exception as e:
            log.error(f'Exception while making API request:\n{e}')
            error = f'Exception: {e}'
        else:
            ## Log response
            log.debug(f'{response.status_code} Response from API for IP address "{ip}"')
            log.trace(f'Response body:\n{pformat(response.text)}')
            error = None

        ## Create the APIResponse object
        apiresponse = APIResponse(ipaddress = ip, url = f'{url}?{params}', error = error, response = response)

        ## Return the result
        return apiresponse