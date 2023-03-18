# -*- coding: utf-8 -*-

"""
2IP API Client

Command line interface for interacting with the 2IP API.
"""

from sys import stderr
from typing import Optional, Tuple

import click
from loguru import logger
from loguru._defaults import (
    LOGURU_DEBUG_NO,
    LOGURU_ERROR_NO,
    LOGURU_INFO_NO,
    LOGURU_SUCCESS_NO,
    LOGURU_TRACE_NO,
    LOGURU_WARNING_NO,
)


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
    2IP Reseller API Client - CLI
    """
    # Ensure CLI called with __main__
    ctx.ensure_object(dict)

    # Set available logging levels
    levels = {
        0: LOGURU_ERROR_NO,
        1: LOGURU_WARNING_NO,
        2: LOGURU_SUCCESS_NO,
        3: LOGURU_INFO_NO,
        4: LOGURU_DEBUG_NO,
        5: LOGURU_TRACE_NO,
    }

    # Check if __debug__; if so allow changing verbosity
    if __debug__:
        # Get the log level that should be used. If the log level is out of range (ie. above 5) the level will default
        # to LOGURU_TRACE_NO
        level = levels.get(verbosity, LOGURU_TRACE_NO)
    else:
        # If __debug__ is False, set the log level to LOGURU_ERROR_NO
        level = LOGURU_ERROR_NO

    # Set logging level
    logger.remove()
    logger.add(stderr, level=level)
    logger.opt(lazy=True)

    # Log logging has been setup
    logger.debug(f"Log level set to {verbosity}")
    if not __debug__:
        logger.warning("Running in optimized mode; logging level set to ERROR")

    # Set up the API client
    client = Client(
        key=key,
        url=url,
        timeout=timeout,
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
