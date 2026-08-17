"""Recommendation Engine package for Featuresmith.

This module provides the centralized Recommendation Engine that merges findings
from all review sections into a single ranked, explainable list of recommendations.
"""

from __future__ import annotations

from featuresmith.recommendation.engine import RecommendationEngine
from featuresmith.recommendation.schema import Recommendation

__all__ = [
    "RecommendationEngine",
    "Recommendation",
]
