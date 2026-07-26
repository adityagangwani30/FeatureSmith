"""Integration tests for the Featuresmith CLI."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest
from typer.testing import CliRunner

import featuresmith as fs
from featuresmith_cli.main import app


@pytest.fixture  # type: ignore[untyped-decorator]
def sample_csv(tmp_path: Path) -> Path:
    """Create a temporary CSV file with data issues.

    Contains:
    - A constant column 'constant' (triggers warning)
    - A column 'missing' with > 50% missingness (triggers critical)
    """
    df = pd.DataFrame(
        {
            "clean": [1, 2, 3, 4, 5],
            "constant": [42, 42, 42, 42, 42],
            "missing": [1.0, None, None, None, 5.0],
        }
    )
    path = tmp_path / "dataset.csv"
    df.to_csv(path, index=False)
    return path


@pytest.fixture  # type: ignore[untyped-decorator]
def sample_xlsx(tmp_path: Path) -> Path:
    """Create a temporary Excel file with data issues."""
    df = pd.DataFrame(
        {
            "clean": [1, 2, 3, 4, 5],
            "constant": [42, 42, 42, 42, 42],
        }
    )
    path = tmp_path / "dataset.xlsx"
    df.to_excel(path, index=False)
    return path


@pytest.fixture  # type: ignore[untyped-decorator]
def sample_parquet(tmp_path: Path) -> Path:
    """Create a temporary Parquet file with data issues.

    Uses polars (the core parquet connector backend) so no extra
    engine dependency (pyarrow / fastparquet) is required.
    """
    import polars as pl

    df = pl.DataFrame(
        {
            "clean": [1, 2, 3, 4, 5],
            "constant": [42, 42, 42, 42, 42],
        }
    )
    path = tmp_path / "dataset.parquet"
    df.write_parquet(path)
    return path


def test_cli_help() -> None:
    """Test analyze help display."""
    runner = CliRunner()
    result = runner.invoke(app, ["analyze", "--help"])
    assert result.exit_code == 0
    assert "Show version info" in result.stdout
    assert "Path to the local tabular dataset" in result.stdout


def test_cli_version() -> None:
    """Test CLI version option."""
    runner = CliRunner()
    result = runner.invoke(app, ["analyze", "--version"])
    assert result.exit_code == 0
    assert "Featuresmith CLI" in result.stdout
    assert "core" in result.stdout

    # Test top-level global flag
    result_global = runner.invoke(app, ["--version"])
    assert result_global.exit_code == 0
    assert "Featuresmith CLI" in result_global.stdout


def test_cli_analyze_csv_severities(sample_csv: Path) -> None:
    """Test that CLI exits with appropriate codes based on severity threshold."""
    runner = CliRunner()

    # 1. Under --severity critical, it should exit with 1 because 'missing' triggers critical
    result_critical = runner.invoke(
        app, ["analyze", str(sample_csv), "--severity", "critical"]
    )
    assert result_critical.exit_code == 1
    assert (
        "quality.fully_empty_columns" not in result_critical.stdout
    )  # warning, filtered out
    assert (
        "quality.missing_value_threshold" in result_critical.stdout
    )  # critical, displayed

    # 2. Under --severity warning, it should also exit with 1
    result_warning = runner.invoke(
        app, ["analyze", str(sample_csv), "--severity", "warning"]
    )
    assert result_warning.exit_code == 1
    assert "quality.constant_columns" in result_warning.stdout  # warning, displayed
    assert (
        "quality.missing_value_threshold" in result_warning.stdout
    )  # critical, displayed


def test_cli_analyze_csv_clean_exit(sample_csv: Path) -> None:
    """Test CLI exits with 0 if no findings match or exceed the threshold."""
    runner = CliRunner()
    # We load only the constant column dataset, which triggers warnings only.
    # If we filter by 'critical', exit code should be 0.
    df = pd.DataFrame(
        {
            "clean": [1, 2, 3, 4, 5],
            "constant": [42, 42, 42, 42, 42],
        }
    )
    clean_csv = sample_csv.parent / "clean.csv"
    df.to_csv(clean_csv, index=False)

    result = runner.invoke(app, ["analyze", str(clean_csv), "--severity", "critical"])
    assert result.exit_code == 0
    assert "constant" not in result.stdout  # filtered out
    assert "No quality findings discovered" in result.stdout


def test_cli_analyze_excel(sample_xlsx: Path) -> None:
    """Test Excel source analysis."""
    runner = CliRunner()
    result = runner.invoke(app, ["analyze", str(sample_xlsx), "--severity", "info"])
    assert result.exit_code == 1  # exits with 1 due to warning finding
    assert "quality.constant_columns" in result.stdout


def test_cli_analyze_parquet(sample_parquet: Path) -> None:
    """Test Parquet source analysis."""
    runner = CliRunner()
    result = runner.invoke(app, ["analyze", str(sample_parquet), "--severity", "info"])
    assert result.exit_code == 1
    assert "quality.constant_columns" in result.stdout


def test_cli_analyze_json_format(sample_csv: Path) -> None:
    """Test that JSON output matches canonical serialization."""
    runner = CliRunner()
    result = runner.invoke(
        app, ["analyze", str(sample_csv), "--format", "json", "--severity", "info"]
    )
    assert result.exit_code == 1

    # Output must be parseable JSON
    data = json.loads(result.stdout)
    assert "profile" in data
    assert "findings" in data
    assert "executed_rules" in data
    assert len(data["findings"]) > 0


def test_cli_analyze_missing_file() -> None:
    """Test file not found handling returns exit code 3."""
    runner = CliRunner()
    result = runner.invoke(app, ["analyze", "non_existent_file.csv"])
    assert result.exit_code == 3
    assert "Error:" in result.stderr
    assert "does not exist" in result.stderr


def test_cli_analyze_unsupported_format(tmp_path: Path) -> None:
    """Test unsupported format returns exit code 2."""
    runner = CliRunner()
    txt_file = tmp_path / "data.txt"
    txt_file.touch()

    result = runner.invoke(app, ["analyze", str(txt_file)])
    assert result.exit_code == 2
    assert "Error:" in result.stderr
    assert "Unsupported source" in result.stderr


def test_cli_analyze_invalid_target_column(sample_csv: Path) -> None:
    """Test invalid target column validation returns exit code 2."""
    runner = CliRunner()
    result = runner.invoke(
        app, ["analyze", str(sample_csv), "--target", "non_existent_col"]
    )
    assert result.exit_code == 2
    assert "Error:" in result.stderr
    assert "Target column 'non_existent_col' not found" in result.stderr


def test_cli_analyze_output_file_txt(sample_csv: Path, tmp_path: Path) -> None:
    """Test output file generation in text format."""
    runner = CliRunner()
    output_file = tmp_path / "report.txt"
    result = runner.invoke(
        app, ["analyze", str(sample_csv), "--output", str(output_file)]
    )
    assert result.exit_code == 1
    assert output_file.exists()

    content = output_file.read_text(encoding="utf-8")
    assert "Featuresmith Dataset Analysis Report" in content
    # ANSI escape characters should be stripped
    assert "\x1b" not in content


def test_cli_analyze_output_file_json(sample_csv: Path, tmp_path: Path) -> None:
    """Test output file generation in JSON format."""
    runner = CliRunner()
    output_file = tmp_path / "report.json"
    result = runner.invoke(
        app,
        [
            "analyze",
            str(sample_csv),
            "--format",
            "json",
            "--output",
            str(output_file),
        ],
    )
    assert result.exit_code == 1
    assert output_file.exists()

    content = output_file.read_text(encoding="utf-8")
    data = json.loads(content)
    assert "findings" in data


def test_cli_analyze_quiet(sample_csv: Path, tmp_path: Path) -> None:
    """Test quiet mode suppresses stdout but writes output file."""
    runner = CliRunner()
    output_file = tmp_path / "report.txt"
    result = runner.invoke(
        app,
        [
            "analyze",
            str(sample_csv),
            "--quiet",
            "--output",
            str(output_file),
            "--severity",
            "info",
        ],
    )
    assert result.exit_code == 1
    # stdout must be completely empty
    assert result.stdout == ""

    # Output file must still be correctly written
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "Featuresmith Dataset Analysis Report" in content


def test_cli_surface_parity_with_sdk(sample_csv: Path) -> None:
    """Test surface parity between Python SDK analyze() and CLI analyze command."""
    # 1. Run SDK analyze
    sdk_result = fs.analyze(sample_csv)

    # 2. Run CLI in JSON format to extract outputs
    runner = CliRunner()
    cli_result = runner.invoke(
        app, ["analyze", str(sample_csv), "--format", "json", "--severity", "info"]
    )
    assert cli_result.exit_code == 1

    cli_data = json.loads(cli_result.stdout)

    # 3. Assert SDK and CLI findings parity
    sdk_findings = {f.title: f.severity for f in sdk_result.findings}
    cli_findings = {f["title"]: f["severity"] for f in cli_data["findings"]}

    assert sdk_findings == cli_findings
    assert (
        sdk_result.profile.dataset_summary.row_count
        == cli_data["profile"]["dataset_summary"]["row_count"]
    )
    assert (
        sdk_result.profile.dataset_summary.column_count
        == cli_data["profile"]["dataset_summary"]["column_count"]
    )
