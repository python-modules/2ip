# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

from .georesult import GeoResult

@dataclass(frozen = False)
class Geo(object):
    """Dataclass to store all results from multiple Geo IP lookups

    Examples:
        >>> result1 = GeoLookupResult(ip = '192.0.2.1')
        >>> result2 = GeoLookupResult(ip = '192.0.2.2', city = 'Somewhere', country = 'Some Country')
        >>> results = GeoLookup([result1, result2])
    """
    ## Assign slots
    __slots__ = [ 'results' ]

    ## Set results type
    results: List[GeoResult]

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
                'zip_code': None,
                'error': None,
                'code': 200},
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
                'zip_code': None,
                'error': None,
                'code': 200}}
        """
        ## Create empty list of results to return
        result_dict = {}

        ## Loop over each result
        for result in self.results:
            ## Skip any duplicate results
            if result.ip in result_dict:
                continue
            ## Add the result to results dict
            result_dict[result.ip] = result.__dict__

        ## Return results
        return result_dict

