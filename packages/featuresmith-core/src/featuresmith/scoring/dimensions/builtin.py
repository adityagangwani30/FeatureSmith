"""Built-in ML Readiness scoring dimensions.

The dimension set maps to the designed 8 dimensions from
``docs/features/ML-Readiness-Score.md`` section 7.1:
Schema Health, Missing Values, Feature Quality, Distribution Health,
Class Balance, Leakage Risk, Data Quality, and Consistency.
Each dimension reads exactly one review section (or multiple for consolidated dimensions).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from featuresmith.core.rule_finding import RuleFinding
from featuresmith.scoring.base import ScoreDimension
from featuresmith.scoring.dimensions.base import (
    SectionScoreDimension,
    score_from_findings,
)
from featuresmith.scoring.schema import DimensionScore

if TYPE_CHECKING:
    from featuresmith.review.schema import ReviewResult

if TYPE_CHECKING:
    from featuresmith.review.schema import ReviewResult


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


class FeatureQualityDimension(SectionScoreDimension):
    """Scores feature quality from ``review.quality.feature_quality`` findings."""

    id = "score.feature_quality"
    label = "Feature Quality"
    section_id = "review.quality.feature_quality"


class DistributionHealthDimension(SectionScoreDimension):
    """Scores distribution health from ``review.quality.basic_statistics`` findings.

    This is a stub implementation that reads from basic_statistics section.
    When OutlierReviewer and DistributionReviewer are implemented, this dimension
    will be updated to read from their sections.
    """

    id = "score.distribution_health"
    label = "Distribution Health"
    section_id = "review.quality.basic_statistics"


class ClassBalanceDimension:
    """Scores class balance from target column statistics.

    This dimension is only applicable for classification tasks with a target column.
    It reads target column statistics from the ProfileResult directly.

    NOTE: The minority-class detector required for this dimension is not yet
    implemented (see ML-Readiness-Score.md §7.1 status table: Class Balance ❌).
    This dimension is therefore never applicable and is omitted from the aggregate
    until the detector is implemented. Per spec §7.4: "an inapplicable dimension
    must never silently count as a perfect or zero score."
    """

    id = "score.class_balance"
    label = "Class Balance"
    default_weight: float = 1.0

    def applicable(self, result: ReviewResult) -> bool:
        """Return whether this dimension applies to the given review.

        The minority-class detector is not yet implemented, so this dimension
        is never applicable. It will be enabled when the detector reads target
        column class proportions from ProfileResult.
        """
        return False

    def compute(self, result: ReviewResult) -> DimensionScore:
        """Compute the class balance score from target column statistics.

        This method should not be called since applicable() returns False.
        Included for interface completeness.
        """
        raise NotImplementedError(
            "ClassBalanceDimension.compute() should not be called; "
            "the minority-class detector is not yet implemented."
        )


class LeakageRiskDimension(SectionScoreDimension):
    """Scores leakage risk from ``review.leakage`` findings."""

    id = "score.leakage_risk"
    label = "Leakage Risk"
    section_id = "review.leakage"


class DataQualityDimension:
    """Scores data quality from duplicate rows and constant columns.

    This consolidated dimension replaces the two separate dimensions:
    DuplicateRecordsDimension and ConstantColumnsDimension.
    It reads from two review sections: duplicates and constants.
    High cardinality is scored separately in the Consistency dimension
    per the ML-Readiness-Score spec §7.1.
    """

    id = "score.data_quality"
    label = "Data Quality"
    default_weight: float = 1.0

    def applicable(self, result: ReviewResult) -> bool:
        """Return whether any of the backing sections exist."""
        section_ids = {
            "review.quality.duplicates",
            "review.quality.constants",
        }
        return any(section.id in section_ids for section in result.sections)

    def compute(self, result: ReviewResult) -> DimensionScore:
        """Compute the data quality score from duplicates and constants sections."""
        section_ids = {
            "review.quality.duplicates",
            "review.quality.constants",
        }
        all_findings: list[RuleFinding] = []
        for section in result.sections:
            if section.id in section_ids:
                all_findings.extend(section.findings)

        findings = tuple(all_findings)
        score = score_from_findings(findings)

        # Build rationale
        if not findings:
            rationale = f"{self.label} scored {score:g}/100 with no issues found."
        else:
            counts: dict[str, int] = {}
            for finding in findings:
                severity = (
                    finding.severity
                    if finding.severity in {"critical", "warning", "info"}
                    else "info"
                )
                counts[severity] = counts.get(severity, 0) + 1
            ordered = sorted(
                counts.items(),
                key=lambda item: {"critical": 30, "warning": 15, "info": 5}.get(
                    item[0], 0
                ),
                reverse=True,
            )
            summary = ", ".join(f"{count} {severity}" for severity, count in ordered)
            rationale = (
                f"{self.label} scored {score:g}/100; {len(findings)} finding(s) lowered "
                f"the score ({summary})."
            )

        # Build actions
        actions: list[str] = []
        for finding in findings:
            where = (
                f"in column '{finding.column_name}'"
                if finding.column_name is not None
                else "across the dataset"
            )
            actions.append(f"Address the flagged issue: {finding.title} ({where}).")

        return DimensionScore(
            id=self.id,
            label=self.label,
            score=score,
            weight=self.default_weight,
            rationale=rationale,
            contributing_findings=findings,
            suggested_actions=tuple(actions),
        )


class ConsistencyDimension:
    """Scores consistency from data types and cardinality.

    This consolidated dimension replaces the two separate dimensions:
    DataTypesDimension and HighCardinalityDimension (which was double-counted).
    It reads from two review sections: types and cardinality.
    """

    id = "score.consistency"
    label = "Consistency"
    default_weight: float = 1.0

    def applicable(self, result: ReviewResult) -> bool:
        """Return whether any of the backing sections exist."""
        section_ids = {"review.schema.types", "review.quality.cardinality"}
        return any(section.id in section_ids for section in result.sections)

    def compute(self, result: ReviewResult) -> DimensionScore:
        """Compute the consistency score from types and cardinality sections."""
        section_ids = {"review.schema.types", "review.quality.cardinality"}
        all_findings: list[RuleFinding] = []
        for section in result.sections:
            if section.id in section_ids:
                all_findings.extend(section.findings)

        findings = tuple(all_findings)
        score = score_from_findings(findings)

        # Build rationale
        if not findings:
            rationale = f"{self.label} scored {score:g}/100 with no issues found."
        else:
            counts: dict[str, int] = {}
            for finding in findings:
                severity = (
                    finding.severity
                    if finding.severity in {"critical", "warning", "info"}
                    else "info"
                )
                counts[severity] = counts.get(severity, 0) + 1
            ordered = sorted(
                counts.items(),
                key=lambda item: {"critical": 30, "warning": 15, "info": 5}.get(
                    item[0], 0
                ),
                reverse=True,
            )
            summary = ", ".join(f"{count} {severity}" for severity, count in ordered)
            rationale = (
                f"{self.label} scored {score:g}/100; {len(findings)} finding(s) lowered "
                f"the score ({summary})."
            )

        # Build actions
        actions: list[str] = []
        for finding in findings:
            where = (
                f"in column '{finding.column_name}'"
                if finding.column_name is not None
                else "across the dataset"
            )
            actions.append(f"Address the flagged issue: {finding.title} ({where}).")

        return DimensionScore(
            id=self.id,
            label=self.label,
            score=score,
            weight=self.default_weight,
            rationale=rationale,
            contributing_findings=findings,
            suggested_actions=tuple(actions),
        )


def builtin_dimensions() -> tuple[ScoreDimension, ...]:
    """Return the default built-in scoring dimensions in a stable order.

    Returns:
        A tuple of the eight built-in scoring dimension instances.
    """
    return (
        SchemaHealthDimension(),
        MissingValuesDimension(),
        FeatureQualityDimension(),
        DistributionHealthDimension(),
        ClassBalanceDimension(),
        LeakageRiskDimension(),
        DataQualityDimension(),
        ConsistencyDimension(),
    )
