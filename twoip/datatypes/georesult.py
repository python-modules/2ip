# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from math import asin, cos, radians, sin, sqrt
from typing import Optional

from .baseresult import BaseResult

# Define constant for language standard
LANG = 'ISO 639-1'

@dataclass(frozen = False)
class GeoResult(BaseResult):
    """Dataclass to individual results of Geo lookups for IP's

    Examples:
    """
    ## Assign the fields
    city: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            LANG            : 'EN',
            'description'   : 'The city associated with the IP address represented as a string in English',
        },
    )
    city_rus: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            LANG            : 'RU',
            'description'   : 'The city associated with the IP address represented as a string in Russian',
        },
    )
    region: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            LANG            : 'EN',
            'description'   : 'The region associated with the IP address represented as a string in English',
        },
    )
    region_rus: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            LANG            : 'RU',
            'description'   : 'The region associated with the IP address represented as a string in Russian',
        },
    )
    region_ua: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            LANG            : 'UK',
            'description'   : 'The region associated with the IP address represented as a string in Ukrainian',
        },
    )
    country_code: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            LANG            : 'EN',
            'description'   : 'The country code associated with the IP address',
        },
    )
    country: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            LANG            : 'EN',
            'description'   : 'The city associated with the IP address represented as a string in English',
        },
    )
    country_rus: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            LANG            : 'RU',
            'description'   : 'The city associated with the IP address represented as a string in Russian',
        },
    )
    country_ua: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            LANG            : 'UK',
            'description'   : 'The city associated with the IP address represented as a string in Ukrainian',
        },
    )
    latitude: Optional[float] = field(
        default = None,
        compare = False,
        metadata = {
            'description'   : 'The latitude',
        },
    )
    longitude: Optional[float] = field(
        default = None,
        compare = False,
        metadata = {
            'description'   : 'The longitude',
        },
    )
    time_zone: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'description'   : 'The time zone',
        },
    )
    zip_code: Optional[int] = field(
        default = None,
        compare = False,
        metadata = {
            'description'   : 'The zip code',
        },
    )

    def __str__(self) -> str:
        """String representation of a single Geo result

        Simply return in the format "IP Country City"

        Examples:
        """
        ## Check if there is an error for the IP
        if self.error:
            ## Set default values for country/city to error
            country = 'Error'
            city = 'Error'
        else:
            ## Set default values for country/city to 'Unknown' if not defined
            ## This is required as a TypeError will be raised if they are not set
            if self.country:
                country = self.country
            else:
                country = 'Unknown'
            if self.city:
                city = self.city
            else:
                city = 'Unknown'

        ## Return the formatted string
        return f'{self.ip:40} {country:20} {city}'

    def distance_to(self, other: object, unit: str = 'kilometer') -> float:
        """Calculate the distance between the geo location of two different IP's

        Both IP's must have the latitude and longitude set otherwise no calculation can be made.

        Arguments:
            other (GeoLookupResult object): The GeoLookupResult object to measure distance to
            unit (str): The unit to output results in. Must be either 'kilometer' or 'mile'. Defaults to 'kilometer'.

        Returns:
            float: The distance between the two IP's.

        Raises:
            ValueError: Latitude or Longtitude is not defined for one or both objects
            RuntimeError: Incorrect unit format specified

        Examples:

        """
        ## Make sure both the objects have a latitude/longitude set
        if not self.latitude or not other.latitude or not self.longitude or not other.longitude:
            raise ValueError('Both GeoResult objects must have a latitude/longitude defined.')

        ## Make sure the unit is set correctly
        if unit != 'kilometer' and unit != 'mile':
            raise RuntimeError('The unit option must be either "kilometer" or "mile"')

        ## Use the haversine formula to calculate the distance
        phi_1, phi_2 = radians(self.latitude), radians(other.latitude)
        lam_1, lam_2 = radians(self.longitude), radians(other.longitude)
        h = (sin((phi_2 - phi_1) / 2)**2
             + cos(phi_1) * cos(phi_2) * sin((lam_2 - lam_1) / 2)**2)

        ## Return the calculated distance
        ## 6371 is the earth radius in KM
        if unit == 'kilometer':
            return 2 * 6371 * asin(sqrt(h))
        elif unit == 'mile':
            return (2 * 6371 * asin(sqrt(h))) * 0.62137119

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