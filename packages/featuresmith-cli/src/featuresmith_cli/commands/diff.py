"""Command handler for featuresmith diff."""

from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path
from typing import Annotated, Literal

import typer

import featuresmith.api as fs
from featuresmith.api import (
    ConnectorError,
    DatasetDiffResult,
    SourceNotFoundError,
    SourceParseError,
    diff_findings,
    render_diff,
)
from featuresmith_cli.commands.analyze import version_callback
from featuresmith_cli.utils import SEVERITY_LEVELS


def _diff_exit_code(result: DatasetDiffResult, fail_on: str) -> int:
    """Return the diff CLI exit code for a fail-on severity threshold.

    Mirrors the analyze/review convention: 0 when no finding meets or exceeds
    the threshold, 1 otherwise.

    Args:
        result: The canonical DatasetDiffResult.
        fail_on: Severity threshold level ("info", "warning", or "critical").

    Returns:
        The process exit code (0 or 1).
    """
    threshold_rank = SEVERITY_LEVELS.get(fail_on, 1)
    has_matched_findings = any(
        SEVERITY_LEVELS.get(finding.severity.lower(), 1) >= threshold_rank
        for finding in diff_findings(result)
    )
    return 1 if has_matched_findings else 0


def diff_command(
    old: Annotated[
        str,
        typer.Argument(
            help="Path to the older dataset snapshot (CSV, Excel, or Parquet)."
        ),
    ],
    new: Annotated[
        str,
        typer.Argument(
            help="Path to the newer dataset snapshot (CSV, Excel, or Parquet)."
        ),
    ],
    target: Annotated[
        str | None,
        typer.Option(
            "--target",
            help="Name of the target column, present in both snapshots, "
            "for the leakage comparison.",
        ),
    ] = None,
    format: Annotated[
        Literal["table", "json"],
        typer.Option("--format", help="Output format to display."),
    ] = "table",
    output: Annotated[
        str | None,
        typer.Option(
            "--output",
            help="Path to save the output report (txt or JSON depending on format).",
        ),
    ] = None,
    fail_on: Annotated[
        Literal["info", "warning", "critical"],
        typer.Option(
            "--fail-on",
            help="Severity threshold for CI-gating exit codes, mirrors analyze/review.",
        ),
    ] = "critical",
    quiet: Annotated[
        bool,
        typer.Option("--quiet", help="Suppress all standard console report output."),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            help="Show full Python tracebacks on error instead of generic messages.",
        ),
    ] = False,
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Show version info and exit.",
        ),
    ] = None,
) -> None:
    """Compare two snapshots of a dataset through the Dataset Diff Engine."""
    try:
        # 1. Load both snapshots (performs file suffix and existence check)
        try:
            old_dataset = fs.load(old)
            new_dataset = fs.load(new)
        except ConnectorError as error:
            err_msg = str(error)
            if isinstance(error, (SourceNotFoundError, SourceParseError)):
                if not quiet:
                    sys.stderr.write(f"Error: {err_msg}\n")
                raise typer.Exit(code=3) from error
            else:
                if not quiet:
                    sys.stderr.write(f"Error: {err_msg}\n")
                raise typer.Exit(code=2) from error

        # 2. Validate target column presence in both snapshots if specified
        if target is not None:
            if target not in new_dataset.schema.names:
                if not quiet:
                    available = ", ".join(new_dataset.schema.names)
                    sys.stderr.write(
                        f"Error: Target column '{target}' not found in newer dataset.\n"
                    )
                    sys.stderr.write(f"Available columns: {available}\n")
                raise typer.Exit(code=2)
            if target not in old_dataset.schema.names:
                if not quiet:
                    available = ", ".join(old_dataset.schema.names)
                    sys.stderr.write(
                        f"Error: Target column '{target}' not found in older dataset.\n"
                    )
                    sys.stderr.write(f"Available columns: {available}\n")
                raise typer.Exit(code=2)

        # 3. Run the Dataset Diff Engine through the public SDK
        try:
            result = fs.diff(
                old_dataset,
                new_dataset,
                target_column=target,
            )
        except ConnectorError as error:
            err_msg = str(error)
            if isinstance(error, (SourceNotFoundError, SourceParseError)):
                if not quiet:
                    sys.stderr.write(f"Error: {err_msg}\n")
                raise typer.Exit(code=3) from error
            else:
                if not quiet:
                    sys.stderr.write(f"Error: {err_msg}\n")
                raise typer.Exit(code=2) from error

        # 4. Render the canonical result (never reshape diff content here)
        if format.lower() == "json":
            json_str = json.dumps(result.to_dict(), indent=2)
            if not quiet:
                sys.stdout.write(json_str + "\n")
            if output:
                Path(output).write_text(json_str, encoding="utf-8")
        else:
            text = render_diff(result, "console")
            if not quiet:
                sys.stdout.write(text + "\n")
            if output:
                Path(output).write_text(text, encoding="utf-8")

        # 5. CI-gating exit code, mirroring the analyze/review convention
        raise typer.Exit(code=_diff_exit_code(result, fail_on.lower()))

    except typer.Exit:
        # Re-raise Typer Exit exceptions to let Click handle exits
        raise
    except Exception as error:
        if verbose:
            traceback.print_exc()
        else:
            sys.stderr.write(f"Unexpected internal error: {error}\n")
        raise typer.Exit(code=4) from error
