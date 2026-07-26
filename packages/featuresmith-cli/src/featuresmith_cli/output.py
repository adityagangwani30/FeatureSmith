"""Output routing and dispatch for Featuresmith CLI results."""

from __future__ import annotations

import io
import sys
from pathlib import Path

from rich.console import Console

from featuresmith.api import RuleResult
from featuresmith_cli.json_output import format_json
from featuresmith_cli.rich_output import render_rich_report
from featuresmith_cli.utils import strip_ansi


def handle_output(
    result: RuleResult,
    format_type: str,
    severity_threshold: str,
    output_path: str | None,
    quiet: bool,
) -> None:
    """Route analysis results to stdout and/or output files.

    Args:
        result: The canonical RuleResult.
        format_type: The format type ('table' or 'json').
        severity_threshold: Findings severity threshold level.
        output_path: Optional path to save the output file to.
        quiet: Suppress stdout printing.
    """
    if format_type == "json":
        json_str = format_json(result, severity_threshold)
        if not quiet:
            sys.stdout.write(json_str + "\n")
        if output_path:
            Path(output_path).write_text(json_str, encoding="utf-8")
    else:  # table format
        # Use a StringIO buffer to capture output if quiet mode is enabled
        buffer = io.StringIO() if quiet else None
        console = Console(record=True, file=buffer, width=200)

        render_rich_report(result, severity_threshold, console)

        if output_path:
            # Capture the table output, strip colors, and save to file
            styled_text = console.export_text(clear=False)
            plain_text = strip_ansi(styled_text)
            Path(output_path).write_text(plain_text, encoding="utf-8")
