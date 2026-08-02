"""Built-in ML Readiness scoring dimensions.

The dimension set maps one-to-one onto the built-in Review Engine reviewers
implemented so far (``docs/features/ML-Readiness-Score.md`` section 7.1):
Schema Health, Missing Values, Duplicate Records, Data Types, Constant Columns,
High Cardinality, Dataset Structure, and Leakage Risk. Each dimension reads
exactly one review section; dimensions whose reviewer does not yet exist (e.g.
Feature Quality, Distribution Health, Class Balance) ship in a future sprint
once their reviewers land.
"""

from __future__ import annotations

from featuresmith.scoring.dimensions.base import SectionScoreDimension


class SchemaHealthDimension(SectionScoreDimension):
    """Scores schema health from ``review.schema.health`` findings."""

    id = "score.schema_health"
    label = "Schema Health"
    section_id = "review.schema.health"


class MissingValuesDimension(SectionScoreDimension):
    """Scores missingness from ``review.quality.missingness`` findings."""

    id = "score.missing_values"
    label = "Missing Values"
    section_id = "review.quality.missingness"


class DuplicateRecordsDimension(SectionScoreDimension):
    """Scores duplicate rows from ``review.quality.duplicates`` findings."""

    id = "score.duplicate_records"
    label = "Duplicate Records"
    section_id = "review.quality.duplicates"


class DataTypesDimension(SectionScoreDimension):
    """Scores data-type appropriateness from ``review.schema.types`` findings."""

    id = "score.data_types"
    label = "Data Types"
    section_id = "review.schema.types"


class ConstantColumnsDimension(SectionScoreDimension):
    """Scores constant columns from ``review.quality.constants`` findings."""

    id = "score.constant_columns"
    label = "Constant Columns"
    section_id = "review.quality.constants"


class HighCardinalityDimension(SectionScoreDimension):
    """Scores high cardinality from ``review.quality.cardinality`` findings."""

    id = "score.high_cardinality"
    label = "High Cardinality"
    section_id = "review.quality.cardinality"


class DatasetStructureDimension(SectionScoreDimension):
    """Scores dataset structure from basic-statistics distribution findings."""

    id = "score.dataset_structure"
    label = "Dataset Structure"
    section_id = "review.quality.basic_statistics"


class LeakageRiskDimension(SectionScoreDimension):
    """Scores leakage risk from ``review.leakage`` findings."""

    id = "score.leakage_risk"
    label = "Leakage Risk"
    section_id = "review.leakage"


def builtin_dimensions() -> tuple[SectionScoreDimension, ...]:
    """Return the default built-in scoring dimensions in a stable order.

    Returns:
        A tuple of the eight built-in scoring dimension instances.
    """
    return (
        SchemaHealthDimension(),
        MissingValuesDimension(),
        DuplicateRecordsDimension(),
        DataTypesDimension(),
        ConstantColumnsDimension(),
        HighCardinalityDimension(),
        DatasetStructureDimension(),
        LeakageRiskDimension(),
    )
