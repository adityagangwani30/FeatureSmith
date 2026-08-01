"""Merge review sections into a canonical ReviewResult."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import UTC, datetime

from featuresmith.core.profile_result import DatasetSummary
from featuresmith.review.schema import ReviewResult, ReviewSection, Severity


class ResultAggregator:
    """Aggregates reviewer sections into a single, frozen ReviewResult.

    Aggregation is a pure merge: sections are sorted by severity (most severe
    first), an overall summary is templated from the sections, and no section
    content is ever altered — traceability from a section back to its reviewer
    and findings is preserved untouched.
    """

    def aggregate(
        self,
        *,
        engine_version: str,
        dataset_summary: DatasetSummary,
        sections: Sequence[ReviewSection],
        generated_at: datetime | None = None,
        failed_reviewers: Mapping[str, str] | None = None,
    ) -> ReviewResult:
        """Merge sections into a frozen, severity-sorted ReviewResult.

        Args:
            engine_version: Version of the Review Engine result schema.
            dataset_summary: The dataset-level summary of the reviewed dataset.
            sections: The sections produced by the dispatched reviewers.
            generated_at: Timestamp to record; defaults to the current UTC time.
            failed_reviewers: Optional mapping of reviewer ID to error message
                for reviewers that failed during execution; when present, a
                warning is folded into the overall summary.

        Returns:
            A frozen ReviewResult with sections sorted by severity.
        """
        sorted_sections = tuple(
            sorted(
                sections,
                key=lambda section: section.severity.rank,
                reverse=True,
            )
        )
        overall_summary = _build_overall_summary(sorted_sections)
        if failed_reviewers:
            overall_summary = (
                f"{overall_summary} "
                f"{len(failed_reviewers)} reviewer(s) failed and were skipped."
            )
        return ReviewResult(
            engine_version=engine_version,
            dataset_summary=dataset_summary,
            generated_at=generated_at or _utc_now(),
            sections=sorted_sections,
            overall_summary=overall_summary,
        )


def _build_overall_summary(sections: Sequence[ReviewSection]) -> str:
    """Build a short, templated, non-AI roll-up of the review."""
    if not sections:
        return "Review complete: no reviewers ran."
    total_findings = sum(len(section.findings) for section in sections)
    passed = sum(1 for section in sections if section.severity is Severity.PASSED)
    return (
        f"{passed} of {len(sections)} sections passed with "
        f"{total_findings} finding(s) identified across the review."
    )


def _utc_now() -> datetime:
    """Return the current UTC timestamp as an aware datetime."""
    return datetime.now(UTC)
