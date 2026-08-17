"""Serializable schema for the Plan primitive.

The Plan is the central domain primitive of the Dataset Contract lifecycle.
It represents an ordered, deterministic, inspectable set of steps derived from
accepted recommendations. Every Plan traces back to specific recommendations
and findings, ensuring full traceability from action to evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# Version of the Plan schema. Increment when the Plan/PlanItem structure changes.
PLAN_SCHEMA_VERSION = "0.1.0"


@dataclass(frozen=True, slots=True)
class PlanItem:
    """A single step in a Plan, derived from an accepted Recommendation.

    Attributes:
        id: Stable, namespaced identifier for this plan item.
        recommendation_id: The ID of the Recommendation this item was derived from.
        title: Human-readable summary of the action.
        rationale: Plain-language explanation grounded in the underlying findings.
        confidence: Confidence level inherited from the Recommendation (0.0 to 1.0).
        severity: The severity inherited from the Recommendation.
        affected_columns: Columns this plan item applies to.
        suggested_action: Concrete, executable action to take.
        originating_findings: The rule finding objects that produced the originating
            Recommendation.
        originating_reviewers: The reviewer IDs that produced the originating findings.
    """

    id: str
    recommendation_id: str
    title: str
    rationale: str
    confidence: float
    severity: str
    affected_columns: tuple[str, ...] = ()
    suggested_action: str = ""
    originating_findings: tuple[Any, ...] = field(default_factory=tuple)
    originating_reviewers: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """Validate and freeze mutable fields."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        if self.severity not in ("critical", "warning", "info"):
            raise ValueError("severity must be 'critical', 'warning', or 'info'")
        object.__setattr__(self, "affected_columns", tuple(self.affected_columns))
        object.__setattr__(
            self, "originating_findings", tuple(self.originating_findings)
        )
        object.__setattr__(
            self, "originating_reviewers", tuple(self.originating_reviewers)
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the plan item to a dictionary of primitive values."""
        from typing import cast

        from featuresmith.core.profile_result import _asdict_custom

        return cast(dict[str, Any], _asdict_custom(self))


@dataclass(frozen=True, slots=True)
class Plan:
    """A deterministic, inspectable plan derived from accepted recommendations.

    The Plan is the central domain primitive that every authoring path
    (rule-based, natural-language, future AI) converges on. It is:
    - Deterministic: same accepted recommendations always produce the same Plan
    - Inspectable: every step is readable before anything runs
    - Serializable: fully serializable with versioned schema
    - Traceable: every step traces back to originating findings and reviewers
    - AI-independent: a Plan from rules and a Plan from NL are identical objects

    Attributes:
        plan_schema_version: Version of the Plan schema.
        items: Ordered tuple of PlanItem objects.
        source_review_id: Optional identifier of the ReviewResult this Plan was derived from.
        accepted_recommendation_ids: The recommendation IDs that were accepted to create this Plan.
    """

    plan_schema_version: str
    items: tuple[PlanItem, ...] = ()
    source_review_id: str | None = None
    accepted_recommendation_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Freeze sequence fields to keep the plan immutable."""
        object.__setattr__(self, "items", tuple(self.items))
        object.__setattr__(
            self, "accepted_recommendation_ids", tuple(self.accepted_recommendation_ids)
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the plan to a dictionary of primitive values."""
        from typing import cast

        from featuresmith.core.profile_result import _asdict_custom

        return cast(dict[str, Any], _asdict_custom(self))
