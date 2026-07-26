"""In-memory pandas and Polars dataframe connector."""

from __future__ import annotations

import pandas as pd
import polars as pl

from featuresmith.connectors.base import BaseConnector
from featuresmith.core.dataset import Dataset
from featuresmith.core.exceptions import UnsupportedFormatError


class DataFrameConnector(BaseConnector):
    """Wrap in-memory pandas or Polars dataframes without copying them."""

    def can_load(self, source: object) -> bool:
        """Return whether the source is a supported dataframe instance."""
        return isinstance(source, (pd.DataFrame, pl.DataFrame))

    def validate(self, source: object) -> None:
        """Validate that the source is a pandas or Polars dataframe."""
        if not self.can_load(source):
            raise UnsupportedFormatError("Expected a pandas or Polars DataFrame.")

    def load(self, source: object) -> Dataset:
        """Wrap an in-memory dataframe in the normalized dataset contract."""
        self.validate(source)
        if isinstance(source, pd.DataFrame):
            return Dataset.from_dataframe(
                source,
                backend="pandas",
                metadata={"format": "dataframe"},
            )
        if isinstance(source, pl.DataFrame):
            return Dataset.from_dataframe(
                source,
                backend="polars",
                metadata={"format": "dataframe"},
            )
        raise UnsupportedFormatError("Expected a pandas or Polars DataFrame.")
