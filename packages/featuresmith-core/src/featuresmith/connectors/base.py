"""Base contract for source connectors."""

from __future__ import annotations

from abc import ABC, abstractmethod

from featuresmith.core.dataset import Dataset


class BaseConnector(ABC):
    """Load one supported source type into the normalized :class:`Dataset`."""

    @abstractmethod
    def can_load(self, source: object) -> bool:
        """Return whether this connector supports the supplied source."""

    @abstractmethod
    def validate(self, source: object) -> None:
        """Validate a supported source or raise a typed connector error."""

    @abstractmethod
    def load(self, source: object) -> Dataset:
        """Load a validated source into a normalized dataset."""
