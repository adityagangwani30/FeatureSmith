"""Command handler for featuresmith review."""

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
    ReviewCategory,
    ReviewResult,
    SourceNotFoundError,
    SourceParseError,
    render,
)
from featuresmith_cli.commands.analyze import version_callback
from featuresmith_cli.utils import SEVERITY_LEVELS

_CATEGORY_OPTIONS = {category.value: category for category in ReviewCategory}


def _parse_categories(value: str) -> list[ReviewCategory]:
    """Parse a comma-separated ``--only`` value into reviewer categories.

    Args:
        value: Comma-separated category names.

    Returns:
        The parsed list of reviewer categories.

    Raises:
        ValueError: If any token is not a known review category.
    """
    categories: list[ReviewCategory] = []
    for token in value.split(","):
        category = _CATEGORY_OPTIONS.get(token.strip())
        if category is None:
            raise ValueError(f"Unknown review category '{token.strip()}'.")
        categories.append(category)
    return categories


def _review_exit_code(result: ReviewResult, fail_on: str) -> int:
    """Return the review CLI exit code for a fail-on severity threshold.

    Mirrors the analyze exit-code convention: 0 when no finding meets or
    exceeds the threshold, 1 otherwise.

    Args:
        result: The canonical ReviewResult.
        fail_on: Severity threshold level ("info", "warning", or "critical").

    Returns:
        The process exit code (0 or 1).
    """
    threshold_rank = SEVERITY_LEVELS.get(fail_on, 1)
    has_matched_findings = any(
        SEVERITY_LEVELS.get(finding.severity.lower(), 1) >= threshold_rank
        for section in result.sections
        for finding in section.findings
    )
    return 1 if has_matched_findings else 0


def review_command(
    source: Annotated[
        str,
        typer.Argument(
            help="Path to the local tabular dataset (CSV, Excel, or Parquet)."
        ),
    ],
    previous: Annotated[
        str | None,
        typer.Option(
            "--previous",
            help="Path to a prior snapshot for diff-aware review (not yet available).",
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
            help="Severity threshold for CI-gating exit codes, mirrors analyze.",
        ),
    ] = "critical",
    only: Annotated[
        str | None,
        typer.Option(
            "--only",
            help="Comma-separated reviewer categories to run "
            "(schema, quality, leakage, diff, feature_quality, custom).",
        ),
    ] = None,
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
    """Review a local tabular dataset through the Review Engine."""
    try:
        categories: list[ReviewCategory] | None = None
        if only is not None:
            try:
                categories = _parse_categories(only)
            except ValueError as error:
                if not quiet:
                    sys.stderr.write(f"Error: {error}\n")
                raise typer.Exit(code=2) from error

        if previous is not None:
            if not quiet:
                sys.stderr.write(
                    "Error: Diff-aware review ('--previous') is not available yet.\n"
                )
            raise typer.Exit(code=2)

        # 1. Run the Review Engine through the public SDK
        try:
            result = fs.review(source, enabled_categories=categories)
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

        # 2. Render the canonical result (never reshape review content here)
        if format.lower() == "json":
            json_str = json.dumps(result.to_dict(), indent=2)
            if not quiet:
                sys.stdout.write(json_str + "\n")
            if output:
                Path(output).write_text(json_str, encoding="utf-8")
        else:
            text = render(result, "console")
            if not quiet:
                sys.stdout.write(text + "\n")
            if output:
                Path(output).write_text(text, encoding="utf-8")

        # 3. CI-gating exit code, mirroring the analyze convention
        raise typer.Exit(code=_review_exit_code(result, fail_on.lower()))

    except typer.Exit:
        # Re-raise Typer Exit exceptions to let Click handle exits
        raise
    except Exception as error:
        if verbose:
            traceback.print_exc()
        else:
            sys.stderr.write(f"Unexpected internal error: {error}\n")
        raise typer.Exit(code=4) from error
