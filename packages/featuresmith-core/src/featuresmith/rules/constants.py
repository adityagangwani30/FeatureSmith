"""Rules for constant and fully empty columns."""

from __future__ import annotations

from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.rules.base import BaseRule


class ConstantColumnsRule(BaseRule):
    """Flags columns that contain only one unique value (excluding fully empty)."""

    @property
    def id(self) -> str:
        return "quality.constant_columns"

    @property
    def name(self) -> str:
        return "Constant Columns"

    @property
    def description(self) -> str:
        return "Detects columns containing only one unique value, offering no predictive power."

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
            # A column is constant if it has only 1 unique value and is not fully empty
            if col_prof.is_constant and not col_prof.is_fully_empty:
                findings.append(
                    RuleFinding(
                        rule_id=self.id,
                        rule_name=self.name,
                        category=self.category,
                        severity=self.severity,
                        column_name=col_name,
                        title=f"Constant column '{col_name}'",
                        description=(
                            f"Column '{col_name}' contains only one unique value "
                            f"(excluding nulls) and provides no variance."
                        ),
                        evidence={
                            "is_constant": True,
                            "is_fully_empty": False,
                        },
                        confidence=1.0,
                    )
                )

        return findings


class FullyEmptyColumnsRule(BaseRule):
    """Flags columns that contain only missing (null) values."""

    @property
    def id(self) -> str:
        return "quality.fully_empty_columns"

    @property
    def name(self) -> str:
        return "Fully Empty Columns"

    @property
    def description(self) -> str:
        return "Detects columns containing only null values."

    @property
    def category(self) -> str:
        return "quality"

    @property
    def severity(self) -> str:
        return "critical"

    @property
    def enabled_by_default(self) -> bool:
        return True

    def evaluate(self, profile: ProfileResult) -> list[RuleFinding]:
        findings: list[RuleFinding] = []

        for col_name, col_prof in profile.column_profiles.items():
            if col_prof.is_fully_empty:
                findings.append(
                    RuleFinding(
                        rule_id=self.id,
                        rule_name=self.name,
                        category=self.category,
                        severity=self.severity,
                        column_name=col_name,
                        title=f"Fully empty column '{col_name}'",
                        description=f"Column '{col_name}' contains only null/missing values.",
                        evidence={
                            "is_fully_empty": True,
                            "missing_percentage": 100.0,
                        },
                        confidence=1.0,
                    )
                )

        return findings
