"""Base contract for source connectors."""

from __future__ import annotations

from abc import ABC, abstractmethod

from featuresmith.core.dataset import Dataset


class BaseConnector(ABC):
    """Abstract base class for all Featuresmith data connectors.

    Connectors are responsible for loading and normalizing external tabular
    sources (such as files or database connections) or in-memory representations
    into a standardized Dataset object.
    """

    @abstractmethod
    def can_load(self, source: object) -> bool:
        """Determine whether the connector supports the supplied source.

        Args:
            source: The input source object (e.g. file path or DataFrame).

        Returns:
            bool: True if this connector supports loading from the source,
                False otherwise.
        """

    @abstractmethod
    def validate(self, source: object) -> None:
        """Validate the source structurally or raise a typed connector error.

        Args:
            source: The input source object to validate.

        Raises:
            ConnectorError: If validation fails because the source is missing,
                unsupported, or invalid.
        """

    @abstractmethod
    def load(self, source: object) -> Dataset:
        """Load and normalize a validated source into a Dataset.

        Args:
            source: The input source object to load.

        Returns:
            Dataset: The loaded and normalized dataset wrapper.

        Raises:
            ConnectorError: If loading fails due to parsing or read errors.
        """
