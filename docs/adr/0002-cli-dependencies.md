# ADR 0002: CLI dependencies (Typer and Rich)

## Status

Accepted — Sprint 5

## Context

Sprint 5 introduces a production-ready command line interface (CLI) in `featuresmith-cli` exposing the core SDK.
The CLI requires robust argument parsing, option validation, auto-generated help documents, and interactive output capabilities.
It also requires a structured, human-readable terminal output format displaying table data, severity colors, summaries, and execution metrics.

## Decision

The `featuresmith-cli` package will depend on:

- `typer` (compatible release) as the CLI application framework, building on top of click.
- `rich` (compatible release) as the formatting engine for styled terminal tables, panels, and progression indicators.

## Alternatives considered

- Standard-library `argparse`: rejected due to verbose boilerplate, manual validation of options, and lack of built-in type-hint mapping which makes extending subcommands error-prone.
- Raw ANSI escapes: rejected because `rich` provides structured components (Table, Panel, Columns, Console output capturing) and automatic `NO_COLOR` and cross-platform terminal compatibility.

## Consequences

- The CLI surface is kept extremely thin, using Typer's type-hints to automatically parse and validate arguments.
- Terminal rendering uses desaturated theme tokens matching the desaturated product palette, and handles edge cases such as plain-text export generation automatically.
