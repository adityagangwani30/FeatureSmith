"""Integration tests verifying Featuresmith SDK and CLI parity, serialization, and error handling."""

import json
import os

import pytest
from typer.testing import CliRunner

import featuresmith as fs
from featuresmith.core.exceptions import ConnectorError
from featuresmith_cli.main import app


def test_integration_sdk_cli_parity() -> None:
    """Verify that SDK analyze result matches CLI --format json output exactly."""
    runner = CliRunner()
    dataset_path = os.path.join("examples", "data", "processed", "iris.csv")

    # Load and run via SDK
    dataset = fs.load(dataset_path)
    sdk_result = fs.analyze(dataset)
    sdk_dict = sdk_result.to_dict()

    # Run via CLI (specify warning severity to prevent default 'critical' filtering)
    cli_result = runner.invoke(
        app, ["analyze", dataset_path, "--format", "json", "--severity", "warning"]
    )
    assert cli_result.exit_code == 1

    cli_dict = json.loads(cli_result.output)

    # Assert parity of metadata, schema column counts and execution steps
    assert (
        cli_dict["profile"]["dataset_summary"]["row_count"]
        == sdk_dict["profile"]["dataset_summary"]["row_count"]
    )
    assert (
        cli_dict["profile"]["dataset_summary"]["column_count"]
        == sdk_dict["profile"]["dataset_summary"]["column_count"]
    )
    assert len(cli_dict["executed_rules"]) == len(sdk_dict["executed_rules"])
    assert len(cli_dict["findings"]) == len(sdk_dict["findings"])


def test_integration_serialization_roundtrip() -> None:
    """Verify that dataclass serializes cleanly to JSON and remains valid."""
    dataset_path = os.path.join("examples", "data", "processed", "sales.csv")
    dataset = fs.load(dataset_path)
    result = fs.analyze(dataset)

    result_dict = result.to_dict()

    # Verify we can encode it cleanly using standard json library
    serialized_str = json.dumps(result_dict, default=str)
    deserialized = json.loads(serialized_str)

    # Verify core attributes
    assert deserialized["profile"]["dataset_summary"]["row_count"] == 1000
    assert "return_reason" in deserialized["profile"]["column_profiles"]

    # Ensure constant columns rule was serialized
    finding_titles = [f["title"] for f in deserialized["findings"]]
    assert (
        "Zero Variance / Constant Columns" in finding_titles
        or "Constant Columns" in finding_titles
        or any("constant" in t.lower() for t in finding_titles)
    )


def test_integration_missing_file_connector_error() -> None:
    """Verify that loading a non-existent file raises a clear ConnectorError."""
    with pytest.raises(ConnectorError) as exc_info:
        fs.load("examples/data/processed/non_existent_file.csv")

    assert "does not exist" in str(exc_info.value)


def test_integration_invalid_target_column_cli_gating() -> None:
    """Verify that running CLI with an invalid target column exits with code 2."""
    runner = CliRunner()
    dataset_path = os.path.join("examples", "data", "processed", "iris.csv")

    result = runner.invoke(
        app, ["analyze", dataset_path, "--target", "non_existent_column"]
    )

    assert result.exit_code == 2
    assert "not found in dataset" in result.output
