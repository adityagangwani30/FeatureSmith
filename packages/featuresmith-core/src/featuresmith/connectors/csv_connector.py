"""CSV connector backed by Polars."""

from __future__ import annotations

from pathlib import Path

import polars as pl

from featuresmith.connectors._paths import validate_file_source
from featuresmith.connectors.base import BaseConnector
from featuresmith.core.dataset import Dataset
from featuresmith.core.exceptions import SourceParseError


class CsvConnector(BaseConnector):
    """Load local CSV files into Polars-backed datasets."""

    _SUFFIXES = (".csv",)

    def can_load(self, source: object) -> bool:
        """Return whether the source is a CSV path."""
        return (
            isinstance(source, (str, Path))
            and Path(source).suffix.lower() in self._SUFFIXES
        )

    def validate(self, source: object) -> None:
        """Validate that the CSV source exists and is a regular file."""
        validate_file_source(source, self._SUFFIXES)

    def load(self, source: object) -> Dataset:
        """Load a CSV file as a normalized Polars dataset."""
        path = validate_file_source(source, self._SUFFIXES)
        try:
            dataframe = pl.read_csv(path)
        except (OSError, pl.exceptions.PolarsError) as error:
            raise SourceParseError(f"Could not read CSV file '{path}'.") from error
        return Dataset.from_dataframe(
            dataframe,
            backend="polars",
            source=str(path),
            file_size=path.stat().st_size,
            metadata={"format": "csv"},
        )
