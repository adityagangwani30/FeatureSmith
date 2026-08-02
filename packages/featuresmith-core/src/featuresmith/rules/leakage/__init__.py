"""Deterministic leakage pattern detectors.

This package matures the rule engine's naive leakage rule into a family of
named, inspectable pattern detectors (``Dataset-Diff-And-Leakage-Detection.md``
§7.2). ``LeakageRuleTargetCorrelation`` is re-exported here unchanged so the
rule engine's existing imports keep working.
"""

from __future__ import annotations

from featuresmith.rules.leakage.base import LeakagePatternDetector
from featuresmith.rules.leakage.duplicate_target import DuplicateTargetDetector
from featuresmith.rules.leakage.identifier import IdentifierShapeDetector
from featuresmith.rules.leakage.schema import LeakageFinding, confidence_label
from featuresmith.rules.leakage.suspicious import SuspiciousCorrelationDetector
from featuresmith.rules.leakage.target_correlation import (
    LeakageRuleTargetCorrelation,
    TargetCorrelationDetector,
)
from featuresmith.rules.leakage.timestamp import (
    FutureInfoDetector,
    TimestampLeakageDetector,
)

__all__ = [
    "LeakagePatternDetector",
    "LeakageFinding",
    "confidence_label",
    "LeakageRuleTargetCorrelation",
    "TargetCorrelationDetector",
    "IdentifierShapeDetector",
    "TimestampLeakageDetector",
    "FutureInfoDetector",
    "DuplicateTargetDetector",
    "SuspiciousCorrelationDetector",
    "builtin_detectors",
]


def builtin_detectors() -> tuple[LeakagePatternDetector, ...]:
    """Return the default set of leakage pattern detectors.

    The order is stable and deterministic; the LeakageReviewer runs detectors
    in this order and merges findings per column.

    Returns:
        A tuple of the six built-in detector instances.
    """
    return (
        TargetCorrelationDetector(),
        IdentifierShapeDetector(),
        TimestampLeakageDetector(),
        FutureInfoDetector(),
        DuplicateTargetDetector(),
        SuspiciousCorrelationDetector(),
    )
