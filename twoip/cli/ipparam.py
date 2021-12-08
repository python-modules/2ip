# -*- coding: utf-8 -*-

"""
Click Parameter Type - IP Address

This parameter type will ensure the value provided is an IP address and convert it into the relevant IPv4Address or IPv6Address object.
"""

from click import ParamType
from ipaddress import ip_address, IPv4Address, IPv6Address
from typing import Union


class IPAddressParam(ParamType):
    """Validate the parameter is an IPv4/IPv6 address and normalize into an IPv4Address or IPv6Address object.

    Examples:
        '192.0.2.0' will become IPv4Address('192.0.2.0')
        '2001:0DB8:0004:3f:00::2' will become IPv6Address('2001:db8:4:3f::2')
    """

    name = "IP Address"

    def convert(self, value: str, param, context) -> Union[IPv4Address, IPv6Address]:
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
                context,
            )
        else:
            return address
