# -*- coding: utf-8 -*-

"""
2IP API Client

Store the lookup results of a provider lookup
"""

from ipaddress import (
    ip_network,
    IPv4Address,
    IPv6Address,
    IPv4Network,
    IPv6Network,
)
from urllib.parse import urlparse, ParseResult

from dataclassy import dataclass

from twoip.dataclasses._common import Base, BaseResults


@dataclass(slots=True)
class ProviderResult(Base):
    """
    Define and store the geographic lookup result for a single IP address
    """

    # The IP address represented as a string from the Geo lookup
    ip: str

    # The route of the IP address represented as a string from the Geo lookup
    route: str

    # The route mask of the IP address represented as an integer from the Geo lookup
    mask: int | None = None

    # The name of the route object that contains the prefix in English
    name_ripe: str | None = None

    # The name of the route object that contains the prefix in Russian
    name_rus: str | None = None

    # The website that owns the route object that contains the prefix as a string
    site: str | None = None

    # The autonomous system that advertises the route represented as an integer
    asn: int | None = None

    # The website that owns the route object that contains the prefix as a parsed URL object
    url: ParseResult | None = None

    # The IP address represented as an IP address object
    ipaddress: IPv4Address | IPv6Address

    # The prefix containing the IP address as an IP network object
    prefix: IPv4Network | IPv6Network | None = None

    # The IP range start
    ip_range_start: IPv4Address | IPv6Address | None = None

    # The IP range end
    ip_range_end: IPv4Address | IPv6Address | None = None

    def __post_init__(self):
        """
        On post init clean data up
        """

        # Create an IP network object if possible from the route/mask
        if self.route and self.mask:
            self.prefix = ip_network(f"{self.route}/{self.mask}")

        # Convert the route mask to an integer
        if self.mask:
            self.mask = int(self.mask)

        # Convert the AS number into an integer
        if self.asn:
            self.asn = int(self.asn)

        # If no site, set to none
        if not self.site:
            self.site = None
        else:
            # Convert the site to a URL object
            try:
                self.url = urlparse(self.site)
            except Exception:  # pylint: disable=broad-except
                self.url = None

        # If IP range start set, convert to an IP address from integer
        if self.ip_range_start:
            self.ip_range_start = IPv4Address(int(self.ip_range_start))

        # If IP range end set, convert to an IP address from integer
        if self.ip_range_end:
            self.ip_range_end = IPv4Address(int(self.ip_range_end))

        # If no name defined in English, set to none
        if not self.name_ripe:
            self.name_ripe = None

        # If no name defined in Russian, set to none
        if not self.name_rus:
            self.name_rus = None


@dataclass(slots=True)
class ProviderResults(BaseResults):
    """
    Define and store the results from multiple provider lookups
    """

    results: list[ProviderResult]

    # Set the default list of table headers to output for tables
    _table_headers: list[str] = [
        "IP Address",
        "Provider",
        "ASN",
        "Prefix",
        "Website",
    ]

    def to_table(
        self, tablefmt: str = "outline", sort: str | int = "IP Address"
    ) -> str:
        """
        Return the results as a formatted table
        """

        # Create dict to store the data for table
        data: list[list[str]] = []

        # Loop over each result
        for result in self.results:
            # Append the individual result data to table data
            data.append(
                [
                    f"{result.ipaddress}",
                    result.name_ripe if result.name_ripe else "-",
                    f"{result.asn}" if result.asn else "-",
                    f"{result.prefix}" if result.prefix else "-",
                    result.site if result.site else "-",
                ]
            )

        # Return the generated table
        return self._generate_table(data=data, tablefmt=tablefmt, sort=sort)
