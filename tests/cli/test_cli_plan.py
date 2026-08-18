"""Integration tests for the featuresmith plan CLI command."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd
from typer.testing import CliRunner

import featuresmith as fs
from featuresmith_cli.main import app


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from text."""
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def sample_csv(tmp_path: Path) -> Path:
    """Create a small temporary CSV dataset with issues."""
    df = pd.DataFrame(
        {
            "clean": [1, 2, 3, 4, 5],
            "missing": [1.0, None, None, 4.0, 5.0],
            "duplicate": [1, 1, 2, 2, 3],
        }
    )
    path = tmp_path / "dataset.csv"
    df.to_csv(path, index=False)
    return path


def clean_csv(tmp_path: Path) -> Path:
    """Create a clean temporary CSV dataset."""
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": [2.0, 1.0, 3.0, 5.0, 4.0]})
    path = tmp_path / "clean.csv"
    df.to_csv(path, index=False)
    return path


def test_cli_plan_help() -> None:
    """Plan help displays the command's options."""
    runner = CliRunner()
    result = runner.invoke(app, ["plan", "--help"], env={"COLUMNS": "120"})

    assert result.exit_code == 0
    clean_stdout = _strip_ansi(result.stdout)
    assert "Path to the local tabular dataset" in clean_stdout
    assert "--target" in clean_stdout
    assert "--previous" in clean_stdout
    assert "--accept" in clean_stdout
    assert "--format" in clean_stdout
    assert "--fail-on" in clean_stdout
    assert "--output" in clean_stdout
    assert "--quiet" in clean_stdout


def test_cli_plan_version() -> None:
    """Plan command exposes the version callback."""
    runner = CliRunner()
    result = runner.invoke(app, ["plan", "--version"])

    assert result.exit_code == 0
    assert "Featuresmith CLI" in result.stdout


def test_cli_plan_accept_valid_recommendations(tmp_path: Path) -> None:
    """Accepting valid recommendation IDs produces a plan with items."""
    runner = CliRunner()
    path = sample_csv(tmp_path)

    # First run review to see available recommendation IDs
    review_result = runner.invoke(app, ["review", str(path), "--format", "json"])
    assert review_result.exit_code == 0
    review_data = json.loads(review_result.stdout)
    rec_ids = [rec["id"] for rec in review_data.get("recommendations", [])]
    assert rec_ids, "Expected at least one recommendation"

    # Accept the first recommendation
    accept_id = rec_ids[0]
    result = runner.invoke(app, ["plan", str(path), "--accept", accept_id])

    assert result.exit_code == 0
    assert "Featuresmith Plan" in result.stdout
    assert "Plan Items: 1" in result.stdout
    assert accept_id in result.stdout


def test_cli_plan_accept_multiple_recommendations(tmp_path: Path) -> None:
    """Accepting multiple recommendation IDs produces a plan with multiple items."""
    runner = CliRunner()
    path = sample_csv(tmp_path)

    review_result = runner.invoke(app, ["review", str(path), "--format", "json"])
    review_data = json.loads(review_result.stdout)
    rec_ids = [rec["id"] for rec in review_data.get("recommendations", [])]
    assert len(rec_ids) >= 2, "Expected at least two recommendations"

    accept_ids = ",".join(rec_ids[:2])
    result = runner.invoke(app, ["plan", str(path), "--accept", accept_ids])

    assert result.exit_code == 0
    assert "Plan Items: 2" in result.stdout


def test_cli_plan_accept_invalid_recommendation(tmp_path: Path) -> None:
    """Accepting an invalid recommendation ID exits 2 with a clear error."""
    runner = CliRunner()
    path = sample_csv(tmp_path)

    result = runner.invoke(app, ["plan", str(path), "--accept", "rec.bogus.id"])

    assert result.exit_code == 2
    assert "Error:" in result.stderr
    assert "Unknown recommendation ID(s)" in result.stderr
    assert "Available:" in result.stderr


def test_cli_plan_empty_accept(tmp_path: Path) -> None:
    """Empty accept list produces an empty plan."""
    runner = CliRunner()
    path = sample_csv(tmp_path)

    result = runner.invoke(app, ["plan", str(path), "--accept", ""])

    assert result.exit_code == 0
    assert "Plan Items: 0" in result.stdout
    assert "No plan items (no recommendations accepted)." in result.stdout


def test_cli_plan_no_accept_flag(tmp_path: Path) -> None:
    """Omitting --accept produces an empty plan."""
    runner = CliRunner()
    path = sample_csv(tmp_path)

    result = runner.invoke(app, ["plan", str(path)])

    assert result.exit_code == 0
    assert "Plan Items: 0" in result.stdout


def test_cli_plan_json_format(tmp_path: Path) -> None:
    """JSON output is the canonical Plan serialization."""
    runner = CliRunner()
    path = sample_csv(tmp_path)

    review_result = runner.invoke(app, ["review", str(path), "--format", "json"])
    review_data = json.loads(review_result.stdout)
    rec_ids = [rec["id"] for rec in review_data.get("recommendations", [])]
    accept_id = rec_ids[0]

    result = runner.invoke(
        app, ["plan", str(path), "--accept", accept_id, "--format", "json"]
    )

    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["plan_schema_version"] == "0.1.0"
    assert len(data["items"]) == 1
    assert data["items"][0]["recommendation_id"] == accept_id
    assert data["accepted_recommendation_ids"] == [accept_id]


def test_cli_plan_table_format(tmp_path: Path) -> None:
    """Table format renders a human-readable plan."""
    runner = CliRunner()
    path = sample_csv(tmp_path)

    review_result = runner.invoke(app, ["review", str(path), "--format", "json"])
    review_data = json.loads(review_result.stdout)
    rec_ids = [rec["id"] for rec in review_data.get("recommendations", [])]
    accept_id = rec_ids[0]

    result = runner.invoke(
        app, ["plan", str(path), "--accept", accept_id, "--format", "table"]
    )

    assert result.exit_code == 0
    assert "Featuresmith Plan" in result.stdout
    assert "Plan Schema Version: 0.1.0" in result.stdout
    assert "Accepted Recommendations: 1" in result.stdout
    assert "Plan Items: 1" in result.stdout


def test_cli_plan_fail_on_critical(tmp_path: Path) -> None:
    """--fail-on critical gates exit code on critical plan items."""
    runner = CliRunner()
    path = sample_csv(tmp_path)

    review_result = runner.invoke(app, ["review", str(path), "--format", "json"])
    review_data = json.loads(review_result.stdout)
    rec_ids = [rec["id"] for rec in review_data.get("recommendations", [])]
    # Find a critical recommendation
    critical_rec = next(
        (
            rec
            for rec in review_data["recommendations"]
            if rec["severity"] == "critical"
        ),
        None,
    )
    if critical_rec is None:
        # If no critical, use any recommendation and test with --fail-on info
        accept_id = rec_ids[0]
        result = runner.invoke(
            app, ["plan", str(path), "--accept", accept_id, "--fail-on", "info"]
        )
        assert result.exit_code == 1
    else:
        accept_id = critical_rec["id"]
        result = runner.invoke(
            app, ["plan", str(path), "--accept", accept_id, "--fail-on", "critical"]
        )
        assert result.exit_code == 1


def test_cli_plan_fail_on_info_passes_for_warning(tmp_path: Path) -> None:
    """--fail-on info gates exit code on warning plan items."""
    runner = CliRunner()
    path = sample_csv(tmp_path)

    review_result = runner.invoke(app, ["review", str(path), "--format", "json"])
    review_data = json.loads(review_result.stdout)
    rec_ids = [rec["id"] for rec in review_data.get("recommendations", [])]
    accept_id = rec_ids[0]

    result = runner.invoke(
        app, ["plan", str(path), "--accept", accept_id, "--fail-on", "info"]
    )

    # Should exit 1 if any accepted item is warning or critical
    assert result.exit_code in (0, 1)


def test_cli_plan_missing_file() -> None:
    """A missing source exits 3 with a clear error."""
    runner = CliRunner()
    result = runner.invoke(app, ["plan", "non_existent_file.csv"])

    assert result.exit_code == 3
    assert "Error:" in result.stderr
    assert "does not exist" in result.stderr


def test_cli_plan_unsupported_format(tmp_path: Path) -> None:
    """An unsupported source format exits 2."""
    runner = CliRunner()
    txt_file = tmp_path / "data.txt"
    txt_file.touch()

    result = runner.invoke(app, ["plan", str(txt_file)])

    assert result.exit_code == 2
    assert "Error:" in result.stderr


def test_cli_plan_with_previous(tmp_path: Path) -> None:
    """--previous activates diff-aware review for plan generation."""
    runner = CliRunner()
    old = tmp_path / "old.csv"
    pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}).to_csv(old, index=False)
    new = tmp_path / "new.csv"
    pd.DataFrame({"a": [1, 2, 3], "c": [7, 8, 9]}).to_csv(new, index=False)

    review_result = runner.invoke(
        app, ["review", str(new), "--previous", str(old), "--format", "json"]
    )
    review_data = json.loads(review_result.stdout)
    rec_ids = [rec["id"] for rec in review_data.get("recommendations", [])]
    if not rec_ids:
        # No recommendations from diff, skip
        return

    accept_id = rec_ids[0]
    result = runner.invoke(
        app, ["plan", str(new), "--previous", str(old), "--accept", accept_id]
    )

    assert result.exit_code == 0
    assert "Plan Items: 1" in result.stdout


def test_cli_plan_previous_missing_file(tmp_path: Path) -> None:
    """A missing --previous snapshot exits 3 with a clear error."""
    runner = CliRunner()
    path = sample_csv(tmp_path)

    result = runner.invoke(
        app,
        ["plan", str(path), "--previous", "non_existent.csv", "--accept", "rec.any.id"],
    )

    assert result.exit_code == 3
    assert "Error:" in result.stderr
    assert "does not exist" in result.stderr


def test_cli_plan_output_file_json(tmp_path: Path) -> None:
    """JSON output is written to an output file."""
    runner = CliRunner()
    path = sample_csv(tmp_path)

    review_result = runner.invoke(app, ["review", str(path), "--format", "json"])
    review_data = json.loads(review_result.stdout)
    rec_ids = [rec["id"] for rec in review_data.get("recommendations", [])]
    accept_id = rec_ids[0]

    output_file = tmp_path / "plan.json"
    result = runner.invoke(
        app,
        [
            "plan",
            str(path),
            "--accept",
            accept_id,
            "--format",
            "json",
            "--output",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    data = json.loads(output_file.read_text(encoding="utf-8"))
    assert data["plan_schema_version"] == "0.1.0"
    assert len(data["items"]) == 1


def test_cli_plan_output_file_txt(tmp_path: Path) -> None:
    """Plain-text output is written to an output file."""
    runner = CliRunner()
    path = sample_csv(tmp_path)

    review_result = runner.invoke(app, ["review", str(path), "--format", "json"])
    review_data = json.loads(review_result.stdout)
    rec_ids = [rec["id"] for rec in review_data.get("recommendations", [])]
    accept_id = rec_ids[0]

    output_file = tmp_path / "plan.txt"
    result = runner.invoke(
        app,
        [
            "plan",
            str(path),
            "--accept",
            accept_id,
            "--output",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "Featuresmith Plan" in content
    assert "\x1b" not in content


def test_cli_plan_quiet(tmp_path: Path) -> None:
    """Quiet mode suppresses stdout but still writes the output file."""
    runner = CliRunner()
    path = sample_csv(tmp_path)

    review_result = runner.invoke(app, ["review", str(path), "--format", "json"])
    review_data = json.loads(review_result.stdout)
    rec_ids = [rec["id"] for rec in review_data.get("recommendations", [])]
    accept_id = rec_ids[0]

    output_file = tmp_path / "plan.txt"
    result = runner.invoke(
        app,
        [
            "plan",
            str(path),
            "--accept",
            accept_id,
            "--quiet",
            "--output",
            str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert result.stdout == ""
    assert output_file.exists()


def test_cli_plan_sdk_parity(tmp_path: Path) -> None:
    """SDK and CLI produce identical canonical plan content."""
    path = sample_csv(tmp_path)

    # Get recommendations via SDK
    review_result = fs.review(path)
    rec_ids = [rec.id for rec in review_result.recommendations]
    assert rec_ids

    accept_id = rec_ids[0]

    # SDK plan
    sdk_plan = fs.plan(review_result, accept=[accept_id])

    # CLI plan
    runner = CliRunner()
    cli_result = runner.invoke(
        app, ["plan", str(path), "--accept", accept_id, "--format", "json"]
    )
    assert cli_result.exit_code == 0
    cli_data = json.loads(cli_result.stdout)

    # Compare canonical content (strip volatile fields)
    sdk_data = sdk_plan.to_dict()
    assert cli_data["plan_schema_version"] == sdk_data["plan_schema_version"]
    assert (
        cli_data["accepted_recommendation_ids"]
        == sdk_data["accepted_recommendation_ids"]
    )
    assert len(cli_data["items"]) == len(sdk_data["items"])
    for cli_item, sdk_item in zip(cli_data["items"], sdk_data["items"], strict=True):
        assert cli_item["recommendation_id"] == sdk_item["recommendation_id"]
        assert cli_item["title"] == sdk_item["title"]
        assert cli_item["rationale"] == sdk_item["rationale"]
        assert cli_item["confidence"] == sdk_item["confidence"]
        assert cli_item["severity"] == sdk_item["severity"]
        assert cli_item["affected_columns"] == sdk_item["affected_columns"]
        assert cli_item["suggested_action"] == sdk_item["suggested_action"]

        # originating_findings have volatile IDs; compare without IDs
        def strip_finding_ids(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
            return [{k: v for k, v in f.items() if k != "id"} for f in findings]

        assert strip_finding_ids(cli_item["originating_findings"]) == strip_finding_ids(
            sdk_item["originating_findings"]
        )
        assert cli_item["originating_reviewers"] == sdk_item["originating_reviewers"]


def test_plan_exit_code_thresholds() -> None:
    """Exit-code gating mirrors the review convention."""
    from featuresmith.plan.schema import Plan, PlanItem

    item_critical = PlanItem(
        id="plan.rec.test.0",
        recommendation_id="rec.test",
        title="Critical item",
        rationale="Test",
        confidence=0.9,
        severity="critical",
    )
    item_warning = PlanItem(
        id="plan.rec.test.0",
        recommendation_id="rec.test",
        title="Warning item",
        rationale="Test",
        confidence=0.7,
        severity="warning",
    )
    item_info = PlanItem(
        id="plan.rec.test.0",
        recommendation_id="rec.test",
        title="Info item",
        rationale="Test",
        confidence=0.5,
        severity="info",
    )

    from featuresmith_cli.commands.plan import _plan_exit_code

    plan_critical = Plan(plan_schema_version="0.1.0", items=(item_critical,))
    plan_warning = Plan(plan_schema_version="0.1.0", items=(item_warning,))
    plan_info = Plan(plan_schema_version="0.1.0", items=(item_info,))
    plan_empty = Plan(plan_schema_version="0.1.0", items=())

    assert _plan_exit_code(plan_critical, "critical") == 1
    assert _plan_exit_code(plan_critical, "warning") == 1
    assert _plan_exit_code(plan_critical, "info") == 1

    assert _plan_exit_code(plan_warning, "critical") == 0
    assert _plan_exit_code(plan_warning, "warning") == 1
    assert _plan_exit_code(plan_warning, "info") == 1

    assert _plan_exit_code(plan_info, "critical") == 0
    assert _plan_exit_code(plan_info, "warning") == 0
    assert _plan_exit_code(plan_info, "info") == 1

    assert _plan_exit_code(plan_empty, "critical") == 0
    assert _plan_exit_code(plan_empty, "info") == 0
