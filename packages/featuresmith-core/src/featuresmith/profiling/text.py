"""Text column profiling module."""

from __future__ import annotations

import pandas as pd
import polars as pl
from featuresmith.core.dataset import Dataset
from featuresmith.core.profile_result import TextProfile


def profile_text_column(dataset: Dataset, col_name: str) -> TextProfile:
    """Profile a single text column.

    Args:
        dataset: The normalized dataset.
        col_name: Name of the column.

    Returns:
        A TextProfile object.
    """
    df = dataset.dataframe
    row_count = dataset.row_count

    if dataset.backend == "pandas":
        series = df[col_name]
        non_null_series = series.dropna().astype(str)
        count = len(non_null_series)

        if count == 0:
            return TextProfile(
                column_name=col_name,
                avg_length=None,
                min_length=None,
                max_length=None,
                empty_strings=int((series == "").sum()) if row_count > 0 else 0,
                whitespace_only=0,
                char_count=0,
                word_count=0,
            )

        lengths = non_null_series.str.len()
        avg_length = float(lengths.mean())
        min_length = int(lengths.min())
        max_length = int(lengths.max())
        
        # Count empty strings in the entire series (including any null/nan that might be empty? No, exact matches to "")
        empty_strings = int((series == "").sum())
        
        # Whitespace-only matches: one or more whitespace characters
        whitespace_only = int(non_null_series.str.match(r"^\s+$").sum())
        char_count = int(lengths.sum())
        
        # Word counts: find all non-whitespace chunks and sum their counts
        word_count = int(non_null_series.str.findall(r"\S+").str.len().sum())

    else:
        # Polars
        col = pl.col(col_name)
        non_null_col = col.drop_nulls().cast(pl.String)

        # Select all stats in one pass
        res = df.select([
            non_null_col.len().alias("count"),
            non_null_col.str.len_chars().mean().alias("avg_len"),
            non_null_col.str.len_chars().min().alias("min_len"),
            non_null_col.str.len_chars().max().alias("max_len"),
            (col == "").sum().alias("empty_strings"),
            col.str.contains(r"^\s+$").sum().alias("whitespace_only"),
            non_null_col.str.len_chars().sum().alias("char_count"),
            non_null_col.str.extract_all(r"\S+").list.len().sum().alias("word_count"),
        ])

        count = int(res.get_column("count")[0])
        empty_strings = int(res.get_column("empty_strings")[0] or 0)
        whitespace_only = int(res.get_column("whitespace_only")[0] or 0)

        if count == 0:
            return TextProfile(
                column_name=col_name,
                avg_length=None,
                min_length=None,
                max_length=None,
                empty_strings=empty_strings,
                whitespace_only=whitespace_only,
                char_count=0,
                word_count=0,
            )

        avg_length = float(res.get_column("avg_len")[0])
        min_length = int(res.get_column("min_len")[0])
        max_length = int(res.get_column("max_len")[0])
        char_count = int(res.get_column("char_count")[0])
        word_count = int(res.get_column("word_count")[0] or 0)

    return TextProfile(
        column_name=col_name,
        avg_length=avg_length,
        min_length=min_length,
        max_length=max_length,
        empty_strings=empty_strings,
        whitespace_only=whitespace_only,
        char_count=char_count,
        word_count=word_count,
    )
