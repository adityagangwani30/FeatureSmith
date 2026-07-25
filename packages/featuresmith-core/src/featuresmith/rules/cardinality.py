"""Rule for detecting categorical columns with high cardinality."""

from __future__ import annotations

from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.rules.base import BaseRule


class HighCardinalityRule(BaseRule):
    """Flags categorical columns that have an unusually high unique value ratio."""

    def __init__(self, threshold: float = 0.50, min_cardinality: int = 20) -> None:
        """Initialize the high cardinality rule.

        Args:
            threshold: Unique ratio threshold (unique count / non-missing count).
                If a value > 1.0 is passed, it is treated as a percentage and converted to ratio.
            min_cardinality: Minimum unique value count required to flag high cardinality.
        """
        if threshold > 1.0:
            self.threshold = threshold / 100.0
        else:
            self.threshold = threshold
        self.min_cardinality = min_cardinality

    @property
    def id(self) -> str:
        return "statistical.high_cardinality"

    @property
    def name(self) -> str:
        return "High Cardinality"

    @property
    def description(self) -> str:
        return "Detects categorical columns with unusually high unique value counts relative to size."

    @property
    def category(self) -> str:
        return "statistical"

    @property
    def severity(self) -> str:
        return "warning"

    @property
    def enabled_by_default(self) -> bool:
        return True

    def evaluate(self, profile: ProfileResult) -> list[RuleFinding]:
        findings: list[RuleFinding] = []

        for col_name, col_prof in profile.column_profiles.items():
            if col_prof.logical_type == "categorical":
                cat_prof = profile.categorical_profiles.get(col_name)
                if cat_prof is not None:
                    cardinality = cat_prof.cardinality
                    non_missing = (
                        profile.dataset_summary.row_count - col_prof.missing_count
                    )

                    if non_missing > 0:
                        ratio = cardinality / non_missing
                        if (
                            ratio > self.threshold
                            and cardinality >= self.min_cardinality
                        ):
                            findings.append(
                                RuleFinding(
                                    rule_id=self.id,
                                    rule_name=self.name,
                                    category=self.category,
                                    severity=self.severity,
                                    column_name=col_name,
                                    title=f"High cardinality in column '{col_name}'",
                                    description=(
                                        f"Column '{col_name}' is categorical but has a high ratio "
                                        f"of unique values: {cardinality} unique values out of "
                                        f"{non_missing} non-null rows ({ratio * 100:.2f}% ratio)."
                                    ),
                                    evidence={
                                        "cardinality": cardinality,
                                        "non_missing_count": non_missing,
                                        "unique_ratio": ratio,
                                        "threshold": self.threshold,
                                        "min_cardinality": self.min_cardinality,
                                    },
                                    confidence=1.0,
                                )
                            )

        return findings
