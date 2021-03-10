# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

# Requirements for generating output (CSV or table)
from csv import writer as csvwriter, QUOTE_NONNUMERIC
from ipaddress import IPv4Address
from io import StringIO
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
        ## Output results as a table by default
        return self.to_table()

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

    @staticmethod
    def __generate_headers(fields: List[str]) -> list:
        """Generate headers from a list of fields

        Args:
            fields (List[str]): The list of fields to output

        Returns:
            list: The list of header data

        Raises:
            KeyError: Requested field does not exist
            ValueError: Requested field is not allowed to be output into table
        """
        ## Create a test ProviderResult object
        result = ProviderResult(ipaddress = IPv4Address('192.0.2.0'))

        ## Create dict to store table headers
        headers = []

        ## Make sure each field exists in the ProviderResult object
        ## If the field does exist, the header will then be retrieved
        for field in fields:

            ## Check for field
            if not hasattr(result, field):
                raise KeyError(f'The requested field "{field}" does not exist in the ProviderResult object')

            ## Get field title; if no title set it means the field can't be output to a table
            try:
                title = result.get_meta(field = field, name = 'title')
            except KeyError:
                raise ValueError(f'The requested field "{field}" cannot be output to a table')
            else:
                headers.append(title)

        ## Return the headers
        return headers

    def to_table(self, fields: List[str] = ['ip', 'autonomous_system', 'name', 'website']) -> str:
        """Format multiple provider lookup results into a table

        Args:
            fields (List[str], optional): The list of fields to output. Defaults to ['ip', 'autonomous_system', 'name', 'website'].

        Returns:
            str: The formatted table
        """
        ## Retrieve headers for table
        headers = self.__generate_headers(fields = fields)

        ## Create list to store data of each result
        data: List[List[str]] = []

        ## Loop over each result
        for result in self.results:

            ## Create list to store the table data for this result
            result_data: List[str] = []

            ## Get each requested field, format as string and add to result data
            for field in fields:
                result_data.append(f'{getattr(result, field)}')

            ## Add the fields to the table data
            data.append(result_data)

        ## Generate and return table
        return tabulate(tabular_data = data, headers = headers, tablefmt = 'pretty')

    def to_csv(self, fields: List[str] = ['ip', 'autonomous_system', 'name', 'website'], delimiter: str = ',') -> str:
        """Format multiple provider lookup results into a CSV

        Args:
            fields (List[str], optional): The list of fields to output. Defaults to ['ip', 'autonomous_system', 'name', 'website'].
            delimiter (str, optional): The field delimiter. Defaults to ','.

        Returns:
            str: The CSV
        """
        ## Create header row
        data: List[List[str]] = self.__generate_headers(fields = fields)

        ## Loop over each result
        for result in self.results:

            ## Create list to store the table data for this result
            result_data: List[str] = []

            ## Get each requested field, format as string and add to result data
            for field in fields:
                result_data.append(f'{getattr(result, field)}')

            ## Add the fields to the table data
            data.append(result_data)

        ## Generate the CSV
        output = StringIO()
        writer = csvwriter(output, quoting = QUOTE_NONNUMERIC, delimiter = delimiter)
        writer.writerows(data)

        ## Return the CSV
        return output.getvalue()