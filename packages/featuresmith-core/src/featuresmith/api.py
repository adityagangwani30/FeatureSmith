"""Public SDK entry module for Featuresmith."""

from __future__ import annotations

from featuresmith.connectors.registry import default_registry
from featuresmith.core.dataset import Dataset


def load(source: object) -> Dataset:
    """Load a supported tabular source into a normalized dataset.

    Args:
        source: A local CSV, Excel, or Parquet path, or an in-memory pandas or
            Polars dataframe.

    Returns:
        A normalized dataset suitable for later pipeline stages.

    Raises:
        ConnectorError: If the source is missing, unsupported, or unreadable.
    """
    return default_registry().load(source)
