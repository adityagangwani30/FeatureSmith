"""Utility constants and helpers for the Featuresmith CLI."""

from __future__ import annotations

import re

# Mapping of severity levels to integer ranks for comparison and filtering
SEVERITY_LEVELS = {
    "info": 1,
    "warning": 2,
    "critical": 3,
}

# Regex to match ANSI escape sequences (used to strip styling for file exports)
ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from a styled terminal string.

    Args:
        text: The string containing terminal color/formatting codes.

    Returns:
        str: The raw text without escape codes.
    """
    return ANSI_ESCAPE.sub("", text)


def get_version_info() -> str:
    """Resolve and return version information for the CLI and core package.

    Returns:
        str: A formatted version string.
    """
    from featuresmith_cli import __version__ as cli_version

    try:
        from importlib.metadata import version

        core_version = version("featuresmith-core")
    except Exception:
        core_version = "0.0.4-dev"

    return f"Featuresmith CLI v{cli_version} (core v{core_version})"
