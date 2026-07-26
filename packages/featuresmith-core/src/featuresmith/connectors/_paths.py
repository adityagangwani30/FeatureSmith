"""Private helpers shared by local-file connectors."""

from __future__ import annotations

from pathlib import Path

from featuresmith.core.exceptions import SourceNotFoundError, UnsupportedFormatError


def validate_file_source(source: object, suffixes: tuple[str, ...]) -> Path:
    """Return a validated local file path for one of the supplied suffixes."""
    if not isinstance(source, (str, Path)):
        raise UnsupportedFormatError("Expected a local file path.")

    path = Path(source)
    if path.suffix.lower() not in suffixes:
        formats = ", ".join(suffixes)
        raise UnsupportedFormatError(
            f"Unsupported file format. Expected one of: {formats}."
        )
    if not path.exists():
        raise SourceNotFoundError(f"Source file does not exist: {path}.")
    if not path.is_file():
        raise SourceNotFoundError(f"Source path is not a file: {path}.")
    return path
