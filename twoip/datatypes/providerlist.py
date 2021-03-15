# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import List, Literal

# Requirements for generating output (CSV or table)
from ipaddress import IPv4Address

from .baselist import BaseList
from .providerresult import ProviderResult

@dataclass(frozen = False)
class ProviderList(BaseList):
    """Dataclass to store all results from multiple provider lookups

    Examples:
    """
    ## Assign slots
    __slots__ = [ 'results' ]

    ## Set results type
    results: List[ProviderResult]

    def __str__(self) -> str:
        """Return a table of results

        This is the same as calling the to_table() function on the results.

        Returns:
            str: The results table
        """
        return self.to_table()

    @staticmethod
    def _sample() -> ProviderResult:
        """Generate a sample ProviderResult object

        This is used to retrieve table headers and other information.

        Returns:
            ProviderResult: The sample ProviderResult object
        """
        return ProviderResult(ipaddress = IPv4Address('192.0.2.0'))

    @staticmethod
    def _default_fields(format: Literal['table','csv']) -> List[str]:
        """Return a list of default fields to retrieve when generating output

        The 'ip' field is always excluded as that will be printed by default

        Returns:
            List[str]: The list of default fields to output
        """
        if format == 'table':
            return ['success_icon', 'autonomous_system', 'name', 'website']
        else:
            return ['success', 'autonomous_system', 'name', 'website']