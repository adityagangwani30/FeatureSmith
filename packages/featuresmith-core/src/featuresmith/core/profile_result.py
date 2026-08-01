"""Canonical schema for profiling results."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class DatasetSummary:
    """High-level summary of the dataset.

    Attributes:
        row_count: Number of rows in the dataset.
        column_count: Number of columns in the dataset.
        size_in_bytes: Approximate size in bytes if known.
        missing_percentage: Overall percentage of missing cells.
        duplicate_percentage: Percentage of duplicate rows in the dataset.
        num_numeric_columns: Number of numeric columns.
        num_categorical_columns: Number of categorical columns.
        num_datetime_columns: Number of datetime columns.
        num_text_columns: Number of text columns.
        num_constant_columns: Number of constant columns.
        num_fully_empty_columns: Number of fully empty columns.
    """

    row_count: int
    column_count: int
    size_in_bytes: int | None
    missing_percentage: float
    duplicate_percentage: float
    num_numeric_columns: int
    num_categorical_columns: int
    num_datetime_columns: int
    num_text_columns: int
    num_constant_columns: int
    num_fully_empty_columns: int


@dataclass(frozen=True, slots=True)
class ColumnProfile:
    """General profile summary for a single column.

    Attributes:
        name: Column name.
        dtype: Native datatype string.
        logical_type: Inferred logical type ("numeric", "categorical", "datetime", "text").
        missing_count: Count of missing values in the column.
        missing_percentage: Percentage of missing values.
        is_constant: Whether the column is constant (contains 1 or fewer unique values).
        is_fully_empty: Whether the column is fully empty (all values are missing).
    """

    name: str
    dtype: str
    logical_type: str
    missing_count: int
    missing_percentage: float
    is_constant: bool
    is_fully_empty: bool


@dataclass(frozen=True, slots=True)
class NumericProfile:
    """Detailed profiling statistics for a numeric column.

    Attributes:
        column_name: Name of the column.
        count: Total non-missing count.
        missing_count: Total missing count.
        missing_percentage: Percentage of missing values.
        unique_count: Number of unique non-missing values.
        mean: Arithmetic mean.
        median: 50th percentile.
        mode: The most common value (first if multiple).
        minimum: Minimum value.
        maximum: Maximum value.
        range: Maximum - minimum.
        variance: Sample variance (ddof=1).
        std_dev: Sample standard deviation (ddof=1).
        q1: 25th percentile.
        q2: 50th percentile (median).
        q3: 75th percentile.
        iqr: Interquartile range (q3 - q1).
        sum: Sum of all values.
        zero_count: Number of zeros.
        negative_count: Number of negative values.
        positive_count: Number of positive values.
        skewness: Skewness of the distribution.
        kurtosis: Kurtosis of the distribution.
    """

    column_name: str
    count: int
    missing_count: int
    missing_percentage: float
    unique_count: int
    mean: float | None
    median: float | None
    mode: float | None
    minimum: float | None
    maximum: float | None
    range: float | None
    variance: float | None
    std_dev: float | None
    q1: float | None
    q2: float | None
    q3: float | None
    iqr: float | None
    sum: float | None
    zero_count: int
    negative_count: int
    positive_count: int
    skewness: float | None
    kurtosis: float | None


@dataclass(frozen=True, slots=True)
class CategoricalProfile:
    """Detailed profiling statistics for a categorical column.

    Attributes:
        column_name: Name of the column.
        cardinality: Number of unique non-missing categories.
        unique_count: Number of unique non-missing values.
        missing_count: Total missing count.
        frequency_table: Mapping of value string representation to count (capped to a maximum size, default 1000).
        top_values: List of (value, count) pairs for top frequent items.
        least_frequent_values: List of (value, count) pairs for least frequent items.
        most_common_category: Name of the most frequent category.
        entropy: Shannon entropy of categories (base 2).
    """

    column_name: str
    cardinality: int
    unique_count: int
    missing_count: int
    frequency_table: Mapping[str, int]
    top_values: Sequence[tuple[str, int]]
    least_frequent_values: Sequence[tuple[str, int]]
    most_common_category: str | None
    entropy: float | None

    def __post_init__(self) -> None:
        """Freeze mutable fields to improve immutability consistency."""
        from types import MappingProxyType

        object.__setattr__(
            self, "frequency_table", MappingProxyType(dict(self.frequency_table))
        )
        object.__setattr__(self, "top_values", tuple(self.top_values))
        object.__setattr__(
            self, "least_frequent_values", tuple(self.least_frequent_values)
        )


@dataclass(frozen=True, slots=True)
class DatetimeProfile:
    """Detailed profiling statistics for a datetime column.

    Attributes:
        column_name: Name of the column.
        minimum: Earliest timestamp string (ISO 8601).
        maximum: Latest timestamp string (ISO 8601).
        range_days: Range of timestamps in days.
        missing_count: Number of missing values.
        earliest_record: Same as minimum.
        latest_record: Same as maximum.
    """

    column_name: str
    minimum: str | None
    maximum: str | None
    range_days: float | None
    missing_count: int
    earliest_record: str | None
    latest_record: str | None


@dataclass(frozen=True, slots=True)
class TextProfile:
    """Detailed profiling statistics for a text column.

    Attributes:
        column_name: Name of the column.
        avg_length: Average character length.
        min_length: Minimum character length.
        max_length: Maximum character length.
        empty_strings: Number of empty string values ("").
        whitespace_only: Number of strings containing only whitespace.
        char_count: Total character count across all strings.
        word_count: Total word count across all strings.
    """

    column_name: str
    avg_length: float | None
    min_length: int | None
    max_length: int | None
    empty_strings: int
    whitespace_only: int
    char_count: int
    word_count: int


@dataclass(frozen=True, slots=True)
class MissingValueSummary:
    """Summary of missingness across the dataset.

    Attributes:
        column_missing_counts: Mapping of column name to missing count.
        column_missing_percentages: Mapping of column name to missing percentage.
        total_missing: Total count of missing cells.
        dataset_missing_percentage: Overall dataset-wide missing cell percentage.
    """

    column_missing_counts: Mapping[str, int]
    column_missing_percentages: Mapping[str, float]
    total_missing: int
    dataset_missing_percentage: float

    def __post_init__(self) -> None:
        """Freeze mutable fields to improve immutability consistency."""
        from types import MappingProxyType

        object.__setattr__(
            self,
            "column_missing_counts",
            MappingProxyType(dict(self.column_missing_counts)),
        )
        object.__setattr__(
            self,
            "column_missing_percentages",
            MappingProxyType(dict(self.column_missing_percentages)),
        )


@dataclass(frozen=True, slots=True)
class DuplicateSummary:
    """Summary of duplicate records and redundant columns.

    Attributes:
        duplicate_rows_count: Number of duplicate rows.
        duplicate_percentage: Percentage of duplicate rows.
        constant_columns: List of constant column names.
        fully_empty_columns: List of fully empty column names.
    """

    duplicate_rows_count: int
    duplicate_percentage: float
    constant_columns: Sequence[str]
    fully_empty_columns: Sequence[str]

    def __post_init__(self) -> None:
        """Freeze mutable fields to improve immutability consistency."""
        object.__setattr__(self, "constant_columns", tuple(self.constant_columns))
        object.__setattr__(self, "fully_empty_columns", tuple(self.fully_empty_columns))


@dataclass(frozen=True, slots=True)
class CorrelationSummary:
    """Summary of pairwise column correlations.

    Attributes:
        pearson: Mapping of colA -> colB -> Pearson correlation value.
        spearman: Reserved for Spearman correlations.
        kendall: Reserved for Kendall correlations.
    """

    pearson: Mapping[str, Mapping[str, float | None]]
    spearman: Mapping[str, Mapping[str, float | None]] = field(default_factory=dict)
    kendall: Mapping[str, Mapping[str, float | None]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze mutable fields to improve immutability consistency."""
        from types import MappingProxyType

        pearson_frozen = {k: MappingProxyType(dict(v)) for k, v in self.pearson.items()}
        object.__setattr__(self, "pearson", MappingProxyType(pearson_frozen))

        spearman_frozen = {
            k: MappingProxyType(dict(v)) for k, v in self.spearman.items()
        }
        object.__setattr__(self, "spearman", MappingProxyType(spearman_frozen))

        kendall_frozen = {k: MappingProxyType(dict(v)) for k, v in self.kendall.items()}
        object.__setattr__(self, "kendall", MappingProxyType(kendall_frozen))


@dataclass(frozen=True, slots=True)
class DatasetMetadata:
    """Descriptive metadata from the data source and connector.

    Attributes:
        source: Source file path or identifier.
        file_size: Size in bytes if applicable.
        backend: DataFrame backend ("polars" or "pandas").
        custom_metadata: Optional dictionary of extra connector metadata.
    """

    source: str | None
    file_size: int | None
    backend: str
    custom_metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze mutable fields to improve immutability consistency."""
        from types import MappingProxyType

        object.__setattr__(
            self, "custom_metadata", MappingProxyType(dict(self.custom_metadata))
        )


@dataclass(frozen=True, slots=True)
class ExecutionMetadata:
    """Metadata about the profiling run itself.

    Attributes:
        start_time: ISO 8601 timestamp when profiling started.
        duration_seconds: Duration of the profiling run.
        featuresmith_version: Version of Featuresmith used.
    """

    start_time: str
    duration_seconds: float
    featuresmith_version: str


@dataclass(frozen=True, slots=True)
class ProfileResult:
    """The canonical, strongly-typed output of the profiling engine.

    Attributes:
        dataset_summary: High-level dataset summary.
        column_profiles: Individual column overview profiles.
        numeric_profiles: Numeric profiling details.
        categorical_profiles: Categorical profiling details.
        datetime_profiles: Datetime profiling details.
        text_profiles: Text profiling details.
        missing_value_summary: Missing value summary.
        duplicate_summary: Duplicate summary.
        correlation_summary: Correlation matrix.
        dataset_metadata: Source metadata.
        execution_metadata: Run execution metadata.
    """

    dataset_summary: DatasetSummary
    column_profiles: Mapping[str, ColumnProfile]
    numeric_profiles: Mapping[str, NumericProfile]
    categorical_profiles: Mapping[str, CategoricalProfile]
    datetime_profiles: Mapping[str, DatetimeProfile]
    text_profiles: Mapping[str, TextProfile]
    missing_value_summary: MissingValueSummary
    duplicate_summary: DuplicateSummary
    correlation_summary: CorrelationSummary
    dataset_metadata: DatasetMetadata
    execution_metadata: ExecutionMetadata

    def __post_init__(self) -> None:
        """Freeze mutable fields to improve immutability consistency."""
        from types import MappingProxyType

        object.__setattr__(
            self, "column_profiles", MappingProxyType(dict(self.column_profiles))
        )
        object.__setattr__(
            self,
            "numeric_profiles",
            MappingProxyType(dict(self.numeric_profiles)),
        )
        object.__setattr__(
            self,
            "categorical_profiles",
            MappingProxyType(dict(self.categorical_profiles)),
        )
        object.__setattr__(
            self,
            "datetime_profiles",
            MappingProxyType(dict(self.datetime_profiles)),
        )
        object.__setattr__(
            self, "text_profiles", MappingProxyType(dict(self.text_profiles))
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the profile result to a dictionary of primitive values.

        Returns:
            A dictionary representation suitable for JSON serialization.
        """
        from typing import cast

        return cast(dict[str, Any], _asdict_custom(self))


def _asdict_custom(obj: Any) -> Any:
    """Recursively convert dataclasses and mapping proxies to standard python primitives.

    Datetime values are converted to ISO-8601 strings and enum members to their
    value so the result stays JSON-serializable.
    """
    import dataclasses
    from datetime import datetime
    from enum import Enum
    from types import MappingProxyType

    if dataclasses.is_dataclass(obj):
        return {
            f.name: _asdict_custom(getattr(obj, f.name))
            for f in dataclasses.fields(obj)
        }
    elif isinstance(obj, (dict, MappingProxyType)):
        return {k: _asdict_custom(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_asdict_custom(v) for v in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, Enum):
        return obj.value
    else:
        return obj
