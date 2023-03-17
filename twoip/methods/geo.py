# -*- coding: utf-8 -*-

"""
2IP API Client

Geographic Lookup API Client
"""

from loguru import logger

from twoip.http import HTTP


class Geo:
    """
    2IP API client - Geographic Lookup Client
    """

    def __init__(self, http: HTTP):
        """
        Set up the Geo API client
        """
        # Define HTTP client
        self.http = http

        # Log setup of Geo API client
        logger.trace("Geo IP client object created")
