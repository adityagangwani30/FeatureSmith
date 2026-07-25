"""Correlation summary module."""

from __future__ import annotations

import math

import pandas as pd
import polars as pl

from featuresmith.core.dataset import Dataset
from featuresmith.core.profile_result import CorrelationSummary


def compute_correlations(
    dataset: Dataset,
    numeric_columns: list[str],
    max_correlation_columns: int = 100,
) -> CorrelationSummary:
    """Compute pairwise Pearson correlation matrix for numeric columns.

    Args:
        dataset: The normalized dataset.
        numeric_columns: List of numeric column names.
        max_correlation_columns: Maximum number of numeric columns to correlate.

    Returns:
        A CorrelationSummary object.
    """
    if not numeric_columns:
        return CorrelationSummary(pearson={})

    # Cap columns to prevent combinatorial blowup
    cols = numeric_columns[:max_correlation_columns]
    df = dataset.dataframe

    pearson: dict[str, dict[str, float | None]] = {c: {} for c in cols}

    if dataset.backend == "pandas":
        # Pandas
        corr_df = df[cols].corr(method="pearson")
        for col1 in cols:
            for col2 in cols:
                val = corr_df.loc[col1, col2]
                if pd.isna(val) or math.isnan(val) or math.isinf(val):
                    pearson[col1][col2] = None
                else:
                    pearson[col1][col2] = float(val)
    else:
        # Polars: compute correlations in parallel using expressions
        exprs = []
        for i, c1 in enumerate(cols):
            for c2 in cols[i:]:
                exprs.append(pl.corr(c1, c2).alias(f"{c1}__{c2}"))

        if exprs:
            res = df.select(exprs)
            for i, c1 in enumerate(cols):
                for c2 in cols[i:]:
                    val = res.get_column(f"{c1}__{c2}")[0]
                    if val is None or math.isnan(val) or math.isinf(val):
                        f_val = None
                    else:
                        f_val = float(val)
                    pearson[c1][c2] = f_val
                    pearson[c2][c1] = f_val

    return CorrelationSummary(pearson=pearson)
