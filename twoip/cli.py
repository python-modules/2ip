# -*- coding: utf-8 -*-

"""
TwoIP API Client - CLI

This file provides the CLI for use with TwoIP.
"""

import logging
from ipaddress import IPv4Address, IPv6Address
from typing import Optional, Literal, Union

import click

from twoip.__version__ import __version__
from twoip.__config__ import __api__
from twoip.parameters import IPAddressParam, URLParam

# Generate sample GeoResult and ProviderResult (used for retrieving available fields
SAMPLE_IP = IPv4Address("192.0.2.0")
# SAMPLE_GEO = GeoResult(ipaddress=SAMPLE_IP)
# SAMPLE_PROVIDER = ProviderResult(ipaddress=SAMPLE_IP)

# Get command line arguments/options
# Allow use of --help and -h for click
@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-a",
    "--api",
    "api",
    default=__api__,
    help="The base API URL - this should not be changed unless there is a specific reason",
    show_default=True,
    type=URLParam(),
)
@click.option(
    "-c",
    "--connections",
    "connections",
    default=10,
    help="Maximum number of HTTP connections to open to API",
    show_default=True,
    type=click.IntRange(1, 100, clamp=True),
)
# @click.option(
#     "-f",
#     "--field",
#     "fields",
#     help="Field to add to output - specify once for each field",
#     short_help="Field names",
#     type=click.STRING,
#     required=False,
#     multiple=True,
#     autocompletion=__fields_autocomplete,
# )
@click.option(
    "--http2",
    "http2",
    default=True,
    help="Enable HTTP2 support for querying API",
    show_default=True,
    type=bool,
    is_flag=True,
)
@click.argument(
    "ips",
    nargs=-1,
    required=True,
    type=IPAddressParam(),
    metavar="IP",
)
@click.option(
    "-k",
    "--key",
    "key",
    help="The optional API key for 2ip.me",
    type=str,
    required=False,
)
@click.option(
    "-l",
    "--lookup",
    "lookup",
    default="geo",
    help="The lookup provider/type (geo for geographic information or " \
        "provider for provider information)",
    show_default=True,
    type=click.Choice(["geo", "provider"], case_sensitive=False),
    is_eager=True,
)
@click.option(
    "-o",
    "--output",
    "output",
    default="table",
    help="The output format. The output may be formatted as table or CSV " \
        "which you can redirect into a file",
    show_default=True,
    type=click.Choice(["table", "csv", "json"], case_sensitive=False),
)
@click.option(
    "-s",
    "--strict",
    "strict",
    default=False,
    help="Strict mode - any errors will return an exception and exit with " \
        "non-0 exit code",
    show_default=True,
    type=bool,
    is_flag=True,
)
@click.option(
    "-v",
    "--verbose",
    "verbosity",
    count=True,
    help="Set output verbosity level - specify multiple times for further " \
        "debugging",
)
@click.version_option()
def cli(
    ips: tuple[Union[IPv4Address, IPv6Address]],
    api: str = __api__,
    connections: int = 10,
    http2: bool = True,
    key: Optional[str] = None,
    lookup: Literal["geo", "provider"] = "geo",
    output: Literal["table", "csv", "json"] = "table",
    strict: bool = False,
    verbosity: int = 0,
) -> None:
    """The main TwoIP API client.

    This will execute the API query and output the results in the format
    requested.
    """

if __name__ == "__main__":
    cli(auto_envvar_prefix="2IP")
