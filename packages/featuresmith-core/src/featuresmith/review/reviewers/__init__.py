"""Built-in reviewers for the Review Engine.

This package ships the default reviewer set described in
``docs/features/Dataset-Review-PRD.md`` section 7.1, implemented incrementally
across sprints. Sprint 2 ships the schema-health, type, missing-value,
duplicate, constant-column, high-cardinality, and basic-statistics reviewers;
Sprint 4 ships the leakage reviewer; v0.3.0 ships the diff reviewer; v0.4.0
ships the feature-quality reviewer. Outlier and distribution reviewers remain
future work.
"""

from __future__ import annotations

from featuresmith.review.base import BaseReviewer
from featuresmith.review.reviewers.basic_statistics import BasicStatisticsReviewer
from featuresmith.review.reviewers.cardinality import CardinalityReviewer
from featuresmith.review.reviewers.constants import ConstantColumnReviewer
from featuresmith.review.reviewers.diff import DiffReviewer
from featuresmith.review.reviewers.duplicates import DuplicateReviewer
from featuresmith.review.reviewers.feature_quality import FeatureQualityReviewer
from featuresmith.review.reviewers.leakage import LeakageReviewer
from featuresmith.review.reviewers.missing_value import MissingValueReviewer
from featuresmith.review.reviewers.schema_health import SchemaHealthReviewer
from featuresmith.review.reviewers.types import TypeReviewer

__all__ = [
    "BasicStatisticsReviewer",
    "CardinalityReviewer",
    "ConstantColumnReviewer",
    "DiffReviewer",
    "DuplicateReviewer",
    "FeatureQualityReviewer",
    "LeakageReviewer",
    "MissingValueReviewer",
    "SchemaHealthReviewer",
    "TypeReviewer",
    "builtin_reviewers",
]


def builtin_reviewers() -> tuple[BaseReviewer, ...]:
    """Return the default built-in reviewer instances.

    Returns:
        A tuple of reviewer instances registered by default.
    """
    return (
        SchemaHealthReviewer(),
        MissingValueReviewer(),
        DuplicateReviewer(),
        ConstantColumnReviewer(),
        CardinalityReviewer(),
        TypeReviewer(),
        BasicStatisticsReviewer(),
        LeakageReviewer(),
        DiffReviewer(),
        FeatureQualityReviewer(),
    )
