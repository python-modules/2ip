# -*- coding: utf-8 -*-

"""
2ip.me - API Client - Command Line Interface
"""

# Import external modules
import click
import logging
from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import TextIO, Tuple, Optional, Literal, Union, List

# Import local modules
from .logger import Logger
from .twoip import TwoIP

from .datatypes.geo import Geo
from .datatypes.provider import Provider

# Get logger
log = logging.getLogger('twoip')

def __key(key: str = None, keyfile: TextIO = None) -> Union[str, None]:
    """If API key and/or keyfile defined, pick one and return the API key

    Args:
        key (str, optional): The API key string. Defaults to None.
        keyfile (TextIO, optional): The API key file handle. Defaults to None.

    Returns:
        Union[str, None]: If API key was loaded, the API key string
    """
    ## If an API key file is provided, read the key
    if keyfile:
        ## Log a message if an API key was also specified
        if key:
            log.warn('Both an API key and API key file have been specified; the API key file takes priority')
        ## Attempt key load
        try:
            key: str = __load_key(file = keyfile)
        except Exception:
            if key:
                log.warn('Could not load API key from file; using API key option from command line instead')
            else:
                log.warn('Could not load API key from file; defaulting to not using any API key - rate limits will apply')
        else:
            log.verbose('API key loaded from file')
    elif key:
        log.verbose('Using API key from command line option')
    else:
        log.verbose('Not using any API key')

    ## Return the API key
    return key

def __load_key(file: TextIO) -> str:
    """Load API key from file

    Arguments:
        file (TextIO): The file object

    Returns:
        str: The API key

    Raises:
        ValueError: No API key found
        RunTimeException: Exception reading file
    """
    log.debug(f'Attempting to read API key from file "{file.name}"')

    ## Set default value
    key = None

    ## Read from the file object to retrieve API key
    try:
        for line in file:
            if not line.startswith('#'):
                key = line.strip()
    except Exception as e:
        log.warn(f'Exception while trying to read API key from "{file.name}":\n{e}')
        raise RuntimeError(e)

    ## If a key was found, return it otherwise raise exception
    if key:
        log.debug(f'Retrieved API key from file "{file.name}"')
        log.trace(f'Key: {key}')
        return key
    else:
        log.warn(f'No API key could be retrieved from file "{file.name}"; maybe it is empty')
        raise ValueError(f'No API key could be retrieved from file "{file.name}"')

# Validator for IP's
class IPParamType(click.ParamType):
    """IP parameter validator

    This will verify that the IP address provided is a valid IPv4 or IPv6 address.
    Each address will then be returned as an IPv4Address or IPv6Address object.
    """
    name = "ip"

    def convert(self, value: str, param, ctx) -> Union[IPv4Address, IPv6Address]:
        """Validate and normalize the IP returning the IP address as a string
        """
        log.debug(f'Validating IP address "{value}"')
        try:
            # Create ip_address object to test IP is valid
            address: Union[IPv4Address, IPv6Address] = ip_address(value)
        except ValueError:
            self.fail(f'{value!r} is not a valid IP address', param, ctx)
        except Exception as e:
            self.fail(f'Exception validating IP address "{value!r}": {e}', param, ctx)
        else:
            # Return the IP address object
            return address

# Set validator function for click
IPADDRESS = IPParamType()

# Get command line arguments/options
@click.command()
@click.argument(
    'ip',
    nargs       =   -1,
    required    =   True,
    type        =   IPADDRESS,
)
@click.option(
    '-k', '--key', 'key',
    help        =   'The optional API key for 2ip.me',
    type        =   str,
    required    =   False,
)
@click.option(
    '-kf', '--keyfile', 'keyfile',
    help        =   'The optional API key file for 2ip.me',
    type        =   click.File(mode = 'r'),
    required    =   False,
)
@click.option(
    '-t', '--type', 'provider',
    default         = 'geo',
    help            = 'The lookup provider/type (geo for geographic information or provider for provider information)',
    show_default    = True,
    type            = click.Choice(['geo','provider'], case_sensitive = False),
)
@click.option(
    '-o', '--output', 'output',
    default         = 'table',
    help            = 'The output format',
    show_default    = True,
    type            = click.Choice(['table','csv'], case_sensitive = False),
)
@click.option(
    '-v', '--verbose', 'verbosity',
    count       =   True,
    help        =   'Set output verbosity level - specify multiple times for further debugging',
)

# Execute CLI
def cli(
        ## One or more IP's to lookup
        ip: Tuple,
        ## The lookup provider
        provider: Literal['geo','provider'] = 'geo',
        ## An optional API key
        key: Optional[str] = None,
        ## An optional API key file
        keyfile: Optional[TextIO] = None,
        ## The output format
        output: Literal['table','csv'] = 'table',
        ## Logging verbosity
        verbosity: int = 0,
    ) -> None:
    """Perform 2ip.me lookups for one or more IP addresses
    """
    ## Setup logging
    Logger(verbosity = verbosity)

    ## Check arguments
    assert provider in ['geo','provider']
    assert output in ['table','csv']

    ## Debugging
    log.info(f'TwoIP {provider} CLI lookup - Output format set to {output}')

    ## Remove any duplicate IP's and convert to list (from a tuple)
    ip: List[Union[IPv4Address, IPv6Address]] = list(set(ip))

    ## Get the API key if specified
    if key or keyfile:
        key = __key(key = key, keyfile = keyfile)

    ## Create twoip object
    twoip = TwoIP(key = key)

    ## Debugging
    if __debug__ and verbosity >= 5:
        log.trace('IP address list to lookup:')
        for address in ip:
            log.trace(f'{address}')

    ## Perform lookups
    if provider == 'geo':
        results: Geo = twoip.geo(ip = ip)
    elif provider == 'provider':
        results: Provider = twoip.provider(ip = ip)
    else:
        log.fatal(f'Provider lookup type {provider} has not been defined')

    ## Print the results in the requested format
    if output == 'table':
        print(results.to_table())
    elif output == 'csv':
        print(results.to_csv())
    else:
        log.fatal(f'Output type {output} has not been defined')

# Allow using env vars for options
if __name__ == '__main__':
    cli(auto_envvar_prefix = '2IP')