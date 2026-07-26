"""Rule for detecting columns with missing values exceeding a threshold."""

from __future__ import annotations

from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.rules.base import BaseRule


class MissingValueThresholdRule(BaseRule):
    """Flags columns that exceed a configurable missing-value threshold."""

    def __init__(self, threshold: float = 20.0) -> None:
        """Initialize the missing value rule.

        Args:
            threshold: Missing value percentage threshold (0.0 to 100.0).

        Raises:
            ValueError: If threshold is not between 0.0 and 100.0.
        """
        if not (0.0 <= threshold <= 100.0):
            raise ValueError("threshold must be a percentage between 0.0 and 100.0.")
        self.threshold = threshold

    @property
    def id(self) -> str:
        return "quality.missing_value_threshold"

    @property
    def name(self) -> str:
        return "Missing Value Threshold"

    @property
    def description(self) -> str:
        return (
            "Detects columns where the percentage of missing values "
            "exceeds a configurable threshold."
        )

    @property
    def category(self) -> str:
        return "quality"

    @property
    def severity(self) -> str:
        return "warning"

    @property
    def enabled_by_default(self) -> bool:
        return True

    def evaluate(self, profile: ProfileResult) -> list[RuleFinding]:
        findings: list[RuleFinding] = []

        for col_name, col_prof in profile.column_profiles.items():
            if col_prof.missing_percentage > self.threshold:
                # Severity can escalate to critical if missingness is extremely high (e.g. > 50%)
                severity = (
                    "critical" if col_prof.missing_percentage > 50.0 else self.severity
                )
                findings.append(
                    RuleFinding(
                        rule_id=self.id,
                        rule_name=self.name,
                        category=self.category,
                        severity=severity,
                        column_name=col_name,
                        title=f"High missing values in column '{col_name}'",
                        description=(
                            f"Column '{col_name}' has {col_prof.missing_percentage:.2f}% "
                            f"missing values, exceeding the threshold of {self.threshold:.2f}%."
                        ),
                        evidence={
                            "missing_count": col_prof.missing_count,
                            "missing_percentage": col_prof.missing_percentage,
                            "threshold": self.threshold,
                        },
                        confidence=1.0,
                    )
                )

        return findings
