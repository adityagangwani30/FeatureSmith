"""Extension-point interface that every reviewer implements."""

from __future__ import annotations

import abc

from featuresmith.review.context import ReviewContext
from featuresmith.review.schema import ReviewCategory, ReviewSection


class BaseReviewer(abc.ABC):
    """Abstract base class for deterministic dataset reviewers.

    A reviewer assembles one section of a review. It reads from the frozen
    ReviewContext and never mutates it; it runs deterministically and may
    compose one or more rules, or add structure (like schema health) that is
    not a single rule at all. This mirrors the plugin shape of ``BaseRule`` so
    a contributor who has written a rule already knows how to write a
    reviewer.

    Attributes:
        id: Stable, namespaced identifier of the reviewer
            (e.g. "review.quality.missingness").
        category: The reviewer category.
        requires_previous_snapshot: True only for diff-category reviewers, so
            the engine can skip them cleanly when no previous snapshot exists.
    """

    @property
    @abc.abstractmethod
    def id(self) -> str:
        """Return the stable, namespaced identifier of the reviewer."""
        pass

    @property
    @abc.abstractmethod
    def category(self) -> ReviewCategory:
        """Return the reviewer category."""
        pass

    @property
    @abc.abstractmethod
    def requires_previous_snapshot(self) -> bool:
        """Return whether this reviewer needs a previous snapshot to run."""
        pass

    def applicable(self, context: ReviewContext) -> bool:
        """Return whether this reviewer applies to the given context.

        Subclasses override this for a cheap, side-effect-free gate (for
        example, a diff reviewer returning False when no previous snapshot
        exists). The default returns True.

        Args:
            context: The frozen review context.

        Returns:
            True if the reviewer should run for this context.
        """
        return True

    @abc.abstractmethod
    def review(self, context: ReviewContext) -> ReviewSection:
        """Produce this reviewer's section for the given context.

        Args:
            context: The frozen review context.

        Returns:
            A fully-formed ReviewSection (never None).
        """
        pass
