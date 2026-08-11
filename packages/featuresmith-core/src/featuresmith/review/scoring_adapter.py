"""Bridge from the Review Engine to the ML Readiness Score.

The Score Adapter is the sole integration point between the Review Engine and
``featuresmith.scoring`` (``docs/features/ML-Readiness-Score.md`` section 12):
it attaches the computed score onto the frozen ``ReviewResult.score`` field
after aggregation. Scoring never bypasses the engine to read raw findings
directly, and it is never computed by the AI layer.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import replace

from featuresmith.review.schema import ReviewResult
from featuresmith.scoring.aggregator import WeightedAggregator
from featuresmith.scoring.base import ScoreDimension
from featuresmith.scoring.registry import ScoreDimensionRegistry
from featuresmith.scoring.schema import MLReadinessScore


class ScoreAdapter:
    """Attaches the ML Readiness Score to a ReviewResult.

    Args:
        dimensions: The dimensions to consider; defaults to the default
            registry's built-in set.
        weights: Optional per-dimension weight overrides keyed by dimension ID.
        registry: Optional dimension registry; mutually exclusive with
            ``dimensions``.
    """

    def __init__(
        self,
        dimensions: Sequence[ScoreDimension] | None = None,
        weights: Mapping[str, float] | None = None,
        registry: ScoreDimensionRegistry | None = None,
    ) -> None:
        """Initialize the adapter with its underlying weighted aggregator."""
        self._aggregator = WeightedAggregator(
            dimensions=dimensions,
            weights=weights,
            registry=registry,
        )

    def attach(self, result: ReviewResult) -> ReviewResult:
        """Return the review with its score attached, unchanged when no score applies.

        Args:
            result: The frozen ReviewResult.

        Returns:
            A new ReviewResult with ``score`` set, or the original result when
            no dimension is applicable to the review.
        """
        score: MLReadinessScore | None = self._aggregator.compute(result)
        if score is None:
            return result
        return replace(result, score=score)
