"""Main orchestration module for profiling datasets."""

from __future__ import annotations

import time
from datetime import UTC, datetime

import polars as pl

from featuresmith.core.dataset import Dataset
from featuresmith.core.profile_result import (
    ColumnProfile,
    DatasetSummary,
    ExecutionMetadata,
    ProfileResult,
)
from featuresmith.profiling.categorical import profile_categorical_column
from featuresmith.profiling.correlation import compute_correlations
from featuresmith.profiling.datetime import profile_datetime_column
from featuresmith.profiling.duplicates import analyze_duplicates
from featuresmith.profiling.missing import analyze_missing_values
from featuresmith.profiling.numeric import profile_numeric_column
from featuresmith.profiling.quality import (
    find_constant_columns,
    find_fully_empty_columns,
)
from featuresmith.profiling.summary import build_dataset_metadata, classify_logical_type
from featuresmith.profiling.text import profile_text_column


def _get_non_null_unique_count(dataset: Dataset, col_name: str) -> int:
    """Compute the number of unique non-null values in a column."""
    df = dataset.dataframe
    if dataset.backend == "pandas":
        return int(df[col_name].dropna().nunique())
    else:
        # Polars
        return int(df.select(pl.col(col_name).drop_nulls().n_unique())[0, 0])


def _get_missing_count(dataset: Dataset, col_name: str) -> int:
    """Compute the number of missing values in a column."""
    df = dataset.dataframe
    if dataset.backend == "pandas":
        return int(df[col_name].isna().sum())
    else:
        # Polars
        return int(df.select(pl.col(col_name).null_count())[0, 0])


def profile_dataset(
    dataset: Dataset,
    max_correlation_columns: int = 100,
    max_frequency_table_size: int = 1000,
) -> ProfileResult:
    """Orchestrate deterministic profiling of a dataset.

    Args:
        dataset: The normalized Dataset object to profile.
        max_correlation_columns: Limit correlation computations to prevent
            combinatorial blowup (default 100).

    Returns:
        ProfileResult: A strongly-typed statistical profile containing dataset-wide
            summaries, column-level profiles, missingness summaries, duplicate
            statistics, and a Pearson correlation matrix.

    Notes:
        Logical type classification uses a heuristic mapping columns into
        "numeric", "categorical", "datetime", or "text". Pearson correlation
        matrix is computed for numeric columns only and is capped to the first
        `max_correlation_columns` numeric columns to prevent performance degradation.

    Examples:
        >>> import pandas as pd
        >>> from featuresmith.core.dataset import Dataset
        >>> from featuresmith.profiling.profiler import profile_dataset
        >>> df = pd.DataFrame({"a": [1, 2, 3]})
        >>> ds = Dataset.from_dataframe(df, backend="pandas")
        >>> prof = profile_dataset(ds)
        >>> prof.dataset_summary.row_count
        3
    """
    start_time_iso = datetime.now(UTC).isoformat()
    start_perf = time.perf_counter()

    row_count = dataset.row_count
    column_count = dataset.column_count

    numeric_profiles = {}
    categorical_profiles = {}
    datetime_profiles = {}
    text_profiles = {}
    column_profiles = {}

    # 1. Profile each column individually based on classified logical type
    for col_name in dataset.schema.names:
        logical_type = classify_logical_type(dataset, col_name)
        dtype_str = dataset.dtypes[col_name]

        if logical_type == "numeric":
            num_prof = profile_numeric_column(dataset, col_name)
            numeric_profiles[col_name] = num_prof

            missing_count = num_prof.missing_count
            missing_percentage = num_prof.missing_percentage
            is_constant = num_prof.unique_count <= 1
            is_fully_empty = num_prof.count == 0

        elif logical_type == "categorical":
            cat_prof = profile_categorical_column(
                dataset, col_name, max_frequency_table_size=max_frequency_table_size
            )
            categorical_profiles[col_name] = cat_prof

            missing_count = cat_prof.missing_count
            missing_percentage = (
                float((missing_count / row_count) * 100.0) if row_count > 0 else 0.0
            )
            is_constant = cat_prof.unique_count <= 1
            is_fully_empty = cat_prof.cardinality == 0 and missing_count == row_count

        elif logical_type == "datetime":
            dt_prof = profile_datetime_column(dataset, col_name)
            datetime_profiles[col_name] = dt_prof

            missing_count = dt_prof.missing_count
            missing_percentage = (
                float((missing_count / row_count) * 100.0) if row_count > 0 else 0.0
            )
            is_constant = dt_prof.minimum == dt_prof.maximum or (
                dt_prof.minimum is None and dt_prof.maximum is None
            )
            is_fully_empty = dt_prof.minimum is None and dt_prof.maximum is None

        else:  # logical_type == "text"
            txt_prof = profile_text_column(dataset, col_name)
            text_profiles[col_name] = txt_prof

            missing_count = _get_missing_count(dataset, col_name)
            missing_percentage = (
                float((missing_count / row_count) * 100.0) if row_count > 0 else 0.0
            )
            unique_cnt = _get_non_null_unique_count(dataset, col_name)
            is_constant = unique_cnt <= 1
            is_fully_empty = txt_prof.avg_length is None and missing_count == row_count

        column_profiles[col_name] = ColumnProfile(
            name=col_name,
            dtype=dtype_str,
            logical_type=logical_type,
            missing_count=missing_count,
            missing_percentage=missing_percentage,
            is_constant=is_constant,
            is_fully_empty=is_fully_empty,
        )

    # 2. Identify constant and fully empty columns across the dataset
    constant_columns = find_constant_columns(column_profiles)
    fully_empty_columns = find_fully_empty_columns(column_profiles)

    # 3. Compute summaries
    missing_value_summary = analyze_missing_values(dataset)
    duplicate_summary = analyze_duplicates(
        dataset, constant_columns, fully_empty_columns
    )
    correlation_summary = compute_correlations(
        dataset, list(numeric_profiles.keys()), max_correlation_columns
    )
    dataset_metadata = build_dataset_metadata(dataset)

    # 4. Global counts
    dataset_summary = DatasetSummary(
        row_count=row_count,
        column_count=column_count,
        size_in_bytes=dataset.file_size,
        missing_percentage=missing_value_summary.dataset_missing_percentage,
        duplicate_percentage=duplicate_summary.duplicate_percentage,
        num_numeric_columns=len(numeric_profiles),
        num_categorical_columns=len(categorical_profiles),
        num_datetime_columns=len(datetime_profiles),
        num_text_columns=len(text_profiles),
        num_constant_columns=len(constant_columns),
        num_fully_empty_columns=len(fully_empty_columns),
    )

    elapsed_time = time.perf_counter() - start_perf

    from featuresmith import __version__ as pkg_version

    execution_metadata = ExecutionMetadata(
        start_time=start_time_iso,
        duration_seconds=elapsed_time,
        featuresmith_version=pkg_version,
    )

    return ProfileResult(
        dataset_summary=dataset_summary,
        column_profiles=column_profiles,
        numeric_profiles=numeric_profiles,
        categorical_profiles=categorical_profiles,
        datetime_profiles=datetime_profiles,
        text_profiles=text_profiles,
        missing_value_summary=missing_value_summary,
        duplicate_summary=duplicate_summary,
        correlation_summary=correlation_summary,
        dataset_metadata=dataset_metadata,
        execution_metadata=execution_metadata,
    )
