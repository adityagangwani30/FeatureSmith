"""Integration tests for the featuresmith diff CLI command."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd
from typer.testing import CliRunner

from featuresmith_cli.commands.diff import _diff_exit_code
from featuresmith_cli.main import app


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from text."""
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def _write_csv(tmp_path: Path, name: str, data: dict[str, Any]) -> Path:
    """Write a small CSV dataset into the temp directory."""
    path = tmp_path / name
    pd.DataFrame(data).to_csv(path, index=False)
    return path


def _datasets(tmp_path: Path) -> tuple[Path, Path]:
    """Create an older and a newer CSV snapshot."""
    old = _write_csv(tmp_path, "old.csv", {"a": [1, 2, 3], "b": [4, 5, 6]})
    new = _write_csv(tmp_path, "new.csv", {"a": [1, 2, 3], "c": [7, 8, 9]})
    return old, new


def test_cli_diff_help() -> None:
    """Diff help shows the two snapshot arguments and its options."""
    runner = CliRunner()
    result = runner.invoke(app, ["diff", "--help"], env={"COLUMNS": "120"})

    assert result.exit_code == 0
    clean_stdout = _strip_ansi(result.stdout)
    assert "{old}" in clean_stdout
    assert "{new}" in clean_stdout
    assert "--target" in clean_stdout
    assert "--fail-on" in clean_stdout
    assert "--format" in clean_stdout


def test_cli_diff_version() -> None:
    """Diff command exposes the version callback."""
    runner = CliRunner()
    result = runner.invoke(app, ["diff", "--version"])

    assert result.exit_code == 0
    assert "Featuresmith CLI" in result.stdout


def test_cli_diff_unchanged_exits_zero(tmp_path: Path) -> None:
    """Two identical datasets exit 0 and print the report."""
    runner = CliRunner()
    old = _write_csv(tmp_path, "old.csv", {"a": [1, 2, 3], "b": ["x", "y", "z"]})
    new = _write_csv(tmp_path, "new.csv", {"a": [1, 2, 3], "b": ["x", "y", "z"]})

    result = runner.invoke(app, ["diff", str(old), str(new)])

    assert result.exit_code == 0
    assert "Featuresmith Dataset Diff" in result.stdout
    assert "Rows: 3 -> 3" in result.stdout
    assert "No significant changes detected." in result.stdout


def test_cli_diff_regression_fail_on_warning(tmp_path: Path) -> None:
    """A regression with warning findings exits 1 under --fail-on warning."""
    runner = CliRunner()
    old, new = _datasets(tmp_path)

    result = runner.invoke(app, ["diff", str(old), str(new), "--fail-on", "warning"])

    assert result.exit_code == 1
    assert "Overall Dataset Health: regressed" in result.stdout
    assert "Removed: b" in result.stdout


def test_cli_diff_default_fail_on_critical_exits_zero(tmp_path: Path) -> None:
    """Warning-level changes do not fail the default critical gate."""
    runner = CliRunner()
    old, new = _datasets(tmp_path)

    result = runner.invoke(app, ["diff", str(old), str(new)])

    assert result.exit_code == 0


def test_cli_diff_json_format(tmp_path: Path) -> None:
    """JSON output is the canonical DatasetDiffResult serialization."""
    runner = CliRunner()
    old, new = _datasets(tmp_path)

    result = runner.invoke(app, ["diff", str(old), str(new), "--format", "json"])

    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["version"] == "0.2.0"
    assert data["schema"]["added_columns"] == ["c"]
    assert data["schema"]["removed_columns"] == ["b"]
    assert data["summary"]["overall_health"] == "regressed"
    assert "overall_summary" in data


def test_cli_diff_target_column(tmp_path: Path) -> None:
    """--target enables the leakage comparison between snapshots."""
    runner = CliRunner()
    old = _write_csv(
        tmp_path, "old.csv", {"target": [1, 2, 3, 4, 5], "a": [10, 20, 30, 40, 50]}
    )
    new = _write_csv(
        tmp_path, "new.csv", {"target": [1, 2, 3, 4, 5], "leak": [1, 2, 3, 4, 5]}
    )

    result = runner.invoke(
        app, ["diff", str(old), str(new), "--target", "target", "--format", "json"]
    )

    assert result.exit_code == 1
    data = json.loads(result.stdout)
    assert data["leakage"] is not None
    assert data["summary"]["leakage_new"] == 1


def test_cli_diff_target_unknown_column(tmp_path: Path) -> None:
    """An unknown --target column exits 2 with a clear error."""
    runner = CliRunner()
    old, new = _datasets(tmp_path)

    result = runner.invoke(app, ["diff", str(old), str(new), "--target", "bogus"])

    assert result.exit_code == 2
    assert "Target column 'bogus' not found" in result.stderr
    assert "Available columns" in result.stderr


def test_cli_diff_missing_file() -> None:
    """A missing snapshot exits 3 with a clear error."""
    runner = CliRunner()
    result = runner.invoke(
        app, ["diff", "non_existent_old.csv", "non_existent_new.csv"]
    )

    assert result.exit_code == 3
    assert "Error:" in result.stderr
    assert "does not exist" in result.stderr


def test_cli_diff_unsupported_format(tmp_path: Path) -> None:
    """An unsupported source format exits 2."""
    runner = CliRunner()
    old = tmp_path / "old.txt"
    old.touch()
    new = tmp_path / "new.txt"
    new.touch()

    result = runner.invoke(app, ["diff", str(old), str(new)])

    assert result.exit_code == 2
    assert "Error:" in result.stderr


def test_cli_diff_output_file_txt(tmp_path: Path) -> None:
    """The plain-text report is written to an output file."""
    runner = CliRunner()
    old, new = _datasets(tmp_path)
    output_file = tmp_path / "diff.txt"

    result = runner.invoke(
        app, ["diff", str(old), str(new), "--output", str(output_file)]
    )

    assert result.exit_code == 0
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "Featuresmith Dataset Diff" in content


def test_cli_diff_output_file_json(tmp_path: Path) -> None:
    """JSON output is written to an output file."""
    runner = CliRunner()
    old, new = _datasets(tmp_path)
    output_file = tmp_path / "diff.json"

    result = runner.invoke(
        app,
        [
            "diff",
            str(old),
            str(new),
            "--format",
            "json",
            "--output",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    data = json.loads(output_file.read_text(encoding="utf-8"))
    assert data["schema"]["added_columns"] == ["c"]


def test_cli_diff_quiet(tmp_path: Path) -> None:
    """Quiet mode suppresses stdout but still writes the output file."""
    runner = CliRunner()
    old, new = _datasets(tmp_path)
    output_file = tmp_path / "diff.txt"

    result = runner.invoke(
        app,
        ["diff", str(old), str(new), "--quiet", "--output", str(output_file)],
    )

    assert result.exit_code == 0
    assert result.stdout == ""
    assert output_file.exists()


def test_diff_exit_code_thresholds() -> None:
    """Exit-code gating mirrors the analyze/review convention."""
    import featuresmith as fs

    old = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    new = pd.DataFrame({"a": [1, 2, 3], "c": [7, 8, 9]})

    result = fs.diff(old, new)

    assert _diff_exit_code(result, "info") == 1
    assert _diff_exit_code(result, "warning") == 1
    assert _diff_exit_code(result, "critical") == 0

    unchanged = fs.diff(old, old.copy())
    assert _diff_exit_code(unchanged, "info") == 0
    assert _diff_exit_code(unchanged, "critical") == 0
