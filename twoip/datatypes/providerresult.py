# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network
from typing import Optional, Union

from .baseresult import BaseResult

# Define constant for language standard
LANG = 'ISO 639-1'

@dataclass(frozen = False)
class ProviderResult(BaseResult):
    """Dataclass to individual results of providder lookups for IP's

    Examples:

    """
    name: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            LANG            : 'EN',
            'title'         : 'Provider Name',
            'description'   : 'Provider official name in the Internet Routing Registry (IRR) database in English',
        },
    )
    name_rus: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            LANG            : 'RU',
            'description'   : 'Provider official name in the Internet Routing Registry (IRR) database in Russian',
        },
    )
    website: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'description'   : 'The provider website',
        },
    )
    autonomous_system: Optional[int] = field(
        default = None,
        compare = False,
        metadata = {
            'description'   : 'The provider autonomous system number',
        },
    )
    range_start: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'description'   : 'The first IP address of the providers IP range',
        },
    )
    range_end: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'description'   : 'The last IP address of the providers IP range',
        },
    )
    route: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'description'   : 'The network address for the providers IP range',
        },
    )
    length: Optional[int] = field(
        default = None,
        compare = False,
        metadata = {
            'description'   : 'The prefix length for the providers IP range',
        },
    )
    prefix: Optional[Union[IPv4Network, IPv6Network]] = field(
        init = False,
        compare = False,
        metadata = {
            'description'   : 'The providers IP range and prefix length represented as a IPv4Network or IPv6Network object',
        },
    )

    def __post_init__(self) -> object:
        """Function that is executed after creating a new ProviderLookupResult object

        This function will currently validate the IP address and generate the prefix value.

        Raises:
            ValueError: IP address cannot be validated
        """
        ## Convert the ipaddress object to a string and set in the IP field
        self.ip = f'{self.ipaddress}'

        ## Ensure the route and length is available
        if self.route and self.length:
            ## Check if IPv4 or IPv6 and create the network object
            if type(self.ip) == IPv4Address:
                try:
                    prefix = IPv4Network(f'{self.route}/{self.length}')
                except Exception as e:
                    raise ValueError(f'Exception creating IPv4Network object from prefix "{self.route}/{self.length}":\n{e}')
            elif type(self.ip) == IPv6Address:
                try:
                    prefix = IPv6Network(f'{self.route}/{self.length}')
                except Exception as e:
                    raise ValueError(f'Exception creating IPv6Network object from prefix "{self.route}/{self.length}":\n{e}')
            ## Set the prefix
            self.prefix = prefix
        else:
            ## Set prefix to none
            self.prefix = None

    def __str__(self) -> str:
        """String representation of a single provider result

        Simply return in the format "IP AS Name Site"

        Examples:

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

        ## Convert IP to string
        ip = f'{self.ip}'

        ## Return the formatted string
        return f'{ip:40} {autonomous_system:<10} {name:20} {site}'

    def is_global(self) -> bool:
        """Check if the IP address is globally routable address (eg. not multicast or RFC1918)

        Raises:
            ValueError: IP address could not be validated
            RuntimeError: Exception from ip_address

        Returns:
            bool: True if the IP is globally routable

        Examples:

        """
        ## Check if IP is global and return
        try:
            is_global = self.ip.is_global
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

        """
        ## Check if IP is private and return
        try:
            is_private = self.ip.is_private
        except Exception as e:
            raise RuntimeError(f'Exception checking if IP address is private:\n{e}')
        else:
            return is_private