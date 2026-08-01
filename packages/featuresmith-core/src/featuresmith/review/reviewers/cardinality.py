"""Reviewer for high-cardinality categorical columns."""

from __future__ import annotations

from featuresmith.core.rule_finding import RuleFinding
from featuresmith.review.context import ReviewContext
from featuresmith.review.reviewers.base import SectionReviewer
from featuresmith.review.schema import ReviewCategory
from featuresmith.rules.cardinality import HighCardinalityRule


class CardinalityReviewer(SectionReviewer):
    """Reviews categorical high cardinality via ``HighCardinalityRule``."""

    @property
    def id(self) -> str:
        """Return the stable reviewer identifier."""
        return "review.quality.cardinality"

    @property
    def category(self) -> ReviewCategory:
        """Return the reviewer category."""
        return ReviewCategory.QUALITY

    @property
    def title(self) -> str:
        """Return the section heading."""
        return "High Cardinality"

    def _collect_findings(self, context: ReviewContext) -> list[RuleFinding]:
        """Compute high-cardinality findings for the context."""
        config = self._config_for(context)
        rule = HighCardinalityRule(
            threshold=float(config.get("threshold", 0.50)),
            min_cardinality=int(config.get("min_cardinality", 20)),
        )
        return rule.evaluate(context.profile)
