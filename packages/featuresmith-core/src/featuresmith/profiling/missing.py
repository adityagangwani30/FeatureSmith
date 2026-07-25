"""Missing value analysis module."""

from __future__ import annotations

import pandas as pd
import polars as pl
from featuresmith.core.dataset import Dataset
from featuresmith.core.profile_result import MissingValueSummary


def analyze_missing_values(dataset: Dataset) -> MissingValueSummary:
    """Analyze missing values in the dataset.

    Args:
        dataset: The normalized dataset.

    Returns:
        A MissingValueSummary object.
    """
    df = dataset.dataframe
    row_count = dataset.row_count
    col_count = dataset.column_count
    total_cells = row_count * col_count

    column_missing_counts: dict[str, int] = {}
    column_missing_percentages: dict[str, float] = {}
    total_missing = 0

    if col_count == 0 or row_count == 0:
        # Edge case: empty dataset
        for col_name in dataset.schema.names:
            column_missing_counts[col_name] = row_count
            column_missing_percentages[col_name] = 100.0 if row_count > 0 else 0.0
        return MissingValueSummary(
            column_missing_counts=column_missing_counts,
            column_missing_percentages=column_missing_percentages,
            total_missing=row_count * col_count,
            dataset_missing_percentage=100.0 if total_cells > 0 else 0.0,
        )

    if dataset.backend == "pandas":
        # Compute missing counts for all columns at once in pandas
        missing_series = df.isna().sum()
        for col_name in dataset.schema.names:
            count = int(missing_series[col_name])
            column_missing_counts[col_name] = count
            column_missing_percentages[col_name] = float((count / row_count) * 100.0)
            total_missing += count
    else:
        # Polars
        # Compute null counts for all columns in a single select
        null_counts = df.select(
            [pl.col(col).null_count().alias(col) for col in dataset.schema.names]
        )
        for col_name in dataset.schema.names:
            count = int(null_counts.get_column(col_name)[0])
            column_missing_counts[col_name] = count
            column_missing_percentages[col_name] = float((count / row_count) * 100.0)
            total_missing += count

    dataset_missing_percentage = (
        float((total_missing / total_cells) * 100.0) if total_cells > 0 else 0.0
    )

    return MissingValueSummary(
        column_missing_counts=column_missing_counts,
        column_missing_percentages=column_missing_percentages,
        total_missing=total_missing,
        dataset_missing_percentage=dataset_missing_percentage,
    )
