# -*- coding: utf-8 -*-

"""
2IP API Client

Exceptions for parsing responses from the API
"""

from typing import Optional


class _APIException(Exception):
    """
    Base API exception class
    """

    def __init__(self, response: Optional[dict] = None):
        """
        Exception init
        """
        # Store the response if defined
        if response:
            self.response = response


class ResponseParseError(_APIException):
    """
    Exception raised when the API response could not be parsed into an object
    """

    def __str__(self):
        return "The API response could not be parsed into an object successfully."
