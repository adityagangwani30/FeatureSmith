"""Rule for detecting numeric outliers using the Interquartile Range (IQR) method."""

from __future__ import annotations

from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.rules.base import BaseRule


class OutlierDetectionRule(BaseRule):
    """Flags numeric columns that contain values outside the IQR bounds [Q1 - 1.5*IQR, Q3 + 1.5*IQR]."""

    def __init__(self, factor: float = 1.5) -> None:
        """Initialize the outlier detection rule.

        Args:
            factor: The IQR multiplier (default 1.5).
        """
        self.factor = factor

    @property
    def id(self) -> str:
        return "statistical.outliers"

    @property
    def name(self) -> str:
        return "Outlier Detection"

    @property
    def description(self) -> str:
        return (
            "Detects columns containing numeric outliers outside "
            "the standard IQR boundaries."
        )

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

        for col_name, num_prof in profile.numeric_profiles.items():
            q1 = num_prof.q1
            q3 = num_prof.q3
            iqr = num_prof.iqr
            minimum = num_prof.minimum
            maximum = num_prof.maximum

            if (
                q1 is not None
                and q3 is not None
                and iqr is not None
                and minimum is not None
                and maximum is not None
            ):
                lower_bound = q1 - self.factor * iqr
                upper_bound = q3 + self.factor * iqr

                has_lower_outliers = minimum < lower_bound
                has_upper_outliers = maximum > upper_bound

                if has_lower_outliers or has_upper_outliers:
                    # Collect evidence
                    exceeded_bounds = []
                    if has_lower_outliers:
                        exceeded_bounds.append(
                            f"minimum ({minimum}) < lower bound ({lower_bound:.2f})"
                        )
                    if has_upper_outliers:
                        exceeded_bounds.append(
                            f"maximum ({maximum}) > upper bound ({upper_bound:.2f})"
                        )

                    exceeded_str = " and ".join(exceeded_bounds)

                    findings.append(
                        RuleFinding(
                            rule_id=self.id,
                            rule_name=self.name,
                            category=self.category,
                            severity=self.severity,
                            column_name=col_name,
                            title=f"Outliers detected in column '{col_name}'",
                            description=(
                                f"Column '{col_name}' contains values exceeding IQR bounds. "
                                f"Triggered by: {exceeded_str}."
                            ),
                            evidence={
                                "minimum": minimum,
                                "maximum": maximum,
                                "q1": q1,
                                "q3": q3,
                                "iqr": iqr,
                                "lower_bound": lower_bound,
                                "upper_bound": upper_bound,
                                "factor": self.factor,
                                "has_lower_outliers": has_lower_outliers,
                                "has_upper_outliers": has_upper_outliers,
                            },
                            confidence=1.0,
                        )
                    )

        return findings
