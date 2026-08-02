"""Explicit registry for ML Readiness scoring dimensions.

Registration is kept explicit and static in this phase; entry-point discovery
of community-contributed dimensions is a future plugin-system concern,
mirroring the reviewer and rule registries.
"""

from __future__ import annotations

from collections.abc import Iterable

from featuresmith.scoring.base import ScoreDimension


class ScoreDimensionRegistry:
    """Registry that holds all available scoring dimensions.

    Args:
        dimensions: Optional iterable of dimensions to register initially.
    """

    def __init__(self, dimensions: Iterable[ScoreDimension] = ()) -> None:
        """Initialize the registry with an optional set of initial dimensions."""
        self._dimensions: dict[str, ScoreDimension] = {}
        for dimension in dimensions:
            self.register(dimension)

    def register(self, dimension: ScoreDimension) -> None:
        """Register a scoring dimension by its stable ID.

        Args:
            dimension: The dimension instance to register.
        """
        self._dimensions[dimension.id] = dimension

    def unregister(self, dimension: ScoreDimension | str) -> None:
        """Unregister a dimension by instance or ID.

        Args:
            dimension: The dimension instance or dimension ID to unregister.
        """
        dimension_id = dimension if isinstance(dimension, str) else dimension.id
        if dimension_id in self._dimensions:
            del self._dimensions[dimension_id]

    def list_dimensions(self) -> list[ScoreDimension]:
        """List all currently registered dimensions.

        Returns:
            A list of registered dimension instances.
        """
        return list(self._dimensions.values())

    def get(self, dimension_id: str) -> ScoreDimension | None:
        """Retrieve a registered dimension by its ID.

        Args:
            dimension_id: The ID of the dimension.

        Returns:
            The registered dimension, or None if not found.
        """
        return self._dimensions.get(dimension_id)


def default_registry() -> ScoreDimensionRegistry:
    """Return the default ScoreDimensionRegistry.

    The default registry ships the built-in dimensions that map onto the
    reviewers implemented so far. Remaining dimensions (feature quality,
    distribution health, class balance) land in future sprints once their
    backing reviewers ship, registering through the same registry.
    """
    from featuresmith.scoring.dimensions import builtin_dimensions

    return ScoreDimensionRegistry(builtin_dimensions())
