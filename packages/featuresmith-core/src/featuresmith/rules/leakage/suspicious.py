"""Suspicious-correlation leakage detector."""

from __future__ import annotations

import math
import re
from collections.abc import Mapping
from typing import Any

from featuresmith.core.profile_result import NumericProfile, ProfileResult
from featuresmith.rules.leakage.base import LeakagePatternDetector
from featuresmith.rules.leakage.schema import LeakageFinding

_DEFAULT_PAIR_THRESHOLD = 0.98
_DEFAULT_NEAR_IDENTICAL_RATIO = 0.05
_DEFAULT_TARGET_BAND_LOW = 0.90
_DEFAULT_TARGET_BAND_HIGH = 0.99

# Matches names that differ only by a numeric or numeric-word variant, e.g.
# "amount" vs "amount_2" or "feature_1" vs "feature_2".
_VARIANT_SUFFIX = re.compile(r"[_\s-]?\d+$")


class SuspiciousCorrelationDetector(LeakagePatternDetector):
    """Flags suspicious correlations with a secondary signal, never magnitude alone.

    Two scenarios are recognized: a pair of numeric columns with very high
    mutual correlation AND a near-identical distribution or near-identical name
    (likely duplicate/derived features), and a column whose correlation with a
    declared target sits just below the target-leakage threshold (suspicious
    but plausible, reported at low confidence).
    """

    def __init__(
        self,
        pair_threshold: float = _DEFAULT_PAIR_THRESHOLD,
        near_identical_ratio: float = _DEFAULT_NEAR_IDENTICAL_RATIO,
        target_band_low: float = _DEFAULT_TARGET_BAND_LOW,
        target_band_high: float = _DEFAULT_TARGET_BAND_HIGH,
    ) -> None:
        """Initialize the suspicious-correlation detector.

        Args:
            pair_threshold: Absolute Pearson threshold for flagging a column pair.
            near_identical_ratio: Maximum relative mean/std deviation treated as
                a near-identical distribution.
            target_band_low: Lower bound of the target-correlation band reported
                as suspicious-but-plausible.
            target_band_high: Exclusive upper bound of that band.
        """
        self._defaults = {
            "suspicious_correlation_threshold": pair_threshold,
            "near_identical_ratio": near_identical_ratio,
            "suspicious_target_low": target_band_low,
            "suspicious_target_high": target_band_high,
        }

    @property
    def id(self) -> str:
        return "suspicious_correlation"

    @property
    def name(self) -> str:
        return "Suspicious Correlation"

    def detect(
        self,
        profile: ProfileResult,
        *,
        target_column: str | None = None,
        config: Mapping[str, Any] | None = None,
    ) -> list[LeakageFinding]:
        config = config or {}
        pair_threshold = float(
            config.get(
                "suspicious_correlation_threshold",
                self._defaults["suspicious_correlation_threshold"],
            )
        )
        near_ratio = float(
            config.get("near_identical_ratio", self._defaults["near_identical_ratio"])
        )
        band_low = float(
            config.get("suspicious_target_low", self._defaults["suspicious_target_low"])
        )
        band_high = float(
            config.get(
                "suspicious_target_high", self._defaults["suspicious_target_high"]
            )
        )

        pearson = profile.correlation_summary.pearson
        findings: list[LeakageFinding] = []

        # Target-adjacent band: strong but sub-leakage correlation with the target.
        if target_column is not None and target_column in pearson:
            for col_name in pearson:
                if col_name == target_column:
                    continue
                corr = pearson[col_name].get(target_column)
                if corr is None or not math.isfinite(corr):
                    continue
                abs_corr = abs(corr)
                if band_low <= abs_corr < band_high:
                    findings.append(
                        LeakageFinding(
                            pattern=self.id,
                            column_name=col_name,
                            title=(
                                f"Suspicious correlation between '{col_name}' and the target"
                            ),
                            rationale=(
                                f"Column '{col_name}' correlates with the target "
                                f"'{target_column}' at Pearson {corr:.3f}, below the "
                                f"target-leakage threshold of {band_high:.3f} but high enough "
                                "to warrant a closer look."
                            ),
                            evidence={
                                "target_column": target_column,
                                "correlation": corr,
                                "band_low": band_low,
                                "band_high": band_high,
                            },
                            confidence=0.4,
                            severity="info",
                            suggested_action=(
                                f"Investigate the relationship between '{col_name}' and the "
                                "target; it may be legitimate, or it may partially encode the outcome."
                            ),
                        )
                    )

        # Pair correlations: high magnitude combined with a secondary signal.
        columns = [
            col_name
            for col_name in pearson
            if col_name in profile.numeric_profiles
            and (target_column is None or col_name != target_column)
        ]
        for index, col1 in enumerate(columns):
            for col2 in columns[index + 1 :]:
                corr = pearson[col1].get(col2)
                if corr is None or not math.isfinite(corr):
                    continue
                abs_corr = abs(corr)
                if abs_corr < pair_threshold:
                    continue

                near_identical = _near_identical(
                    profile.numeric_profiles[col1],
                    profile.numeric_profiles[col2],
                    near_ratio,
                )
                if not near_identical and not _name_similar(col1, col2):
                    continue

                if abs_corr >= 0.999:
                    confidence = 0.8
                else:
                    confidence = 0.6

                if near_identical:
                    secondary = "near-identical distributions"
                else:
                    secondary = "near-identical names"
                findings.append(
                    LeakageFinding(
                        pattern=self.id,
                        column_name=col1,
                        title=f"Suspicious correlation between '{col1}' and '{col2}'",
                        rationale=(
                            f"Columns '{col1}' and '{col2}' correlate at Pearson {corr:.3f} "
                            f"(threshold {pair_threshold:.3f}) and share {secondary}. Highly "
                            "correlated, near-duplicate features can encode the target or "
                            "each other, inflating model confidence without adding information."
                        ),
                        evidence={
                            "column_a": col1,
                            "column_b": col2,
                            "correlation": corr,
                            "threshold": pair_threshold,
                            "secondary_signal": secondary,
                        },
                        confidence=confidence,
                        severity="warning",
                        suggested_action=(
                            f"Inspect '{col1}' and '{col2}'; consider removing one if they "
                            "encode the same information, and confirm neither contains outcome data."
                        ),
                    )
                )
        return findings


def _near_identical(
    first: NumericProfile,
    second: NumericProfile,
    ratio: float,
) -> bool:
    """Return whether two numeric profiles have near-identical mean and spread."""
    if (
        first.mean is None
        or second.mean is None
        or first.std_dev is None
        or second.std_dev is None
    ):
        return False
    mean_scale = max(abs(first.mean), abs(second.mean), 1e-9)
    std_scale = max(abs(first.std_dev), abs(second.std_dev), 1e-9)
    return (
        abs(first.mean - second.mean) / mean_scale <= ratio
        and abs(first.std_dev - second.std_dev) / std_scale <= ratio
    )


def _name_similar(first: str, second: str) -> bool:
    """Return whether two column names look like variants of each other."""
    first_lower = first.lower()
    second_lower = second.lower()
    if first_lower == second_lower:
        return True
    if len(first_lower) > 3 and len(second_lower) > 3:
        if first_lower.startswith(second_lower) or second_lower.startswith(first_lower):
            return True
        base_first = _VARIANT_SUFFIX.sub("", first_lower)
        base_second = _VARIANT_SUFFIX.sub("", second_lower)
        if base_first == base_second and base_first:
            return True
    return False
