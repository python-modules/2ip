# -*- coding: utf-8 -*-

from typing import Union
from dataclasses import dataclass, field
from ipaddress import IPv4Address, IPv6Address

@dataclass
class GeoResult:
    """Dataclass to store IP's that have been looked up with the Geo API
    """
    ip: Union[IPv4Address, IPv6Address] = field(
        metadata = {
            'description'   : 'The IP address represented as a string',
        },
    )
    city: str = field(
        default = None,
        metadata = {
            'ISO 639-1'     : 'EN',
            'description'   : 'The city associated with the IP address represented as a string in English',
        },
    )
    city_rus: str = field(
        default = None,
        metadata = {
            'ISO 639-1'     : 'RU',
            'description'   : 'The city associated with the IP address represented as a string in Russian',
        },
    )
    region: str = field(
        default = None,
        metadata = {
            'ISO 639-1'     : 'EN',
            'description'   : 'The region associated with the IP address represented as a string in English',
        },
    )
    region_rus: str = field(
        default = None,
        metadata = {
            'ISO 639-1'     : 'RU',
            'description'   : 'The region associated with the IP address represented as a string in Russian',
        },
    )
    region_ua: str = field(
        default = None,
        metadata = {
            'ISO 639-1'     : 'UK',
            'description'   : 'The region associated with the IP address represented as a string in Ukrainian',
        },
    )
    country: str = field(
        default = None,
        metadata = {
            'ISO 639-1'     : 'EN',
            'description'   : 'The city associated with the IP address represented as a string in English',
        },
    )
    country_rus: str = field(
        default = None,
        metadata = {
            'ISO 639-1'     : 'RU',
            'description'   : 'The city associated with the IP address represented as a string in Russian',
        },
    )
    country_ua: str = field(
        default = None,
        metadata = {
            'ISO 639-1'     : 'UK',
            'description'   : 'The city associated with the IP address represented as a string in Ukrainian',
        },
    )
    latitude: float = field(
        default = None,
        metadata = {
            'description'   : 'The latitude',
        },
    )
    longitude: float = field(
        default = None,
        metadata = {
            'description'   : 'The longitude',
        },
    )
    time_zone: Optional[str] = field(
        default = None,
        metadata = {
            'description'   : 'The time zone',
        },
    )
    zip_code: Optional[int] = field(
        default = None,
        metadata = {
            'description'   : 'The zip code',
        },
    )

    def __str__(self):
        """String representation of a Geo result

        Simply return in the format "IP - Country"
        """
        return f'{self.ip} - {self.country}'