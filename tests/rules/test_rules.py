"""Comprehensive tests for the Featuresmith Rule Engine and default rules."""

from __future__ import annotations

import pandas as pd
import polars as pl

import featuresmith as fs
from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.core.rule_result import RuleResult
from featuresmith.rules.base import BaseRule
from featuresmith.rules.constants import FullyEmptyColumnsRule
from featuresmith.rules.engine import RuleEngine
from featuresmith.rules.registry import RuleRegistry


def test_missing_value_threshold_rule() -> None:
    """Test MissingValueThresholdRule detects high missingness."""
    df = pd.DataFrame(
        {
            "clean": [1, 2, 3, 4, 5],
            "dirty": [1, None, None, 4, 5],  # 40% missing
        }
    )
    result = fs.analyze(
        df, rule_config={"quality.missing_value_threshold": {"threshold": 30.0}}
    )

    findings = [
        f for f in result.findings if f.rule_id == "quality.missing_value_threshold"
    ]
    assert len(findings) == 1
    assert findings[0].column_name == "dirty"
    assert findings[0].evidence["missing_percentage"] == 40.0

    # Test negative case
    result_neg = fs.analyze(
        df, rule_config={"quality.missing_value_threshold": {"threshold": 50.0}}
    )
    findings_neg = [
        f for f in result_neg.findings if f.rule_id == "quality.missing_value_threshold"
    ]
    assert len(findings_neg) == 0


def test_duplicate_rows_rule() -> None:
    """Test DuplicateRowsRule flags excess duplicates."""
    # 2 duplicates out of 5 rows = 40% duplicate percentage
    df = pd.DataFrame(
        {
            "a": [1, 2, 2, 3, 3],
            "b": [1, 2, 2, 3, 3],
        }
    )
    result = fs.analyze(df, rule_config={"quality.duplicate_rows": {"threshold": 25.0}})

    findings = [f for f in result.findings if f.rule_id == "quality.duplicate_rows"]
    assert len(findings) == 1
    assert findings[0].column_name is None
    assert findings[0].evidence["duplicate_percentage"] == 40.0

    # Negative case
    result_neg = fs.analyze(
        df, rule_config={"quality.duplicate_rows": {"threshold": 50.0}}
    )
    findings_neg = [
        f for f in result_neg.findings if f.rule_id == "quality.duplicate_rows"
    ]
    assert len(findings_neg) == 0


def test_constant_and_empty_columns_rules() -> None:
    """Test ConstantColumnsRule and FullyEmptyColumnsRule detect static/null columns."""
    df = pd.DataFrame(
        {
            "normal": [1, 2, 3, 4, 5],
            "constant": [42, 42, 42, 42, 42],
            "empty": [None, None, None, None, None],
        }
    )
    result = fs.analyze(df)

    findings_const = [
        f for f in result.findings if f.rule_id == "quality.constant_columns"
    ]
    findings_empty = [
        f for f in result.findings if f.rule_id == "quality.fully_empty_columns"
    ]

    assert len(findings_const) == 1
    assert findings_const[0].column_name == "constant"

    assert len(findings_empty) == 1
    assert findings_empty[0].column_name == "empty"


def test_high_cardinality_rule() -> None:
    """Test HighCardinalityRule flags categorical columns with too many unique values."""
    # Use 10 unique values (exactly at the boundary: not >10, so stays categorical)
    # repeated over 30 rows -> ratio = 10/30 = 33%, with min_cardinality=5
    # Test with threshold=0.20 so 33% ratio triggers the rule.
    # cat_low has only 2 unique values (a/b), so it should not trigger.
    cat_high_vals = [f"cat_{i % 10}" for i in range(30)]  # 10 unique values out of 30
    cat_low_vals = ["a", "b"] * 15  # 2 unique values

    df = pd.DataFrame(
        {
            "cat_high": cat_high_vals,
            "cat_low": cat_low_vals,
        }
    )

    result = fs.analyze(
        df,
        rule_config={
            "statistical.high_cardinality": {"threshold": 0.20, "min_cardinality": 5}
        },
    )

    findings = [
        f for f in result.findings if f.rule_id == "statistical.high_cardinality"
    ]
    assert len(findings) >= 1
    assert any(f.column_name == "cat_high" for f in findings)
    assert not any(f.column_name == "cat_low" for f in findings)

    # Negative case — raise threshold so nothing fires
    result_neg = fs.analyze(
        df,
        rule_config={
            "statistical.high_cardinality": {"threshold": 0.90, "min_cardinality": 5}
        },
    )
    findings_neg = [
        f for f in result_neg.findings if f.rule_id == "statistical.high_cardinality"
    ]
    assert len(findings_neg) == 0


def test_outlier_detection_rule() -> None:
    """Test IQR-based OutlierDetectionRule."""
    df = pd.DataFrame(
        {
            "normal": [10, 11, 10, 12, 10, 11, 10, 12, 11, 10],
            "outliers": [10, 11, 10, 12, 100, 11, 10, -50, 11, 10],
        }
    )
    result = fs.analyze(df)

    findings = [f for f in result.findings if f.rule_id == "statistical.outliers"]
    assert len(findings) >= 1
    assert any(f.column_name == "outliers" for f in findings)
    assert not any(f.column_name == "normal" for f in findings)


def test_high_correlation_rule() -> None:
    """Test HighCorrelationRule detects highly correlated columns."""
    df = pd.DataFrame(
        {
            "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "y": [
                1.1,
                2.05,
                3.1,
                3.95,
                5.0,
                6.05,
                6.9,
                8.1,
                9.05,
                10.0,
            ],  # Correlation ~0.999
            "z": [10, 2, 8, 4, 6, 1, 9, 3, 7, 5],  # Uncorrelated
        }
    )
    result = fs.analyze(
        df, rule_config={"statistical.high_correlation": {"threshold": 0.95}}
    )

    findings = [
        f for f in result.findings if f.rule_id == "statistical.high_correlation"
    ]
    assert len(findings) == 1
    assert (
        findings[0].column_name == "x" and findings[0].evidence["column_b"] == "y"
    ) or (findings[0].column_name == "y" and findings[0].evidence["column_b"] == "x")


def test_leakage_rule() -> None:
    """Test LeakageRuleTargetCorrelation detecting features leaking target."""
    df = pd.DataFrame(
        {
            "feature": [1, 2, 3, 4, 5],
            "target": [1.001, 2.002, 3.003, 4.004, 5.005],  # Correlation ~1.0
            "normal": [5, 2, 8, 1, 9],
        }
    )

    # 1. Run with target_column specified -> should flag feature as leakage
    result = fs.analyze(
        df,
        target_column="target",
        rule_config={"leakage.potential_leakage": {"threshold": 0.99}},
    )
    findings = [f for f in result.findings if f.rule_id == "leakage.potential_leakage"]
    assert len(findings) == 1
    assert findings[0].column_name == "feature"
    assert findings[0].severity == "critical"

    # 2. Run without target_column specified -> should return empty findings (no target inference)
    result_no_target = fs.analyze(
        df, rule_config={"leakage.potential_leakage": {"threshold": 0.99}}
    )
    findings_no_target = [
        f for f in result_no_target.findings if f.rule_id == "leakage.potential_leakage"
    ]
    assert len(findings_no_target) == 0


def test_empty_dataset() -> None:
    """Test running rule engine on an empty dataset does not crash."""
    df = pd.DataFrame(columns=["a", "b", "c"])
    result = fs.analyze(df)
    assert isinstance(result, RuleResult)
    # The profiling engine handles empty dataset. The rule engine should run cleanly.
    assert len(result.findings) >= 0


def test_single_column_dataset() -> None:
    """Test rule engine with a single-column dataset."""
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5]})
    result = fs.analyze(df)
    assert isinstance(result, RuleResult)


def test_mixed_dataset() -> None:
    """Test rule engine with mixed datatypes and Polars DataFrame."""
    df = pl.DataFrame(
        {
            "num": [1.0, 2.0, 3.0, 4.0, 5.0],
            "cat": ["a", "b", "a", "b", "a"],
            "empty_col": [None, None, None, None, None],
        }
    )
    result = fs.analyze(df)
    assert isinstance(result, RuleResult)
    assert any(f.rule_id == "quality.fully_empty_columns" for f in result.findings)


def test_rule_engine_config_and_disabling() -> None:
    """Test that we can disable rules and pass custom configurations via RuleEngine."""
    df = pd.DataFrame(
        {
            "const": [1, 1, 1, 1, 1],
            "missing": [1, None, 3, None, 5],
        }
    )

    # Disable quality.constant_columns, run only missing_value_threshold
    result = fs.analyze(
        df,
        enabled_rules=["quality.missing_value_threshold"],
        rule_config={"quality.missing_value_threshold": {"threshold": 30.0}},
    )

    executed = result.executed_rules
    assert "quality.missing_value_threshold" in executed
    assert "quality.constant_columns" not in executed
    assert len(result.findings) == 1
    assert result.findings[0].column_name == "missing"


def test_rule_engine_error_isolation() -> None:
    """Test that a failing rule does not crash the entire execution, but is captured in failed_rules."""

    class CrashingRule(BaseRule):
        @property
        def id(self) -> str:
            return "test.crashing_rule"

        @property
        def name(self) -> str:
            return "Crashing Rule"

        @property
        def description(self) -> str:
            return "A rule designed to fail."

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
            raise ValueError("Intentional crash for testing isolation.")

    registry = RuleRegistry()
    registry.register(CrashingRule())
    # Add a normal rule too
    registry.register(FullyEmptyColumnsRule())

    engine = RuleEngine(registry=registry)
    df = pd.DataFrame({"empty": [None, None, None]})
    prof = fs.profile(df)

    result = engine.run(prof)
    # The normal rule should have completed
    assert "quality.fully_empty_columns" in result.executed_rules
    assert any(f.rule_id == "quality.fully_empty_columns" for f in result.findings)

    # The crashing rule should be registered in failed_rules
    assert "test.crashing_rule" in result.failed_rules
    assert "Intentional crash" in result.failed_rules["test.crashing_rule"]


def test_rules_invalid_thresholds() -> None:
    """Verify that rules raise ValueError for invalid configurations."""
    import pytest

    from featuresmith.rules.cardinality import HighCardinalityRule
    from featuresmith.rules.duplicates import DuplicateRowsRule
    from featuresmith.rules.missing import MissingValueThresholdRule

    with pytest.raises(ValueError, match="percentage between 0.0 and 100.0"):
        MissingValueThresholdRule(threshold=-1.0)
    with pytest.raises(ValueError, match="percentage between 0.0 and 100.0"):
        MissingValueThresholdRule(threshold=100.1)

    with pytest.raises(ValueError, match="percentage between 0.0 and 100.0"):
        DuplicateRowsRule(threshold=-0.1)
    with pytest.raises(ValueError, match="percentage between 0.0 and 100.0"):
        DuplicateRowsRule(threshold=150.0)

    with pytest.raises(ValueError, match="ratio between 0.0 and 1.0"):
        HighCardinalityRule(threshold=-0.01)
    with pytest.raises(ValueError, match="ratio between 0.0 and 1.0"):
        HighCardinalityRule(threshold=1.01)


def test_rule_engine_eager_validation() -> None:
    """Verify that RuleEngine raises appropriate exceptions eagerly for invalid configs."""
    import pytest

    df = pd.DataFrame({"a": [1, 2, 3]})
    prof = fs.profile(df)
    engine = RuleEngine()

    # 1. Unknown rule ID
    with pytest.raises(ValueError, match="Unknown rule ID in config"):
        engine.run(prof, rule_config={"non_existent_rule": {}})

    # 2. Typos in config parameter names
    with pytest.raises(TypeError, match="unexpected keyword argument"):
        engine.run(
            prof,
            rule_config={"quality.missing_value_threshold": {"threshhold": 30.0}},
        )

    # 3. Incorrect config parameter types
    with pytest.raises(TypeError, match="Incorrect type for parameter"):
        engine.run(
            prof,
            rule_config={
                "quality.missing_value_threshold": {"threshold": "not-a-float"}
            },
        )

    # 4. Out of bounds values
    with pytest.raises(ValueError, match="percentage between 0.0 and 100.0"):
        engine.run(
            prof,
            rule_config={"quality.missing_value_threshold": {"threshold": 120.0}},
        )
