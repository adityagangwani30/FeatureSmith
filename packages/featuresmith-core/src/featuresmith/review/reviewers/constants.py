"""Reviewer for constant columns."""

from __future__ import annotations

from featuresmith.core.rule_finding import RuleFinding
from featuresmith.review.context import ReviewContext
from featuresmith.review.reviewers.base import SectionReviewer
from featuresmith.review.schema import ReviewCategory
from featuresmith.rules.constants import ConstantColumnsRule


class ConstantColumnReviewer(SectionReviewer):
    """Reviews constant columns via ``ConstantColumnsRule``."""

    @property
    def id(self) -> str:
        """Return the stable reviewer identifier."""
        return "review.quality.constants"

    @property
    def category(self) -> ReviewCategory:
        """Return the reviewer category."""
        return ReviewCategory.QUALITY

    @property
    def title(self) -> str:
        """Return the section heading."""
        return "Constant Columns"

    def _collect_findings(self, context: ReviewContext) -> list[RuleFinding]:
        """Compute constant-column findings for the context."""
        return ConstantColumnsRule().evaluate(context.profile)
