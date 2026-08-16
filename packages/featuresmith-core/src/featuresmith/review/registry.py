"""Explicit reviewer registry for the Review Engine."""

from __future__ import annotations

from collections.abc import Iterable

from featuresmith.review.base import BaseReviewer


class ReviewerRegistry:
    """Registry that holds all available reviewers for review execution.

    Registration is kept explicit and static in this phase; entry-point
    discovery is a future plugin-system concern.
    """

    def __init__(self, reviewers: Iterable[BaseReviewer] = ()) -> None:
        """Initialize the registry with an optional set of initial reviewers.

        Args:
            reviewers: Iterable of reviewer instances to register.
        """
        self._reviewers: dict[str, BaseReviewer] = {}
        for reviewer in reviewers:
            self.register(reviewer)

    def register(self, reviewer: BaseReviewer) -> None:
        """Register a new reviewer instance.

        Args:
            reviewer: An instance of a BaseReviewer subclass.
        """
        self._reviewers[reviewer.id] = reviewer

    def unregister(self, reviewer: BaseReviewer | str) -> None:
        """Unregister a reviewer by instance or ID.

        Args:
            reviewer: The reviewer instance or reviewer ID to unregister.
        """
        reviewer_id = reviewer if isinstance(reviewer, str) else reviewer.id
        if reviewer_id in self._reviewers:
            del self._reviewers[reviewer_id]

    def list_reviewers(self) -> list[BaseReviewer]:
        """List all currently registered reviewers.

        Returns:
            A list of registered reviewer instances.
        """
        return list(self._reviewers.values())

    def get(self, reviewer_id: str) -> BaseReviewer | None:
        """Retrieve a registered reviewer by its ID.

        Args:
            reviewer_id: The ID of the reviewer.

        Returns:
            The registered BaseReviewer instance, or None if not found.
        """
        return self._reviewers.get(reviewer_id)


def default_registry() -> ReviewerRegistry:
    """Return the default ReviewerRegistry.

    The default registry ships the built-in reviewers implemented so far:
    schema health, data types, missing values, duplicate rows, constant
    columns, high cardinality, basic statistics, leakage detection, and the
    diff reviewer. Remaining reviewers (outliers, distribution, feature
    quality) land in future sprints and register through the same registry.
    """
    from featuresmith.review.reviewers import builtin_reviewers

    return ReviewerRegistry(builtin_reviewers())
