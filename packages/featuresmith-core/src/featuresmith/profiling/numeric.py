"""Numeric column profiling module."""

from __future__ import annotations

import math
from typing import Any
import numpy as np
import pandas as pd
import polars as pl

from featuresmith.core.dataset import Dataset
from featuresmith.core.profile_result import NumericProfile


def _to_float(val: Any) -> float | None:
    """Safely convert a value to a Python float, returning None if NaN/Inf."""
    if val is None:
        return None
    # Check for pandas/numpy nulls
    if isinstance(val, (float, int)) and (math.isnan(val) or math.isinf(val)):
        return None
    try:
        # If it's a series or list, we grab first element
        if hasattr(val, "item"):
            val = val.item()
        elif hasattr(val, "iloc"):
            val = val.iloc[0]
            
        f = float(val)
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    except (ValueError, TypeError):
        return None


def _to_int(val: Any) -> int:
    """Convert a value to a Python int."""
    if val is None:
        return 0
    try:
        if hasattr(val, "item"):
            val = val.item()
        return int(val)
    except (ValueError, TypeError):
        return 0


def profile_numeric_column(dataset: Dataset, col_name: str) -> NumericProfile:
    """Profile a single numeric column.

    Args:
        dataset: The normalized dataset.
        col_name: Name of the column.

    Returns:
        A NumericProfile object.
    """
    df = dataset.dataframe
    row_count = dataset.row_count

    if dataset.backend == "pandas":
        series = df[col_name]
        non_null_series = series.dropna()
        count = int(non_null_series.count())
        missing_count = int(series.isna().sum())
        missing_percentage = float((missing_count / row_count) * 100.0) if row_count > 0 else 0.0
        unique_count = int(non_null_series.nunique())

        if count == 0:
            return NumericProfile(
                column_name=col_name,
                count=0,
                missing_count=missing_count,
                missing_percentage=missing_percentage,
                unique_count=0,
                mean=None,
                median=None,
                mode=None,
                minimum=None,
                maximum=None,
                range=None,
                variance=None,
                std_dev=None,
                q1=None,
                q2=None,
                q3=None,
                iqr=None,
                sum=None,
                zero_count=0,
                negative_count=0,
                positive_count=0,
                skewness=None,
                kurtosis=None,
            )

        mean = _to_float(non_null_series.mean())
        median = _to_float(non_null_series.median())
        minimum = _to_float(non_null_series.min())
        maximum = _to_float(non_null_series.max())
        
        rng = None
        if minimum is not None and maximum is not None:
            rng = maximum - minimum

        variance = _to_float(non_null_series.var(ddof=1))
        std_dev = _to_float(non_null_series.std(ddof=1))
        
        q1 = _to_float(non_null_series.quantile(0.25))
        q2 = _to_float(non_null_series.quantile(0.50))
        q3 = _to_float(non_null_series.quantile(0.75))
        
        iqr = None
        if q1 is not None and q3 is not None:
            iqr = q3 - q1

        sm = _to_float(non_null_series.sum())
        zero_count = int((non_null_series == 0).sum())
        negative_count = int((non_null_series < 0).sum())
        positive_count = int((non_null_series > 0).sum())
        
        # Mode
        modes = non_null_series.mode()
        mode = _to_float(modes.iloc[0]) if not modes.empty else None

        skewness = _to_float(non_null_series.skew())
        kurtosis = _to_float(non_null_series.kurt())

    else:
        # Polars
        col = pl.col(col_name)
        non_null_col = col.drop_nulls()

        # Compute everything in a single select statement
        res = df.select([
            col.len().alias("total_len"),
            col.null_count().alias("missing_count"),
            non_null_col.n_unique().alias("unique_count"),
            non_null_col.mean().alias("mean"),
            non_null_col.median().alias("median"),
            non_null_col.min().alias("min"),
            non_null_col.max().alias("max"),
            non_null_col.var(ddof=1).alias("var"),
            non_null_col.std(ddof=1).alias("std"),
            non_null_col.quantile(0.25).alias("q1"),
            non_null_col.quantile(0.50).alias("q2"),
            non_null_col.quantile(0.75).alias("q3"),
            non_null_col.sum().alias("sum"),
            (non_null_col == 0).sum().alias("zero_count"),
            (non_null_col < 0).sum().alias("negative_count"),
            (non_null_col > 0).sum().alias("positive_count"),
            non_null_col.skew().alias("skew"),
            non_null_col.kurtosis().alias("kurt"),
            non_null_col.mode().sort().first().alias("mode")
        ])

        total_len = _to_int(res.get_column("total_len")[0])
        missing_count = _to_int(res.get_column("missing_count")[0])
        missing_percentage = float((missing_count / total_len) * 100.0) if total_len > 0 else 0.0
        unique_count = _to_int(res.get_column("unique_count")[0])
        count = total_len - missing_count

        if count == 0:
            return NumericProfile(
                column_name=col_name,
                count=0,
                missing_count=missing_count,
                missing_percentage=missing_percentage,
                unique_count=0,
                mean=None,
                median=None,
                mode=None,
                minimum=None,
                maximum=None,
                range=None,
                variance=None,
                std_dev=None,
                q1=None,
                q2=None,
                q3=None,
                iqr=None,
                sum=None,
                zero_count=0,
                negative_count=0,
                positive_count=0,
                skewness=None,
                kurtosis=None,
            )

        mean = _to_float(res.get_column("mean")[0])
        median = _to_float(res.get_column("median")[0])
        minimum = _to_float(res.get_column("min")[0])
        maximum = _to_float(res.get_column("max")[0])
        
        rng = None
        if minimum is not None and maximum is not None:
            rng = maximum - minimum

        variance = _to_float(res.get_column("var")[0])
        std_dev = _to_float(res.get_column("std")[0])
        
        q1 = _to_float(res.get_column("q1")[0])
        q2 = _to_float(res.get_column("q2")[0])
        q3 = _to_float(res.get_column("q3")[0])
        
        iqr = None
        if q1 is not None and q3 is not None:
            iqr = q3 - q1

        sm = _to_float(res.get_column("sum")[0])
        zero_count = _to_int(res.get_column("zero_count")[0])
        negative_count = _to_int(res.get_column("negative_count")[0])
        positive_count = _to_int(res.get_column("positive_count")[0])
        
        mode = _to_float(res.get_column("mode")[0])
        skewness = _to_float(res.get_column("skew")[0])
        kurtosis = _to_float(res.get_column("kurt")[0])

    return NumericProfile(
        column_name=col_name,
        count=count,
        missing_count=missing_count,
        missing_percentage=missing_percentage,
        unique_count=unique_count,
        mean=mean,
        median=median,
        mode=mode,
        minimum=minimum,
        maximum=maximum,
        range=rng,
        variance=variance,
        std_dev=std_dev,
        q1=q1,
        q2=q2,
        q3=q3,
        iqr=iqr,
        sum=sm,
        zero_count=zero_count,
        negative_count=negative_count,
        positive_count=positive_count,
        skewness=skewness,
        kurtosis=kurtosis,
    )
