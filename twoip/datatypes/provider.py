# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import Union, Optional, List

# Define constant for language standard
LANG = 'ISO 639-1'

@dataclass(frozen = False)
class ProviderLookupResult:
    """Dataclass to individual results of providder lookups for IP's

    Examples:
        >>> result1 = ProviderLookupResult(ip = '192.0.2.1')
        >>> result2 = ProviderLookupResult(
            ip = '192.0.2.2',
            name = 'Some Company',
            site = 'https://www.example.com',
            autonomous_system = 64496,
            range_start = '192.0.2.0',
            range_end = '192.0.2.255',
            route = '192.0.2.0',
            length = '24')
    """
    ## Assign the fields
    ip: Union[IPv4Address, IPv6Address] = field(
        metadata = {
            'description'   : 'The IP address represented as a string',
        },
    )
    name: Optional[str] = field(
        default = None,
        metadata = {
            LANG            : 'EN',
            'description'   : 'Provider official name in the Internet Routing Registry (IRR) database in English',
        },
    )
    name_rus: Optional[str] = field(
        default = None,
        metadata = {
            LANG            : 'RU',
            'description'   : 'Provider official name in the Internet Routing Registry (IRR) database in Russian',
        },
    )
    site: Optional[str] = field(
        default = None,
        metadata = {
            'description'   : 'The provider website',
        },
    )
    autonomous_system: Optional[int] = field(
        default = None,
        metadata = {
            'description'   : 'The provider autonomous system number',
        },
    )
    range_start: Optional[str] = field(
        default = None,
        metadata = {
            'description'   : 'The first IP address of the providers IP range',
        },
    )
    range_end: Optional[str] = field(
        default = None,
        metadata = {
            'description'   : 'The last IP address of the providers IP range',
        },
    )
    route: Optional[str] = field(
        default = None,
        metadata = {
            'description'   : 'The network address for the providers IP range',
        },
    )
    length: Optional[int] = field(
        default = None,
        metadata = {
            'description'   : 'The prefix length for the providers IP range',
        },
    )
    prefix: Optional[str] = field(
        init = False,
        metadata = {
            'description'   : 'The providers IP range and prefix length represented in CIDR format',
        },
    )
    error: Optional[str] = field(
        default = None,
        metadata = {
            'description'   : 'The error message/information if the provider lookup failed',
        },
    )

    def __post_init__(self) -> object:
        """Function that is executed after creating a new ProviderLookupResult object

        This function will currently validate the IP address and generate the prefix value.

        Raises:
            ValueError: IP address cannot be validated
        """
        ## Create IP address object which will validate/normalize the IP
        try:
            ip = ip_address(self.ip)
        except ValueError as e:
            raise ValueError(f'The IP address "{self.ip}" does not appear to be valid:\n{e}')
        except Exception as e:
            raise RuntimeError(f'Exception creating ipaddress object from IP "{self.ip}":\n{e}')

        ## Set the normalized IP address string
        self.ip = f'{ip}'

        ## Create the prefix representation if possible
        if self.route and self.length:
            self.prefix = f'{self.route}/{self.length}'
        else:
            self.prefix = None

    def __str__(self) -> str:
        """String representation of a single provider result

        Simply return in the format "IP AS Name Site"

        Examples:
            >>> print(ProviderLookupResult(ip = '192.0.2.1'))
            192.0.2.1                                Unknown    Unknown              Unknown
            >>> print(ProviderLookupResult(ip = '192.0.2.2', autonomous_system = 64496, name = 'Company', site = 'https://www.example.com'))
            192.0.2.2                                64496      Company              https://www.example.com
        """
        ## Check if there is an error for the IP
        if self.error:
            ## Set default values for AS/name/site to error
            autonomous_system = 'Error'
            name = 'Error'
            site = 'Error'
        else:
            ## Set default values for AS/name/site to 'Unknown' if not defined
            ## This is required as a TypeError will be raised if they are not set
            if self.autonomous_system:
                autonomous_system = self.autonomous_system
            else:
                autonomous_system = 'Unknown'
            if self.name:
                name = self.name
            else:
                name = 'Unknown'
            if self.site:
                site = self.site
            else:
                site = 'Unknown'

        ## Return the formatted string
        return f'{self.ip:40} {autonomous_system:<10} {name:20} {site}'

    def is_global(self) -> bool:
        """Check if the IP address is globally routable address (eg. not multicast or RFC1918)

        Raises:
            ValueError: IP address could not be validated
            RuntimeError: Exception from ip_address

        Returns:
            bool: True if the IP is globally routable

        Examples:
            >>> result1 = ProviderLookupResult(ip = '10.0.0.0')
            >>> result2 = ProviderLookupResult(ip = '1.0.0.0')
            >>> result1.is_global()
            False
            >>> result2.is_global()
            True
        """
        ## Attempt to create ip_address object for IP
        try:
            ip = ip_address(self.ip)
        except ValueError as e:
            raise ValueError(f'IP address is not valid:\n{e}')
        except Exception as e:
            raise RuntimeError(f'Exception creating ip_address object:\n{e}')

        ## Check if IP is global and return
        try:
            is_global = ip.is_global
        except Exception as e:
            raise RuntimeError(f'Exception checking if IP address is global:\n{e}')
        else:
            return is_global

    def is_private(self) -> bool:
        """Check if the IP address is private IP address (eg. RFC1918)

        Note: This does NOT include multicast, link local, loopback and other IP's that are not globally routable.
        This check can be used in conjunction with is_global() to check for other IP types.

        Raises:
            ValueError: IP address could not be validated
            RuntimeError: Exception from ip_address

        Returns:
            bool: True if the IP is private

        Examples:
            >>> result1 = ProviderLookupResult(ip = '10.0.0.0')
            >>> result2 = ProviderLookupResult(ip = '1.0.0.0')
            >>> result1.is_private()
            True
            >>> result2.is_private()
            False
        """
        ## Attempt to create ip_address object for IP
        try:
            ip = ip_address(self.ip)
        except ValueError as e:
            raise ValueError(f'IP address is not valid:\n{e}')
        except Exception as e:
            raise RuntimeError(f'Exception creating ip_address object:\n{e}')

        ## Check if IP is private and return
        try:
            is_private = ip.is_private
        except Exception as e:
            raise RuntimeError(f'Exception checking if IP address is private:\n{e}')
        else:
            return is_private

@dataclass(frozen = False)
class ProviderLookup:
    """Dataclass to store all results from multiple provider lookups

    Examples:
        >>> result1 = ProviderLookupResult(ip = '192.0.2.1')
        >>> result2 = ProviderLookupResult(
            ip = '192.0.2.2',
            name = 'Some Company',
            site = 'https://www.example.com',
            autonomous_system = 64496,
            range_start = '192.0.2.0',
            range_end = '192.0.2.255',
            route = '192.0.2.0',
            length = '24')
    """
    ## Assign slots
    __slots__ = [ 'results' ]

    ## Set results type
    results: List[ProviderLookupResult]

    def __str__(self) -> str:
        """String representation of all Geo results

        Simply return in the format "IP AS Name Site"

        Examples:
            >>> result1 = ProviderLookupResult(ip = '192.0.2.1')
            >>> result2 = ProviderLookupResult(ip = '192.0.2.2', autonomous_system = 64496, name = 'Company', site = 'https://www.example.com')
            >>> results = ProviderLookup([result1, result2])
            >>> print(results)
            192.0.2.1                                64496      Some Company         https://www.example.com
            192.0.2.2                                64496      Some Company         https://www.example.com
        """
        ## Create list to store formatted results
        output = []

        ## Loop over each result
        for result in self.results:
            ## Append the string representation to the output list
            output.append(result.__str__())

        ## Return the formatted output
        return '\n'.join(output)

    def to_dict(self) -> dict:
        """Return all Geo lookup results as a dict with a key by IP address

        Duplicates will be ignored.

        Examples:
            >>> result1 = ProviderLookupResult(ip = '192.0.2.1')
            >>> result2 = ProviderLookupResult(ip = '192.0.2.2', autonomous_system = 64496, name = 'Company', site = 'https://www.example.com')
            >>> results = ProviderLookup([result1, result2])
            >>> results.to_dict()
            {'192.0.2.1': {'autonomous_system': None,
                'error': None,
                'ip': '192.0.2.1',
                'length': None,
                'name': None,
                'name_rus': None,
                'prefix': None,
                'range_end': None,
                'range_start': None,
                'route': None,
                'site': None},
            '192.0.2.2': {'autonomous_system': 64496,
                'error': None,
                'ip': '192.0.2.2',
                'length': None,
                'name': 'Company',
                'name_rus': None,
                'prefix': None,
                'range_end': None,
                'range_start': None,
                'route': None,
                'site': 'https://www.example.com'}}
        """
        ## Create empty list of results to return
        result_dict = {}

        ## Loop over each result
        for result in self.results:
            ## Check if the result is already present and skip if required
            if result.ip in result_dict:
                continue
            ## Add the result to results dict
            result_dict[result.ip] = result.__dict__

        ## Return results
        return result_dict