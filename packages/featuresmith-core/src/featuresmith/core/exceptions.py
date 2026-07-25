"""Typed exceptions raised by Featuresmith core components."""


class ConnectorError(Exception):
    """Raised when a data source cannot be validated or loaded."""
