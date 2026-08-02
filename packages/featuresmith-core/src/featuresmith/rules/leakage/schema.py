"""Typed schema for leakage pattern detector findings."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


def confidence_label(confidence: float) -> str:
    """Map a numeric confidence onto a Low/Medium/High label.

    The label is used as a plain-language hedge in rendered output; detectors
    never claim certainty about a finding. High covers 0.7 and above, Medium
    covers 0.4 and above, and everything below 0.4 is Low.

    Args:
        confidence: A confidence value in [0.0, 1.0].

    Returns:
        "High", "Medium", or "Low" depending on the confidence value.
    """
    if confidence >= 0.7:
        return "High"
    if confidence >= 0.4:
        return "Medium"
    return "Low"


@dataclass(frozen=True, slots=True)
class LeakageFinding:
    """A single leakage finding produced by one pattern detector.

    This is the detector-level result type described in
    ``Dataset-Diff-And-Leakage-Detection.md`` §9: every finding names the
    pattern that fired, the column it applies to, the rationale in terms of the
    underlying statistic, a confidence level, and a suggested action. The
    ``LeakageReviewer`` maps these onto the shared ``RuleFinding`` schema so the
    review section stays homogeneous with every other reviewer section.

    Attributes:
        pattern: The stable detector/pattern identifier (e.g. "target_correlation").
        column_name: The column this finding applies to.
        title: Short title summarizing the finding.
        rationale: Why the detector fired, in terms of the underlying statistic.
        evidence: Mapping of metrics or values that triggered the finding.
        confidence: Confidence in the finding, a float in [0.0, 1.0].
        severity: Severity ("info", "warning", or "critical").
        suggested_action: Concrete action the user can take to investigate.
    """

    pattern: str
    column_name: str
    title: str
    rationale: str
    evidence: Mapping[str, Any]
    confidence: float
    severity: str
    suggested_action: str

    def __post_init__(self) -> None:
        """Freeze the evidence mapping to keep the finding immutable."""
        from types import MappingProxyType

        object.__setattr__(self, "evidence", MappingProxyType(dict(self.evidence)))
