# -*- coding: utf-8 -*-

"""
2IP API Client

Exceptions for requests sent/received from the API
"""

from typing import Optional

from httpx import Response


class _APIException(Exception):
    """
    Base API exception class
    """

    def __init__(self, response: Optional[Response] = None):
        """
        Exception init
        """
        # Store the response if defined
        if response:
            self.response = response


class APIContentTypeError(_APIException):
    """
    Exception raised when the API content type does not match the expected type
    """

    def __str__(self):
        return "API response contained an unexpected content type."


class APIParserError(_APIException):
    """
    Exception raised when the API response cannot be parsed as JSON
    """

    def __str__(self):
        return "API response could not be parsed as JSON."


class APIResponseCodeError(_APIException):
    """
    Exception raised when the API response code is not 2xx
    """

    def __str__(self):
        return f"API response code was not 2xx: {self.response.status_code}"
