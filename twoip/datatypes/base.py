# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List, Optional, Literal

# Requirements for generating output (CSV or table)
from csv import writer as csvwriter, QUOTE_NONNUMERIC
from io import StringIO
from tabulate import tabulate

@dataclass(frozen = False)
class Base(object):
    """Base dataclass for multiple lookup results

    This dataclass is used for both Geo and Provider lookup result types.
    """
    def to_dict(self) -> dict:
        """Generate dict from a list of results using the IP address as a key for each entry

        Args:
            results (List[object]): The object containing the results

        Returns:
            dict: The generated dict

        Examples:
            >>> result1 = GeoResult(ipaddress = IPv4Address('192.0.2.0'), city = 'Some City', country = 'Some Country')
            >>> result2 = GeoResult(ipaddress = IPv6Address('2001:0db8::1'), city = 'Some City', country = 'Some Country')
            >>> geo_results = Geo(results = [result1, result2])
            >>> geo_results.to_dict()
            {
                '192.0.2.0': {
                    'ip': '192.0.2.0',
                    'ipaddress': IPv4Address('192.0.2.0'),
                    'city': 'Some City',
                    'country': 'Some Country',
                    ...
                },
                '2001:0db8::1': {
                    'ip': '2001:0db8::1,
                    'ipaddress': IPv6Address('2001:0db8::1'),
                    'city': 'Some City',
                    'country': 'Some Country',
                    ...
                },
            }
        """
        ## Create empty list of results to return
        result_dict: dict = {}

        ## Loop over each result
        for result in self.results:

            ## Skip any duplicate results
            if result.ip in result_dict:
                continue

            ## Add the result to results dict
            result_dict[result.ip] = result.__dict__

        ## Return results
        return result_dict

    def __retrieve_data(self, fields: List[str]) -> list:
        """Loop over each result and retrieve the requested attributes/fields

        Args:
            results (List[object]): The object containing the results
            fields (List[str]): The fields to retrieve

        Returns:
            list: The list of results

        Examples:
            >>> result1 = GeoResult(ipaddress = IPv4Address('192.0.2.0'), city = 'Some City', country = 'Some Country')
            >>> result2 = GeoResult(ipaddress = IPv6Address('2001:0db8::1'), city = 'Some City', country = 'Some Country')
            >>> geo_results = Geo(results = [result1, result2])
            >>> geo_results.retrieve_data(fields = ['ip', 'city', 'country'])
            [
                ['192.0.2.0', 'Some City', 'Some Country'],
                ['2001:0db8::1', 'Some City', 'Some Country'],
            ]
        """

        ## Create empty dict to store the data
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

        ## Return the generated data
        return data

    def __headers(self, fields: List[str]) -> list:
        """Generate table/CSV headers from a list of fields

        Args:
            sample (object): A sample object to generate the headers from
            fields (List[str]): The fields to retrieve headers from

        Returns:
            list: The list of header data

        Raises:
            KeyError: Requested field does not exist
            ValueError: Requested field is not allowed to be output into table

        Examples:
            >>> sample = GeoResult(ipaddress = IPv4Address('192.0.2.0'))
            >>> Geo.headers(sample = sample, fields = ['ip', 'country'])
            ['IP Address', 'Country']
        """
        ## Generate sample object
        sample = self._sample()

        ## Create dict to store table headers
        headers = []

        ## Make sure each field exists in the ProviderResult object
        ## If the field does exist, the header will then be retrieved
        for field in fields:

            ## Check for field
            if not hasattr(sample, field):
                raise KeyError(f'The requested field "{field}" does not exist in the GeoResult object')

            ## Get field title; if no title set it means the field can't be output to a table
            try:
                title = sample.get_meta(field = field, name = 'title')
            except KeyError:
                raise ValueError(f'The requested field "{field}" cannot be output to a table')
            else:
                headers.append(title)

        ## Return the headers
        return headers

    def __parse_fields(self, format: Literal['table','csv'], fields: Optional[List[str]] = None) -> List[str]:
        ## If no fields were provided, use the default fields
        if not fields:
            fields = self._default_fields(format = format)

        ## Insert the IP field to the start
        if 'ip' in fields:
            fields.insert(0, fields.pop(fields.index('ip')))
        else:
            fields.insert(0, 'ip')

        ## Return parsed/generated fields
        return fields

    def to_table(self, fields: Optional[List[str]] = None) -> str:
        """Format multiple geo or provider lookup results into a table

        Args:
            fields (List[str], optional): The list of fields to output

        Returns:
            str: The formatted table

        Examples:
        """
        ## Parse fields list or generate default fields if not specified
        fields = self.__parse_fields(format = 'table', fields = fields)

        ## Retrieve headers for table
        headers = self.__headers(fields = fields)

        ## Parse fields list or generate default fields if not specified
        data = self.__retrieve_data(fields = fields)

        ## Generate and return table
        return tabulate(tabular_data = data, headers = headers, tablefmt = 'pretty')

    def to_csv(self, fields: Optional[List[str]] = None, delimiter: str = ',') -> str:
        """Format multiple geo lookup results into a CSV

        Args:
            fields (List[str], optional): The list of fields to output. Defaults to ['ip', 'city', 'country'].
            delimiter (str, optional): The field delimiter. Defaults to ','.

        Returns:
            str: The CSV

        Examples:
        """
        ## Parse fields list or generate default fields if not specified
        fields = self.__parse_fields(format = 'csv', fields = fields)

        ## Retrieve headers for table
        headers = [self.__headers(fields = fields)]

        ## Retrieve the data
        data = self.__retrieve_data(fields = fields)

        ## Generate the CSV
        output = StringIO()
        writer = csvwriter(output, quoting = QUOTE_NONNUMERIC, delimiter = delimiter)
        writer.writerows(headers)
        writer.writerows(data)

        ## Return the CSV
        return output.getvalue()