# -*- coding: utf-8 -*-

"""
2IP API Client

Geographic Lookup API Client
"""

from ipaddress import ip_address, IPv4Address, IPv6Address
from functools import lru_cache
from pprint import pformat

from loguru import logger

from twoip.http import HTTP
from twoip.dataclasses.provider import ProviderResult, ProviderResults


class Provider:
    """
    2IP API client - Provider Lookup Client
    """

    def __init__(self, http: HTTP):
        """
        Set up the Provider API client
        """
        # Define HTTP client
        self.http = http

        # Set the API endpoint
        self._endpoint = "/provider.json"

        # Log setup of Provider API client
        logger.trace("Provider IP client object created")

    @staticmethod
    def __to_ip_list(
        addresses: list[str | IPv4Address | IPv6Address],
    ) -> list[IPv4Address | IPv6Address]:
        """
        Convert the supplied list of IP addresses into a list of IP address objects
        """
        logger.debug("Converting list of IP addresses to list of IP address objects")
        logger.trace(f"Addresses to convert:\n{pformat(addresses)}")

        # Create list of address objects to return
        addresses_list: list[IPv4Address | IPv6Address] = []

        # Loop over each IP address
        for address in addresses:
            # Check if address is already an IPv4Address or IPv6Address object
            logger.trace(
                f"Checking if IP address is already an IP address object: {address}"
            )
            if isinstance(address, (IPv4Address, IPv6Address)):
                # Add address to list
                logger.trace(
                    f"Address is already an IP address object, adding to list: {address}"
                )
                addresses_list.append(address)
            else:
                # Convert to IP address object
                logger.trace(f"Creating IP address object for address: {address}")
                try:
                    address_obj: IPv4Address | IPv6Address = ip_address(address)
                except ValueError as exc:
                    logger.critical(
                        f"Could not create IP address object from the IP address: {address}"
                    )
                    raise ValueError(f"Invalid IP address '{address}'") from exc

                # Append to list
                addresses_list.append(address_obj)

        # Remove any duplicate objects from the IP list
        logger.debug("IP address list created; deduplicating list")
        addresses_list = list(set(addresses_list))

        # Return the built list
        logger.debug("Returning list of IP address objects")
        logger.trace(f"IP address list:\n{pformat(addresses_list)}")
        return addresses_list

    @lru_cache(maxsize=25000)
    def __lookup(self, address: IPv4Address | IPv6Address) -> ProviderResult:
        """
        Send the lookup to the API and parse response into a ProviderResult object
        """
        logger.debug(f"Sending lookup to API for IP address: {address}")

        # Set the IP parameter to send to API
        params = {"ip": f"{address}"}

        # Make the API request
        response = self.http.get(path=self._endpoint, params=params)

        # Rename the "as" attribute to "asn" if defined
        if "as" in response:
            response["asn"] = response.pop("as")

        # Parse the response and return
        logger.trace("Parsing response into a ProviderResult object")
        return ProviderResult(ipaddress=address, **response)

    def lookup(
        self,
        addresses: str
        | IPv4Address
        | IPv6Address
        | list[str | IPv4Address | IPv6Address],
    ) -> ProviderResults:
        """
        Retrieve the geographic provider information for one or IP addresses
        """
        logger.info("Setting up a new provider lookup")

        # Ensure the addresses are a list
        if isinstance(addresses, (str, IPv4Address, IPv6Address)):
            logger.debug(f"Converting single IP address to list: {addresses}")
            addresses = [addresses]

        # Convert the addresses to a list of IP address objects
        ips = self.__to_ip_list(addresses)

        # Create list to store the results
        results: list[ProviderResult] = []

        # Loop through each IP address and perform a lookup
        for address in ips:
            # Send the lookup to the API (if not cached) and add to results
            results.append(self.__lookup(address))

        # Create a ProviderResults object to return
        provider_results = ProviderResults(results=results)

        # Return the lookup results
        logger.info("Provider lookup finished")
        return provider_results
