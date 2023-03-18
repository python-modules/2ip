# -*- coding: utf-8 -*-

"""
2IP API Client

Command line interface for interacting with the 2IP API.
"""

from typing import Optional, Tuple

import click

from twoip.__version__ import __version__
from twoip.client import Client
from twoip.validators.url import URL
from twoip.methods import Provider


# Get command line arguments/options
@click.group()
@click.version_option(
    version=__version__,
    prog_name="2IP Command Line Interface API Client",
)
@click.option(
    "-k",
    "--key",
    "key",
    envvar="API_KEY",
    help="The API key to use for authentication",
    required=False,
    type=str,
)
@click.option(
    "-t",
    "--timeout",
    "timeout",
    default="30",
    envvar="TIMEOUT",
    help="The timeout for HTTP requests to the API",
    type=click.IntRange(min=1, max=120),
)
@click.option(
    "-u",
    "--url",
    "url",
    envvar="API_URL",
    help="Override the base URL for the 2IP API",
    required=False,
    type=URL(),
)
@click.option(
    "-v",
    "--verbose",
    "verbosity",
    count=True,
    help="Set output verbosity level - specify multiple times for further debugging",
)
@click.pass_context
def cli(
    ctx,
    timeout: int,
    key: Optional[str] = None,
    url: Optional[str] = None,
    verbosity: int = 1,
) -> None:
    """
    2IP API Client - CLI
    """
    # Ensure CLI called with __main__
    ctx.ensure_object(dict)

    # Set up the API client
    client = Client(
        key=key,
        url=url,
        timeout=timeout,
        verbosity=verbosity,
    )

    # Pass the lookup client to the context
    ctx.obj["client"] = client


@cli.command()
@click.argument(
    "addresses",
    nargs=-1,
    required=True,
    type=str,
)
@click.pass_context
def provider(ctx, addresses: Tuple[str]):
    """
    Perform a provider lookup for one or more IP addresses
    """
    # Get Provider lookup client
    provider_m: Provider = ctx.obj["client"].provider()

    # Run lookup
    result = provider_m.lookup(addresses=list(dict.fromkeys(addresses)))

    print(result.to_table())


if __name__ == "__main__":
    cli(obj={})  # pylint: disable=no-value-for-parameter
