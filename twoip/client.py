# -*- coding: utf-8 -*-

"""
TwoIP API Client

This file provides the glue to make/parse the HTTP requests and return
relevant results.
"""

import logging
import pprint

from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import Optional, Union, Literal

from twoip.__config__ import __api__, __logger__
from twoip.log import Log
from twoip.http import HTTP

class Client:

    """
    TwoIP API Client
    """

    def __init__(
        self,
        api: str = __api__,
        connections: int = 10,
        http2: bool = True,
        key: Optional[str] = None,
        strict: bool = False,
        verbosity: int = 0,
    ) -> object:
        """Initialize the TwoIP API client

        Args:
            verbosity (int, optional): The verbosity level for log messages

        Returns:
            object: The TwoIP API client object
        """
        ## Set up logging
        Log(verbosity = verbosity)
        self.log = logging.getLogger(__logger__)

        ## Don't allow more than 100 connections
        if connections < 1 or connections > 100:
            self.log.error(f'A minimum of 1 connection and a maximum of 100 ' \
                'connections must be used ({connections} is out of range)')
            ## If running in strict mode, raise an exception
            if strict:
                raise ValueError(f'A minimum of 1 connection and a maximum ' \
                    'of 100 connections must be used')
            ## Otherwise, lower number of connections to expected value
            else:
                connections = 100

        ## Set variables from initialization
        self._api = api
        self._connections = connections
        self._http2 = http2
        self._key = key
        self._strict = strict

        ## Log
        self.log.debug("TwoIP API Client initialized")
        self.log.debug("Configuration:")
        self.log.debug(f"    API: {self._api}")
        self.log.debug(f"    API Connections: {self._connections}")
        self.log.debug(f"    HTTP2: {self._http2}")
        self.log.debug(f"    API Key: {self._key}")
        self.log.debug(f"    Strict: {self._strict}")

        ## Warn if not using API key
        if not key:
            self.log.warn("No API key provided; API requests subject to rate limit")

    def lookup(
        self,
        ip: Union[str, IPv4Address, IPv6Address] = None,
        ips: Union[tuple[Union[str, IPv4Address, IPv6Address]], list[Union[str, IPv4Address, IPv6Address]]] = None,
        lookup: Literal["geo", "provider"] = "geo",
    ) -> object:
        """Perform the lookup against the 2IP API
        """
        ## Make sure either an IP or a list/tuple of IPs is provided
        if not ip and not ips:
            self.log.fatal("An IP or a list/tuple of IPs must be provided to lookup")

        ## Normalize IPs
        self.log.trace("Normalizing and de-duplicating provided IPs")
        try:
            if ip:
                ips = self.__normalize_ips(ip)
            elif ips:
                ips = self.__normalize_ips(ips)
        except ValueError as e:
            self.log.fatal(f"Unable to normalize IPs: {e}")
        except Exception as e:
            self.log.fatal(f"Exception while normalizing IPs: {e}")

        ## Log debugging info but avoid if running in optimized mode as this could be expensive
        if __debug__:
            self.log.debug(f"Request to lookup {len(ips)} IPs with the {lookup} provider")
            self.log.trace(f"IPs:\n{pprint.pformat(ips)}")

    @staticmethod
    def __normalize_ips(ips: Union[tuple[Union[str, IPv4Address, IPv6Address]], list[Union[str, IPv4Address, IPv6Address], str, IPv4Address, IPv6Address]]) -> list[Union[IPv4Address, IPv6Address]]:
        """Normalize IPs
        """

        ## Convert to list from the current format and deduplicate
        if isinstance(ips, tuple):
            ips = list(dict.fromkeys([f'{ip_address(ip)}' if isinstance(ip, str) else f'{ip}' for ip in list(ips)]))
        elif isinstance(ips, list):
            ips = list(dict.fromkeys([f'{ip_address(ip)}' if isinstance(ip, str) else f'{ip}' for ip in ips]))
        elif isinstance(ips, str):
            ips = [f'{ip_address(ips)}']
        elif isinstance(ips, IPv4Address) or isinstance(ips, IPv6Address):
            ips = [f'{ips}']
        else:
            raise ValueError("IPs must be provided as a list/tuple of IPs, a string, or an IPv4Address/IPv6Address object")

        ## Return IP's
        return ips
