"""Reviewer for data-type appropriateness."""

from __future__ import annotations

from featuresmith.core.rule_finding import RuleFinding
from featuresmith.review.context import ReviewContext
from featuresmith.review.reviewers.base import SectionReviewer
from featuresmith.review.schema import ReviewCategory


class TypeReviewer(SectionReviewer):
    """Reviews inferred data types for misuse.

    Flags numeric columns that behave like identifiers (every non-null value
    is distinct, so they carry no predictive signal) and columns classified as
    free text, which typically require dedicated text handling.
    """

    @property
    def id(self) -> str:
        """Return the stable reviewer identifier."""
        return "review.schema.types"

    @property
    def category(self) -> ReviewCategory:
        """Return the reviewer category."""
        return ReviewCategory.SCHEMA

    @property
    def title(self) -> str:
        """Return the section heading."""
        return "Data Types"

    def _collect_findings(self, context: ReviewContext) -> list[RuleFinding]:
        """Compute data-type findings for the context."""
        config = self._config_for(context)
        identifier_min_count = int(config.get("identifier_min_count", 10))
        findings: list[RuleFinding] = []
        for col_name, num_prof in context.profile.numeric_profiles.items():
            if (
                num_prof.count >= identifier_min_count
                and num_prof.unique_count == num_prof.count
            ):
                findings.append(self._identifier_finding(col_name, num_prof.count))
        for col_name, col_prof in context.profile.column_profiles.items():
            if col_prof.logical_type == "text":
                findings.append(
                    RuleFinding(
                        rule_id=self.id,
                        rule_name=self.title,
                        category=self.category.value,
                        severity="info",
                        column_name=col_name,
                        title=f"Text column '{col_name}'",
                        description=(
                            f"Column '{col_name}' is classified as free text and may "
                            "require dedicated text preprocessing before modeling."
                        ),
                        evidence={"logical_type": "text"},
                        confidence=1.0,
                    )
                )
        return findings

    def _identifier_finding(self, col_name: str, count: int) -> RuleFinding:
        """Build an identifier-like column finding."""
        return RuleFinding(
            rule_id=self.id,
            rule_name=self.title,
            category=self.category.value,
            severity="info",
            column_name=col_name,
            title=f"Identifier-like column '{col_name}'",
            description=(
                f"Column '{col_name}' is numeric but every non-null value is "
                f"distinct ({count} unique values); it likely acts as an "
                "identifier rather than a predictive feature."
            ),
            evidence={
                "unique_count": count,
                "non_missing_count": count,
                "logical_type": "numeric",
            },
            confidence=1.0,
        )
