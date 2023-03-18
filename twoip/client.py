# -*- coding: utf-8 -*-

"""
2IP API Client

Make requests to the 2IP API and parse the responses into the relevant dataclasses.
"""

from typing import Optional

from loguru import logger

from twoip.http import HTTP
from twoip.methods import Provider
from twoip.dataclasses.settings import Settings


class Client:
    """
    2IP API Client class
    """

    def __init__(
        self,
        key: Optional[str] = None,
        url: Optional[str] = None,
        timeout: int = 30,
        user_agent: Optional[str] = None,
        http2: bool = True,
    ):  # pylint: disable=too-many-arguments
        """
        Set up the new API client
        """
        # Load settings defined in CLI args/env vars
        logger.debug("Creating new 2IP Reseller API client")
        logger.trace("Loading settings")
        self.settings = Settings(
            key=key,
            url=url,  # type: ignore
            timeout=timeout,
            user_agent=user_agent,  # type: ignore
            http2=http2,
        )
        logger.trace(f"Loaded settings:\n{self.settings.pretty()}")

        # Create the HTTP client that will be used to send requests
        self.http = HTTP(settings=self.settings)

    def provider(self) -> object:
        """
        Return the 2IP Geo IP API client
        """
        return Provider(http=self.http)
