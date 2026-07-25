"""Rule engine and deterministic rule definitions for Featuresmith."""

from featuresmith.rules.base import BaseRule
from featuresmith.rules.cardinality import HighCardinalityRule
from featuresmith.rules.constants import ConstantColumnsRule, FullyEmptyColumnsRule
from featuresmith.rules.correlation import HighCorrelationRule
from featuresmith.rules.duplicates import DuplicateRowsRule
from featuresmith.rules.engine import RuleEngine
from featuresmith.rules.leakage import LeakageRuleTargetCorrelation
from featuresmith.rules.missing import MissingValueThresholdRule
from featuresmith.rules.outliers import OutlierDetectionRule
from featuresmith.rules.registry import RuleRegistry, default_registry

__all__ = [
    "BaseRule",
    "RuleEngine",
    "RuleRegistry",
    "default_registry",
    "MissingValueThresholdRule",
    "DuplicateRowsRule",
    "ConstantColumnsRule",
    "FullyEmptyColumnsRule",
    "HighCardinalityRule",
    "OutlierDetectionRule",
    "HighCorrelationRule",
    "LeakageRuleTargetCorrelation",
]
