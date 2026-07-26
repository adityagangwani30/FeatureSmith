"""Typed exceptions raised by Featuresmith core components."""


class ConnectorError(Exception):
    """Raised when a data source cannot be validated or loaded."""


class SourceNotFoundError(ConnectorError):
    """Raised when the target source path or file does not exist."""


class UnsupportedFormatError(ConnectorError):
    """Raised when the data source has an unsupported format or invalid type."""


class SourceParseError(ConnectorError):
    """Raised when parsing or reading the data source fails."""
