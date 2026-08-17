"""Command handler for featuresmith plan."""

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
    Plan,
    SourceNotFoundError,
    SourceParseError,
    render,
)
from featuresmith_cli.commands.analyze import version_callback
from featuresmith_cli.utils import SEVERITY_LEVELS


def _plan_exit_code(plan: Plan, fail_on: str) -> int:
    """Return the plan CLI exit code for a fail-on severity threshold.

    Mirrors the review exit-code convention: 0 when no plan item meets or
    exceeds the threshold, 1 otherwise.

    Args:
        plan: The canonical Plan.
        fail_on: Severity threshold level ("info", "warning", or "critical").

    Returns:
        The process exit code (0 or 1).
    """
    threshold_rank = SEVERITY_LEVELS.get(fail_on, 1)
    has_matched_items = any(
        SEVERITY_LEVELS.get(item.severity.lower(), 1) >= threshold_rank
        for item in plan.items
    )
    return 1 if has_matched_items else 0


def plan_command(
    source: Annotated[
        str,
        typer.Argument(
            help="Path to the local tabular dataset (CSV, Excel, or Parquet)."
        ),
    ],
    target: Annotated[
        str | None,
        typer.Option(
            "--target",
            help="Name of the target column in the dataset for leakage evaluation.",
        ),
    ] = None,
    previous: Annotated[
        str | None,
        typer.Option(
            "--previous",
            help="Path to a prior snapshot for diff-aware review.",
        ),
    ] = None,
    accept: Annotated[
        str | None,
        typer.Option(
            "--accept",
            help="Comma-separated recommendation IDs to accept into the plan.",
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
            help="Severity threshold for CI-gating exit codes, mirrors review.",
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
    """Generate a deterministic Plan from a dataset review.

    The Plan is compiled from accepted recommendations in a ReviewResult.
    Run ``featuresmith review`` first to see available recommendations and their IDs,
    then use ``--accept`` to select which recommendations to include in the Plan.
    """
    try:
        # 1. Load the dataset (performs file suffix and existence check)
        try:
            dataset = fs.load(source)
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

        # 1b. Load the previous snapshot for diff-aware review, when given
        if previous is not None:
            try:
                previous_dataset = fs.load(previous)
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
        else:
            previous_dataset = None

        # 2. Validate target column presence in schema if specified
        if target is not None:
            if target not in dataset.schema.names:
                if not quiet:
                    available = ", ".join(dataset.schema.names)
                    sys.stderr.write(
                        f"Error: Target column '{target}' not found in dataset.\n"
                    )
                    sys.stderr.write(f"Available columns: {available}\n")
                raise typer.Exit(code=2)
            if (
                previous_dataset is not None
                and target not in previous_dataset.schema.names
            ):
                if not quiet:
                    available = ", ".join(previous_dataset.schema.names)
                    sys.stderr.write(
                        f"Error: Target column '{target}' not found in previous dataset.\n"
                    )
                    sys.stderr.write(f"Available columns: {available}\n")
                raise typer.Exit(code=2)

        # 3. Run the Review Engine through the public SDK
        try:
            result = fs.review(
                dataset,
                previous=previous_dataset,
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

        # 4. Parse accepted recommendation IDs
        accepted_ids: list[str] = []
        if accept is not None:
            accepted_ids = [rid.strip() for rid in accept.split(",") if rid.strip()]

        # 5. Compile the Plan from accepted recommendations
        try:
            plan = fs.plan(result, accept=accepted_ids)
        except ValueError as error:
            if not quiet:
                sys.stderr.write(f"Error: {error}\n")
            raise typer.Exit(code=2) from error

        # 6. Render the canonical result (never reshape plan content here)
        if format.lower() == "json":
            json_str = json.dumps(plan.to_dict(), indent=2)
            if not quiet:
                sys.stdout.write(json_str + "\n")
            if output:
                Path(output).write_text(json_str, encoding="utf-8")
        else:
            text = render(plan, "console")
            if not quiet:
                sys.stdout.write(text + "\n")
            if output:
                Path(output).write_text(text, encoding="utf-8")

        # 7. CI-gating exit code, mirroring the review convention
        raise typer.Exit(code=_plan_exit_code(plan, fail_on.lower()))

    except typer.Exit:
        # Re-raise Typer Exit exceptions to let Click handle exits
        raise
    except Exception as error:
        if verbose:
            traceback.print_exc()
        else:
            sys.stderr.write(f"Unexpected internal error: {error}\n")
        raise typer.Exit(code=4) from error
