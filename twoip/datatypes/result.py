# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from ipaddress import IPv4Address, IPv6Address
from typing import Union, Optional

# Define constant for language standard
LANG = 'ISO 639-1'

@dataclass(frozen = False)
class Result(object):
    """Dataclass to individual results of Geo lookups for IP's

    Examples:
        >>> result1 = GeoLookupResult(ip = '192.0.2.1')
        >>> result2 = GeoLookupResult(ip = '192.0.2.2', city = 'Somewhere', country = 'Some Country')
    """
    ## Assign the fields
    ip: str = field(
        init = False,
        compare = False,
        metadata = {
            'title'         : 'IP Address',
            'description'   : 'The IP address that was looked up',
        },
    )
    ipaddress: Union[IPv4Address, IPv6Address] = field(
        compare = True,
        metadata = {
            'description'   : 'The IP address that was looked up represented as an ipaddress object',
        },
    )
    http_code: Optional[int] = field(
        default = None,
        compare = False,
        metadata = {
            'title'         : 'HTTP Code',
            'description'   : 'The HTTP response code from the API',
        },
    )
    api_response_raw: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'description'   : 'The raw API response body represented as a string',
        },
    )
    error: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'title'         : 'Error',
            'description'   : 'The error message/information if the geo lookup failed',
        },
    )

    def __post_init__(self) -> object:
        """Function that is executed after creating a new Result object
        """
        ## Convert the ipaddress object to a string and set in the IP field
        self.ip = f'{self.ipaddress}'

    def get_meta(self, field: str, name: str) -> str:
        """Retrieve metadata for a field
        """
        ## Get the attribute to ensure it exists
        try:
            attribute = self.__dataclass_fields__[field]
        except KeyError:
            raise KeyError(f'The field "{field}" does not exist')

        ## Get the metadata
        try:
            data = attribute.metadata[name]
        except KeyError:
            raise KeyError(f'The metadata entry name "{name}" does not exist')

        ## Return the metadata
        return data