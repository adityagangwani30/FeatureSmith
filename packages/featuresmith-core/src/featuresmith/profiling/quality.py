"""Quality analysis utilities."""

from __future__ import annotations

from featuresmith.core.profile_result import ColumnProfile


def find_constant_columns(column_profiles: dict[str, ColumnProfile]) -> list[str]:
    """Identify columns that contain constant values.

    Args:
        column_profiles: Mapping of column name to ColumnProfile.

    Returns:
        List of constant column names.
    """
    return [name for name, profile in column_profiles.items() if profile.is_constant]


def find_fully_empty_columns(column_profiles: dict[str, ColumnProfile]) -> list[str]:
    """Identify columns that are completely empty (all missing).

    Args:
        column_profiles: Mapping of column name to ColumnProfile.

    Returns:
        List of fully empty column names.
    """
    return [name for name, profile in column_profiles.items() if profile.is_fully_empty]
