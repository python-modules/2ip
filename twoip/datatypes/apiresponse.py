# -*- coding: utf-8 -*-

from dataclasses import dataclass, field, InitVar
from datetime import timedelta
from httpx import Response, Cookies, Headers
from ipaddress import IPv4Address, IPv6Address
from json.decoder import JSONDecodeError
from typing import Union, List, Dict, Optional

@dataclass(frozen = False)
class APIResponse(object):
    """Dataclass used to store the results of an API lookup for further parsing
    """

    ## Assign the fields that should be passed to this dataclass
    ipaddress: Union[IPv4Address, IPv6Address] = field(
        compare = True,
        metadata = {
            'description'   : 'The IP address that was looked up represented as an ipaddress object',
        },
    )
    url: str = field(
        compare = False,
        metadata = {
            'title'         : 'URL',
            'description'   : 'The URL the request was made to',
        },
    )
    params: dict = field(
        compare = False,
        metadata = {
            'title'         : 'Params',
            'description'   : 'The request parameters',
        },
    )
    response: InitVar[Optional[Response]] = field(
        default = None,
        compare = False,
        metadata = {
            'description'   : 'The httpx response object',
        },
    )
    error: Optional[str] = field(
        default = None,
        compare = False,
        metadata = {
            'title'         : 'Error',
            'description'   : 'httpx error while making request',
        },
    )

    ## Assign all other fields which are generated after initialization
    ip: str = field(
        init = False,
        compare = False,
        metadata = {
            'title'         : 'IP Address',
            'description'   : 'The IP address that was looked up represented as a string',
        },
    )
    content: bytes = field(
        init = False,
        compare = False,
        metadata = {
            'title'         : 'Content',
            'description'   : 'The raw response content as bytes',
        },
    )
    cookies: Cookies = field(
        init = False,
        compare = False,
        metadata = {
            'title'         : 'Cookies',
            'description'   : 'Any cookies from the response',
        },
    )
    elapsed: timedelta = field(
        init = False,
        compare = False,
        metadata = {
            'title'         : 'Elapsed',
            'description'   : 'The amount of time elapsed for the request',
        },
    )
    headers: Headers = field(
        init = False,
        compare = False,
        metadata = {
            'title'         : 'headers',
            'description'   : 'The response headers',
        },
    )
    http_version: str = field(
        init = False,
        compare = False,
        metadata = {
            'title'         : 'HTTP Version',
            'description'   : 'The HTTP version used for the request',
        },
    )
    is_error: bool = field(
        init = False,
        compare = False,
        metadata = {
            'title'         : 'Error',
            'description'   : 'If the request returned an error',
        },
    )
    is_redirect: bool = field(
        init = False,
        compare = False,
        metadata = {
            'title'         : 'Redirect',
            'description'   : 'If the request resuled in a redirect',
        },
    )
    status_code: int = field(
        init = False,
        compare = False,
        metadata = {
            'title'         : 'HTTP code',
            'description'   : 'The HTTP code from the response',
        },
    )
    json: Union[dict, None] = field(
        init = False,
        compare = False,
        metadata = {
            'title'         : 'JSON',
            'description'   : 'The response parsed as JSON (into a dict)',
        },
    )
    text: str = field(
        init = False,
        compare = False,
        metadata = {
            'title'         : 'Text',
            'description'   : 'The response as text',
        },
    )

    def __post_init__(self, response: Union[Response, None]) -> object:
        """Break out the attributes from the response object
        """
        ## Set the IP
        self.ip = f'{self.ipaddress}'

        ## Make sure there is a response
        if response:

            ## Create list of attributes that can be handled without any special parsing/handling
            attributes: List[str] = ['content', 'cookies', 'elapsed', 'headers', 'http_version', 'is_error', 'is_redirect', 'status_code', 'text']

            ## Set the attributes from unparsed list
            self.__set_attributes_unparsed(attributes = attributes, response = response)

            ## Try and parse response as JSON if there is no error defined
            if not self.error:
                self.__parse_response_json(response = response)

    def __set_attributes_unparsed(self, attributes: List[str], response: Response) -> None:
        """Set attributes that do not require any special parsing

        If the attribute cannot be set it will be set to 'None'

        Arguments:
            attributes (List[str]): The list of attributes to set
            response (Response): The response object

        Raises:
            RunTimeError: Unhandled exception getting attribute
        """
        ## Loop over each attribute name
        for attribute in attributes:

            ## Try getting attribute, if it does not exist the value will be set to none
            try:
                value = getattr(response, attribute)
            except AttributeError:
                value = None
            except Exception as e:
                raise RuntimeError(f'Exception getting attribute "{attribute}" from API response object: {e}')

            ## Set the attribute
            setattr(self, attribute, value)

    def __parse_response_json(self, response: Response) -> None:
        """Attempt to parse response as JSON

        If the response cannot be parsed the error attribute will be set.

        Arguments:
            response (Response): The response object
        """
        ## Try and parse response as JSON
        try:
            self.json = response.json()
        except JSONDecodeError:
            self.json = None
            self.error = 'Could not parse API response as JSON'
        except Exception as e:
            self.json = None
            self.error = f'Exception while parsing response as JSON: {e}'