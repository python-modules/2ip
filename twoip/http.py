# -*- coding: utf-8 -*-

"""
2IP API Client

This module handles making the HTTP requests to the 2IP API.
"""

from pprint import pformat

import httpx
from loguru import logger

# Import exceptions that may be raised
from twoip.exceptions.api import (
    APIContentTypeError,
    APIResponseCodeError,
    APIParserError,
    APIQuotaExceeded,
)
from twoip.dataclasses.settings import Settings


class HTTP:
    """
    HTTP API class for handling requests to the 2IP API
    """

    def __init__(self, settings: Settings):
        """
        Set up the HTTP class.

        Args:
            settings (Settings): The settings object to use for the HTTP class
        """
        # Define settings
        self.settings = settings

        # Log setup of HTTP class
        logger.debug("New HTTP class initialized")
        logger.trace("HTTP client configuration:")
        logger.trace(f"  - API URL: {self.settings.url}")
        logger.trace(f"  - API Key: {self.settings.key}")
        logger.trace(f"  - HTTP/2: {self.settings.http2}")
        logger.trace(f"  - Timeout: {self.settings.timeout}")
        logger.trace(f"  - User Agent: {self.settings.user_agent}")

        # Create default headers that will be used for all requests
        self._headers: dict[str, str] = {
            "Accept": "application/json",
            "User-Agent": settings.user_agent,
        }

        # Set API key parameter if defined to use for all requests
        self._params: dict[str, str] | None = None
        if self.settings.key:
            self._params = {
                "key": self.settings.key,
            }

        # Create the httpx client object
        self.client = httpx.Client(
            headers=self._headers,
            params=self._params,
            http2=self.settings.http2,
            base_url=self.settings.url,
            timeout=self.settings.timeout,
        )
        logger.trace("httpx HTTP Client object created")

    @staticmethod
    def __check_code(response: httpx.Response) -> None:
        """
        Check the response code from the API and raise an exception if the code is not 200
        """
        logger.debug("Checking HTTP response code")

        # Check if rate limit exceeded
        if response.status_code == 429:
            logger.critical("HTTP response code indicates rate limit exceeded")
            raise APIQuotaExceeded(response=response)

        # Raise exception if response code is invalid
        try:
            response.raise_for_status()
            logger.debug(f"HTTP response code {response.status_code} indicates success")
        except httpx.HTTPStatusError as exc:
            raise APIResponseCodeError(response=response) from exc

    @staticmethod
    def __is_json(response: httpx.Response) -> bool:
        """
        Check if the supplied API response contains JSON data
        """
        # Get the headers from response and convert all to lower case
        headers = dict(
            (k.lower(), v.lower()) for k, v in dict(response.headers).items()
        )

        # Check if content-type header is present
        logger.debug(
            "Checking for 'application/json' in content type header from response"
        )
        if headers["content-type"]:
            logger.trace(f"Content type header: {headers['content-type']}")
            # Check if content-type header is JSON
            if "application/json" in headers["content-type"]:
                logger.debug("Found 'application/json' in content type header")
                return True

        # Couldn't get content-type header or it wasn't JSON
        logger.debug(
            "Could not find 'application/json' in content type header; assuming response is not JSON"
        )
        return False

    def __get(self, path: str, params: dict | None) -> dict:
        """
        Send a GET request to the API and deserialize the result from JSON
        """
        # Log the start of the request
        logger.debug(f"Sending HTTP GET request to {path}")
        if params:
            logger.trace(f"Request parameters: {pformat(params)}")

        # Send the request
        response = self.client.get(
            path,
            params=params,
        )

        # Check the response code
        self.__check_code(response)

        # Make sure response is JSON
        if not self.__is_json(response):
            raise APIContentTypeError(response=response)

        # Try to deserialize and return
        try:
            return response.json()
        except Exception as exc:
            raise APIParserError(response=response) from exc

    def get(self, path: str, params: dict | None = None) -> dict:
        """
        Send a GET request to the 2IP API, decode the response as JSON and return a dict of the result

        Args:
            path (str): The path to send the request to.
            params (dict, optional): The parameters to send with the request. Defaults to None.

        Returns:
            dict: The response data as a dict.
        """
        # Make the request
        response = self.__get(path=path, params=params)

        # Return the response
        logger.trace(f"Returning API response data:\n{pformat(response)}")
        return response
