"""Rule for detecting excessive duplicate rows."""

from __future__ import annotations

from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.rules.base import BaseRule


class DuplicateRowsRule(BaseRule):
    """Flags datasets that contain an excessive percentage of duplicate rows."""

    def __init__(self, threshold: float = 10.0) -> None:
        """Initialize the duplicate rows rule.

        Args:
            threshold: Duplicate rows percentage threshold (0 to 100).
                If a value <= 1.0 is passed, it is treated as a ratio and converted to percentage.
        """
        if 0.0 < threshold <= 1.0:
            self.threshold = threshold * 100.0
        else:
            self.threshold = threshold

    @property
    def id(self) -> str:
        return "quality.duplicate_rows"

    @property
    def name(self) -> str:
        return "Duplicate Rows"

    @property
    def description(self) -> str:
        return "Detects if the percentage of duplicate rows exceeds a threshold."

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

        summary = profile.duplicate_summary
        if summary.duplicate_percentage > self.threshold:
            findings.append(
                RuleFinding(
                    rule_id=self.id,
                    rule_name=self.name,
                    category=self.category,
                    severity=self.severity,
                    column_name=None,
                    title="Excessive duplicate rows detected",
                    description=(
                        f"The dataset contains {summary.duplicate_percentage:.2f}% duplicate rows "
                        f"({summary.duplicate_rows_count} rows), exceeding the threshold of {self.threshold:.2f}%."
                    ),
                    evidence={
                        "duplicate_rows_count": summary.duplicate_rows_count,
                        "duplicate_percentage": summary.duplicate_percentage,
                        "threshold": self.threshold,
                    },
                    confidence=1.0,
                )
            )

        return findings
