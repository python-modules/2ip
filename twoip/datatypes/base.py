# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List

@dataclass(frozen = False)
class Base(object):
    """Base dataclass for multiple lookup results

    This dataclass is used for both Geo and Provider lookup result types.
    """
    @staticmethod
    def __to_dict(results: List[object]) -> dict:
        """Generate dict from a list of results using the IP address as a key for each entry

        Args:
            results (List[object]): The object containing the results

        Returns:
            dict: The generated dict
        """
        ## Create empty list of results to return
        result_dict: dict = {}

        ## Loop over each result
        for result in results:

            ## Skip any duplicate results
            if result.ip in result_dict:
                continue

            ## Add the result to results dict
            result_dict[result.ip] = result.__dict__

        ## Return results
        return result_dict

    @staticmethod
    def __retrieve_data(results: List[object], fields: List[str]) -> list:
        """Loop over each result and retrieve the requested attributes/fields

        Args:
            results (List[object]): The object containing the results
            fields (List[str]): The fields to retrieve

        Returns:
            list: The list of results
        """

        ## Create empty dict to store the data
        data: List[List[str]] = []

        ## Loop over each result
        for result in results:

            ## Create list to store the table data for this result
            result_data: List[str] = []

            ## Get each requested field, format as string and add to result data
            for field in fields:
                result_data.append(f'{getattr(result, field)}')

            ## Add the fields to the table data
            data.append(result_data)

        ## Return the generated data
        return data

    @staticmethod
    def __retrieve_headers(sample: object, fields: List[str]) -> list:
        """Generate headers from a list of fields

        Args:
            sample (object): A sample object to generate the headers from
            fields (List[str]): The fields to retrieve headers from

        Returns:
            list: The list of header data

        Raises:
            KeyError: Requested field does not exist
            ValueError: Requested field is not allowed to be output into table
        """
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