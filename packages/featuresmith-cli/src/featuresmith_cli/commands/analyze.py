"""Command handler for featuresmith analyze."""

from __future__ import annotations

import sys
import traceback
from typing import Annotated, Literal

import typer

import featuresmith.api as fs
from featuresmith.api import ConnectorError, SourceNotFoundError, SourceParseError
from featuresmith_cli.output import handle_output
from featuresmith_cli.utils import SEVERITY_LEVELS, get_version_info


def version_callback(value: bool) -> None:
    """Print the version string and exit if the flag is set.

    Args:
        value: Boolean flag value.
    """
    if value:
        typer.echo(get_version_info())
        raise typer.Exit()


def analyze_command(
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
    format: Annotated[
        Literal["table", "json"],
        typer.Option("--format", help="Output format to display."),
    ] = "table",
    output: Annotated[
        str | None,
        typer.Option(
            "--output",
            help="Path to save the output report (JSON or txt depending on format).",
        ),
    ] = None,
    severity: Annotated[
        Literal["info", "warning", "critical"],
        typer.Option(
            "--severity",
            help="Severity threshold for displayed findings and exit-code gating.",
        ),
    ] = "critical",
    max_correlation_columns: Annotated[
        int,
        typer.Option(
            "--max-correlation-columns",
            help="Combinatorial cutoff limit for correlation profiling.",
        ),
    ] = 100,
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
    """Analyze a local tabular dataset and evaluate quality rules."""
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

        # 3. Call core analyze SDK
        result = fs.analyze(
            dataset,
            target_column=target,
            max_correlation_columns=max_correlation_columns,
        )

        # 4. Process and dispatch output formatting
        handle_output(
            result=result,
            format_type=format.lower(),
            severity_threshold=severity.lower(),
            output_path=output,
            quiet=quiet,
        )

        # 5. Evaluate exit codes based on severity threshold filter
        threshold_rank = SEVERITY_LEVELS.get(severity.lower(), 1)
        has_matched_findings = any(
            SEVERITY_LEVELS.get(finding.severity.lower(), 1) >= threshold_rank
            for finding in result.findings
        )

        if has_matched_findings:
            raise typer.Exit(code=1)
        else:
            raise typer.Exit(code=0)

    except typer.Exit:
        # Re-raise Typer Exit exceptions to let Click handle exits
        raise
    except Exception as error:
        if verbose:
            traceback.print_exc()
        else:
            sys.stderr.write(f"Unexpected internal error: {error}\n")
        raise typer.Exit(code=4) from error
