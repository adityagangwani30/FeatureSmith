"""Typed schemas shared by core pipeline stages."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ColumnSchema:
    """Describe one column in a normalized dataset.

    Attributes:
        name: The column name as exposed by the dataframe backend.
        dtype: The backend's stable string representation of the column dtype.
    """

    name: str
    dtype: str


@dataclass(frozen=True, slots=True)
class DatasetSchema:
    """Describe the columns available in a normalized dataset.

    Attributes:
        columns: Ordered column descriptors from the source dataframe.
    """

    columns: tuple[ColumnSchema, ...]

    @property
    def names(self) -> tuple[str, ...]:
        """Return the ordered column names."""
        return tuple(column.name for column in self.columns)
