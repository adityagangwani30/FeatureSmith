"""Duplicate-target-information leakage detector."""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

from featuresmith.core.profile_result import ProfileResult
from featuresmith.rules.leakage.base import LeakagePatternDetector
from featuresmith.rules.leakage.schema import LeakageFinding

_DEFAULT_THRESHOLD = 0.999


class DuplicateTargetDetector(LeakagePatternDetector):
    """Flags columns that are a near-deterministic copy or transform of the target.

    A column whose Pearson correlation with the declared target is essentially
    perfect (>= 0.999 by default) carries the same information as the target —
    it is either a copy, a rounding, or a linear re-binning of it. The detector
    only runs when a target column is declared.
    """

    def __init__(self, threshold: float = _DEFAULT_THRESHOLD) -> None:
        """Initialize the duplicate-target detector.

        Args:
            threshold: Pearson correlation threshold above which a column is
                treated as a duplicate of the target (default 0.999).
        """
        self._default_threshold = threshold

    @property
    def id(self) -> str:
        return "duplicate_target"

    @property
    def name(self) -> str:
        return "Duplicate Target Information"

    def detect(
        self,
        profile: ProfileResult,
        *,
        target_column: str | None = None,
        config: Mapping[str, Any] | None = None,
    ) -> list[LeakageFinding]:
        config = config or {}
        threshold = float(
            config.get("duplicate_correlation_threshold", self._default_threshold)
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

            if abs_corr >= 0.9999:
                confidence, severity = 1.0, "critical"
            else:
                confidence, severity = 0.7, "warning"

            findings.append(
                LeakageFinding(
                    pattern=self.id,
                    column_name=col_name,
                    title=f"Column '{col_name}' appears to duplicate the target",
                    rationale=(
                        f"Column '{col_name}' correlates with the target '{target_column}' "
                        f"at Pearson {corr:.3f} (threshold {threshold:.3f}), indicating it is "
                        "very likely a deterministic transform — a copy, rounding, or re-bin — "
                        "of the target itself."
                    ),
                    evidence={
                        "target_column": target_column,
                        "correlation": corr,
                        "threshold": threshold,
                    },
                    confidence=confidence,
                    severity=severity,
                    suggested_action=(
                        f"Confirm whether '{col_name}' is derived from the target; if it is, "
                        "remove it from the feature set before training."
                    ),
                )
            )
        return findings
