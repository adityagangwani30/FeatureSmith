"""Leakage reviewer that runs the pattern detectors and merges findings."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from featuresmith.core.rule_finding import RuleFinding
from featuresmith.review.context import ReviewContext
from featuresmith.review.reviewers.base import SectionReviewer
from featuresmith.review.schema import ReviewCategory
from featuresmith.rules.leakage import (
    LeakageFinding,
    LeakagePatternDetector,
    builtin_detectors,
    confidence_label,
)

_SEVERITY_RANK = {"critical": 3, "warning": 2, "info": 1}


class LeakageReviewer(SectionReviewer):
    """Reviews a dataset for target leakage through named pattern detectors.

    The reviewer dispatches every ``LeakagePatternDetector`` against the frozen
    profile, then merges findings that point at the same column into one
    ``RuleFinding`` citing every contributing pattern — never two redundant
    findings for one column (``Dataset-Diff-And-Leakage-Detection.md`` §8.2).
    """

    def __init__(
        self, detectors: Sequence[LeakagePatternDetector] | None = None
    ) -> None:
        """Initialize the leakage reviewer with its detector set.

        Args:
            detectors: The detectors to run; defaults to the built-in set.
        """
        self._detectors = tuple(
            detectors if detectors is not None else builtin_detectors()
        )
        self._pattern_names = {
            detector.id: detector.name for detector in self._detectors
        }

    @property
    def id(self) -> str:
        """Return the stable reviewer identifier."""
        return "review.leakage"

    @property
    def category(self) -> ReviewCategory:
        """Return the reviewer category."""
        return ReviewCategory.LEAKAGE

    @property
    def title(self) -> str:
        """Return the section heading."""
        return "Leakage Detection"

    def _collect_findings(self, context: ReviewContext) -> list[RuleFinding]:
        """Compute leakage findings for the context by dispatching detectors."""
        config = self._config_for(context)
        raw: list[LeakageFinding] = []
        for detector in self._detectors:
            raw.extend(
                detector.detect(
                    context.profile,
                    target_column=context.config.target_column,
                    config=config,
                )
            )
        return _merge_findings(raw, self._pattern_names)


def _merge_findings(
    findings: Sequence[LeakageFinding], pattern_names: Mapping[str, str]
) -> list[RuleFinding]:
    """Merge detector findings per column into one RuleFinding each."""
    by_column: dict[str, list[LeakageFinding]] = {}
    for finding in findings:
        by_column.setdefault(finding.column_name, []).append(finding)

    merged: list[RuleFinding] = []
    for column, column_findings in by_column.items():
        if len(column_findings) == 1:
            merged.append(_to_rule_finding(column_findings[0], pattern_names))
        else:
            merged.append(_merge_column(column, column_findings, pattern_names))
    return merged


def _to_rule_finding(
    finding: LeakageFinding, pattern_names: Mapping[str, str]
) -> RuleFinding:
    """Map a single detector finding onto the shared RuleFinding schema."""
    pattern_name = pattern_names.get(finding.pattern, finding.pattern)
    return RuleFinding(
        rule_id=f"leakage.{finding.pattern}",
        rule_name=pattern_name,
        category="leakage",
        severity=finding.severity,
        column_name=finding.column_name,
        title=finding.title,
        description=(
            f"Pattern: {pattern_name}. {finding.rationale} "
            f"Suggested action: {finding.suggested_action}"
        ),
        evidence={
            "pattern": finding.pattern,
            "confidence": finding.confidence,
            **finding.evidence,
        },
        confidence=finding.confidence,
        metadata={
            "pattern": finding.pattern,
            "confidence_level": confidence_label(finding.confidence),
            "rationale": finding.rationale,
            "suggested_action": finding.suggested_action,
        },
    )


def _merge_column(
    column: str,
    findings: Sequence[LeakageFinding],
    pattern_names: Mapping[str, str],
) -> RuleFinding:
    """Merge several detector findings for one column into a single finding."""
    patterns = [finding.pattern for finding in findings]
    names = [pattern_names.get(pattern, pattern) for pattern in patterns]
    worst = max(findings, key=lambda f: _SEVERITY_RANK.get(f.severity, 0))
    confidence = max(finding.confidence for finding in findings)
    rationale = " ".join(
        f"{name}: {finding.rationale}"
        for name, finding in zip(names, findings, strict=True)
    )
    return RuleFinding(
        rule_id="leakage.multiple_patterns",
        rule_name="Multiple Leakage Patterns",
        category="leakage",
        severity=worst.severity,
        column_name=column,
        title=f"Multiple leakage patterns in column '{column}'",
        description=(
            f"Column '{column}' triggered {len(findings)} leakage pattern(s): "
            f"{', '.join(names)}. {rationale}"
        ),
        evidence={
            "patterns": patterns,
            "confidence": confidence,
        },
        confidence=confidence,
        metadata={
            "patterns": patterns,
            "confidence_level": confidence_label(confidence),
            "rationale": rationale,
        },
    )
