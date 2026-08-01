"""Reviewer for dataset schema health."""

from __future__ import annotations

from featuresmith.core.rule_finding import RuleFinding
from featuresmith.review.context import ReviewContext
from featuresmith.review.reviewers.base import SectionReviewer
from featuresmith.review.schema import ReviewCategory
from featuresmith.rules.constants import FullyEmptyColumnsRule


class SchemaHealthReviewer(SectionReviewer):
    """Reviews dataset-level and column-level schema health.

    Surfaces fully empty columns via ``FullyEmptyColumnsRule`` and adds
    structural findings for empty datasets and datasets with no columns.
    """

    @property
    def id(self) -> str:
        """Return the stable reviewer identifier."""
        return "review.schema.health"

    @property
    def category(self) -> ReviewCategory:
        """Return the reviewer category."""
        return ReviewCategory.SCHEMA

    @property
    def title(self) -> str:
        """Return the section heading."""
        return "Schema Health"

    def _collect_findings(self, context: ReviewContext) -> list[RuleFinding]:
        """Compute schema health findings for the context."""
        summary = context.profile.dataset_summary
        findings: list[RuleFinding] = []
        if summary.row_count == 0:
            findings.append(
                RuleFinding(
                    rule_id=self.id,
                    rule_name=self.title,
                    category=self.category.value,
                    severity="warning",
                    column_name=None,
                    title="Dataset has no rows",
                    description="The dataset contains zero rows; no data is available to review.",
                    evidence={"row_count": 0},
                    confidence=1.0,
                )
            )
        if summary.column_count == 0:
            findings.append(
                RuleFinding(
                    rule_id=self.id,
                    rule_name=self.title,
                    category=self.category.value,
                    severity="warning",
                    column_name=None,
                    title="Dataset has no columns",
                    description="The dataset declares zero columns.",
                    evidence={"column_count": 0},
                    confidence=1.0,
                )
            )
        if summary.row_count > 0:
            findings.extend(FullyEmptyColumnsRule().evaluate(context.profile))
        return findings
