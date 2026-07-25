"""Public SDK entry module for Featuresmith."""

from __future__ import annotations

from featuresmith.connectors.registry import default_registry
from featuresmith.core.dataset import Dataset
from featuresmith.core.profile_result import ProfileResult
from featuresmith.profiling import profile_dataset


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


def profile(source: object) -> ProfileResult:
    """Profile a supported tabular source or Dataset and return statistical summaries.

    Args:
        source: A Dataset object, a local file path (CSV, Excel, Parquet),
            or an in-memory pandas or Polars dataframe.

    Returns:
        A strongly-typed ProfileResult containing detailed summaries and stats.

    Raises:
        ConnectorError: If the source is a file path/dataframe that fails to load.
    """
    if isinstance(source, Dataset):
        dataset = source
    else:
        dataset = load(source)
    return profile_dataset(dataset)
