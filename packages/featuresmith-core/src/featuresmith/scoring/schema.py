"""Serializable schemas for the ML Readiness Score.

The ML Readiness Score is computed entirely from findings the Review Engine's
reviewers already produced. These models mirror ``docs/features/
ML-Readiness-Score.md`` section 8.1 and reuse the existing ``RuleFinding``
schema so every dimension's contribution traces back to an inspectable finding.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from featuresmith.core.rule_finding import RuleFinding


@dataclass(frozen=True, slots=True)
class DimensionScore:
    """The score and explanation for one scoring dimension.

    Attributes:
        id: Stable, namespaced dimension identifier (e.g. ``score.missing_values``).
        label: Human-readable dimension name (e.g. "Missing Values").
        score: The dimension score on a 0-100 scale.
        weight: The weight used when aggregating into the overall score.
        rationale: Plain-language explanation of why the dimension scored as
            it did, derived deterministically from the contributing findings.
        contributing_findings: The findings that reduced this dimension's
            score (empty when the dimension scored full marks).
        suggested_actions: Concrete, finding-derived actions that would improve
            this dimension's score.
    """

    id: str
    label: str
    score: float
    weight: float
    rationale: str
    contributing_findings: tuple[RuleFinding, ...] = ()
    suggested_actions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        """Freeze sequence fields to keep the dimension immutable."""
        object.__setattr__(
            self, "contributing_findings", tuple(self.contributing_findings)
        )
        object.__setattr__(self, "suggested_actions", tuple(self.suggested_actions))

    def to_dict(self) -> dict[str, Any]:
        """Serialize the dimension to a dictionary of primitive values.

        Returns:
            A dictionary representation suitable for JSON serialization.
        """
        from typing import cast

        from featuresmith.core.profile_result import _asdict_custom

        return cast(dict[str, Any], _asdict_custom(self))


@dataclass(frozen=True, slots=True)
class MLReadinessScore:
    """The versioned, explainable overall ML Readiness Score.

    Attributes:
        scoring_version: Version of the scoring formula (dimension list,
            default weights, and per-dimension scoring function) that produced
            this score. Separate from the Review Engine version because the
            formula can evolve independently of the engine.
        overall: The overall score on a 0-100 scale, a weighted mean of the
            applicable dimension scores.
        dimensions: The scores of the applicable dimensions that contributed
            to the overall score.
        summary: A short, plain-language explanation of the overall score.
        positive_findings: Human-readable statements for dimensions that scored
            a perfect 100 with no issues found.
        negative_findings: The findings that lowered the score across the
            applicable dimensions, deduplicated and sorted by severity.
    """

    scoring_version: str
    overall: float
    dimensions: tuple[DimensionScore, ...] = ()
    summary: str = ""
    positive_findings: tuple[str, ...] = ()
    negative_findings: tuple[RuleFinding, ...] = ()

    def __post_init__(self) -> None:
        """Freeze sequence fields to keep the score immutable."""
        object.__setattr__(self, "dimensions", tuple(self.dimensions))
        object.__setattr__(self, "positive_findings", tuple(self.positive_findings))
        object.__setattr__(self, "negative_findings", tuple(self.negative_findings))

    def to_dict(self) -> dict[str, Any]:
        """Serialize the score to a dictionary of primitive values.

        Returns:
            A dictionary representation suitable for JSON serialization.
        """
        from typing import cast

        from featuresmith.core.profile_result import _asdict_custom

        return cast(dict[str, Any], _asdict_custom(self))
