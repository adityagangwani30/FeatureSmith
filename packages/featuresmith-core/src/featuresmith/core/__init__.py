"""Core primitives for Featuresmith."""

from featuresmith.core.dataset import Dataset
from featuresmith.core.exceptions import ConnectorError
from featuresmith.core.profile_result import (
    CategoricalProfile,
    ColumnProfile,
    CorrelationSummary,
    DatasetMetadata,
    DatasetSummary,
    DatetimeProfile,
    DuplicateSummary,
    ExecutionMetadata,
    MissingValueSummary,
    NumericProfile,
    ProfileResult,
    TextProfile,
)
from featuresmith.core.schema import ColumnSchema, DatasetSchema

__all__ = [
    "ColumnSchema",
    "ConnectorError",
    "Dataset",
    "DatasetSchema",
    "ColumnProfile",
    "CategoricalProfile",
    "CorrelationSummary",
    "DatasetMetadata",
    "DatasetSummary",
    "DatetimeProfile",
    "DuplicateSummary",
    "ExecutionMetadata",
    "MissingValueSummary",
    "NumericProfile",
    "ProfileResult",
    "TextProfile",
]
