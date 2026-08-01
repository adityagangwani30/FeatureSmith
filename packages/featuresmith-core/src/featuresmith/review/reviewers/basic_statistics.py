"""Reviewer for numeric distribution health based on basic statistics."""

from __future__ import annotations

from featuresmith.core.rule_finding import RuleFinding
from featuresmith.review.context import ReviewContext
from featuresmith.review.reviewers.base import SectionReviewer
from featuresmith.review.schema import ReviewCategory


class BasicStatisticsReviewer(SectionReviewer):
    """Reviews numeric column distributions through basic statistics.

    Flags highly skewed columns (warning) and columns with extreme kurtosis
    (info) using configurable thresholds.
    """

    @property
    def id(self) -> str:
        """Return the stable reviewer identifier."""
        return "review.quality.basic_statistics"

    @property
    def category(self) -> ReviewCategory:
        """Return the reviewer category."""
        return ReviewCategory.QUALITY

    @property
    def title(self) -> str:
        """Return the section heading."""
        return "Basic Statistics"

    def _collect_findings(self, context: ReviewContext) -> list[RuleFinding]:
        """Compute distribution-health findings for the context."""
        config = self._config_for(context)
        skew_threshold = float(config.get("skew_threshold", 2.0))
        kurtosis_threshold = float(config.get("kurtosis_threshold", 10.0))
        findings: list[RuleFinding] = []
        for col_name, num_prof in context.profile.numeric_profiles.items():
            if (
                num_prof.skewness is not None
                and abs(num_prof.skewness) >= skew_threshold
            ):
                findings.append(
                    RuleFinding(
                        rule_id=self.id,
                        rule_name=self.title,
                        category=self.category.value,
                        severity="warning",
                        column_name=col_name,
                        title=f"High skewness in column '{col_name}'",
                        description=(
                            f"Column '{col_name}' has skewness {num_prof.skewness:.2f}, "
                            f"exceeding the threshold of {skew_threshold:.2f}."
                        ),
                        evidence={
                            "skewness": num_prof.skewness,
                            "threshold": skew_threshold,
                        },
                        confidence=1.0,
                    )
                )
            if (
                num_prof.kurtosis is not None
                and num_prof.kurtosis >= kurtosis_threshold
            ):
                findings.append(
                    RuleFinding(
                        rule_id=self.id,
                        rule_name=self.title,
                        category=self.category.value,
                        severity="info",
                        column_name=col_name,
                        title=f"High kurtosis in column '{col_name}'",
                        description=(
                            f"Column '{col_name}' has kurtosis {num_prof.kurtosis:.2f}, "
                            f"exceeding the threshold of {kurtosis_threshold:.2f}."
                        ),
                        evidence={
                            "kurtosis": num_prof.kurtosis,
                            "threshold": kurtosis_threshold,
                        },
                        confidence=1.0,
                    )
                )
        return findings
