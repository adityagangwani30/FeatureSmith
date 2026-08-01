"""Review Engine orchestration layer for Featuresmith.

The Review Engine sits above the Profiling Engine and Rule Engine and turns
their outputs — ``ProfileResult`` and ``RuleFinding[]`` — into one coherent,
structured review: a single entrypoint, one result object, one rendering
pipeline. See ``docs/features/Review-Engine-Architecture.md`` for the design.
"""

from featuresmith.review.aggregator import ResultAggregator
from featuresmith.review.base import BaseReviewer
from featuresmith.review.context import ReviewConfig, ReviewContext
from featuresmith.review.engine import REVIEW_ENGINE_VERSION, ReviewEngine
from featuresmith.review.registry import ReviewerRegistry, default_registry
from featuresmith.review.render import (
    BaseRenderer,
    ConsoleRenderer,
    RendererRegistry,
    render,
)
from featuresmith.review.schema import (
    ReviewCategory,
    ReviewResult,
    ReviewSection,
    Severity,
)
from featuresmith.review.scoring_adapter import ScoreAdapter

__all__ = [
    "REVIEW_ENGINE_VERSION",
    "BaseRenderer",
    "BaseReviewer",
    "ConsoleRenderer",
    "RendererRegistry",
    "ResultAggregator",
    "ReviewCategory",
    "ReviewConfig",
    "ReviewContext",
    "ReviewEngine",
    "ReviewResult",
    "ReviewSection",
    "ReviewerRegistry",
    "ScoreAdapter",
    "Severity",
    "default_registry",
    "render",
]
