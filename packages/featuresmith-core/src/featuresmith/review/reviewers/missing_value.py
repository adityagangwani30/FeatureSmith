"""Reviewer for missing-value health."""

from __future__ import annotations

from featuresmith.core.rule_finding import RuleFinding
from featuresmith.review.context import ReviewContext
from featuresmith.review.reviewers.base import SectionReviewer
from featuresmith.review.schema import ReviewCategory
from featuresmith.rules.missing import MissingValueThresholdRule


class MissingValueReviewer(SectionReviewer):
    """Reviews missingness per column via ``MissingValueThresholdRule``.

    Fully empty columns are intentionally excluded: they are surfaced by the
    schema health reviewer so each issue is reported exactly once.
    """

    @property
    def id(self) -> str:
        """Return the stable reviewer identifier."""
        return "review.quality.missingness"

    @property
    def category(self) -> ReviewCategory:
        """Return the reviewer category."""
        return ReviewCategory.QUALITY

    @property
    def title(self) -> str:
        """Return the section heading."""
        return "Missing Values"

    def _collect_findings(self, context: ReviewContext) -> list[RuleFinding]:
        """Compute missing-value findings, excluding fully empty columns."""
        config = self._config_for(context)
        threshold = float(config.get("threshold", 20.0))
        findings = MissingValueThresholdRule(threshold=threshold).evaluate(
            context.profile
        )
        return [
            finding
            for finding in findings
            if not self._is_fully_empty(context, finding)
        ]

    @staticmethod
    def _is_fully_empty(context: ReviewContext, finding: RuleFinding) -> bool:
        """Return whether the finding's column is fully empty."""
        column = finding.column_name
        if column is None:
            return False
        profile = context.profile.column_profiles.get(column)
        return profile is not None and profile.is_fully_empty
