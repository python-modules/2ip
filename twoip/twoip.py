#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import requests
from ipaddress import ip_address
from typing import Optional, Union

class TwoIP(object):
    """
    2ip.me API client
    """

    # The API URL
    api = 'https://api.2ip.me'

    # List of available API endpoints
    endpoints = {
        'ip': {
            'geo': {
                'format': [ 'json', 'xml' ],
                'description': 'Geographic information for IP addresses',
            },
            'provider': {
                'format': [ 'json', 'xml' ],
                'description': 'Provider information for IP addresses',
            },
        },
    }

    def __init__(self, key: Optional[str] = None) -> object:
        """Set up new 2ip.me API client.

        Parameters
        ----------
        key : str, optional
            Optional API key to use for requests to the API

        Returns
        -------
        TwoIP : object
            The TwoIP API object

        Examples
        --------
        >>> twoip = TwoIP(key = None)
        """
        # Set API key
        self.__key = key

        # Create empty cache
        self.__cache = {}
        for endpoint_type in self.endpoints:
            for type in self.endpoints[endpoint_type]:
                self.__cache[type] = {}
                for format in self.endpoints[endpoint_type][type]['format']:
                    self.__cache[type][format] = {}

        # Debugging
        if key:
            logging.debug(f'Setup of new TwoIP object')
        else:
            logging.debug(f'Setup of new TwoIP object (No API key used - rate limits will apply)')

    @staticmethod
    def __api_request(url: str, params: Optional[dict] = None) -> object:
        """Send request to the 2ip API and return the requests object.

        Parameters
        ----------
        url : str
            The URL to send request to

        params : dict, Optional
            Optional GET parameters to add to the request

        Returns
        -------
        object
            The requests object

        Raises
        ------
        RuntimeError
            If the API request fails
        """
        # Send the request
        try:
            req = requests.request(method = 'GET', url = url, params = params)
        except Exception as e:
            raise RuntimeError('API request failed') from e

        # Make sure API request didn't result in rate limit
        if req.status_code == 429:
            raise RuntimeError(f'API has reached rate limit; retry in an hour or use an API key')

        # Make sure response code is fine
        if req.status_code != 200:
            raise RuntimeError(f'Received unexpected response code "{req.status_code}" from API')

        # Return the requests object
        return req

    def __api_param(self, params: dict) -> dict:
        """Add API key to the list of parameters for the API request if available.

        Parameters
        ----------
        params : dict
            The parameters to add API key to

        Returns
        -------
        dict
            The built parameter list
        """
        # Add API key if available
        if self.__key:
            params['key'] = self.__key

        # Return params
        return params

    @staticmethod
    def __test_ip(ip: str) -> bool:
        """Test if the IP address provided is really an IP address.

        Parameters
        ----------
        params : ip
            The IP address to test

        Returns
        -------
        bool
            True if the string provided is an IP address or False if it is not an IP address
        """
        logging.debug(f'Testing if "{ip}" is a valid IP address')

        # Check for exception when creating an ip_address object
        try:
            ip_address(ip)
        except Exception as e:
            logging.error(f'Could not validate string "{ip}" as an IP address: {e}')
            return False

        # IP provided is valid
        return True

    def __execute_ip(self, ip: str, format: str, type: str) -> Union[dict, str]:
        """Execute an API lookup for an IP address based provider (geographic information or provider information)

        Parameters
        ----------
        ip : str
            The IP address to lookup

        format : {'json', 'xml'}
            The format for which results should be returned - json results will be returned as a dict

        type : {'geo','provider'}
            The API type to lookup ('geo' for geographic information or 'provider' for provider information)

        Returns
        -------
        dict or str
            The lookup result in either dict format (for JSON lookups) or string format (for XML lookups)
        """
        # Make sure there is an endpoint for the requested type
        if not self.endpoints['ip'][type]:
            raise ValueError(f'Invalid lookup type "{type}" requested')

        # Make sure that the format selected is valid
        if format not in self.endpoints['ip'][type]['format']:
            raise ValueError(f'The "{type}" API endpoint does not support the requested format "{format}"')

        # Build the API URL that the request will be made to
        url = f'{self.api}/{type}.{format}'

        # Set the parameters for the request (this will add the API key if available)
        params = self.__api_param({'ip': ip})

        # Send API request
        try:
            response = self.__api_request(url = url, params = params)
        except Exception as e:
            logging.error('Failed to send API request: {e}')
            raise RuntimeError('Could not run API lookup') from e

        # Make sure content type of the response is expected
        if response.headers.get('Content-Type') != f'application/{format}':
            if response.headers.get('Content-Type'):
                raise RuntimeError(f'Expecting Content-Type header "application/{format}" but got "{req.headers.get("Content-Type")}"')
            else:
                raise RuntimeError(f'API request did not provide any Content-Type header')

        # If the format requests is XML, return it immediately otherwise attempt to parse the json response into a dict
        if format == 'xml':
            return response.text
        elif format == 'json':
            try:
                json = response.json()
            except Exception as e:
                raise RuntimeError('Exception parsing response from API as json') from e
            return json
        else:
            raise RuntimeError(f'No output handler configured for the output format "{format}"')

    def geo(self, ip: str, format: str = 'json', force: bool = False, cache: bool = True) -> Union[dict, str]:
        """Perform a Geographic information lookup to the 2ip API.

        By default, lookups will be cached. Subsequent lookups will use the cache (unless disabled) to prevent excessive API requests.

        Parameters
        ----------
        ip : str
            The IP address to lookup

        format : {'xml','json'}
            The requested output format - JSON will result in a dict otherwise XML will result in a str

        force : bool, default = False
            Force request to be sent to the API even if the lookup has already been cached

        cache: bool, default = True
            Allow caching of the request (cache can still be bypassed by using the force parameter)

        Returns
        -------
        dict or str
            The response from API in either a dictionary (if the format is set to json) or a string (if the format is set to XML)

        Raises
        ------
        ValueError
            Invalid IP address or invalid output format requested

        RuntimeError
            API request failure

        Examples
        --------
        >>> twoip = TwoIP(key = '12345678')
        >>> twoip.geo(ip = '192.0.2.0')
        {'ip': '192.0.2.0', 'country_code': '-', 'country': '-', 'country_rus': 'Неизвестно', 'country_ua': 'Невідомо',
        'region': '-', 'region_rus': 'Неизвестно', 'region_ua': 'Невідомо', 'city': '-', 'city_rus': 'Неизвестно',
        'city_ua': 'Невідомо', 'zip_code': '-', 'time_zone': '-'}
        """
        # Make sure IP address provided is valid
        if self.__test_ip(ip = ip):
            logging.debug(f'2ip geo API lookup request for IP "{ip}" (force: {force})')
        else:
            raise ValueError(f'Could not run geo lookup for invalid IP address "{ip}"')

        # If the lookup is cached and this is not a forced lookup, return the cached result
        if ip in self.__cache['geo'][format]:
            logging.debug(f'Cached API entry available for IP "{ip}"')
            if force:
                logging.debug('Cached entry will be ignored for lookup; proceeding with API request')
            else:
                logging.debug('Cached entry will be returned; use the force parameter to force API request')
                return self.__cache['geo'][format][ip]

        # Run the request
        response = self.__execute_ip(ip = ip, format = format, type = 'geo')

        # Cache the response if allowed
        if cache:
            self.__cache['geo'][format][ip] = response

        # Return response
        return response

    def provider(self, ip: str, format: str = 'json', force: bool = False, cache: bool = True) -> Union[dict, str]:
        """Perform a provider information lookup to the 2ip API.

        By default, lookups will be cached. Subsequent lookups will use the cache (unless disabled) to prevent excessive API requests.

        Parameters
        ----------
        ip : str
            The IP address to lookup

        format : {'xml','json'}
            The requested output format - JSON will result in a dict otherwise XML will result in a str

        force : bool, default = False
            Force request to be sent to the API even if the lookup has already been cached

        cache: bool, default = True
            Allow caching of the request (cache can still be bypassed by using the force parameter)

        Returns
        -------
        dict or str
            The response from API in either a dictionary (if the format is set to json) or a string (if the format is set to XML)

        Raises
        ------
        ValueError
            Invalid IP address or invalid output format requested

        RuntimeError
            API request failure

        Examples
        --------
        >>> twoip = TwoIP(key = '12345678')
        >>> twoip.provider(ip = '192.0.2.0')
        {'ip': '192.0.2.0', 'name_ripe': 'Reserved AS', 'name_rus': '', 'ip_range_start': '3221225984', 'ip_range_end': '3221226239',
        'route': '192.0.2.0', 'mask': '24'}
        """
        # Make sure IP address provided is valid
        if self.__test_ip(ip = ip):
            logging.debug(f'2ip provider API lookup request for IP "{ip}" (force: {force})')
        else:
            raise ValueError(f'Could not run provider lookup for invalid IP address "{ip}"')

        # If the lookup is cached and this is not a forced lookup, return the cached result
        if ip in self.__cache['provider'][format]:
            logging.debug(f'Cached API entry available for IP "{ip}"')
            if force:
                logging.debug('Cached entry will be ignored for lookup; proceeding with API request')
            else:
                logging.debug('Cached entry will be returned; use the force parameter to force API request')
                return self.__cache['provider'][format][ip]

        # Run the request
        response = self.__execute_ip(ip = ip, format = format, type = 'provider')

        # Cache the response if allowed
        if cache:
            self.__cache['provider'][format][ip] = response

        # Return response
        return response