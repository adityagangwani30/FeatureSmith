"""Datetime column profiling module."""

from __future__ import annotations

from datetime import date, datetime
import pandas as pd
import polars as pl

from featuresmith.core.dataset import Dataset
from featuresmith.core.profile_result import DatetimeProfile


def profile_datetime_column(dataset: Dataset, col_name: str) -> DatetimeProfile:
    """Profile a single datetime column.

    Args:
        dataset: The normalized dataset.
        col_name: Name of the column.

    Returns:
        A DatetimeProfile object.
    """
    df = dataset.dataframe

    if dataset.backend == "pandas":
        series = df[col_name]
        missing_count = int(series.isna().sum())

        min_val = series.min()
        max_val = series.max()

        # Check if min_val/max_val are null (NaT)
        if pd.isna(min_val) or pd.isna(max_val):
            return DatetimeProfile(
                column_name=col_name,
                minimum=None,
                maximum=None,
                range_days=None,
                missing_count=missing_count,
                earliest_record=None,
                latest_record=None,
            )

        # Handle conversion to standard datetime if they are Timestamp objects
        if hasattr(min_val, "to_pydatetime"):
            min_dt = min_val.to_pydatetime()
        else:
            min_dt = min_val

        if hasattr(max_val, "to_pydatetime"):
            max_dt = max_val.to_pydatetime()
        else:
            max_dt = max_val

        # If min_dt/max_dt are date (not datetime) objects, convert them to datetimes to subtract safely
        if isinstance(min_dt, date) and not isinstance(min_dt, datetime):
            min_dt = datetime.combine(min_dt, datetime.min.time())
        if isinstance(max_dt, date) and not isinstance(max_dt, datetime):
            max_dt = datetime.combine(max_dt, datetime.min.time())

        # ISO format
        minimum = min_val.isoformat()
        maximum = max_val.isoformat()
        range_days = float((max_dt - min_dt).total_seconds() / 86400.0)

    else:
        # Polars
        missing_count = int(df.select(pl.col(col_name).null_count())[0, 0])
        min_val = df.select(pl.col(col_name).min())[0, 0]
        max_val = df.select(pl.col(col_name).max())[0, 0]

        if min_val is None or max_val is None:
            return DatetimeProfile(
                column_name=col_name,
                minimum=None,
                maximum=None,
                range_days=None,
                missing_count=missing_count,
                earliest_record=None,
                latest_record=None,
            )

        # Polars returns datetime.date or datetime.datetime objects directly
        min_dt = min_val
        max_dt = max_val

        if isinstance(min_dt, date) and not isinstance(min_dt, datetime):
            min_dt = datetime.combine(min_dt, datetime.min.time())
        if isinstance(max_dt, date) and not isinstance(max_dt, datetime):
            max_dt = datetime.combine(max_dt, datetime.min.time())

        minimum = min_val.isoformat()
        maximum = max_val.isoformat()
        range_days = float((max_dt - min_dt).total_seconds() / 86400.0)

    return DatetimeProfile(
        column_name=col_name,
        minimum=minimum,
        maximum=maximum,
        range_days=range_days,
        missing_count=missing_count,
        earliest_record=minimum,
        latest_record=maximum,
    )
