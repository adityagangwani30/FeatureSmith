"""Rule for detecting highly correlated numeric feature pairs."""

from __future__ import annotations

from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.rules.base import BaseRule


class HighCorrelationRule(BaseRule):
    """Flags pairs of numeric columns with Pearson correlation exceeding a threshold."""

    def __init__(self, threshold: float = 0.90) -> None:
        """Initialize the high correlation rule.

        Args:
            threshold: Pearson correlation coefficient threshold (0.0 to 1.0).
        """
        self.threshold = threshold

    @property
    def id(self) -> str:
        return "statistical.high_correlation"

    @property
    def name(self) -> str:
        return "High Correlation"

    @property
    def description(self) -> str:
        return "Detects numeric feature pairs with high linear correlation (Pearson)."

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
        pearson = profile.correlation_summary.pearson

        columns = list(pearson.keys())
        for i, col1 in enumerate(columns):
            for col2 in columns[i + 1 :]:
                corr = pearson[col1].get(col2)
                if corr is not None and abs(corr) >= self.threshold:
                    findings.append(
                        RuleFinding(
                            rule_id=self.id,
                            rule_name=self.name,
                            category=self.category,
                            severity=self.severity,
                            column_name=col1,  # Primary column is col1
                            title=f"High correlation between '{col1}' and '{col2}'",
                            description=(
                                f"Columns '{col1}' and '{col2}' are highly correlated "
                                f"with a Pearson correlation coefficient of {corr:.3f} "
                                f"(exceeds threshold of {self.threshold:.3f})."
                            ),
                            evidence={
                                "column_a": col1,
                                "column_b": col2,
                                "correlation": corr,
                                "threshold": self.threshold,
                            },
                            confidence=1.0,
                        )
                    )

        return findings
