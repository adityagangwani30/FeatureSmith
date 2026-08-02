"""Main entry point for the Featuresmith CLI."""

from __future__ import annotations

import typer

from featuresmith_cli.commands.analyze import analyze_command, version_callback
from featuresmith_cli.commands.diff import diff_command
from featuresmith_cli.commands.review import review_command

# Create the Typer CLI application
app = typer.Typer(
    name="featuresmith",
    help="Featuresmith CLI: Reusable data profiling and rules engine.",
    no_args_is_help=True,
)

# Register analyze command
app.command(name="analyze")(analyze_command)

# Register review command
app.command(name="review")(review_command)

# Register diff command
app.command(name="diff")(diff_command)


# Add a top-level version callback on the CLI itself (e.g. featuresmith --version)
@app.callback()  # type: ignore[untyped-decorator]
def main(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version info and exit.",
    ),
) -> None:
    """Featuresmith command line interface."""
    pass


if __name__ == "__main__":
    app()
