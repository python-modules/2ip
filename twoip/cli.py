# -*- coding: utf-8 -*-

"""
2ip.me - API Client - Command Line Interface
"""

# Import external modules
import click
import logging
from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import TextIO, Tuple, Optional, Literal, Union, List
from urllib import parse as urlparse

# Import local modules
from .logger import Logger
from .twoip import TwoIP

from .datatypes.geo import Geo
from .datatypes.georesult import GeoResult
from .datatypes.provider import Provider
from .datatypes.providerresult import ProviderResult

# Import version info
from .__version__ import __version__

# Get logger
log = logging.getLogger('twoip')

# Base API url
API = 'https://api.2ip.ua'

# Generate sample GeoResult and ProviderResult (used for retrieving available fields
SAMPLE_IP = IPv4Address('192.0.2.0')
SAMPLE_GEO = GeoResult(ipaddress = SAMPLE_IP)
SAMPLE_PROVIDER = ProviderResult(ipaddress = SAMPLE_IP)

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

def __fields(provider: Literal['geo','provider'] = 'geo') -> List[Tuple]:
    """Retrieve a list of available fields for output

    Arguments:
        provider (Literal['geo','provider']): The provider type

    Returns:
        List[Tuple]: A list of fields in the format ('name','title')
    """
    ## Retrieve fields from the sample object
    if provider == 'geo':
        fields = SAMPLE_GEO.fields()
    elif provider == 'provider':
        fields = SAMPLE_PROVIDER.fields()
    else:
        fields = ()

    ## Remove the 'ip' field as it is always returned
    fields = [field for field in fields if 'ip' != field[0]]

    ## Return the newly generated tuple
    return fields

def __fields_autocomplete(ctx, args, incomplete):
    """Allow autocomplete for field names
    """
    ## Get the provider name from current context and retrieve the list of fields
    if 'provider' in ctx.params and ctx.params['provider']:
        provider: Literal['geo','provider'] = ctx.params['provider']
        ## Retrieve fields for provider
        fields: List[Tuple] = __fields(provider = provider)
    else:
        ## No provider name, get default fields
        fields: List[Tuple] = __fields()

    ## Check if any fields have already been defined
    if ctx.params and ctx.params['fields']:

        ## Filter out any defined fields from the fields list
        fields = [field for field in fields if field[0] not in ctx.params['fields']]

    ## Return autocomplete
    return [c for c in fields if incomplete in c[0]]

# Validator for URL's
def __validate_url(ctx, param, value):
    """Validate the API URL parameter
    """
    ## Try to parse with urlparse
    try:
        url = urlparse.urlparse(value)
    except Exception:
        raise click.BadParameter('Could not parse URL')

    ## Valdate required parts are available
    if all([url.scheme, url.netloc]):
        if url.path:
            return f'{url.scheme}://{url.netloc}{url.path}'
        else:
            return f'{url.scheme}://{url.netloc}'
    else:
        raise click.BadParameter('URL is not correctly formed')

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

# Get command line arguments/options
# Allow use of --help and -h for click
@click.command(context_settings = dict(help_option_names=['-h', '--help']))
@click.argument(
    'ip',
    nargs           = -1,
    required        = True,
    type            = IPParamType(),
)
@click.option(
    '-c', '--connections', 'connections',
    default         = 10,
    help            = 'Maximum number of HTTP connections to open to API',
    show_default    = True,
    type            = click.IntRange(1, 100, clamp = True),
)
@click.option(
    '-f', '--field', 'fields',
    help            = 'Field to add to output - specify once for each field',
    type            = click.STRING,
    required        = False,
    multiple        = True,
    autocompletion  = __fields_autocomplete,
)
@click.option(
    '-h2', '--http2', 'http2',
    default         = True,
    help            = 'Enable HTTP2 support for querying API',
    show_default    = True,
    type            = bool,
    is_flag         = True,
)
@click.option(
    '-k', '--key', 'key',
    help            = 'The optional API key for 2ip.me',
    type            = str,
    required        = False,
)
@click.option(
    '-kf', '--keyfile', 'keyfile',
    help            = 'The optional API key file for 2ip.me',
    type            = click.File(mode = 'r'),
    required        = False,
)
@click.option(
    '-o', '--output', 'output',
    default         = 'table',
    help            = 'The output format',
    show_default    = True,
    type            = click.Choice(['table','csv'], case_sensitive = False),
)
@click.option(
    '-s', '--strict', 'strict',
    default         = False,
    help            = 'Strict mode - any errors will return an exception',
    show_default    = True,
    type            = bool,
    is_flag         = True,
)
@click.option(
    '-t', '--type', 'provider',
    default         = 'geo',
    help            = 'The lookup provider/type (geo for geographic information or provider for provider information)',
    show_default    = True,
    type            = click.Choice(['geo','provider'], case_sensitive = False),
    is_eager        = True,
)
@click.option(
    '-u', '--url', 'url',
    default         = API,
    help            = 'The base API URL',
    show_default    = True,
    type            = click.STRING,
    callback        = __validate_url,
)
@click.option(
    '-v', '--verbose', 'verbosity',
    count           =   True,
    help            = 'Set output verbosity level - specify multiple times for further debugging',
)
@click.version_option()

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
        ## Strict mode
        strict: bool = False,
        ## Maximum HTTP connections
        connections: int = 10,
        ## Enable HTTP2
        http2: bool = True,
        ## Output fields
        fields: Optional[Tuple] = None,
        ## API URL
        url: str = API,
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

    ## Check if user defined fields
    if fields:

        ## Get list of fields available
        available_fields = __fields(provider = provider)

        ## Convert the fields into a list and remove duplicates
        fields = list(dict.fromkeys(fields))

        ## Make sure the selected list of fields is valid
        for field in fields:
            assert any(field in i for i in available_fields) == True

    ## Debugging
    log.info(f'TwoIP {provider} CLI lookup - Output format set to {output}')

    ## Remove any duplicate IP's and convert to list (from a tuple)
    ip: List[Union[IPv4Address, IPv6Address]] = list(dict.fromkeys(ip))

    ## Get the API key if specified
    if key or keyfile:
        key = __key(key = key, keyfile = keyfile)

    ## Make sure no more than 100 connections to API are used
    if connections < 1 or connections > 100:
        log.fatal(f'A minimum of 1 connection and a maximum of 100 connections must be used')

    ## Create twoip object
    twoip = TwoIP(
        key = key,
        strict = strict,
        connections = connections,
        http2 = http2,
        api = url,
    )

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
        print(results.to_table(fields))
    elif output == 'csv':
        print(results.to_csv(fields))
    else:
        log.fatal(f'Output type {output} has not been defined')

# Allow using env vars for options
if __name__ == '__main__':
    cli(auto_envvar_prefix = '2IP')