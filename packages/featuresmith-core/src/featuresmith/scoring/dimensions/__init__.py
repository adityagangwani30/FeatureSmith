"""Built-in scoring dimensions for the ML Readiness Score."""

from __future__ import annotations

from featuresmith.scoring.dimensions.base import (
    SEVERITY_DEDUCTIONS,
    SectionScoreDimension,
    build_actions,
    build_rationale,
    score_from_findings,
)
from featuresmith.scoring.dimensions.builtin import (
    ConstantColumnsDimension,
    DatasetStructureDimension,
    DataTypesDimension,
    DuplicateRecordsDimension,
    HighCardinalityDimension,
    LeakageRiskDimension,
    MissingValuesDimension,
    SchemaHealthDimension,
    builtin_dimensions,
)

__all__ = [
    "SEVERITY_DEDUCTIONS",
    "ConstantColumnsDimension",
    "DataTypesDimension",
    "DatasetStructureDimension",
    "DuplicateRecordsDimension",
    "HighCardinalityDimension",
    "LeakageRiskDimension",
    "MissingValuesDimension",
    "SchemaHealthDimension",
    "SectionScoreDimension",
    "build_actions",
    "build_rationale",
    "builtin_dimensions",
    "score_from_findings",
]
