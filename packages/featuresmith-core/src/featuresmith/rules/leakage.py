"""Rule for detecting potential target leakage using high correlation."""

from __future__ import annotations

from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.rules.base import BaseRule


class LeakageRuleTargetCorrelation(BaseRule):
    """Flags columns that have an extremely high correlation with the target column."""

    def __init__(
        self, target_column: str | None = None, threshold: float = 0.99
    ) -> None:
        """Initialize the target correlation leakage rule.

        Args:
            target_column: The name of the target column. If None, the rule will skip execution.
            threshold: Pearson correlation coefficient threshold (default 0.99).
        """
        self.target_column = target_column
        self.threshold = threshold

    @property
    def id(self) -> str:
        return "leakage.potential_leakage"

    @property
    def name(self) -> str:
        return "Potential Target Leakage"

    @property
    def description(self) -> str:
        return (
            "Detects columns that are extremely highly correlated with the target column, "
            "which often indicates they contain information from the future (leakage)."
        )

    @property
    def category(self) -> str:
        return "leakage"

    @property
    def severity(self) -> str:
        return "critical"

    @property
    def enabled_by_default(self) -> bool:
        return True

    def evaluate(self, profile: ProfileResult) -> list[RuleFinding]:
        findings: list[RuleFinding] = []

        if self.target_column is None:
            # Without a target column, we do not infer one, per "No target inference" requirement.
            return findings

        pearson = profile.correlation_summary.pearson

        # Verify target column is numeric/has computed correlations
        if self.target_column not in pearson:
            return findings

        for col_name in pearson:
            if col_name == self.target_column:
                continue

            corr = pearson[col_name].get(self.target_column)
            if corr is not None and abs(corr) >= self.threshold:
                findings.append(
                    RuleFinding(
                        rule_id=self.id,
                        rule_name=self.name,
                        category=self.category,
                        severity=self.severity,
                        column_name=col_name,
                        title=f"Potential target leakage in '{col_name}'",
                        description=(
                            f"Column '{col_name}' is extremely highly correlated with "
                            f"target '{self.target_column}' (Pearson correlation = {corr:.3f}, "
                            f"threshold {self.threshold:.3f}), which suggests potential target leakage."
                        ),
                        evidence={
                            "target_column": self.target_column,
                            "correlation": corr,
                            "threshold": self.threshold,
                        },
                        confidence=1.0,
                    )
                )

        return findings
