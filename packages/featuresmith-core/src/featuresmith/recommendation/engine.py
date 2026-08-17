"""Centralized Recommendation Engine for Featuresmith.

The Recommendation Engine merges findings from all review sections into a single
ranked, explainable list of recommendations. This replaces the per-reviewer
fallback formatter and ensures consistent recommendation shape, confidence
semantics, and ranking logic across all reviewer categories.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from featuresmith.core.rule_finding import RuleFinding
from featuresmith.recommendation.schema import Recommendation

if TYPE_CHECKING:
    from featuresmith.review.schema import ReviewSection

# Fixed per-severity confidence base (used when finding confidence is not available)
_SEVERITY_CONFIDENCE_BASE: Mapping[str, float] = {
    "critical": 0.9,
    "warning": 0.7,
    "info": 0.5,
}

# Per-severity rank for sorting (higher = more severe)
_SEVERITY_RANK: Mapping[str, int] = {
    "critical": 3,
    "warning": 2,
    "info": 1,
}


class RecommendationEngine:
    """Generates ranked recommendations from review findings.

    The engine collects all findings across all review sections, groups them
    by affected column and semantic similarity, and produces one recommendation
    per group. Recommendations are ranked by severity, confidence, and column
    count to surface the most impactful actions first.
    """

    def __init__(self) -> None:
        """Initialize the recommendation engine."""
        pass

    def generate(self, sections: Sequence[ReviewSection]) -> Sequence[Recommendation]:
        """Generate ranked recommendations from review sections.

        Args:
            sections: The review sections produced by dispatched reviewers.

        Returns:
            A tuple of Recommendation objects, ranked by severity (descending),
            then confidence (descending), then number of affected columns
            (descending).
        """
        # Collect all findings with their originating section/reviewer info
        all_findings: list[
            tuple[RuleFinding, str, str]
        ] = []  # (finding, section_id, reviewer_id)
        for section in sections:
            for finding in section.findings:
                all_findings.append((finding, section.id, section.id))

        if not all_findings:
            return ()

        # Group findings by column and pattern similarity
        grouped = self._group_findings(all_findings)

        # Generate one recommendation per group
        recommendations: list[Recommendation] = []
        for group in grouped:
            rec = self._create_recommendation(group)
            recommendations.append(rec)

        # Rank recommendations
        recommendations.sort(key=self._recommendation_sort_key, reverse=True)

        return tuple(recommendations)

    def _group_findings(
        self, findings: Sequence[tuple[RuleFinding, str, str]]
    ) -> list[list[tuple[RuleFinding, str, str]]]:
        """Group findings by affected column and semantic pattern.

        Findings affecting the same column with similar rule_ids are grouped
        together to produce a single recommendation per column/issue.
        """
        groups: dict[str, list[tuple[RuleFinding, str, str]]] = {}

        for finding, section_id, reviewer_id in findings:
            # Create a grouping key: column + rule category prefix
            column = finding.column_name or "dataset"
            # Use the rule_id prefix (e.g., "quality.missingness", "leakage.target_correlation")
            rule_prefix = (
                finding.rule_id.split(".")[0]
                if "." in finding.rule_id
                else finding.rule_id
            )
            key = f"{column}:{rule_prefix}"

            groups.setdefault(key, []).append((finding, section_id, reviewer_id))

        return list(groups.values())

    def _create_recommendation(
        self, group: Sequence[tuple[RuleFinding, str, str]]
    ) -> Recommendation:
        """Create a single recommendation from a group of related findings."""
        # Find the worst severity in the group
        worst_severity = max(
            (finding.severity for finding, _, _ in group),
            key=lambda s: _SEVERITY_RANK.get(s, 0),
        )

        # Compute confidence as the max of finding confidences, or severity base
        max_confidence = max(
            (finding.confidence for finding, _, _ in group),
            default=_SEVERITY_CONFIDENCE_BASE.get(worst_severity, 0.5),
        )

        # Collect affected columns
        affected_columns = tuple(
            sorted(
                {
                    finding.column_name
                    for finding, _, _ in group
                    if finding.column_name is not None
                }
            )
        )

        # Collect originating reviewers and findings
        originating_reviewers = tuple(
            sorted({reviewer_id for _, _, reviewer_id in group})
        )
        originating_findings = tuple(finding for finding, _, _ in group)

        # Generate title and rationale
        title = self._generate_title(group, worst_severity)
        rationale = self._generate_rationale(group)
        suggested_action = self._generate_action(group, worst_severity)

        # Generate stable ID from the group key
        first_finding = group[0][0]
        column = first_finding.column_name or "dataset"
        rule_prefix = (
            first_finding.rule_id.split(".")[0]
            if "." in first_finding.rule_id
            else first_finding.rule_id
        )
        rec_id = f"rec.{rule_prefix}.{column}"

        return Recommendation(
            id=rec_id,
            title=title,
            rationale=rationale,
            confidence=max_confidence,
            severity=worst_severity,
            affected_columns=affected_columns,
            suggested_action=suggested_action,
            accepted=False,
            originating_findings=originating_findings,
            originating_reviewers=originating_reviewers,
        )

    def _generate_title(
        self, group: Sequence[tuple[RuleFinding, str, str]], worst_severity: str
    ) -> str:
        """Generate a human-readable title for the recommendation."""
        first_finding = group[0][0]
        column = first_finding.column_name
        rule_name = first_finding.rule_name

        if column:
            return f"Fix {rule_name.lower()} in column '{column}'"
        return f"Fix {rule_name.lower()}"

    def _generate_rationale(self, group: Sequence[tuple[RuleFinding, str, str]]) -> str:
        """Generate a plain-language rationale from the grouped findings."""
        if len(group) == 1:
            finding = group[0][0]
            return finding.description

        # Multiple findings - combine rationales
        descriptions = [finding.description for finding, _, _ in group]
        return "Multiple related issues: " + "; ".join(descriptions)

    def _generate_action(
        self, group: Sequence[tuple[RuleFinding, str, str]], worst_severity: str
    ) -> str:
        """Generate a concrete suggested action from the grouped findings."""
        first_finding = group[0][0]
        column = first_finding.column_name
        rule_id = first_finding.rule_id

        # Action templates based on rule category
        if rule_id.startswith("quality.missingness"):
            return (
                f"Impute or drop missing values in column '{column}'."
                if column
                else "Address missing values across the dataset."
            )
        elif rule_id.startswith("quality.duplicates"):
            return "Remove duplicate rows from the dataset."
        elif rule_id.startswith("quality.constants"):
            return (
                f"Drop constant column '{column}'."
                if column
                else "Drop constant columns."
            )
        elif rule_id.startswith("quality.cardinality"):
            return (
                f"Reduce cardinality of column '{column}' (e.g., target encoding, binning)."
                if column
                else "Reduce high cardinality in categorical columns."
            )
        elif rule_id.startswith("quality.basic_statistics"):
            return (
                f"Investigate distribution of column '{column}' (skew/kurtosis)."
                if column
                else "Investigate distribution anomalies."
            )
        elif rule_id.startswith("leakage"):
            return (
                f"Remove or transform leakage column '{column}'."
                if column
                else "Remove or transform leakage features."
            )
        elif rule_id.startswith("schema.health"):
            return "Address schema issues (empty dataset, fully empty columns)."
        elif rule_id.startswith("schema.types"):
            return (
                f"Review identifier-like column '{column}'."
                if column
                else "Review data type appropriateness."
            )
        elif rule_id.startswith("quality.feature_quality"):
            return (
                f"Review low-signal column '{column}' for removal or transformation."
                if column
                else "Review low-signal features."
            )
        else:
            return f"Address the flagged issue: {first_finding.title}."

    def _recommendation_sort_key(self, rec: Recommendation) -> tuple[int, float, int]:
        """Sort key for ranking recommendations.

        Priority: severity (desc) -> confidence (desc) -> affected column count (desc)
        """
        severity_rank = _SEVERITY_RANK.get(rec.severity, 0)
        return (severity_rank, rec.confidence, len(rec.affected_columns))
