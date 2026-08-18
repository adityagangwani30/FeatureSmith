"""Comprehensive tests for FeatureQualityReviewer."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
import pytest

import featuresmith as fs
from featuresmith.core.dataset import Dataset
from featuresmith.review.context import ReviewConfig, ReviewContext
from featuresmith.review.reviewers import FeatureQualityReviewer
from featuresmith.review.schema import ReviewCategory, ReviewSection, Severity


def run_reviewer(
    reviewer: FeatureQualityReviewer, df: pd.DataFrame, **config: Any
) -> ReviewSection:
    """Run FeatureQualityReviewer against a dataframe with optional configuration."""
    dataset: Dataset = fs.load(df)
    profile = fs.profile(dataset)
    context = ReviewContext(
        profile=profile,
        dataset=dataset,
        config=ReviewConfig(
            reviewer_config={reviewer.id: config} if config else {},
            target_column=config.get("target_column"),
        ),
    )
    return reviewer.review(context)


def near_constant_df() -> pd.DataFrame:
    """DataFrame with near-constant columns (variance ~1e-12)."""
    return pd.DataFrame(
        {
            "normal_var": [1.0, 2.0, 3.0, 4.0, 5.0],
            "near_const_small": [1.0 + 1e-7 * i for i in range(5)],
            "near_const_large": [100.0 + 1e-7 * i for i in range(5)],
            "const": [42.0, 42.0, 42.0, 42.0, 42.0],
        }
    )


def redundant_df() -> pd.DataFrame:
    """DataFrame with highly correlated column pairs."""
    np.random.seed(42)
    base = np.random.randn(50)
    # x and x_duplicate: correlation ~0.99 (high but < 0.999)
    x = base
    x_dup = base * 0.99 + np.random.randn(50) * 0.14
    # y and y_duplicate: correlation ~0.98 (high but < 0.999)
    y = base * 2 + 1 + np.random.randn(50) * 0.5
    y_dup = y * 0.98 + np.random.randn(50) * 0.2
    # independent: no correlation
    independent = np.random.randn(50) * 10
    return pd.DataFrame(
        {
            "x": x,
            "x_duplicate": x_dup,
            "y": y,
            "y_duplicate": y_dup,
            "independent": independent,
        }
    )


def low_signal_df() -> pd.DataFrame:
    """DataFrame with high-cardinality categorical and low target correlation."""
    np.random.seed(42)
    n = 100
    target = np.random.randn(n)
    # High cardinality categorical (50 unique out of 100 = 0.5 ratio) - will be flagged
    # as potentially low-signal since it has no correlation with target
    high_card_cat = [f"cat_{i % 50}" for i in range(n)]
    # Low cardinality categorical - should not be flagged
    low_card = ["a", "b"] * (n // 2)
    return pd.DataFrame(
        {
            "target": target,
            "high_card_low_signal": high_card_cat,
            "low_card": low_card,
        }
    )


def empty_df() -> pd.DataFrame:
    """Empty DataFrame with declared columns."""
    return pd.DataFrame(
        {
            "a": pd.Series([], dtype="float64"),
            "b": pd.Series([], dtype="object"),
        }
    )


def small_df() -> pd.DataFrame:
    """Very small DataFrame (3 rows)."""
    return pd.DataFrame(
        {
            "x": [1.0, 2.0, 3.0],
            "y": [4.0, 5.0, 6.0],
            "cat": ["a", "b", "c"],
        }
    )


def all_constant_df() -> pd.DataFrame:
    """All numeric columns are constant."""
    return pd.DataFrame(
        {
            "const1": [1.0, 1.0, 1.0, 1.0],
            "const2": [2.0, 2.0, 2.0, 2.0],
            "cat": ["a", "a", "a", "a"],
        }
    )


def no_numeric_df() -> pd.DataFrame:
    """Only categorical columns."""
    return pd.DataFrame(
        {
            "cat1": ["a", "b", "c", "d", "e"],
            "cat2": ["x", "y", "z", "x", "y"],
        }
    )


def no_categorical_df() -> pd.DataFrame:
    """Only numeric columns."""
    return pd.DataFrame(
        {
            "num1": [1.0, 2.0, 3.0, 4.0, 5.0],
            "num2": [5.0, 4.0, 3.0, 2.0, 1.0],
        }
    )


class TestNearConstantDetection:
    """Tests for near-constant column detection with variance threshold."""

    def test_default_variance_threshold(self) -> None:
        """Default threshold (1e-10) flags near-constant columns."""
        reviewer = FeatureQualityReviewer()
        section = run_reviewer(reviewer, near_constant_df())

        assert section.id == "review.quality.feature_quality"
        assert section.category == ReviewCategory.QUALITY
        near_const_findings = [
            f for f in section.findings if f.rule_id.endswith(".near_constant")
        ]
        assert len(near_const_findings) >= 2
        cols = {f.column_name for f in near_const_findings}
        assert "near_const_small" in cols
        assert "near_const_large" in cols
        assert "const" in cols

    def test_custom_variance_threshold(self) -> None:
        """Configurable variance threshold works correctly."""
        reviewer = FeatureQualityReviewer()
        # Higher threshold - more columns flagged
        section = run_reviewer(reviewer, near_constant_df(), variance_threshold=1e-5)
        near_const_findings = [
            f for f in section.findings if f.rule_id.endswith(".near_constant")
        ]
        assert len(near_const_findings) >= 3

        # Lower threshold - fewer columns flagged
        section = run_reviewer(reviewer, near_constant_df(), variance_threshold=1e-15)
        near_const_findings = [
            f for f in section.findings if f.rule_id.endswith(".near_constant")
        ]
        assert len(near_const_findings) >= 1

    def test_near_constant_finding_structure(self) -> None:
        """Near-constant finding has correct structure and evidence."""
        reviewer = FeatureQualityReviewer()
        section = run_reviewer(reviewer, near_constant_df())
        finding = next(
            f for f in section.findings if f.rule_id.endswith(".near_constant")
        )

        assert finding.rule_id == "review.quality.feature_quality.near_constant"
        assert finding.rule_name == "Near-Constant Column"
        assert finding.category == "quality"
        assert finding.severity == "warning"
        assert finding.confidence == 0.9
        assert "variance" in finding.evidence
        assert "threshold" in finding.evidence
        assert "unique_count" in finding.evidence
        assert "count" in finding.evidence
        assert finding.evidence["variance"] < finding.evidence["threshold"]


class TestRedundantColumnDetection:
    """Tests for redundant column pair detection with correlation threshold."""

    def test_default_correlation_threshold(self) -> None:
        """Default threshold (0.95) flags highly correlated pairs."""
        reviewer = FeatureQualityReviewer()
        section = run_reviewer(reviewer, redundant_df())

        redundant_findings = [
            f for f in section.findings if f.rule_id.endswith(".redundant")
        ]
        assert len(redundant_findings) >= 2

        pairs = {
            (f.evidence["column_a"], f.evidence["column_b"]) for f in redundant_findings
        }
        assert ("x", "x_duplicate") in pairs or ("x_duplicate", "x") in pairs
        assert ("y", "y_duplicate") in pairs or ("y_duplicate", "y") in pairs

    def test_custom_correlation_threshold(self) -> None:
        """Configurable correlation threshold works correctly."""
        reviewer = FeatureQualityReviewer()
        # Lower threshold - more pairs flagged
        section = run_reviewer(reviewer, redundant_df(), correlation_threshold=0.90)
        redundant_findings = [
            f for f in section.findings if f.rule_id.endswith(".redundant")
        ]
        assert len(redundant_findings) >= 2

        # Higher threshold - fewer pairs flagged
        section = run_reviewer(reviewer, redundant_df(), correlation_threshold=0.999)
        redundant_findings = [
            f for f in section.findings if f.rule_id.endswith(".redundant")
        ]
        assert len(redundant_findings) == 0

    def test_redundant_finding_structure(self) -> None:
        """Redundant finding has correct structure and evidence."""
        reviewer = FeatureQualityReviewer()
        section = run_reviewer(reviewer, redundant_df())
        finding = next(f for f in section.findings if f.rule_id.endswith(".redundant"))

        assert finding.rule_id == "review.quality.feature_quality.redundant"
        assert finding.rule_name == "Redundant Column Pair"
        assert finding.category == "quality"
        assert finding.severity == "warning"
        assert finding.confidence == 0.85
        assert "column_a" in finding.evidence
        assert "column_b" in finding.evidence
        assert "correlation" in finding.evidence
        assert "threshold" in finding.evidence
        assert abs(finding.evidence["correlation"]) >= finding.evidence["threshold"]


class TestLowSignalDetection:
    """Tests for low-signal high-cardinality column detection with target_column."""

    def test_low_signal_with_target(self) -> None:
        """Low-signal detection works when target_column is provided."""
        reviewer = FeatureQualityReviewer()
        section = run_reviewer(reviewer, low_signal_df(), target_column="target")

        low_signal_findings = [
            f for f in section.findings if f.rule_id.endswith(".low_signal")
        ]
        # Should find high_card_low_signal (categorical with high cardinality, no target correlation)
        assert len(low_signal_findings) >= 1

        cols = {f.column_name for f in low_signal_findings}
        assert "high_card_low_signal" in cols

    def test_low_signal_respects_min_target_correlation(self) -> None:
        """Configurable min_target_correlation threshold works."""
        reviewer = FeatureQualityReviewer()
        # Low threshold - more columns flagged
        section = run_reviewer(
            reviewer,
            low_signal_df(),
            target_column="target",
            min_target_correlation=0.10,
        )
        low_signal_findings = [
            f for f in section.findings if f.rule_id.endswith(".low_signal")
        ]
        count_low = len(low_signal_findings)

        # High threshold - fewer columns flagged
        section = run_reviewer(
            reviewer,
            low_signal_df(),
            target_column="target",
            min_target_correlation=0.50,
        )
        low_signal_findings = [
            f for f in section.findings if f.rule_id.endswith(".low_signal")
        ]
        count_high = len(low_signal_findings)

        assert count_high <= count_low

    def test_no_target_column_no_low_signal(self) -> None:
        """Low-signal detection is skipped when no target_column."""
        reviewer = FeatureQualityReviewer()
        section = run_reviewer(reviewer, low_signal_df())  # No target_column

        low_signal_findings = [
            f for f in section.findings if f.rule_id.endswith(".low_signal")
        ]
        assert len(low_signal_findings) == 0

    def test_low_signal_finding_structure(self) -> None:
        """Low-signal finding has correct structure and evidence."""
        reviewer = FeatureQualityReviewer()
        section = run_reviewer(reviewer, low_signal_df(), target_column="target")
        low_signal_findings = [
            f for f in section.findings if f.rule_id.endswith(".low_signal")
        ]

        assert len(low_signal_findings) >= 1
        finding = low_signal_findings[0]

        assert finding.rule_id == "review.quality.feature_quality.low_signal"
        assert finding.category == "quality"
        assert finding.severity == "info"
        assert "cardinality" in finding.evidence
        assert "unique_ratio" in finding.evidence
        assert "target_column" in finding.evidence


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_dataset(self) -> None:
        """Empty dataset handled gracefully."""
        reviewer = FeatureQualityReviewer()
        section = run_reviewer(reviewer, empty_df())

        assert section.id == "review.quality.feature_quality"
        # Should not crash, may have no findings or schema health findings
        assert isinstance(section.findings, tuple)

    def test_small_dataset(self) -> None:
        """Very small dataset (3 rows) handled gracefully."""
        reviewer = FeatureQualityReviewer()
        section = run_reviewer(reviewer, small_df())

        assert section.id == "review.quality.feature_quality"
        assert isinstance(section.findings, tuple)

    def test_all_constant_numeric_columns(self) -> None:
        """All constant numeric columns are flagged."""
        reviewer = FeatureQualityReviewer()
        section = run_reviewer(reviewer, all_constant_df())

        near_const_findings = [
            f for f in section.findings if f.rule_id.endswith(".near_constant")
        ]
        cols = {f.column_name for f in near_const_findings}
        assert "const1" in cols
        assert "const2" in cols

    def test_no_numeric_columns(self) -> None:
        """Dataset with no numeric columns handled gracefully."""
        reviewer = FeatureQualityReviewer()
        section = run_reviewer(reviewer, no_numeric_df())

        assert section.id == "review.quality.feature_quality"
        assert isinstance(section.findings, tuple)
        near_const_findings = [
            f for f in section.findings if f.rule_id.endswith(".near_constant")
        ]
        assert len(near_const_findings) == 0
        redundant_findings = [
            f for f in section.findings if f.rule_id.endswith(".redundant")
        ]
        assert len(redundant_findings) == 0

    def test_no_categorical_columns(self) -> None:
        """Dataset with no categorical columns handled gracefully."""
        reviewer = FeatureQualityReviewer()
        section = run_reviewer(reviewer, no_categorical_df(), target_column="num1")

        assert section.id == "review.quality.feature_quality"
        assert isinstance(section.findings, tuple)
        low_signal_findings = [
            f for f in section.findings if f.rule_id.endswith(".low_signal")
        ]
        assert len(low_signal_findings) == 0


class TestDeterministicResults:
    """Tests that verify deterministic results across multiple runs."""

    def test_near_constant_deterministic(self) -> None:
        """Near-constant detection produces identical results across runs."""
        reviewer = FeatureQualityReviewer()
        df = near_constant_df()

        findings_sets = []
        for _ in range(5):
            section = run_reviewer(reviewer, df)
            near_const = tuple(
                (f.column_name, f.evidence["variance"])
                for f in section.findings
                if f.rule_id.endswith(".near_constant")
            )
            findings_sets.append(near_const)

        assert len(set(findings_sets)) == 1

    def test_redundant_deterministic(self) -> None:
        """Redundant detection produces identical results across runs."""
        reviewer = FeatureQualityReviewer()
        df = redundant_df()

        findings_sets = []
        for _ in range(5):
            section = run_reviewer(reviewer, df)
            redundant = tuple(
                (
                    f.evidence["column_a"],
                    f.evidence["column_b"],
                    round(f.evidence["correlation"], 6),
                )
                for f in section.findings
                if f.rule_id.endswith(".redundant")
            )
            findings_sets.append(redundant)

        assert len(set(findings_sets)) == 1

    def test_low_signal_deterministic(self) -> None:
        """Low-signal detection produces identical results across runs."""
        reviewer = FeatureQualityReviewer()
        df = low_signal_df()

        findings_sets = []
        for _ in range(5):
            section = run_reviewer(reviewer, df, target_column="target")
            low_signal = tuple(
                (
                    f.column_name,
                    f.evidence["cardinality"],
                    round(f.evidence.get("target_correlation", 0), 6),
                )
                for f in section.findings
                if f.rule_id.endswith(".low_signal")
            )
            findings_sets.append(low_signal)

        assert len(set(findings_sets)) == 1


class TestReviewerIdentityAndTraceability:
    """Tests for reviewer ID, category, severity, finding IDs, traceability."""

    def test_reviewer_id(self) -> None:
        """Reviewer has correct stable ID."""
        reviewer = FeatureQualityReviewer()
        assert reviewer.id == "review.quality.feature_quality"

    def test_reviewer_category(self) -> None:
        """Reviewer has correct category."""
        reviewer = FeatureQualityReviewer()
        assert reviewer.category == ReviewCategory.QUALITY

    def test_reviewer_title(self) -> None:
        """Reviewer has correct title."""
        reviewer = FeatureQualityReviewer()
        assert reviewer.title == "Feature Quality"

    def test_finding_ids_are_stable_and_namespaced(self) -> None:
        """All finding rule_ids are namespaced under reviewer ID."""
        reviewer = FeatureQualityReviewer()
        section = run_reviewer(reviewer, near_constant_df())

        for finding in section.findings:
            assert finding.rule_id.startswith("review.quality.feature_quality.")
            assert finding.rule_id in {
                "review.quality.feature_quality.near_constant",
                "review.quality.feature_quality.redundant",
                "review.quality.feature_quality.low_signal",
            }

    def test_severity_levels_correct(self) -> None:
        """Each finding type has correct severity."""
        reviewer = FeatureQualityReviewer()
        section = run_reviewer(reviewer, near_constant_df())

        for finding in section.findings:
            if finding.rule_id.endswith(".near_constant"):
                assert finding.severity == "warning"
            elif finding.rule_id.endswith(".redundant"):
                assert finding.severity == "warning"
            elif finding.rule_id.endswith(".low_signal"):
                assert finding.severity == "info"

    def test_evidence_contains_traceable_fields(self) -> None:
        """Findings contain evidence for traceability."""
        from types import MappingProxyType

        reviewer = FeatureQualityReviewer()
        section = run_reviewer(reviewer, near_constant_df())

        for finding in section.findings:
            assert finding.evidence is not None
            assert isinstance(finding.evidence, MappingProxyType)
            assert len(finding.evidence) > 0

            # Each finding type has specific traceable fields
            if finding.rule_id.endswith(".near_constant"):
                assert "variance" in finding.evidence
                assert "threshold" in finding.evidence
            elif finding.rule_id.endswith(".redundant"):
                assert "column_a" in finding.evidence
                assert "column_b" in finding.evidence
                assert "correlation" in finding.evidence
                assert "threshold" in finding.evidence
            elif finding.rule_id.endswith(".low_signal"):
                assert "cardinality" in finding.evidence
                assert "unique_ratio" in finding.evidence


class TestCleanDataset:
    """Tests with a clean dataset that should pass all checks."""

    def test_clean_dataset_passes(self) -> None:
        """Clean dataset with no issues passes all feature quality checks."""
        np.random.seed(123)
        n = 100
        df = pd.DataFrame(
            {
                "x": np.random.randn(n),
                "y": np.random.randn(n) * 2 + 5,
                "z": np.random.randn(n) * 0.5 - 2,
                "cat": np.random.choice(["a", "b", "c", "d", "e", "f", "g", "h"], n),
            }
        )
        reviewer = FeatureQualityReviewer()
        section = run_reviewer(reviewer, df, target_column="x")

        # Should have no findings for a clean dataset
        assert section.severity == Severity.PASSED
        assert len(section.findings) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
