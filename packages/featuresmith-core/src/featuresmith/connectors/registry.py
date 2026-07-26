"""Static connector registration and source dispatch for Sprint 2."""

from __future__ import annotations

from collections.abc import Iterable

from featuresmith.connectors.base import BaseConnector
from featuresmith.connectors.csv_connector import CsvConnector
from featuresmith.connectors.dataframe_connector import DataFrameConnector
from featuresmith.connectors.excel_connector import ExcelConnector
from featuresmith.connectors.parquet_connector import ParquetConnector
from featuresmith.core.dataset import Dataset
from featuresmith.core.exceptions import UnsupportedFormatError


class ConnectorRegistry:
    """Select a registered connector for a supported input source.

    Registration is intentionally explicit during Sprint 2. It establishes the
    extension boundary without entry-point discovery or dynamic loading.
    """

    def __init__(self, connectors: Iterable[BaseConnector] = ()) -> None:
        """Create a registry with optional initial connector instances."""
        self._connectors = list(connectors)

    def register(self, connector: BaseConnector) -> None:
        """Register a connector instance for subsequent source dispatch."""
        self._connectors.append(connector)

    def load(self, source: object) -> Dataset:
        """Load a source with the first registered connector that supports it.

        Raises:
            ConnectorError: If no registered connector supports the source.
        """
        for connector in self._connectors:
            if connector.can_load(source):
                return connector.load(source)
        raise UnsupportedFormatError(
            "Unsupported source. Use a CSV, Excel, Parquet, pandas DataFrame, "
            "or Polars DataFrame."
        )


def default_registry() -> ConnectorRegistry:
    """Return the built-in Sprint 2 connector registry."""
    return ConnectorRegistry(
        (
            DataFrameConnector(),
            CsvConnector(),
            ExcelConnector(),
            ParquetConnector(),
        )
    )
