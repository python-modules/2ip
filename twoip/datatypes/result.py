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
    ip: Union[IPv4Address, IPv6Address] = field(
        compare = True,
        metadata = {
            'description'   : 'The IP address that was looked up',
        },
    )
    http_code: Optional[int] = field(
        default = None,
        compare = False,
        metadata = {
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
            'description'   : 'The error message/information if the geo lookup failed',
        },
    )