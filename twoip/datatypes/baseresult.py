# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from ipaddress import IPv4Address, IPv6Address
from typing import Union, Optional, List, Tuple

@dataclass(frozen = False)
class BaseResult(object):
    """Base dataclass for a single lookup result

    This dataclass is used for both Geo and Provider lookup result types.
    """
    ## Assign the fields
    ip: str = field(
        init = False,
        compare = False,
        metadata = {
            'title'         : 'IP Address',
            'description'   : 'The IP address that was looked up represented as a string',
        },
    )
    ipaddress: Union[IPv4Address, IPv6Address] = field(
        compare = True,
        metadata = {
            'description'   : 'The IP address that was looked up represented as an ipaddress object',
        },
    )
    http_code: Optional[int] = field(
        default = None,
        compare = False,
        metadata = {
            'title'         : 'HTTP Code',
            'description'   : 'The HTTP response code from the API',
        },
    )
    api_response_raw: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'description'   : 'The raw API response body represented as a string',
        },
    )
    error: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'title'         : 'Error',
            'description'   : 'The error message/information if the geo lookup failed',
        },
    )
    success: bool = field(
        init = False,
        compare = False,
        metadata = {
            'title'         : 'Success',
            'description'   : 'If the lookup was successful or not',
        },
    )
    success_icon: str = field(
        init = False,
        compare = False,
        metadata = {
            'title'         : 'Success',
            'description'   : 'If the lookup was successful or not (icon format)',
        },
    )

    def __post_init__(self) -> object:
        """Function that is executed after creating a new BaseResult object

        Currently this function will create the ip attribute to represent the IP address as a string.
        """
        ## Convert the ipaddress object to a string and set in the IP field
        self.ip = f'{self.ipaddress}'

        ## Check if the HTTP status is 200 and if there is any error; if not the lookup was successful
        if self.http_code == 200 and not self.error:
            self.success = True,
            self.success_icon = '✔'
        else:
            self.success = True,
            self.success_icon = '✖'

    def get_meta(self, field: str, name: str) -> str:
        """Retrieve metadata for a field

        Args:
            field (str): The field name to retrieve the metadata for
            name (str): The metadata entry to retrieve

        Raises:
            KeyError: The field or metadata attribute does not exist

        Returns:
            str: The metadata entry
        """
        ## Get the attribute to ensure it exists
        try:
            attribute = self.__dataclass_fields__[field]
        except KeyError:
            raise KeyError(f'The field "{field}" does not exist')

        ## Get the metadata
        try:
            data = attribute.metadata[name]
        except KeyError:
            raise KeyError(f'The metadata entry name "{name}" does not exist')

        ## Return the metadata
        return data

    def describe(self) -> str:
        """Describe the object by parsing the metadata defined for each field

        Returns:
            str: The description output as a string
        """
        ## Prepare list of data to output
        output: List[str] = ['Field list:']

        ## Loop each attribute
        for field in self.__dataclass_fields__:

            output.append(f'- Field: {field}')

            ## Attempt to get field title
            try:
                output.append(f'\t- Title: {self.get_meta(field = field, name = "title")}')
            except Exception:
                pass

            ## Attempt to get field description
            try:
                output.append(f'\t- Description: {self.get_meta(field = field, name = "description")}')
            except Exception:
                pass

        ## Return output
        return '\n'.join(output)

    def is_global(self) -> bool:
        """Check if the IP address is globally routable address (eg. not multicast or RFC1918)

        Raises:
            RuntimeError: Exception from ip_address

        Returns:
            bool: True if the IP is globally routable

        Examples:

        """
        ## Check if IP is global and return
        try:
            is_global = self.ipaddress.is_global
        except Exception as e:
            raise RuntimeError(f'Exception checking if IP address is global:\n{e}')
        else:
            return is_global

    def is_private(self) -> bool:
        """Check if the IP address is private IP address (eg. RFC1918)

        Note: This does NOT include multicast, link local, loopback and other IP's that are not globally routable.
        This check can be used in conjunction with is_global() to check for other IP types.

        Raises:
            RuntimeError: Exception from ip_address

        Returns:
            bool: True if the IP is private

        Examples:

        """
        ## Check if IP is private and return
        try:
            is_private = self.ipaddress.is_private
        except Exception as e:
            raise RuntimeError(f'Exception checking if IP address is private:\n{e}')
        else:
            return is_private

    def fields(self) -> List[Tuple(str, str)]:
        """Return a list of available fields and their titles

        Returns:
            List[Tuple(str, str)]: The list of fields. Each field is a tuple in the format (field, Title)
        """
        ## Create list to store fields
        fields = []

        ## Loop each attribute
        for field in self.__dataclass_fields__:

            ## Attempt to get field title - if there is a result it can be added to output
            try:
                fields.append((f'{field}', f'{self.get_meta(field = field, name = "title")}'))
            except Exception:
                pass

        ## Return list of fields
        return fields