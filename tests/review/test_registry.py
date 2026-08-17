"""Tests for the ReviewerRegistry."""

from __future__ import annotations

from featuresmith.review.base import BaseReviewer
from featuresmith.review.context import ReviewContext
from featuresmith.review.registry import ReviewerRegistry, default_registry
from featuresmith.review.schema import ReviewCategory, ReviewSection, Severity


class DummyReviewer(BaseReviewer):
    """A minimal reviewer used to exercise the registry."""

    def __init__(self, reviewer_id: str) -> None:
        """Create a reviewer with a fixed ID."""
        self._id = reviewer_id

    @property
    def id(self) -> str:
        """Return the reviewer ID."""
        return self._id

    @property
    def category(self) -> ReviewCategory:
        """Return the reviewer category."""
        return ReviewCategory.QUALITY

    @property
    def requires_previous_snapshot(self) -> bool:
        """Return whether a previous snapshot is required."""
        return False

    def review(self, context: ReviewContext) -> ReviewSection:
        """Produce an empty section."""
        return ReviewSection(
            id=self.id,
            title="Dummy",
            category=self.category,
            severity=Severity.PASSED,
        )


def test_registry_register_and_get() -> None:
    """Reviewers are retrievable by ID after registration."""
    registry = ReviewerRegistry()
    reviewer = DummyReviewer("review.quality.a")

    registry.register(reviewer)

    assert registry.get("review.quality.a") is reviewer


def test_registry_unregister_by_instance_and_id() -> None:
    """Unregister works with either an instance or an ID."""
    registry = ReviewerRegistry()
    reviewer = DummyReviewer("review.quality.a")
    registry.register(reviewer)

    registry.unregister(reviewer)
    assert registry.get("review.quality.a") is None

    registry.register(reviewer)
    registry.unregister("review.quality.a")
    assert registry.get("review.quality.a") is None


def test_registry_list_reviewers() -> None:
    """list_reviewers returns all registered reviewers."""
    registry = ReviewerRegistry(
        (DummyReviewer("review.quality.a"), DummyReviewer("review.quality.b"))
    )

    ids = {reviewer.id for reviewer in registry.list_reviewers()}
    assert ids == {"review.quality.a", "review.quality.b"}


def test_default_registry_ships_builtin_reviewers() -> None:
    """The default registry ships the built-in reviewer set."""
    registry = default_registry()

    ids = {reviewer.id for reviewer in registry.list_reviewers()}
    assert ids == {
        "review.schema.health",
        "review.schema.types",
        "review.quality.missingness",
        "review.quality.duplicates",
        "review.quality.constants",
        "review.quality.cardinality",
        "review.quality.basic_statistics",
        "review.quality.feature_quality",
        "review.leakage",
        "review.diff",
    }
