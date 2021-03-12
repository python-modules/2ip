# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

# Requirements for generating output (CSV or table)
from csv import writer as csvwriter, QUOTE_NONNUMERIC
from ipaddress import IPv4Address
from io import StringIO
from tabulate import tabulate

from .base import Base
from .providerresult import ProviderResult

@dataclass(frozen = False)
class Provider(Base):
    """Dataclass to store all results from multiple provider lookups

    Examples:
    """
    ## Assign slots
    __slots__ = [ 'results' ]

    ## Set results type
    results: List[ProviderResult]

    def __str__(self) -> str:
        """Return a table of results

        This is the same as calling the to_table() function on the results.

        Returns:
            str: The results table
        """
        return self.to_table()

    def __generate_headers(self, fields: List[str]) -> list:
        """Generate headers from a list of fields

        Args:
            fields (List[str]): The list of fields to output

        Returns:
            list: The list of header data

        Examples:
        """
        ## Create a sample GeoResult object
        sample = ProviderResult(ipaddress = IPv4Address('192.0.2.0'))

        ## Retrieve headers
        headers = self.headers(sample = sample, fields = fields)

        ## Return the headers
        return headers

    def to_table(self, fields: List[str] = ['ip', 'success_icon', 'autonomous_system', 'name', 'website']) -> str:
        """Format multiple provider lookup results into a table

        Args:
            fields (List[str], optional): The list of fields to output. Defaults to ['ip', 'autonomous_system', 'name', 'website'].

        Returns:
            str: The formatted table

        Examples:
        """
        ## Retrieve headers for table
        headers = self.__generate_headers(fields = fields)

        ## Retrieve the data
        data = self.retrieve_data(fields = fields)

        ## Generate and return table
        return tabulate(tabular_data = data, headers = headers, tablefmt = 'pretty')

    def to_csv(self, fields: List[str] = ['ip', 'success', 'autonomous_system', 'name', 'website'], delimiter: str = ',') -> str:
        """Format multiple provider lookup results into a CSV

        Args:
            fields (List[str], optional): The list of fields to output. Defaults to ['ip', 'autonomous_system', 'name', 'website'].
            delimiter (str, optional): The field delimiter. Defaults to ','.

        Returns:
            str: The CSV

        Examples:
        """
        ## Create header row
        headers = self.__generate_headers(fields = fields)

        ## Retrieve the data
        data = self.retrieve_data(fields = fields)

        ## Generate the CSV
        output = StringIO()
        writer = csvwriter(headers + data, quoting = QUOTE_NONNUMERIC, delimiter = delimiter)
        writer.writerows(data)

        ## Return the CSV
        return output.getvalue()