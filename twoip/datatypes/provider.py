# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

from tabulate import tabulate

from .providerresult import ProviderResult

@dataclass(frozen = False)
class Provider(object):
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
    results: List[ProviderResult]

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
                'site': None,
                'code': 200},
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
                'site': 'https://www.example.com',
                'code': 200}}
        """
        ## Create empty list of results to return
        result_dict = {}

        ## Loop over each result
        for result in self.results:

            ## Skip any duplicate results
            if result.ip in result_dict:
                continue

            ## Convert IP to string to use a dict key
            ip = f'{result.ip}'

            ## Add the result to results dict
            result_dict[ip] = result.__dict__

        ## Return results
        return result_dict

    def to_table(self) -> str:
        """Format the results into a table
        """
        ## Table header
        headers: List[str] = [ 'IP Address', 'ASN', 'Name', 'Website' ]

        ## Create list to store data of each result
        data: List[List[str]] = []

        ## Loop over each result
        for result in self.results:

            ## Append result to data list
            data.append([
                f'{result.ip}',
                f'{result.autonomous_system}',
                f'{result.name}',
                f'{result.website}'])

        ## Generate and return table
        return tabulate(tabular_data = data, headers = headers, tablefmt = 'pretty')