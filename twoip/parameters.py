# -*- coding: utf-8 -*-

# pylint: disable=broad-except, invalid-name

"""
TwoIP API Client - CLI - IP/URL Parameter Types

This file contains the validation logic for the IP/URL parameter type
that is used by the CLI (for 'click').
"""

from urllib import parse
from ipaddress import ip_address, IPv4Address, IPv6Address
from typing import Union
from click import ParamType

class URLParam(ParamType):
    """Validate the parameter is a valid URL

    Examples:
        'https://google.com' will pass validation
        'fsd4g,d' will fail validation
    """

    name: str = "URL"

    def convert(self, value: str, param, ctx) -> str:
        """The function which will perform validation or normalization

        Arguments:
            value (str): The URL to validate

        Returns:
            str: The validated URL
        """
        ## Attempt URL validation
        try:
            url = parse.urlparse(value)
        except Exception as e:
            ## Pass the exception to click
            self.fail(
                f'Exception validating "{value!r}" as a valid URL: {e}',
                param,
                ctx,
            )

        ## Make sure the URL is formed correctly
        if all([url.scheme, url.netloc]):
            if url.path:
                formatted_url: str = f"{url.scheme}://{url.netloc}{url.path}"
            else:
                formatted_url: str = f"{url.scheme}://{url.netloc}"
        else:
            self.fail(
                f'URL {value!r} is not correctly formed',
                param,
                ctx,
            )

        ## Return formatted url
        return formatted_url

class IPAddressParam(ParamType):
    """Validate the parameter is an IPv4/IPv6 address and normalize into an
    IPv4Address or IPv6Address object.

    Examples:
        '192.0.2.0' will become IPv4Address('192.0.2.0')
        '2001:0DB8:0004:3f:00::2' will become IPv6Address('2001:db8:4:3f::2')
    """

    name: str = "IP Address"

    def convert(self, value: str, param, ctx) -> Union[IPv4Address, IPv6Address]:
        """The function which will perform validation or normalization

        Arguments:
            value (str): The IPv4/IPv6 address

        Returns:
            Union[IPv4Address, IPv6Address]: The IPv4Address or IPv6Address object
        """
        ## Attempt address creation
        try:
            address: Union[IPv4Address, IPv6Address] = ip_address(value)
        except ValueError:
            ## Not a valid IPv4/IPv6 address
            self.fail(
                f'Could not validate "{value!r}" as a valid IPv4 or IPv6 IP address'
            )
        except Exception as e:
            ## Other exception types should be handled
            self.fail(
                f'Exception validating "{value!r}" as a valid IPv4 or IPv6 IP address: {e}',
                param,
                ctx,
            )

        ## Return validated address object
        return address
