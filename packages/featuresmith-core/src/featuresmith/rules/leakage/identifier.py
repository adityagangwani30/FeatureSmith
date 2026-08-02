"""Identifier-shape leakage detector."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from featuresmith.core.profile_result import NumericProfile, ProfileResult
from featuresmith.rules.leakage.base import LeakagePatternDetector
from featuresmith.rules.leakage.schema import LeakageFinding

_DEFAULT_CORRELATION_THRESHOLD = 0.50

# Matches ID-like column names such as "id", "user_id", "uuid", "session_key",
# "record_hash", "access_token", or "_id". Shape checks are correlation-gated,
# so an ID-like *name* alone never fires a finding.
_IDENTIFIER_NAME = re.compile(
    r"(^|_)(id|uuid|guid|key|hash|token)(_|$)|^_?id$",
    re.IGNORECASE,
)


class IdentifierShapeDetector(LeakagePatternDetector):
    """Flags columns with an ID-like shape that also correlate with the target.

    The detector performs a shape check first (near-unique, sequential, or
    ID-named) and a correlation check second, exactly as specified in
    ``Dataset-Diff-And-Leakage-Detection.md`` §7.2: a legitimately unique but
    predictive column is not flagged on shape alone. Without a declared target
    column the detector returns no findings.
    """

    def __init__(
        self, correlation_threshold: float = _DEFAULT_CORRELATION_THRESHOLD
    ) -> None:
        """Initialize the identifier-shape detector.

        Args:
            correlation_threshold: Minimum absolute Pearson correlation with the
                target at which an ID-shaped column is flagged (default 0.50).
        """
        self._default_correlation_threshold = correlation_threshold

    @property
    def id(self) -> str:
        return "identifier"

    @property
    def name(self) -> str:
        return "Identifier Shape"

    def detect(
        self,
        profile: ProfileResult,
        *,
        target_column: str | None = None,
        config: Mapping[str, Any] | None = None,
    ) -> list[LeakageFinding]:
        config = config or {}
        threshold = float(
            config.get(
                "identifier_correlation_threshold", self._default_correlation_threshold
            )
        )
        if target_column is None:
            return []

        pearson = profile.correlation_summary.pearson
        if target_column not in pearson:
            return []

        findings: list[LeakageFinding] = []
        for col_name, shape_signals in _identifier_shapes(profile).items():
            if col_name == target_column:
                continue

            corr = pearson.get(col_name, {}).get(target_column)
            if corr is None:
                continue

            abs_corr = abs(corr)
            if abs_corr < threshold:
                continue

            if abs_corr >= 0.9:
                confidence, severity = 0.95, "critical"
            elif abs_corr >= 0.7:
                confidence, severity = 0.85, "critical"
            else:
                confidence, severity = 0.65, "warning"

            shape_text = ", ".join(shape_signals)
            findings.append(
                LeakageFinding(
                    pattern=self.id,
                    column_name=col_name,
                    title=f"Identifier-like column '{col_name}' correlates with the target",
                    rationale=(
                        f"Column '{col_name}' has an identifier-like shape ({shape_text}) "
                        f"and correlates with the target '{target_column}' at Pearson "
                        f"{corr:.3f}, at or above the threshold of {threshold:.3f}. "
                        "An identifier that tracks the outcome is a common leakage vector."
                    ),
                    evidence={
                        "target_column": target_column,
                        "correlation": corr,
                        "threshold": threshold,
                        "shape_signals": shape_signals,
                    },
                    confidence=confidence,
                    severity=severity,
                    suggested_action=(
                        f"Verify whether '{col_name}' is a row identifier or transaction "
                        "identifier. If it is, drop it from the feature set; identifiers "
                        "can leak the outcome through the rows they encode."
                    ),
                )
            )
        return findings


def _identifier_shapes(profile: ProfileResult) -> dict[str, list[str]]:
    """Return columns with an identifier-like shape and the signals that fired.

    Signals are intentionally cheap and deterministic: an ID-like name, a
    near-unique numeric column, or a sequential numeric column.

    Args:
        profile: The computed ProfileResult.

    Returns:
        A mapping of column name to the list of shape signals that matched.
    """
    shapes: dict[str, list[str]] = {}
    for col_name, num_prof in profile.numeric_profiles.items():
        signals: list[str] = []
        if _IDENTIFIER_NAME.match(col_name):
            signals.append("ID-like name")
        if num_prof.count >= 5 and num_prof.unique_count > 0:
            unique_ratio = num_prof.unique_count / num_prof.count
            if unique_ratio >= 0.9:
                signals.append("near-unique")
            if _is_sequential(num_prof):
                signals.append("sequential")
        if signals:
            shapes[col_name] = signals
    return shapes


def _is_sequential(num_prof: NumericProfile) -> bool:
    """Return whether a numeric profile looks like a consecutive integer run."""
    if num_prof.minimum is None or num_prof.maximum is None:
        return False
    if num_prof.count != num_prof.unique_count:
        return False
    if num_prof.count < 5:
        return False
    span = num_prof.maximum - num_prof.minimum
    return span >= 4 and abs(span - (num_prof.count - 1)) < 1e-9
