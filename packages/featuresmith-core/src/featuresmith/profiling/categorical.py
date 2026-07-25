"""Categorical column profiling module."""

from __future__ import annotations

import math

import polars as pl

from featuresmith.core.dataset import Dataset
from featuresmith.core.profile_result import CategoricalProfile


def profile_categorical_column(dataset: Dataset, col_name: str) -> CategoricalProfile:
    """Profile a single categorical column.

    Args:
        dataset: The normalized dataset.
        col_name: Name of the column.

    Returns:
        A CategoricalProfile object.
    """
    df = dataset.dataframe

    # Calculate missing count first
    if dataset.backend == "pandas":
        series = df[col_name]
        missing_count = int(series.isna().sum())
    else:
        # Polars
        missing_count = int(df.select(pl.col(col_name).null_count())[0, 0])

    # Get non-null counts as frequency table
    frequency_table: dict[str, int] = {}
    if dataset.backend == "pandas":
        series = df[col_name].dropna()
        if len(series) > 0:
            # Group and count
            vc = series.astype(str).value_counts(dropna=True)
            frequency_table = {str(k): int(v) for k, v in vc.to_dict().items()}
    else:
        # Polars
        non_null_df = df.select(pl.col(col_name).drop_nulls().cast(pl.String))
        if non_null_df.height > 0:
            # Group by and count
            freq_df = (
                non_null_df.group_by(col_name)
                .len()
                .sort(by=["len", col_name], descending=[True, False])
            )
            categories = freq_df.get_column(col_name).to_list()
            counts = freq_df.get_column("len").to_list()
            frequency_table = {
                str(k): int(v) for k, v in zip(categories, counts, strict=True)
            }

    cardinality = len(frequency_table)
    unique_count = cardinality

    if cardinality == 0:
        return CategoricalProfile(
            column_name=col_name,
            cardinality=0,
            unique_count=0,
            missing_count=missing_count,
            frequency_table={},
            top_values=[],
            least_frequent_values=[],
            most_common_category=None,
            entropy=None,
        )

    # Deterministic sorting: count descending, key/value string ascending
    sorted_items = sorted(frequency_table.items(), key=lambda x: (-x[1], x[0]))
    top_values = sorted_items[:10]

    # Deterministic sorting for least frequent: count ascending, key/value string ascending
    sorted_least = sorted(frequency_table.items(), key=lambda x: (x[1], x[0]))
    least_frequent_values = sorted_least[:10]

    most_common_category = top_values[0][0] if top_values else None

    # Entropy (Shannon entropy with base 2)
    total_non_null = sum(frequency_table.values())
    entropy = 0.0
    for count in frequency_table.values():
        p = count / total_non_null
        if p > 0:
            entropy -= p * math.log2(p)

    return CategoricalProfile(
        column_name=col_name,
        cardinality=cardinality,
        unique_count=unique_count,
        missing_count=missing_count,
        frequency_table=frequency_table,
        top_values=top_values,
        least_frequent_values=least_frequent_values,
        most_common_category=most_common_category,
        entropy=entropy,
    )
