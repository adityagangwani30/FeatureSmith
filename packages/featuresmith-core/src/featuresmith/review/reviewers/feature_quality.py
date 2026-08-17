"""Reviewer for feature quality: near-constant, redundant, and low-signal columns."""

from __future__ import annotations

from featuresmith.core.rule_finding import RuleFinding
from featuresmith.review.context import ReviewContext
from featuresmith.review.reviewers.base import SectionReviewer
from featuresmith.review.schema import ReviewCategory


class FeatureQualityReviewer(SectionReviewer):
    """Reviews feature quality by detecting near-constant, redundant, and low-signal columns.

    This reviewer identifies three categories of low-quality features:
    1. Near-constant columns: numeric columns with variance below a threshold
    2. Redundant columns: pairs of numeric columns with very high correlation
    3. Low-signal columns: high-cardinality categorical columns with low target correlation
    """

    @property
    def id(self) -> str:
        """Return the stable reviewer identifier."""
        return "review.quality.feature_quality"

    @property
    def category(self) -> ReviewCategory:
        """Return the reviewer category."""
        return ReviewCategory.QUALITY

    @property
    def title(self) -> str:
        """Return the section heading."""
        return "Feature Quality"

    def _collect_findings(self, context: ReviewContext) -> list[RuleFinding]:
        """Compute feature quality findings for the context."""
        config = self._config_for(context)
        variance_threshold = float(config.get("variance_threshold", 1e-10))
        correlation_threshold = float(config.get("correlation_threshold", 0.95))
        min_target_correlation = float(config.get("min_target_correlation", 0.05))

        findings: list[RuleFinding] = []

        # 1. Near-constant columns (low variance)
        findings.extend(self._detect_near_constant_columns(context, variance_threshold))

        # 2. Redundant columns (high pairwise correlation)
        findings.extend(self._detect_redundant_columns(context, correlation_threshold))

        # 3. Low-signal columns (high cardinality + low target correlation)
        if context.config.target_column:
            findings.extend(
                self._detect_low_signal_columns(context, min_target_correlation)
            )

        return findings

    def _detect_near_constant_columns(
        self, context: ReviewContext, variance_threshold: float
    ) -> list[RuleFinding]:
        """Detect numeric columns with variance below threshold."""
        findings: list[RuleFinding] = []

        for col_name, num_prof in context.profile.numeric_profiles.items():
            # Skip fully empty columns (handled by schema health reviewer)
            if num_prof.count == 0:
                continue

            # Check if variance is below threshold (near-constant)
            if num_prof.variance is not None and num_prof.variance < variance_threshold:
                findings.append(
                    RuleFinding(
                        rule_id=f"{self.id}.near_constant",
                        rule_name="Near-Constant Column",
                        category=self.category.value,
                        severity="warning",
                        column_name=col_name,
                        title=f"Near-constant column '{col_name}'",
                        description=(
                            f"Column '{col_name}' has variance {num_prof.variance:.2e}, "
                            f"below the threshold of {variance_threshold:.2e}. "
                            f"It provides minimal predictive signal."
                        ),
                        evidence={
                            "variance": num_prof.variance,
                            "threshold": variance_threshold,
                            "unique_count": num_prof.unique_count,
                            "count": num_prof.count,
                        },
                        confidence=0.9,
                    )
                )

        return findings

    def _detect_redundant_columns(
        self, context: ReviewContext, correlation_threshold: float
    ) -> list[RuleFinding]:
        """Detect pairs of numeric columns with very high correlation."""
        findings: list[RuleFinding] = []
        pearson = context.profile.correlation_summary.pearson

        columns = list(pearson.keys())
        for i, col1 in enumerate(columns):
            for col2 in columns[i + 1 :]:
                corr = pearson[col1].get(col2)
                if corr is not None and abs(corr) >= correlation_threshold:
                    findings.append(
                        RuleFinding(
                            rule_id=f"{self.id}.redundant",
                            rule_name="Redundant Column Pair",
                            category=self.category.value,
                            severity="warning",
                            column_name=col1,
                            title=f"Redundant columns: '{col1}' and '{col2}'",
                            description=(
                                f"Columns '{col1}' and '{col2}' are highly correlated "
                                f"with Pearson correlation {corr:.3f} "
                                f"(exceeds threshold of {correlation_threshold:.3f}). "
                                f"One may be redundant for modeling."
                            ),
                            evidence={
                                "column_a": col1,
                                "column_b": col2,
                                "correlation": corr,
                                "threshold": correlation_threshold,
                            },
                            confidence=0.85,
                        )
                    )

        return findings

    def _detect_low_signal_columns(
        self, context: ReviewContext, min_target_correlation: float
    ) -> list[RuleFinding]:
        """Detect high-cardinality categorical columns with low target correlation."""
        findings: list[RuleFinding] = []

        target_column = context.config.target_column
        if not target_column:
            return findings

        # Get target column profile
        target_prof = context.profile.column_profiles.get(target_column)
        if not target_prof or target_prof.logical_type != "numeric":
            # Target correlation only makes sense for numeric targets
            return findings

        # Check categorical columns for high cardinality + low target correlation
        for col_name, cat_prof in context.profile.categorical_profiles.items():
            if col_name == target_column:
                continue

            cardinality = cat_prof.cardinality
            non_missing = (
                context.profile.dataset_summary.row_count
                - context.profile.column_profiles[col_name].missing_count
            )

            if non_missing <= 0:
                continue

            # High cardinality check
            unique_ratio = cardinality / non_missing
            if unique_ratio < 0.5 or cardinality < 20:
                continue  # Not high cardinality

            # Check correlation with target (using numeric encoding if available)
            # For categorical columns, we check if there's a numeric profile
            # that correlates with target. This is a simplified check.
            # In practice, we'd need target encoding correlation, but for now
            # we flag high-cardinality categoricals as potentially low-signal
            # when they have no strong correlation with target.

            # Get correlation with target from pearson matrix
            pearson = context.profile.correlation_summary.pearson
            target_corr = None
            if col_name in pearson and target_column in pearson[col_name]:
                target_corr = pearson[col_name][target_column]
            elif target_column in pearson and col_name in pearson[target_column]:
                target_corr = pearson[target_column][col_name]

            # If we have a direct correlation and it's low, flag as low-signal
            # If no direct correlation (categorical), flag based on cardinality alone
            if target_corr is not None:
                if abs(target_corr) < min_target_correlation:
                    findings.append(
                        RuleFinding(
                            rule_id=f"{self.id}.low_signal",
                            rule_name="Low-Signal High-Cardinality Column",
                            category=self.category.value,
                            severity="info",
                            column_name=col_name,
                            title=f"Low-signal high-cardinality column '{col_name}'",
                            description=(
                                f"Column '{col_name}' has high cardinality ({cardinality} unique values, "
                                f"{unique_ratio * 100:.1f}% ratio) but low correlation with target "
                                f"'{target_column}' ({target_corr:.3f}). "
                                f"It may not provide predictive signal."
                            ),
                            evidence={
                                "cardinality": cardinality,
                                "unique_ratio": unique_ratio,
                                "target_correlation": target_corr,
                                "min_target_correlation": min_target_correlation,
                            },
                            confidence=0.7,
                        )
                    )
            else:
                # Categorical column - flag as potentially low-signal based on cardinality
                findings.append(
                    RuleFinding(
                        rule_id=f"{self.id}.low_signal",
                        rule_name="Potentially Low-Signal High-Cardinality Column",
                        category=self.category.value,
                        severity="info",
                        column_name=col_name,
                        title=f"Potentially low-signal column '{col_name}'",
                        description=(
                            f"Column '{col_name}' has high cardinality ({cardinality} unique values, "
                            f"{unique_ratio * 100:.1f}% ratio). "
                            f"Consider target encoding or dimensionality reduction before modeling."
                        ),
                        evidence={
                            "cardinality": cardinality,
                            "unique_ratio": unique_ratio,
                            "target_column": target_column,
                        },
                        confidence=0.6,
                    )
                )

        return findings
