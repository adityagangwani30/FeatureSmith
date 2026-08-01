"""Weighted aggregation of dimension scores into the overall ML Readiness Score.

The aggregation formula is the versioned, documented weighted mean from
``docs/features/ML-Readiness-Score.md`` section 8.2: the overall score is
``sum(score * weight) / sum(weight)`` over the applicable dimensions, rounded
to one decimal place. Inapplicable dimensions are omitted and the weights
renormalize automatically, so an omitted dimension never silently counts as a
perfect or zero score. When no dimension applies, no score is produced.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import replace
from typing import TYPE_CHECKING

from featuresmith.core.rule_finding import RuleFinding
from featuresmith.scoring.base import ScoreDimension
from featuresmith.scoring.dimensions import builtin_dimensions
from featuresmith.scoring.schema import DimensionScore, MLReadinessScore

if TYPE_CHECKING:
    from featuresmith.review.schema import ReviewResult

SCORING_VERSION = "0.1.0"

_SEVERITY_RANK = {"critical": 0, "warning": 1, "info": 2}


class WeightedAggregator:
    """Computes the overall ML Readiness Score from dimension scores.

    Args:
        dimensions: The dimensions to consider; defaults to the built-in set.
        weights: Optional per-dimension weight overrides keyed by dimension ID.
            Overrides replace a dimension's default weight but never change the
            aggregation formula shape.
    """

    def __init__(
        self,
        dimensions: Sequence[ScoreDimension] | None = None,
        weights: Mapping[str, float] | None = None,
    ) -> None:
        """Initialize the aggregator with dimensions and optional weights."""
        self._dimensions: tuple[ScoreDimension, ...] = tuple(
            dimensions or builtin_dimensions()
        )
        self._weights = dict(weights or {})

    def compute(self, result: ReviewResult) -> MLReadinessScore | None:
        """Compute the overall score for a review, or None when no dimension applies.

        Args:
            result: The frozen ReviewResult.

        Returns:
            The frozen MLReadinessScore, or None when no registered dimension is
            applicable to the review.
        """
        applicable = [
            dimension for dimension in self._dimensions if dimension.applicable(result)
        ]
        if not applicable:
            return None

        dim_scores: list[DimensionScore] = []
        for dimension in applicable:
            dimension_score = dimension.compute(result)
            weight = self._weights.get(dimension.id, dimension_score.weight)
            dim_scores.append(replace(dimension_score, weight=weight))

        total_weight = sum(dimension.weight for dimension in dim_scores)
        overall = round(
            sum(dimension.score * dimension.weight for dimension in dim_scores)
            / total_weight,
            1,
        )
        return MLReadinessScore(
            scoring_version=SCORING_VERSION,
            overall=overall,
            dimensions=tuple(dim_scores),
            summary=build_summary(overall, dim_scores),
            positive_findings=build_positive_findings(dim_scores),
            negative_findings=build_negative_findings(dim_scores),
        )


def compute_score(
    result: ReviewResult,
    *,
    dimensions: Sequence[ScoreDimension] | None = None,
    weights: Mapping[str, float] | None = None,
) -> MLReadinessScore | None:
    """Compute the ML Readiness Score for a review in one call.

    Args:
        result: The frozen ReviewResult.
        dimensions: Optional dimensions; defaults to the built-in set.
        weights: Optional per-dimension weight overrides.

    Returns:
        The frozen MLReadinessScore, or None when no dimension applies.
    """
    return WeightedAggregator(dimensions=dimensions, weights=weights).compute(result)


def build_summary(overall: float, dim_scores: Sequence[DimensionScore]) -> str:
    """Build a one-sentence summary of the overall score.

    Args:
        overall: The aggregated overall score.
        dim_scores: The applicable dimension scores.

    Returns:
        A deterministic plain-language sentence.
    """
    healthy = sum(1 for dimension in dim_scores if dimension.score >= 100.0)
    at_risk = len(dim_scores) - healthy
    return (
        f"Overall ML Readiness is {overall:g}/100 across {len(dim_scores)} "
        f"dimension(s); {healthy} fully healthy, {at_risk} with findings "
        "lowering the score."
    )


def build_positive_findings(dim_scores: Sequence[DimensionScore]) -> tuple[str, ...]:
    """List dimensions that scored a perfect 100.

    Args:
        dim_scores: The applicable dimension scores.

    Returns:
        One statement per fully healthy dimension.
    """
    return tuple(
        f"{dimension.label} scored 100/100 with no issues found."
        for dimension in dim_scores
        if dimension.score >= 100.0
    )


def build_negative_findings(
    dim_scores: Sequence[DimensionScore],
) -> tuple[RuleFinding, ...]:
    """Collect the findings that lowered the score, deduplicated and sorted.

    Args:
        dim_scores: The applicable dimension scores.

    Returns:
        The findings ordered by severity (critical first), then rule ID, then
        column name, then title.
    """
    findings: dict[str, RuleFinding] = {}
    for dimension in dim_scores:
        if dimension.score < 100.0:
            for finding in dimension.contributing_findings:
                findings[finding.id] = finding
    return tuple(
        sorted(
            findings.values(),
            key=lambda finding: (
                _SEVERITY_RANK.get(finding.severity, 9),
                finding.rule_id,
                finding.column_name or "",
                finding.title,
            ),
        )
    )
