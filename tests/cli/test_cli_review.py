"""Integration tests for the featuresmith review CLI command."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
from typer.testing import CliRunner

import featuresmith as fs
from featuresmith.review.aggregator import ResultAggregator
from featuresmith_cli.commands.review import _parse_categories, _review_exit_code
from featuresmith_cli.main import app


def sample_csv(tmp_path: Path) -> Path:
    """Create a small temporary CSV dataset."""
    df = pd.DataFrame(
        {
            "clean": [1, 2, 3, 4, 5],
            "missing": [1.0, None, None, 4.0, 5.0],
        }
    )
    path = tmp_path / "dataset.csv"
    df.to_csv(path, index=False)
    return path


def test_cli_review_help() -> None:
    """Review help displays the new command's options."""
    runner = CliRunner()
    result = runner.invoke(app, ["review", "--help"])

    assert result.exit_code == 0
    assert "Path to the local tabular dataset" in result.stdout
    assert "--fail-on" in result.stdout
    assert "--only" in result.stdout


def test_cli_review_version() -> None:
    """Review command exposes the version callback."""
    runner = CliRunner()
    result = runner.invoke(app, ["review", "--version"])

    assert result.exit_code == 0
    assert "Featuresmith CLI" in result.stdout


def test_cli_review_csv(tmp_path: Path) -> None:
    """A review with a warning finding exits 0 and prints the report."""
    runner = CliRunner()
    result = runner.invoke(app, ["review", str(sample_csv(tmp_path))])

    assert result.exit_code == 0
    assert "Featuresmith Dataset Review" in result.stdout
    assert "Rows: 5 | Columns: 2" in result.stdout
    assert "[WARNING] Missing Values (review.quality.missingness)" in result.stdout
    assert "ML Readiness Score (scoring v0.1.0)" in result.stdout
    assert "  Missing Values: 85/100 (1 finding(s))" in result.stdout
    assert "Overall: " in result.stdout


def test_cli_review_no_score(tmp_path: Path) -> None:
    """--no-score omits the score section but keeps the review findings."""
    runner = CliRunner()
    result = runner.invoke(app, ["review", str(sample_csv(tmp_path)), "--no-score"])

    assert result.exit_code == 0
    assert "Featuresmith Dataset Review" in result.stdout
    assert "[WARNING] Missing Values (review.quality.missingness)" in result.stdout
    assert "ML Readiness Score" not in result.stdout


def test_cli_review_no_score_json(tmp_path: Path) -> None:
    """--no-score produces JSON with a null score."""
    runner = CliRunner()
    result = runner.invoke(
        app, ["review", str(sample_csv(tmp_path)), "--format", "json", "--no-score"]
    )

    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["score"] is None
    assert len(data["sections"]) == 7


def test_cli_review_fail_on_warning(tmp_path: Path) -> None:
    """--fail-on warning gates the exit code on warning-or-worse findings."""
    runner = CliRunner()
    result = runner.invoke(
        app, ["review", str(sample_csv(tmp_path)), "--fail-on", "warning"]
    )

    assert result.exit_code == 1


def test_cli_review_json_format(tmp_path: Path) -> None:
    """JSON output is the canonical ReviewResult serialization."""
    runner = CliRunner()
    result = runner.invoke(
        app, ["review", str(sample_csv(tmp_path)), "--format", "json"]
    )

    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["engine_version"] == "0.1.0"
    assert len(data["sections"]) == 7
    missingness = next(
        s for s in data["sections"] if s["id"] == "review.quality.missingness"
    )
    assert missingness["severity"] == "warning"
    assert "overall_summary" in data
    assert "dataset_summary" in data
    assert data["score"]["overall"] == 97.9
    assert len(data["score"]["dimensions"]) == 7


def _strip_finding_ids(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a deep copy with volatile finding IDs removed for comparison."""
    import copy

    cleaned = copy.deepcopy(payload)
    for section in cleaned["sections"]:
        for finding in section["findings"]:
            finding.pop("id", None)
    return cleaned


def test_cli_review_surface_parity_with_sdk(tmp_path: Path) -> None:
    """SDK and CLI produce identical canonical review content."""
    path = sample_csv(tmp_path)
    runner = CliRunner()

    sdk_result = fs.review(path)
    cli_result = runner.invoke(app, ["review", str(path), "--format", "json"])
    assert cli_result.exit_code == 0

    cli_data = _strip_finding_ids(json.loads(cli_result.stdout))
    sdk_data = _strip_finding_ids(sdk_result.to_dict())

    assert cli_data["engine_version"] == sdk_data["engine_version"]
    assert (
        cli_data["dataset_summary"]["row_count"]
        == sdk_data["dataset_summary"]["row_count"]
    )
    assert cli_data["sections"] == sdk_data["sections"]
    assert cli_data["overall_summary"] == sdk_data["overall_summary"]


def test_cli_review_missing_file() -> None:
    """A missing source exits 3 with a clear error."""
    runner = CliRunner()
    result = runner.invoke(app, ["review", "non_existent_file.csv"])

    assert result.exit_code == 3
    assert "Error:" in result.stderr
    assert "does not exist" in result.stderr


def test_cli_review_unsupported_format(tmp_path: Path) -> None:
    """An unsupported source format exits 2."""
    runner = CliRunner()
    txt_file = tmp_path / "data.txt"
    txt_file.touch()

    result = runner.invoke(app, ["review", str(txt_file)])

    assert result.exit_code == 2
    assert "Error:" in result.stderr


def test_cli_review_only_unknown_category(tmp_path: Path) -> None:
    """An unknown --only category exits 2."""
    runner = CliRunner()
    result = runner.invoke(
        app, ["review", str(sample_csv(tmp_path)), "--only", "bogus"]
    )

    assert result.exit_code == 2
    assert "Unknown review category 'bogus'" in result.stderr


def test_cli_review_only_valid_category(tmp_path: Path) -> None:
    """A valid --only category is accepted and runs its reviewers."""
    runner = CliRunner()
    result = runner.invoke(
        app, ["review", str(sample_csv(tmp_path)), "--only", "quality,leakage"]
    )

    assert result.exit_code == 0
    assert "[WARNING] Missing Values (review.quality.missingness)" in result.stdout
    assert "review.schema.health" not in result.stdout


def test_cli_review_previous_not_available(tmp_path: Path) -> None:
    """--previous is rejected with a clear message."""
    runner = CliRunner()
    result = runner.invoke(
        app, ["review", str(sample_csv(tmp_path)), "--previous", "old.csv"]
    )

    assert result.exit_code == 2
    assert "not available yet" in result.stderr


def test_cli_review_output_file_txt(tmp_path: Path) -> None:
    """The plain-text report is written to an output file."""
    runner = CliRunner()
    output_file = tmp_path / "review.txt"
    result = runner.invoke(
        app, ["review", str(sample_csv(tmp_path)), "--output", str(output_file)]
    )

    assert result.exit_code == 0
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "Featuresmith Dataset Review" in content
    assert "\x1b" not in content


def test_cli_review_output_file_json(tmp_path: Path) -> None:
    """JSON output is written to an output file."""
    runner = CliRunner()
    output_file = tmp_path / "review.json"
    result = runner.invoke(
        app,
        [
            "review",
            str(sample_csv(tmp_path)),
            "--format",
            "json",
            "--output",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    data = json.loads(output_file.read_text(encoding="utf-8"))
    assert len(data["sections"]) == 7


def test_cli_review_quiet(tmp_path: Path) -> None:
    """Quiet mode suppresses stdout but still writes the output file."""
    runner = CliRunner()
    output_file = tmp_path / "review.txt"
    result = runner.invoke(
        app,
        [
            "review",
            str(sample_csv(tmp_path)),
            "--quiet",
            "--output",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert result.stdout == ""
    assert output_file.exists()


def test_review_exit_code_thresholds() -> None:
    """Exit-code gating mirrors the analyze convention."""
    from featuresmith.core.profile_result import DatasetSummary
    from featuresmith.core.rule_finding import RuleFinding
    from featuresmith.review.schema import ReviewCategory, ReviewSection, Severity

    summary = DatasetSummary(
        row_count=5,
        column_count=1,
        size_in_bytes=None,
        missing_percentage=0.0,
        duplicate_percentage=0.0,
        num_numeric_columns=1,
        num_categorical_columns=0,
        num_datetime_columns=0,
        num_text_columns=0,
        num_constant_columns=0,
        num_fully_empty_columns=0,
    )
    finding = RuleFinding(
        rule_id="review.test",
        rule_name="Test",
        category="quality",
        severity="critical",
        column_name=None,
        title="Critical finding",
        description="Synthetic.",
        evidence={},
    )
    result = ResultAggregator().aggregate(
        engine_version="0.1.0",
        dataset_summary=summary,
        sections=(
            ReviewSection(
                id="review.quality.a",
                title="Quality",
                category=ReviewCategory.QUALITY,
                severity=Severity.CRITICAL,
                findings=(finding,),
            ),
        ),
    )

    assert _review_exit_code(result, "critical") == 1
    assert _review_exit_code(result, "warning") == 1
    assert _review_exit_code(result, "info") == 1

    clean = ResultAggregator().aggregate(
        engine_version="0.1.0",
        dataset_summary=summary,
        sections=(),
    )
    assert _review_exit_code(clean, "critical") == 0
    assert _review_exit_code(clean, "info") == 0


def test_parse_categories() -> None:
    """--only values parse into reviewer categories."""
    categories = _parse_categories("quality, leakage")

    assert {category.value for category in categories} == {"quality", "leakage"}
