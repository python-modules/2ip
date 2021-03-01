# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from ipaddress import IPv4Address, IPv6Address, ip_address
from math import asin, cos, radians, sin, sqrt
from typing import Union, Optional, List

# Define constant for language standard
LANG = 'ISO 639-1'

@dataclass(frozen = False)
class GeoLookupResult:
    """Dataclass to individual results of Geo lookups for IP's

    Examples:
        >>> result1 = GeoLookupResult(ip = '192.0.2.1')
        >>> result2 = GeoLookupResult(ip = '192.0.2.2', city = 'Somewhere', country = 'Some Country')
    """
    ## Assign the fields
    ip: Union[IPv4Address, IPv6Address] = field(
        metadata = {
            'description'   : 'The IP address represented as a string',
        },
    )
    city: Optional[str] = field(
        default = None,
        metadata = {
            LANG            : 'EN',
            'description'   : 'The city associated with the IP address represented as a string in English',
        },
    )
    city_rus: Optional[str] = field(
        default = None,
        metadata = {
            LANG            : 'RU',
            'description'   : 'The city associated with the IP address represented as a string in Russian',
        },
    )
    region: Optional[str] = field(
        default = None,
        metadata = {
            LANG            : 'EN',
            'description'   : 'The region associated with the IP address represented as a string in English',
        },
    )
    region_rus: Optional[str] = field(
        default = None,
        metadata = {
            LANG            : 'RU',
            'description'   : 'The region associated with the IP address represented as a string in Russian',
        },
    )
    region_ua: Optional[str] = field(
        default = None,
        metadata = {
            LANG            : 'UK',
            'description'   : 'The region associated with the IP address represented as a string in Ukrainian',
        },
    )
    country: Optional[str] = field(
        default = None,
        metadata = {
            LANG            : 'EN',
            'description'   : 'The city associated with the IP address represented as a string in English',
        },
    )
    country_rus: Optional[str] = field(
        default = None,
        metadata = {
            LANG            : 'RU',
            'description'   : 'The city associated with the IP address represented as a string in Russian',
        },
    )
    country_ua: Optional[str] = field(
        default = None,
        metadata = {
            LANG            : 'UK',
            'description'   : 'The city associated with the IP address represented as a string in Ukrainian',
        },
    )
    latitude: Optional[float] = field(
        default = None,
        metadata = {
            'description'   : 'The latitude',
        },
    )
    longitude: Optional[float] = field(
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

    def __post_init__(self) -> object:
        """Function that is executed after creating a new GeoLookupResult object

        This function will currently check and normalize the IP address.

        Raises:
            ValueError: IP address cannot be validated
            RuntimeError: Exception while creating ipaddress object

        """
        ## Create IP address object which will validate/normalize the IP
        try:
            ip = f'{ip_address(self.ip)}'
        except ValueError as e:
            raise ValueError(f'The IP address "{self.ip}" does not appear to be valid:\n{e}')
        except Exception as e:
            raise RuntimeError(f'Exception creating ipaddress object from IP "{self.ip}":\n{e}')

        ## Set the normalized ip as a string
        self.ip = f'{ip}'

    def __str__(self) -> str:
        """String representation of a single Geo result

        Simply return in the format "IP Country City"

        Examples:
            >>> print(GeoLookupResult(ip = '192.0.2.1'))
            192.0.2.1                                Unknown              Unknown
            >>> print(GeoLookupResult(ip = '192.0.2.2', city = 'Somewhere', country = 'Some Country'))
            192.0.2.2                                Some Country         Somewhere
        """
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
            >>> result1 = GeoLookupResult(ip = '192.0.2.1', latitude=80.9739186644168, longitude=164.51642711112837)
            >>> result2 = GeoLookupResult(ip = '192.0.2.2', latitude=74.05075444437098, longitude=-157.51482442257847)
            >>> result1.distance_to(result2)
            1155.9704248739984 ## Result in kilometers
            >>> result1.distance_to(result2, 'mile')
            718.286718508762 ## Result in miles
        """
        ## Make sure both the objects have a latitude/longitude set
        if not self.latitude or not other.latitude or not self.longitude or not other.longitude:
            raise ValueError('Both GeoLookupResult objects must have a latitude/longitude defined.')

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

@dataclass
class GeoLookup:
    """Dataclass to store all results from multiple Geo IP lookups

    Examples:
        >>> result1 = GeoLookupResult(ip = '192.0.2.1')
        >>> result2 = GeoLookupResult(ip = '192.0.2.2', city = 'Somewhere', country = 'Some Country')
        >>> results = GeoLookup([result1, result2])
    """
    ## Assign slots
    __slots__ = [ 'results' ]

    ## Set results type
    results: List[GeoLookupResult]

    def __str__(self) -> str:
        """String representation of all Geo results

        Simply return in the format "IP Country City"

        Examples:
            >>> result1 = GeoLookupResult(ip = '192.0.2.1')
            >>> result2 = GeoLookupResult(ip = '192.0.2.2', city = 'Somewhere', country = 'Some Country')
            >>> results = GeoLookup([result1, result2])
            >>> print(results)
            192.0.2.1                                Unknown              Unknown
            192.0.2.2                                Some Country         Somewhere
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
            >>> result1 = GeoLookupResult(ip = '192.0.2.1')
            >>> result2 = GeoLookupResult(ip = '192.0.2.2', city = 'Somewhere', country = 'Some Country')
            >>> results = GeoLookup([result1, result2])
            >>> results.to_dict()
            {'192.0.2.1': {'city': None,
               'city_rus': None,
               'country': None,
               'country_rus': None,
               'country_ua': None,
               'ip': '192.0.2.1',
               'latitude': None,
               'longitude': None,
               'region': None,
               'region_rus': None,
               'region_ua': None,
               'time_zone': None,
               'zip_code': None},
            '192.0.2.2': {'city': 'Somewhere',
               'city_rus': None,
               'country': 'Some Country',
               'country_rus': None,
               'country_ua': None,
               'ip': '192.0.2.2',
               'latitude': None,
               'longitude': None,
               'region': None,
               'region_rus': None,
               'region_ua': None,
               'time_zone': None,
               'zip_code': None}}
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