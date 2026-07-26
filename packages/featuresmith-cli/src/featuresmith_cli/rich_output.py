"""Rich terminal formatting for Featuresmith CLI results."""

from __future__ import annotations

import math

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from featuresmith.api import RuleResult
from featuresmith_cli.utils import SEVERITY_LEVELS


def format_size(bytes_val: int | None) -> str:
    """Format file size in human-readable bytes units.

    Args:
        bytes_val: The size in bytes.

    Returns:
        str: Format string such as '12.4 KB'.
    """
    if bytes_val is None:
        return "Unknown"
    if bytes_val == 0:
        return "0 Bytes"
    units = ["Bytes", "KB", "MB", "GB"]
    i = int(math.floor(math.log(bytes_val, 1024)))
    p = math.pow(1024, i)
    s = round(bytes_val / p, 2)
    return f"{s} {units[i]}"


def render_rich_report(
    result: RuleResult, severity_threshold: str, console: Console
) -> None:
    """Print a styled terminal report for the analysis result.

    Args:
        result: The canonical RuleResult from the SDK.
        severity_threshold: The severity level threshold to filter findings by.
        console: The rich Console to write to.
    """
    summary = result.profile.dataset_summary
    metadata = result.profile.dataset_metadata
    exec_meta = result.profile.execution_metadata

    # 1. Title Panel
    console.print(
        Panel(
            "[bold white]Featuresmith Dataset Analysis Report[/]",
            expand=False,
            style="bold blue",
        )
    )

    # 2. Dataset Summary Table
    summary_table = Table(
        title="[bold]Dataset Overview[/]", title_justify="left", show_header=False
    )
    summary_table.add_column("Metric", style="dim")
    summary_table.add_column("Value")

    source_path = metadata.source or "In-memory Dataframe"
    summary_table.add_row("Source", source_path)
    summary_table.add_row("Backend", metadata.backend)
    summary_table.add_row("Rows", f"{summary.row_count:,}")
    summary_table.add_row("Columns", f"{summary.column_count:,}")
    summary_table.add_row("Size", format_size(metadata.file_size))
    summary_table.add_row("Missing Cells", f"{summary.missing_percentage:.2f}%")
    summary_table.add_row("Duplicate Rows", f"{summary.duplicate_percentage:.2f}%")

    col_types = (
        f"Numeric: {summary.num_numeric_columns} | "
        f"Categorical: {summary.num_categorical_columns} | "
        f"Datetime: {summary.num_datetime_columns} | "
        f"Text: {summary.num_text_columns}"
    )
    summary_table.add_row("Column Types", col_types)

    console.print(summary_table)
    console.print()

    # 3. Findings Table
    findings_table = Table(
        title="[bold]Analysis Findings & Issues[/]", title_justify="left"
    )
    findings_table.add_column("Severity")
    findings_table.add_column("Column")
    findings_table.add_column("Finding", overflow="fold", min_width=24)
    findings_table.add_column("Description")
    findings_table.add_column("Evidence")

    threshold_rank = SEVERITY_LEVELS.get(severity_threshold, 1)
    findings_displayed = 0

    # Sort findings by severity level descending
    sorted_findings = sorted(
        result.findings,
        key=lambda f: SEVERITY_LEVELS.get(f.severity, 1),
        reverse=True,
    )

    for finding in sorted_findings:
        finding_rank = SEVERITY_LEVELS.get(finding.severity, 1)
        if finding_rank < threshold_rank:
            continue

        findings_displayed += 1

        # Severity Column Styling
        severity_styles = {
            "critical": "[bold red]CRITICAL[/]",
            "warning": "[bold yellow]WARNING[/]",
            "info": "[bold blue]INFO[/]",
        }
        sev_str = severity_styles.get(
            finding.severity, f"[bold blue]{finding.severity.upper()}[/]"
        )

        col_name = finding.column_name if finding.column_name else "[dim]Dataset[/]"

        # Format evidence dict
        evidence_strs = []
        for k, v in finding.evidence.items():
            if isinstance(v, float):
                evidence_strs.append(f"{k}: {v:.4f}")
            else:
                evidence_strs.append(f"{k}: {v}")
        evidence_text = ", ".join(evidence_strs)

        finding_cell = f"{finding.title}\n[dim]{finding.rule_id}[/]"
        findings_table.add_row(
            sev_str, col_name, finding_cell, finding.description, evidence_text
        )

    if findings_displayed > 0:
        console.print(findings_table)
    else:
        console.print(
            f"[dim]No quality findings discovered at or above the '{severity_threshold}' severity threshold.[/]"
        )
    console.print()

    # 4. Execution statistics & Failed Rules
    exec_table = Table(
        title="[bold]Execution Summary[/]", title_justify="left", show_header=False
    )
    exec_table.add_column("Key", style="dim")
    exec_table.add_column("Value")
    exec_table.add_row("Rules Executed", f"{len(result.executed_rules)}")
    exec_table.add_row("Run Time", f"{result.execution_time_ms:.2f} ms")
    exec_table.add_row("Start Time (UTC)", exec_meta.start_time)
    console.print(exec_table)

    if result.failed_rules:
        console.print()
        console.print("[bold yellow]Warnings (Failed Rules):[/]")
        for rule_id, error_trace in result.failed_rules.items():
            console.print(
                f" - [bold yellow]{rule_id}[/]: {error_trace.splitlines()[-1]}"
            )
