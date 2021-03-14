# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from math import asin, cos, radians, sin, sqrt
from typing import Optional

from .baseresult import BaseResult

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
            'lang'          : 'EN',
            'title'         : 'City',
            'description'   : 'The city associated with the IP address represented as a string in English',
        },
    )
    city_rus: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'lang'          : 'RU',
            'title'         : 'City (RU)',
            'description'   : 'The city associated with the IP address represented as a string in Russian',
        },
    )
    region: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'lang'          : 'EN',
            'title'         : 'Region',
            'description'   : 'The region associated with the IP address represented as a string in English',
        },
    )
    region_rus: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'lang'          : 'RU',
            'title'         : 'Region (RU)',
            'description'   : 'The region associated with the IP address represented as a string in Russian',
        },
    )
    region_ua: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'lang'          : 'UA',
            'title'         : 'Region (UA)',
            'description'   : 'The region associated with the IP address represented as a string in Ukrainian',
        },
    )
    country_code: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'title'         : 'Country Code',
            'description'   : 'The country code associated with the IP address',
        },
    )
    country: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'lang'          : 'EN',
            'title'         : 'Country',
            'description'   : 'The city associated with the IP address represented as a string in English',
        },
    )
    country_rus: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'lang'          : 'RU',
            'title'         : 'Country (RU)',
            'description'   : 'The city associated with the IP address represented as a string in Russian',
        },
    )
    country_ua: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'lang'          : 'UA',
            'title'         : 'Country (UA)',
            'description'   : 'The city associated with the IP address represented as a string in Ukrainian',
        },
    )
    latitude: Optional[float] = field(
        default = None,
        compare = False,
        metadata = {
            'title'         : 'Latitude',
            'description'   : 'The latitude',
        },
    )
    longitude: Optional[float] = field(
        default = None,
        compare = False,
        metadata = {
            'title'         : 'Longitude',
            'description'   : 'The longitude',
        },
    )
    time_zone: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'title'         : 'Time Zone',
            'description'   : 'The time zone',
        },
    )
    zip_code: Optional[int] = field(
        default = None,
        compare = False,
        metadata = {
            'title'         : 'ZIP Code',
            'description'   : 'The ZIP code',
        },
    )

    def __post_init__(self) -> object:
        """Function that is executed after creating a new GeoLookupResult object

        This function will create the IP string and set the success icon.
        """
        ## Convert the ipaddress object to a string and set in the IP field
        self.ip = f'{self.ipaddress}'

        ## Set the success/success icon values
        self._init_success()

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