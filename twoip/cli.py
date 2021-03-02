# -*- coding: utf-8 -*-

"""
2ip.me - API Client - Command Line Interface
"""

# Import external modules
import click
import logging as log
from typing import Tuple, Optional
from ipaddress import ip_address

# Import local modules
from .log import Log as logger
from .twoip import TwoIP

# Validator for IP's
class IPParamType(click.ParamType):
    """Validate a parameter as an IPv4 or IPv6 address and normalize it
    """
    name = "ip"

    def convert(self, value, param, ctx) -> str:
        """Validate and normalize the IP
        """
        try:
            # Create ip_address object to test IP is valid
            address = ip_address(value)
        except ValueError:
            self.fail(f'{value!r} is not a valid IP address', param, ctx)
        except Exception as e:
            self.fail(
                f'Exception validating IP address "{value!r}": {e}', param, ctx)
        else:
            # Return the valid/noramlized IP address if no exception raised
            return f'{address}'

# Set validator function for click
IPADDRESS = IPParamType()

def __load_key(file: object) -> str:
    """Load API key from file

    Arguments:
        file: The file object

    Returns:
        str: The API key

    Raises:
        ValueError: No API key found
        RunTimeException: Exception reading file
    """
    log.debug('Attempting to read API key from file object')

    ## Set default value
    key = None

    ## Read from the file object to retrieve API key
    try:
        for line in file:
            if not line.startswith('#'):
                key = line.strip()
    except Exception as e:
        log.info('Exception while trying to read API key: {e}')
        raise RuntimeError(e)

    ## If a key was found, return it otherwise raise exception
    if key:
        log.debug('Retrieved API key from file')
        log.trace(f'Key: {key}')
        return key
    else:
        log.debug('No API key could be retrieved from file; maybe it is empty')
        raise ValueError('No API key could be retrieved from file')

# Get command line arguments/options
@click.command()
@click.argument(
    'ips',
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
    '-v', '--verbose', 'verbosity',
    count       =   True,
    help        =   'Set output verbosity level - specify multiple times for further debugging',
)

# Execute CLI
def cli(
        ## One or more IP's to lookup
        ips: Tuple,
        ## An optional API key
        key: Optional[str] = None,
        ## An optional API key file
        keyfile: Optional[str] = None,
        ## Logging verbosity
        verbosity: int = 0
    ) -> None:
    """Perform 2ip.me lookups for one or more IP addresses
    """
    ## Setup logging
    logger(verbosity = verbosity)

    ## Remove any duplicate IP's
    ips = tuple(set(ips))

    ## If an API key file is provided, read the key
    if keyfile:
        ## Log a message if an API key was also specified
        if key:
            log.warn('Both an API key and API key file have been specified; the API key file takes priority')

        ## Attempt key load
        try:
            key = __load_key(file = keyfile)
        except Exception:
            if key:
                log.warn('Could not load API key from file; using API key option from command line instead')
            else:
                log.warn('Could not load API key from file; defaulting to not using any API key - rate limits will apply')
        else:
            log.debug('API key loaded from file')
    else:
        log.debug('Using API key from command line option')

    ## Print debugging
    log.trace("Normalized IP's to lookup:")
    for ip in ips:
        log.trace(ip)

    ## Create twoip object
    twoip = TwoIP(key = key)

# Allow using env vars for options
if __name__ == '__main__':
    cli(auto_envvar_prefix = '2IP')