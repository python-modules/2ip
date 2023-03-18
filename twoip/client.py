# -*- coding: utf-8 -*-

"""
2IP API Client

Make requests to the 2IP API and parse the responses into the relevant dataclasses.
"""

from typing import Optional
from sys import stderr

from loguru import logger
from loguru._defaults import (
    LOGURU_DEBUG_NO,
    LOGURU_ERROR_NO,
    LOGURU_INFO_NO,
    LOGURU_SUCCESS_NO,
    LOGURU_TRACE_NO,
    LOGURU_WARNING_NO,
)

from twoip.http import HTTP
from twoip.methods import Provider
from twoip.dataclasses.settings import Settings


class Client:
    """
    2IP API Client class
    """

    def __init__(
        self,
        http2: bool = True,
        key: Optional[str] = None,
        threads: int = 10,
        timeout: int = 30,
        url: Optional[str] = None,
        user_agent: Optional[str] = None,
        verbosity: int = 0,
    ):  # pylint: disable=too-many-arguments
        """
        Set up the new API client
        """
        # Configure logging
        level = self._setup_log(verbosity=verbosity)

        # Load settings defined in CLI args/env vars
        logger.debug("Creating new 2IP API client")
        logger.trace("Loading settings")
        self.settings = Settings(
            http2=http2,
            key=key,
            threads=threads,
            timeout=timeout,
            url=url,  # type: ignore
            user_agent=user_agent,  # type: ignore
            verbosity=level,
        )
        logger.trace(f"Loaded settings:\n{self.settings.pretty()}")

        # Create the HTTP client that will be used to send requests
        self.http = HTTP(settings=self.settings)

    @staticmethod
    def _setup_log(verbosity: int) -> int:
        """
        Configure the logging level based on the verbosity level
        """
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
            # Get the log level that should be used. If the log level is out of range (ie. above 5) the level will
            # default to LOGURU_TRACE_NO
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

        # Return the actual log level that was set
        return level

    def provider(self) -> object:
        """
        Return the 2IP Provider IP API client
        """
        return Provider(http=self.http, threads=self.settings.threads)
