"""Shared base for dimensions that score a single review section.

Every built-in scoring dimension maps to exactly one Review Engine section
and derives its score deterministically from that section's findings: start at
100 and deduct a fixed, versioned amount per finding based on severity. This
keeps the formula auditable and keeps the score traceable to the exact
``RuleFinding`` objects a reviewer produced.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from featuresmith.core.rule_finding import RuleFinding
from featuresmith.scoring.schema import DimensionScore

if TYPE_CHECKING:
    from featuresmith.review.schema import ReviewResult

#: Fixed per-severity deduction (in score points) applied per finding.
SEVERITY_DEDUCTIONS: dict[str, float] = {
    "critical": 30.0,
    "warning": 15.0,
    "info": 5.0,
}


def score_from_findings(findings: tuple[RuleFinding, ...]) -> float:
    """Compute a 0-100 score from a section's findings.

    Args:
        findings: The findings attached to the reviewed section.

    Returns:
        A score clamped to [0, 100] and rounded to one decimal place.
    """
    deduction = sum(
        SEVERITY_DEDUCTIONS.get(finding.severity, 0.0) for finding in findings
    )
    return round(max(0.0, 100.0 - deduction), 1)


def build_rationale(label: str, score: float, findings: tuple[RuleFinding, ...]) -> str:
    """Build a plain-language rationale for a dimension score.

    Args:
        label: The dimension's display name.
        score: The computed dimension score.
        findings: The findings that lowered the score (empty when clean).

    Returns:
        A deterministic, human-readable explanation.
    """
    if not findings:
        return f"{label} scored {score:g}/100 with no issues found."
    counts: dict[str, int] = {}
    for finding in findings:
        severity = (
            finding.severity if finding.severity in SEVERITY_DEDUCTIONS else "info"
        )
        counts[severity] = counts.get(severity, 0) + 1
    ordered = sorted(
        counts.items(),
        key=lambda item: SEVERITY_DEDUCTIONS.get(item[0], 0.0),
        reverse=True,
    )
    summary = ", ".join(f"{count} {severity}" for severity, count in ordered)
    return (
        f"{label} scored {score:g}/100; {len(findings)} finding(s) lowered "
        f"the score ({summary})."
    )


def build_actions(findings: tuple[RuleFinding, ...]) -> tuple[str, ...]:
    """Derive concrete remediation actions from a section's findings.

    Args:
        findings: The findings that lowered the dimension's score.

    Returns:
        One action per finding, each pointing back to the flagged issue.
    """
    actions: list[str] = []
    for finding in findings:
        where = (
            f"in column '{finding.column_name}'"
            if finding.column_name is not None
            else "across the dataset"
        )
        actions.append(f"Address the flagged issue: {finding.title} ({where}).")
    return tuple(actions)


class SectionScoreDimension:
    """Base for dimensions that score one named review section.

    Subclasses only declare the stable identifiers; the scoring, rationale,
    and action derivation are shared and versioned here.
    """

    id: str
    label: str
    section_id: str
    default_weight: float = 1.0

    def applicable(self, result: ReviewResult) -> bool:
        """Return whether the dimension's review section exists.

        Args:
            result: The frozen ReviewResult.

        Returns:
            True when the backing reviewer produced its section.
        """
        return any(section.id == self.section_id for section in result.sections)

    def compute(self, result: ReviewResult) -> DimensionScore:
        """Compute the dimension score from its backing section's findings.

        Args:
            result: The frozen ReviewResult.

        Returns:
            The frozen DimensionScore.

        Raises:
            ValueError: If the backing section is absent; callers must gate on
                ``applicable()`` first.
        """
        section = next(
            (section for section in result.sections if section.id == self.section_id),
            None,
        )
        if section is None:
            raise ValueError(
                f"Dimension '{self.id}' requires section '{self.section_id}', "
                "which is absent from the review."
            )
        findings = tuple(section.findings)
        score = score_from_findings(findings)
        return DimensionScore(
            id=self.id,
            label=self.label,
            score=score,
            weight=self.default_weight,
            rationale=build_rationale(self.label, score, findings),
            contributing_findings=findings,
            suggested_actions=build_actions(findings),
        )
