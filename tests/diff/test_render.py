"""Tests for the Dataset Diff rendering pipeline."""

from __future__ import annotations

from typing import cast

import pandas as pd
import pytest

import featuresmith as fs
from featuresmith.diff.render import (
    BaseDiffRenderer,
    DiffConsoleRenderer,
    DiffRendererRegistry,
    render_diff,
)


def _render(old_df: pd.DataFrame, new_df: pd.DataFrame) -> str:
    """Render the diff between two dataframes to the console format."""
    result = fs.diff(old_df, new_df)
    return cast(str, render_diff(result, "console"))


def test_render_console_header_and_health() -> None:
    """The console report includes header, health verdict, and recommendation."""
    old = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    new = pd.DataFrame({"a": [1, 2, 3], "c": [7, 8, 9]})

    text = _render(old, new)

    assert "Featuresmith Dataset Diff" in text
    assert "Rows: 3 -> 3" in text
    assert "Overall Dataset Health: regressed" in text
    assert "Recommendation:" in text
    assert "Dataset Comparison Summary" in text


def test_render_console_schema_section() -> None:
    """Schema changes are rendered in the details section."""
    old = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    new = pd.DataFrame({"a": [1, 2, 3], "c": [7, 8, 9]})

    text = _render(old, new)

    assert "Schema Changes" in text
    assert "Added: c" in text
    assert "Removed: b" in text


def test_render_console_no_changes() -> None:
    """An unchanged dataset renders the no-significant-changes note."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

    text = _render(df, df.copy())

    assert "No significant changes detected." in text


def test_render_console_omits_empty_sections() -> None:
    """Detail sections with no content are omitted entirely."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

    text = _render(df, df.copy())

    assert "Schema Changes" not in text
    assert "Duplicate Records" not in text
    assert "Constant Columns\n" not in text
    assert "Cardinality" not in text
    assert "Statistics" not in text
    assert "Distribution Shifts" not in text


def test_render_is_deterministic() -> None:
    """Rendering the same result twice yields identical output."""
    old = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    new = pd.DataFrame({"a": [1, 2, 3], "c": [7, 8, 9]})
    result = fs.diff(old, new)

    assert render_diff(result, "console") == render_diff(result, "console")


def test_render_unknown_target_raises() -> None:
    """An unregistered render target raises a clear error."""
    old = pd.DataFrame({"a": [1, 2, 3]})
    new = pd.DataFrame({"a": [1, 2, 3]})
    result = fs.diff(old, new)

    with pytest.raises(ValueError, match="Unknown diff renderer"):
        render_diff(result, "html")


def test_console_renderer_registered_under_console_name() -> None:
    """The console renderer registers under the 'console' target name."""
    renderer = DiffConsoleRenderer()

    assert renderer.name == "console"
    assert isinstance(renderer, BaseDiffRenderer)


def test_renderer_registry_get_and_render() -> None:
    """The registry resolves renderers by name."""
    registry = DiffRendererRegistry((DiffConsoleRenderer(),))

    assert registry.get("console") is not None
    assert registry.get("html") is None
