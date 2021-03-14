# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network
from typing import Optional, Union

from .baseresult import BaseResult

@dataclass(frozen = False)
class ProviderResult(BaseResult):
    """Dataclass to individual results of providder lookups for IP's

    Examples:

    """
    name: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'lang'          : 'EN',
            'title'         : 'Provider Name',
            'description'   : 'Provider official name in the Internet Routing Registry (IRR) database in English',
        },
    )
    name_rus: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'lang'          : 'RU',
            'description'   : 'Provider official name in the Internet Routing Registry (IRR) database in Russian',
        },
    )
    website: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'title'         : 'Website',
            'description'   : 'The provider website',
        },
    )
    asn: Optional[int] = field(
        default = None,
        compare = False,
        metadata = {
            'title'         : 'ASN',
            'description'   : 'The provider autonomous system number',
        },
    )
    range_start: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'title'         : 'IP Range Start',
            'description'   : 'The first IP address of the providers IP range',
        },
    )
    range_end: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'title'         : 'IP Range End',
            'description'   : 'The last IP address of the providers IP range',
        },
    )
    route: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'title'         : 'Route',
            'description'   : 'The network address for the providers IP range',
        },
    )
    length: Optional[int] = field(
        default = None,
        compare = False,
        metadata = {
            'title'         : 'Prefix Length',
            'description'   : 'The prefix length for the providers IP range',
        },
    )
    prefix: Optional[Union[IPv4Network, IPv6Network]] = field(
        init = False,
        compare = False,
        metadata = {
            'title'         : 'Prefix',
            'description'   : 'The providers IP range and prefix length represented as a IPv4Network or IPv6Network object',
        },
    )

    def __post_init__(self) -> object:
        """Function that is executed after creating a new ProviderLookupResult object

        This function will create the IP string and set the success icon. The prefix will then be generated.

        Raises:
            ValueError: IP address cannot be validated
        """
        ## Convert the ipaddress object to a string and set in the IP field
        self.ip = f'{self.ipaddress}'

        ## Set the success/success icon values
        self._init_success()

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
            asn = 'Error'
            name = 'Error'
            site = 'Error'
        else:
            ## Set default values for AS/name/site to 'Unknown' if not defined
            ## This is required as a TypeError will be raised if they are not set
            if self.asn:
                asn = self.asn
            else:
                asn = 'Unknown'
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
        return f'{ip:40} {asn:<10} {name:20} {site}'