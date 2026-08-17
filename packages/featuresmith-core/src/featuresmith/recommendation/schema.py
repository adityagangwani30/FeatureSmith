"""Serializable schema for the Recommendation Engine output.

The Recommendation Engine produces a ranked list of ``Recommendation`` objects
from the findings of all review sections. Each recommendation traces back to
specific findings and reviewers, ensuring full traceability from action to
evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from featuresmith.core.rule_finding import RuleFinding


@dataclass(frozen=True, slots=True)
class Recommendation:
    """A single actionable recommendation derived from review findings.

    Attributes:
        id: Stable, namespaced identifier for this recommendation.
        title: Human-readable summary of the recommended action.
        rationale: Plain-language explanation of why this action is recommended,
            grounded in the underlying findings.
        confidence: Confidence level in this recommendation (0.0 to 1.0).
        severity: The highest severity among the contributing findings
            ("critical", "warning", "info").
        affected_columns: Columns this recommendation applies to.
        suggested_action: Concrete, executable action to take.
        accepted: Whether the user has accepted this recommendation for planning.
        originating_findings: The RuleFinding objects that produced this
            recommendation.
        originating_reviewers: The reviewer IDs that produced the originating
            findings.
    """

    id: str
    title: str
    rationale: str
    confidence: float
    severity: str
    affected_columns: tuple[str, ...] = ()
    suggested_action: str = ""
    accepted: bool = False
    originating_findings: tuple[RuleFinding, ...] = field(default_factory=tuple)
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
        """Serialize the recommendation to a dictionary of primitive values."""
        from typing import cast

        from featuresmith.core.profile_result import _asdict_custom

        return cast(dict[str, Any], _asdict_custom(self))
