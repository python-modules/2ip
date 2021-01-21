#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import requests
from ipaddress import ip_address
from typing import Any, Optional

class TwoIP(object):
    """
    2ip.me API client
    """

    # The API URL
    api = 'https://api.2ip.me'

    # List of available API endpoints
    endpoints = {
        'geo': {
            'url': f'{api}/geo.json',
            'description': 'Geographic information',
        },
        'provider': {
            'url': f'{api}/provider.json',
            'description': 'Provider information',
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
        self.__cache = {
            'geo': {},
            'provider': {},
            'hosting': {},
        }

        # Debugging
        if key:
            logging.debug(f'Setup of new TwoIP object')
        else:
            logging.debug(f'Setup of new TwoIP object (No API key used - rate limits will apply)')

    @staticmethod
    def __api_request(url: str, params: Optional[dict] = None) -> Any:
        """Send request to the 2ip API and return content.

        Parameters
        ----------
        url : str
            The URL to send request to

        params : dict, Optional
            Optional GET parameters to add to the request

        Returns
        -------
        Any
            The dictionary response

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

        # Make sure content type is expected
        if req.headers.get('Content-Type') != 'application/json':
            if req.headers.get('Content-Type'):
                raise RuntimeError(f'Expecting Content-Type header "application/json" but got "{req.headers.get("Content-Type")}"')
            else:
                raise RuntimeError(f'API request did not provide any Content-Type header')

        # Make sure the response can be parsed
        try:
            json = req.json()
        except Exception as e:
            raise RuntimeError('Exception parsing response from API as json') from e

        # Return content
        return json

    def __api_param(self, params: dict) -> dict:
        """Add API key to the list of parameters for the API request.

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

    def geo(self, ip: str, force: bool = False, cache: bool = True) -> dict:
        """Perform a Geographic information lookup to the 2ip API.

        By default, lookups will be cached. Subsequent lookups will use the cache (unless disabled) to prevent excessive API requests.

        Parameters
        ----------
        ip : str
            The IP address to lookup

        force : bool, default = False
            Force request to be sent to the API even if the lookup has already been cached

        cache: bool, default = True
            Allow caching of the request (cache can still be bypassed by using the force parameter)

        Returns
        -------
        dict
            The response from API in a dictionary

        Raises
        ------
        ValueError
            Invalid IP address specified

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
        logging.debug(f'2ip Geo API lookup request for IP "{ip}" (force: {force})')

        # Test if the IP to lookup is an actual IP
        try:
            ip_address(ip)
        except Exception as e:
            logging.error(f'Could not run 2ip Geo API lookup due to invalid IP address "{ip}"')
            raise ValueError(f'Could not validate IP address "{ip}", exception from ipaddress: {e}')

        # If the lookup is cached and this is not a forced lookup, return the cached result
        if ip in self.__cache['geo']:
            logging.debug(f'Cached Geo API entry available for IP "{ip}"')
            if force:
                logging.debug('Cached entry will be ignored for lookup; proceeding with API request')
            else:
                logging.debug('Cached entry will be returned; use the force parameter to force API request')
                return self.__cache['geo'][ip]

        # Add API key to parameters if set
        params = self.__api_param({'ip': ip})

        # Set API url
        url = self.endpoints['geo']['url']

        # Send API request
        try:
            response = self.__api_request(url = url, params = params)
        except Exception as e:
            logging.error('Failed to send API request: {e}')
            raise RuntimeError('Could not run API lookup') from e

        # Cache the response if allowed
        if cache:
            self.__cache['geo'][ip] = response

        # Return response
        return response

    def provider(self, ip: str, force: bool = False, cache: bool = True) -> dict:
        """Perform a provider information lookup to the 2ip API.

        By default, lookups will be cached. Subsequent lookups will use the cache (unless disabled) to prevent excessive API requests.

        Parameters
        ----------
        ip : str
            The IP address to lookup

        force : bool, default = False
            Force request to be sent to the API even if the lookup has already been cached

        cache: bool, default = True
            Allow caching of the request (cache can still be bypassed by using the force parameter)

        Returns
        -------
        dict
            The response from API in a dictionary

        Raises
        ------
        ValueError
            Invalid IP address specified

        RuntimeError
            API request failure

        Examples
        --------
        >>> twoip = TwoIP(key = '12345678')
        >>> twoip.provider(ip = '192.0.2.0')
        {'ip': '192.0.2.0', 'name_ripe': 'Reserved AS', 'name_rus': '', 'ip_range_start': '3221225984', 'ip_range_end': '3221226239',
        'route': '192.0.2.0', 'mask': '24'}
        """
        logging.debug(f'2ip provider API lookup request for IP "{ip}" (force: {force})')

        # Test if the IP to lookup is an actual IP
        try:
            ip_address(ip)
        except Exception as e:
            logging.error(f'Could not run 2ip provider API lookup due to invalid IP address "{ip}"')
            raise ValueError(f'Could not validate IP address "{ip}", exception from ipaddress: {e}')

        # If the lookup is cached and this is not a forced lookup, return the cached result
        if ip in self.__cache['provider']:
            logging.debug(f'Cached provider API entry available for IP "{ip}"')
            if force:
                logging.debug('Cached entry will be ignored for lookup; proceeding with API request')
            else:
                logging.debug('Cached entry will be returned; use the force parameter to force API request')
                return self.__cache['provider'][ip]

        # Add API key to parameters if set
        params = self.__api_param({'ip': ip})

        # Set API url
        url = self.endpoints['provider']['url']

        # Send API request
        try:
            response = self.__api_request(url = url, params = params)
        except Exception as e:
            logging.error('Failed to send API request: {e}')
            raise RuntimeError('Could not run API lookup') from e

        # Cache the response if allowed
        if cache:
            self.__cache['provider'][ip] = response

        # Return response
        return response