"""Duplicate analysis module."""

from __future__ import annotations

import pandas as pd
import polars as pl
from featuresmith.core.dataset import Dataset
from featuresmith.core.profile_result import DuplicateSummary


def analyze_duplicates(
    dataset: Dataset, constant_columns: list[str], fully_empty_columns: list[str]
) -> DuplicateSummary:
    """Analyze duplicate rows in the dataset.

    Args:
        dataset: The normalized dataset.
        constant_columns: Pre-identified constant columns.
        fully_empty_columns: Pre-identified fully empty columns.

    Returns:
        A DuplicateSummary object.
    """
    df = dataset.dataframe
    row_count = dataset.row_count

    if row_count == 0:
        return DuplicateSummary(
            duplicate_rows_count=0,
            duplicate_percentage=0.0,
            constant_columns=constant_columns,
            fully_empty_columns=fully_empty_columns,
        )

    if dataset.backend == "pandas":
        duplicate_rows_count = int(df.duplicated().sum())
    else:
        # Polars: duplicate rows count is total rows minus unique rows
        # This is equivalent to pandas duplicated().sum()
        unique_rows_count = df.unique().height
        duplicate_rows_count = row_count - unique_rows_count

    duplicate_percentage = float((duplicate_rows_count / row_count) * 100.0)

    return DuplicateSummary(
        duplicate_rows_count=duplicate_rows_count,
        duplicate_percentage=duplicate_percentage,
        constant_columns=list(constant_columns),
        fully_empty_columns=list(fully_empty_columns),
    )
