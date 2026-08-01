"""Shared base for built-in section reviewers."""

from __future__ import annotations

import abc
from collections.abc import Mapping, Sequence
from typing import Any

from featuresmith.core.rule_finding import RuleFinding
from featuresmith.review.base import BaseReviewer
from featuresmith.review.context import ReviewContext
from featuresmith.review.schema import ReviewSection, Severity


class SectionReviewer(BaseReviewer):
    """Base for reviewers that assemble one section from context-derived findings.

    A section reviewer derives a deterministic list of ``RuleFinding`` objects
    from the frozen context (profile plus per-reviewer configuration), computes
    the section severity as the worst finding severity, and wraps everything in
    a single ``ReviewSection``. Reviewers never re-read or re-profile the
    dataset.
    """

    @property
    def requires_previous_snapshot(self) -> bool:
        """Built-in section reviewers never need a previous snapshot."""
        return False

    @property
    @abc.abstractmethod
    def title(self) -> str:
        """Return the human-readable heading for the produced section."""
        pass

    @abc.abstractmethod
    def _collect_findings(self, context: ReviewContext) -> list[RuleFinding]:
        """Return the deterministic findings for this reviewer's section.

        Args:
            context: The frozen review context.

        Returns:
            The findings to attach to the section (empty when clean).
        """
        pass

    def _config_for(self, context: ReviewContext) -> Mapping[str, Any]:
        """Return this reviewer's per-reviewer configuration mapping.

        Args:
            context: The frozen review context.

        Returns:
            The reviewer configuration; an empty mapping when unset.
        """
        return context.config.reviewer_config.get(self.id, {})

    def review(self, context: ReviewContext) -> ReviewSection:
        """Assemble the reviewer's section for the given context.

        Args:
            context: The frozen review context.

        Returns:
            A fully-formed ReviewSection (never None).
        """
        findings = self._collect_findings(context)
        return ReviewSection(
            id=self.id,
            title=self.title,
            category=self.category,
            severity=section_severity(findings),
            findings=findings,
        )


_FINDING_SEVERITY: Mapping[str, Severity] = {
    "critical": Severity.CRITICAL,
    "warning": Severity.WARNING,
    "info": Severity.INFO,
}


def section_severity(findings: Sequence[RuleFinding]) -> Severity:
    """Compute a section-level severity from a list of findings.

    The section severity is the worst finding severity; a section with no
    findings is ``Severity.PASSED``.

    Args:
        findings: The findings attached to the section.

    Returns:
        The section-level severity.
    """
    severities = [
        _FINDING_SEVERITY[finding.severity]
        for finding in findings
        if finding.severity in _FINDING_SEVERITY
    ]
    if not severities:
        return Severity.PASSED
    return max(severities, key=lambda severity: severity.rank)
