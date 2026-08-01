"""ML Readiness Score — a deterministic, explainable score over a ReviewResult.

The score is computed entirely from findings the Review Engine's reviewers
already produced: every dimension reads only the review's sections, never raw
data, so a given ``ReviewResult`` always produces the same versioned score with
a full per-dimension breakdown. See ``docs/features/ML-Readiness-Score.md``.
"""

from __future__ import annotations

from featuresmith.scoring.aggregator import (
    SCORING_VERSION,
    WeightedAggregator,
    compute_score,
)
from featuresmith.scoring.base import ScoreDimension
from featuresmith.scoring.dimensions import builtin_dimensions
from featuresmith.scoring.registry import ScoreDimensionRegistry, default_registry
from featuresmith.scoring.schema import DimensionScore, MLReadinessScore

__all__ = [
    "SCORING_VERSION",
    "DimensionScore",
    "MLReadinessScore",
    "ScoreDimension",
    "ScoreDimensionRegistry",
    "WeightedAggregator",
    "builtin_dimensions",
    "compute_score",
    "default_registry",
]
