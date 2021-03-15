# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List, Literal

# Requirements for generating output (CSV or table)
from ipaddress import IPv4Address

from .baselist import BaseList
from .georesult import GeoResult

@dataclass(frozen = False)
class GeoList(BaseList):
    """Dataclass to store all results from multiple geo lookups

    Examples:
    """
    ## Assign slots
    __slots__ = [ 'results' ]

    ## Set results type
    results: List[GeoResult]

    def __str__(self) -> str:
        """Return a table of results

        This is the same as calling the to_table() function on the results.

        Returns:
            str: The results table

        Examples:
        """
        return self.to_table()

    @staticmethod
    def _sample() -> GeoResult:
        """Generate a sample GeoResult object

        This is used to retrieve table headers and other information.

        Returns:
            GeoResult: The sample GeoResult object
        """
        return GeoResult(ipaddress = IPv4Address('192.0.2.0'))

    @staticmethod
    def _default_fields(format: Literal['table','csv']) -> List[str]:
        """Return a list of default fields to retrieve when generating output

        The 'ip' field is always excluded as that will be printed by default

        Returns:
            List[str]: The list of default fields to output
        """
        if format == 'table':
            return ['success_icon', 'city', 'country']
        else:
            return ['success', 'city', 'country']