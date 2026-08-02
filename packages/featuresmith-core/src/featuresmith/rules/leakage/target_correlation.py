"""Target-correlation leakage detector, maturing the naive correlation rule."""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.rules.base import BaseRule
from featuresmith.rules.leakage.base import LeakagePatternDetector
from featuresmith.rules.leakage.schema import LeakageFinding

_DEFAULT_THRESHOLD = 0.99


class LeakageRuleTargetCorrelation(BaseRule):
    """Flags columns that have an extremely high correlation with the target column.

    This is the Phase 1 naive correlation-based leakage rule, preserved
    unchanged as a rule-engine rule (registered in ``rules/registry.py``) for
    backward compatibility. ``TargetCorrelationDetector`` is its matured
    successor inside the Review Engine's leakage section.
    """

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


class TargetCorrelationDetector(LeakagePatternDetector):
    """Flags columns with extreme correlation to the declared target.

    This detector matures the naive threshold check into a pattern detector: a
    perfect (or near-perfect) correlation is called a duplicate target and a
    strong correlation above the configured threshold is called potential
    target leakage, each with its own confidence level. It never runs without a
    declared target column.
    """

    def __init__(self, threshold: float = _DEFAULT_THRESHOLD) -> None:
        """Initialize the target-correlation detector.

        Args:
            threshold: Pearson correlation threshold at which a column is
                considered potentially leaked (default 0.99).
        """
        self._default_threshold = threshold

    @property
    def id(self) -> str:
        return "target_correlation"

    @property
    def name(self) -> str:
        return "Target Correlation"

    def detect(
        self,
        profile: ProfileResult,
        *,
        target_column: str | None = None,
        config: Mapping[str, Any] | None = None,
    ) -> list[LeakageFinding]:
        config = config or {}
        threshold = float(
            config.get("target_correlation_threshold", self._default_threshold)
        )
        if target_column is None:
            return []

        pearson = profile.correlation_summary.pearson
        if target_column not in pearson:
            return []

        findings: list[LeakageFinding] = []
        for col_name in pearson:
            if col_name == target_column:
                continue

            corr = pearson[col_name].get(target_column)
            if corr is None or not math.isfinite(corr):
                continue

            abs_corr = abs(corr)
            if abs_corr < threshold:
                continue

            if abs_corr >= 0.999:
                confidence, severity = 1.0, "critical"
            elif abs_corr >= 0.99:
                confidence, severity = 0.9, "critical"
            else:
                confidence, severity = 0.6, "warning"

            findings.append(
                LeakageFinding(
                    pattern=self.id,
                    column_name=col_name,
                    title=f"Potential target leakage in column '{col_name}'",
                    rationale=(
                        f"Column '{col_name}' correlates with the target "
                        f"'{target_column}' at Pearson {corr:.3f}, at or above the "
                        f"leakage threshold of {threshold:.3f}."
                    ),
                    evidence={
                        "target_column": target_column,
                        "correlation": corr,
                        "threshold": threshold,
                    },
                    confidence=confidence,
                    severity=severity,
                    suggested_action=(
                        f"Inspect where '{col_name}' originates; if it is only knowable "
                        "after the target is determined, exclude it from the feature set."
                    ),
                )
            )
        return findings
