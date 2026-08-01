"""Reviewer for duplicate rows."""

from __future__ import annotations

from featuresmith.core.rule_finding import RuleFinding
from featuresmith.review.context import ReviewContext
from featuresmith.review.reviewers.base import SectionReviewer
from featuresmith.review.schema import ReviewCategory
from featuresmith.rules.duplicates import DuplicateRowsRule


class DuplicateReviewer(SectionReviewer):
    """Reviews duplicate rows via ``DuplicateRowsRule``."""

    @property
    def id(self) -> str:
        """Return the stable reviewer identifier."""
        return "review.quality.duplicates"

    @property
    def category(self) -> ReviewCategory:
        """Return the reviewer category."""
        return ReviewCategory.QUALITY

    @property
    def title(self) -> str:
        """Return the section heading."""
        return "Duplicate Rows"

    def _collect_findings(self, context: ReviewContext) -> list[RuleFinding]:
        """Compute duplicate-row findings for the context."""
        config = self._config_for(context)
        threshold = float(config.get("threshold", 10.0))
        return DuplicateRowsRule(threshold=threshold).evaluate(context.profile)
