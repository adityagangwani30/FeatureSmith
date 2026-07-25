"""Core primitives for Featuresmith."""

from featuresmith.core.dataset import Dataset
from featuresmith.core.exceptions import ConnectorError
from featuresmith.core.schema import ColumnSchema, DatasetSchema

__all__ = ["ColumnSchema", "ConnectorError", "Dataset", "DatasetSchema"]
