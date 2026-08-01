"""Built-in reviewers for the Review Engine.

This package is the landing spot for the built-in reviewer set described in
``docs/features/Dataset-Review-PRD.md`` section 7.1 — SchemaHealthReviewer,
MissingValueReviewer, DuplicateRowReviewer, DuplicateColumnReviewer,
TypeReviewer, ConstantColumnReviewer, CardinalityReviewer, OutlierReviewer,
DistributionReviewer, FeatureQualityReviewer, LeakageReviewer, and
DiffReviewer. None of them are implemented yet; they land in dedicated future
sprints and register through ``featuresmith.review.registry``.
"""
