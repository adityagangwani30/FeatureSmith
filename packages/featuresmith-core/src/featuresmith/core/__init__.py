"""Core primitives for Featuresmith."""

from featuresmith.core.dataset import Dataset
from featuresmith.core.exceptions import (
    ConnectorError,
    SourceNotFoundError,
    SourceParseError,
    UnsupportedFormatError,
)
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
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.core.rule_result import RuleResult
from featuresmith.core.schema import ColumnSchema, DatasetSchema

__all__ = [
    "ColumnSchema",
    "ConnectorError",
    "SourceNotFoundError",
    "SourceParseError",
    "UnsupportedFormatError",
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
    "RuleFinding",
    "RuleResult",
]
