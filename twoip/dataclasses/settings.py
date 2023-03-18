# -*- coding: utf-8 -*-

"""
2IP API Client

Store run time configuration related to the API client.
"""

from pprint import pformat

from pydantic import (  # pylint: disable=no-name-in-module
    HttpUrl,
    Field,
    root_validator,
)
from pydantic.dataclasses import dataclass

from twoip.__version__ import __version__
from twoip.constants.api import APISettings


@dataclass
class Settings:
    """
    Define and store the run time arguments for the API client
    """

    url: HttpUrl = Field(
        title="API Base URL",
        description="The base API URL to use when making requests to the 2IP API",
        env="2IP_URL",
    )

    threads: int = Field(
        title="Threads",
        description="The number of threads to use when making HTTP requests 2IP API",
        env="2IP_THREADS",
        ge=1,
        le=25,
    )

    http2: bool = Field(
        title="HTTP/2",
        description="Enable HTTP/2 support for requests to the 2IP API",
        env="2IP_HTTP2",
    )

    timeout: int = Field(
        title="Timeout",
        description="The time out in seconds for requests to the 2IP API",
        env="2IP_TIMEOUT",
        ge=1,
        le=120,
    )

    verbosity: int = Field(
        title="Verbosity",
        description="The logging verbosity/level",
        env="2IP_VERBOSITY",
        ge=1,
        le=120,
    )

    user_agent: str = Field(
        title="User Agent",
        description="The user agent that will be sent to the 2IP API when making requests",
    )

    key: str | None = Field(
        title="API Key",
        description="The API key used to authenticate with the 2IP API",
        default=None,
        env="2IP_KEY",
    )

    @root_validator(pre=True)
    def user_agent_set(cls, values: dict) -> dict:  # pylint: disable=no-self-argument
        """
        Set default user agent for HTTP requests if not defined
        """
        # Check if user agent defined
        if values["user_agent"] is None:
            # User agent not defined; set default
            values["user_agent"] = f"2IP Python API Client v{__version__}"

        # Return the correctly set values
        return values

    @root_validator(pre=True)
    def url_set(cls, values: dict) -> dict:  # pylint: disable=no-self-argument
        """
        Set the default API base URL if not defined
        """
        # Check if API URL defined
        if values["url"] is None:
            # API URL not defined; set default
            values["url"] = APISettings.API_URL.value

        # Return the correctly set values
        return values

    def pretty(self) -> str:
        """
        Return a pretty printed version of the settings
        """
        return pformat(self)
