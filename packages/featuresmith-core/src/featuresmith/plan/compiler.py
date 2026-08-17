"""Plan compiler: builds a deterministic Plan from accepted recommendations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from featuresmith.plan.schema import Plan, PlanItem
from featuresmith.recommendation.schema import Recommendation

if TYPE_CHECKING:
    from featuresmith.review.schema import ReviewResult

PLAN_SCHEMA_VERSION = "0.1.0"


def compile_plan(
    review_result: ReviewResult,
    accepted_recommendation_ids: list[str],
) -> Plan:
    """Compile a Plan from a ReviewResult and a list of accepted recommendation IDs.

    Args:
        review_result: The ReviewResult containing recommendations.
        accepted_recommendation_ids: List of recommendation IDs to include in the Plan.

    Returns:
        A deterministic Plan with items corresponding to the accepted recommendations.

    Raises:
        ValueError: If any accepted_recommendation_id is not found in the review's recommendations.
    """
    # Build a lookup of recommendations by ID
    rec_by_id = {rec.id: rec for rec in review_result.recommendations}

    # Validate all accepted IDs exist
    missing = [rid for rid in accepted_recommendation_ids if rid not in rec_by_id]
    if missing:
        available = sorted(rec_by_id.keys())
        raise ValueError(
            f"Unknown recommendation ID(s): {missing}. Available: {available}"
        )

    # Create PlanItems in the order of accepted_recommendation_ids
    items: list[PlanItem] = []
    for idx, rec_id in enumerate(accepted_recommendation_ids):
        rec = rec_by_id[rec_id]
        item = PlanItem(
            id=f"plan.{rec_id}.{idx}",
            recommendation_id=rec.id,
            title=rec.title,
            rationale=rec.rationale,
            confidence=rec.confidence,
            severity=rec.severity,
            affected_columns=rec.affected_columns,
            suggested_action=rec.suggested_action,
            originating_findings=rec.originating_findings,
            originating_reviewers=rec.originating_reviewers,
        )
        items.append(item)

    return Plan(
        plan_schema_version=PLAN_SCHEMA_VERSION,
        items=tuple(items),
        source_review_id=None,  # Could be populated if ReviewResult had an ID
        accepted_recommendation_ids=tuple(accepted_recommendation_ids),
    )


def compile_plan_from_recommendations(
    recommendations: list[Recommendation],
    accepted_recommendation_ids: list[str],
) -> Plan:
    """Compile a Plan directly from a list of recommendations.

    This is a lower-level function that doesn't require a full ReviewResult.

    Args:
        recommendations: List of all available recommendations.
        accepted_recommendation_ids: List of recommendation IDs to include in the Plan.

    Returns:
        A deterministic Plan with items corresponding to the accepted recommendations.

    Raises:
        ValueError: If any accepted_recommendation_id is not found in the recommendations.
    """
    rec_by_id = {rec.id: rec for rec in recommendations}

    missing = [rid for rid in accepted_recommendation_ids if rid not in rec_by_id]
    if missing:
        available = sorted(rec_by_id.keys())
        raise ValueError(
            f"Unknown recommendation ID(s): {missing}. Available: {available}"
        )

    items: list[PlanItem] = []
    for idx, rec_id in enumerate(accepted_recommendation_ids):
        rec = rec_by_id[rec_id]
        item = PlanItem(
            id=f"plan.{rec_id}.{idx}",
            recommendation_id=rec.id,
            title=rec.title,
            rationale=rec.rationale,
            confidence=rec.confidence,
            severity=rec.severity,
            affected_columns=rec.affected_columns,
            suggested_action=rec.suggested_action,
            originating_findings=rec.originating_findings,
            originating_reviewers=rec.originating_reviewers,
        )
        items.append(item)

    return Plan(
        plan_schema_version=PLAN_SCHEMA_VERSION,
        items=tuple(items),
        source_review_id=None,
        accepted_recommendation_ids=tuple(accepted_recommendation_ids),
    )
