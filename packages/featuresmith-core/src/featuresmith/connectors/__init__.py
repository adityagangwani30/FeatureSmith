"""Connector package for Featuresmith."""

from featuresmith.connectors.base import BaseConnector
from featuresmith.connectors.csv_connector import CsvConnector
from featuresmith.connectors.dataframe_connector import DataFrameConnector
from featuresmith.connectors.excel_connector import ExcelConnector
from featuresmith.connectors.parquet_connector import ParquetConnector
from featuresmith.connectors.registry import ConnectorRegistry, default_registry

__all__ = [
    "BaseConnector",
    "ConnectorRegistry",
    "CsvConnector",
    "DataFrameConnector",
    "ExcelConnector",
    "ParquetConnector",
    "default_registry",
]
