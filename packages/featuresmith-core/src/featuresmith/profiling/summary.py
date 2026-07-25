"""Helper functions for logical type classification and dataset summaries."""

from __future__ import annotations

import pandas as pd
import polars as pl

from featuresmith.core.dataset import Dataset
from featuresmith.core.profile_result import DatasetMetadata


def classify_logical_type(dataset: Dataset, col_name: str) -> str:
    """Classify the logical type of a column.

    Args:
        dataset: The normalized dataset.
        col_name: Name of the column to classify.

    Returns:
        One of "numeric", "categorical", "datetime", or "text".
    """
    df = dataset.dataframe

    # 1. Datetime detection
    if dataset.backend == "pandas":
        series = df[col_name]
        if pd.api.types.is_datetime64_any_dtype(series):
            return "datetime"
    elif dataset.backend == "polars":
        col_type = df.schema[col_name]
        if col_type in (pl.Date, pl.Datetime, pl.Time, pl.Duration):
            return "datetime"

    # 2. Numeric detection
    if dataset.backend == "pandas":
        series = df[col_name]
        if pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_bool_dtype(
            series
        ):
            return "numeric"
    elif dataset.backend == "polars":
        col_type = df.schema[col_name]
        if col_type.is_numeric():
            return "numeric"

    # 3. Boolean/Categorical/String detection
    if dataset.backend == "pandas":
        series = df[col_name]
        if pd.api.types.is_bool_dtype(series):
            return "categorical"
    elif dataset.backend == "polars":
        col_type = df.schema[col_name]
        if col_type == pl.Boolean:
            return "categorical"

    # If it is category, object, string or anything else, we analyze string properties
    # Let's count unique values and average string length.
    if dataset.backend == "pandas":
        series = df[col_name].dropna()
        if len(series) == 0:
            return "categorical"

        # Convert to string to check length
        str_series = series.astype(str)
        total_len = str_series.str.len().sum()
        avg_len = total_len / len(series)
        unique_count = str_series.nunique()
        non_null_count = len(series)
    else:
        # Polars
        series = df.select(pl.col(col_name).drop_nulls())
        non_null_count = len(series)
        if non_null_count == 0:
            return "categorical"

        # Compute stats in Polars
        stats = series.select(
            [
                pl.col(col_name)
                .cast(pl.String)
                .str.len_chars()
                .mean()
                .alias("avg_len"),
                pl.col(col_name).cast(pl.String).n_unique().alias("unique_count"),
            ]
        )
        avg_len = stats.get_column("avg_len")[0] or 0.0
        unique_count = stats.get_column("unique_count")[0] or 0

    # Heuristic for Text vs Categorical
    if avg_len >= 20:
        return "text"
    if (
        non_null_count > 0
        and (unique_count / non_null_count) > 0.5
        and unique_count > 10
    ):
        return "text"

    return "categorical"


def build_dataset_metadata(dataset: Dataset) -> DatasetMetadata:
    """Build the DatasetMetadata structure.

    Args:
        dataset: The normalized dataset.

    Returns:
        A DatasetMetadata object.
    """
    return DatasetMetadata(
        source=dataset.source,
        file_size=dataset.file_size,
        backend=dataset.backend,
        custom_metadata=dict(dataset.metadata),
    )
