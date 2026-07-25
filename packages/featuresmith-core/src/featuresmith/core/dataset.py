"""Normalized dataset abstraction passed between Featuresmith pipeline stages."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from featuresmith.core.schema import ColumnSchema, DatasetSchema


@dataclass(frozen=True, slots=True)
class Dataset:
    """A lightweight, normalized view of a loaded tabular dataset.

    The wrapper is shallowly immutable: its descriptive fields cannot be
    reassigned, while the underlying dataframe remains owned by its backend.
    Connectors construct this object; it deliberately contains no profiling or
    source-specific behavior.

    Attributes:
        dataframe: The loaded pandas or Polars dataframe.
        backend: The dataframe backend identifier, either ``"pandas"`` or
            ``"polars"``.
        schema: Ordered schema inferred from the dataframe.
        metadata: Read-only descriptive metadata supplied by the connector.
        row_count: Number of rows in the dataframe.
        column_count: Number of columns in the dataframe.
        dtypes: Read-only mapping from column name to dtype string.
        source: Original file path when loaded from a file, otherwise ``None``.
        file_size: File size in bytes when loaded from a file, otherwise
            ``None``.
    """

    dataframe: Any
    backend: str
    schema: DatasetSchema
    metadata: Mapping[str, object] = field(default_factory=dict)
    row_count: int = 0
    column_count: int = 0
    dtypes: Mapping[str, str] = field(default_factory=dict)
    source: str | None = None
    file_size: int | None = None

    def __post_init__(self) -> None:
        """Freeze mapping fields so dataset descriptors stay immutable."""
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
        object.__setattr__(self, "dtypes", MappingProxyType(dict(self.dtypes)))

    @classmethod
    def from_dataframe(
        cls,
        dataframe: Any,
        *,
        backend: str,
        source: str | None = None,
        file_size: int | None = None,
        metadata: Mapping[str, object] | None = None,
    ) -> Dataset:
        """Create a normalized dataset from a dataframe backend object.

        Args:
            dataframe: A pandas or Polars dataframe.
            backend: Identifier for the dataframe backend.
            source: Original local file path, if any.
            file_size: Source file size in bytes, if known.
            metadata: Connector-provided descriptive metadata.

        Returns:
            A normalized dataset with an inferred schema and dtype mapping.
        """
        columns = tuple(str(column) for column in dataframe.columns)
        dtype_values = tuple(str(dtype) for dtype in dataframe.dtypes)
        dtypes = dict(zip(columns, dtype_values, strict=True))
        schema = DatasetSchema(
            columns=tuple(
                ColumnSchema(name=name, dtype=dtype) for name, dtype in dtypes.items()
            )
        )
        return cls(
            dataframe=dataframe,
            backend=backend,
            schema=schema,
            metadata=metadata or {},
            row_count=len(dataframe),
            column_count=len(columns),
            dtypes=dtypes,
            source=source,
            file_size=file_size,
        )

    def preview(self, rows: int = 5) -> Any:
        """Return the first requested number of rows from the dataframe.

        Args:
            rows: Number of rows to return. Must be non-negative.

        Returns:
            A dataframe of the same backend containing the requested head rows.

        Raises:
            ValueError: If ``rows`` is negative.
        """
        if rows < 0:
            raise ValueError("Preview row count must be non-negative.")
        return self.dataframe.head(rows)
