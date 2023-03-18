# -*- coding: utf-8 -*-

"""
2IP API Client

Common dataclasses
"""

from json import dumps

from dataclassy import dataclass, as_dict
from tabulate import tabulate


@dataclass(slots=True)
class Base:
    """
    Base dataclass for all methods
    """

    def to_json(self) -> str:
        """
        Return this object as JSON data
        """
        # Return the JSON data
        return dumps(as_dict(self), indent=4)


@dataclass(slots=True)
class BaseResults(Base):
    """
    Base dataclass for all storing multiple results from lookups
    """

    # The table headers to use when generating a table
    _table_headers: list[str]

    def _generate_table(
        self, data: list[list], tablefmt: str, sort: str | int = 1
    ) -> str:
        """
        Generate a table from the supplied data formatting it as requested
        """

        # Ensure that the sort column is in the table headers
        sort_by: str
        if isinstance(sort, str) and sort in self._table_headers:
            sort_by = sort

        else:
            # Check if the sort column is an integer
            if isinstance(sort, int):
                # Set sort index + 1 to account for the index starting at 0
                sort += 1

                # Check if the sort column is a valid index
                if sort < 0 or sort > len(self._table_headers):
                    # Invalid index; raise error
                    raise ValueError(f"Sort column index '{sort}' not in table headers")

                # Valid index; set the sort column to the header at the index
                sort_by = self._table_headers[sort]

            else:
                raise ValueError(
                    f"The sort index {sort} is not a valid sort key for the table. "
                    f"Valid options are: {' '.join(self._table_headers)}"
                )

        # Sort the table data
        data = sorted(data, key=lambda x: x[self._table_headers.index(sort_by)])

        # Return the generated table
        return tabulate(data, headers=self._table_headers, tablefmt=tablefmt)
