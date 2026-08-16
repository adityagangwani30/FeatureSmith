"""Diff-aware reviewer that wraps the standalone Dataset Diff Engine.

The ``DiffReviewer`` is the Review Engine integration of the Dataset Diff
capability (``Architecture.md`` §22.A1). It is an ordinary reviewer: it
declares the ``diff`` category, requires a previous snapshot, and only
activates when ``context.previous_profile`` is set. Its ``review()`` calls the
existing ``compute_diff()`` primitive rather than reimplementing any comparison
logic, then converts the typed ``DatasetDiffResult`` into shared
``RuleFinding`` objects via ``findings_from_diff()`` so the section speaks the
same language as every other review section.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Mapping
from typing import Any

from featuresmith.core.rule_finding import RuleFinding
from featuresmith.diff.engine import compute_diff
from featuresmith.diff.findings import findings_from_diff
from featuresmith.diff.schema import DatasetDiffResult, DiffConfig
from featuresmith.review.context import ReviewContext
from featuresmith.review.reviewers.base import SectionReviewer
from featuresmith.review.schema import ReviewCategory

_DIFF_CONFIG_FIELDS = {field.name for field in dataclasses.fields(DiffConfig)}


class DiffReviewer(SectionReviewer):
    """Compare the reviewed dataset against a previous snapshot.

    The reviewer produces a ``diff``-category section whose findings describe
    exactly what changed between the two snapshots. It never re-profiles the
    previous dataset — it reads ``context.previous_profile`` directly — and it
    never re-derives statistics: the comparison is computed entirely by the
    existing Dataset Diff Engine.
    """

    def __init__(self) -> None:
        """Initialize the reviewer with no computed diff yet."""
        self._diff_result: DatasetDiffResult | None = None

    @property
    def id(self) -> str:
        """Return the stable reviewer identifier."""
        return "review.diff"

    @property
    def title(self) -> str:
        """Return the human-readable heading for the produced section."""
        return "Dataset Diff"

    @property
    def category(self) -> ReviewCategory:
        """Return the reviewer category."""
        return ReviewCategory.DIFF

    @property
    def requires_previous_snapshot(self) -> bool:
        """Diff reviewers only run when a previous snapshot exists."""
        return True

    def applicable(self, context: ReviewContext) -> bool:
        """Return whether a previous snapshot is available for comparison.

        Args:
            context: The frozen review context.

        Returns:
            True only when the context carries a previous profile.
        """
        return context.previous_profile is not None

    @property
    def diff_result(self) -> DatasetDiffResult | None:
        """Return the computed diff for attachment to the ReviewResult.

        Returns:
            The DatasetDiffResult computed by the last ``review()`` call, or
            None when the reviewer has not run yet.
        """
        return self._diff_result

    def _collect_findings(self, context: ReviewContext) -> list[RuleFinding]:
        """Compute the diff and return its findings for the section.

        Args:
            context: The frozen review context.

        Returns:
            The deterministic findings derived from the diff (empty when the
            two snapshots are identical).
        """
        previous = context.previous_profile
        if previous is None:
            return []
        diff_config = self._diff_config(context)
        diff_result = compute_diff(
            previous,
            context.profile,
            target_column=context.config.target_column,
            config=diff_config,
        )
        self._diff_result = diff_result
        return findings_from_diff(diff_result, diff_config)

    def _diff_config(self, context: ReviewContext) -> DiffConfig | None:
        """Resolve a DiffConfig from this reviewer's configuration mapping.

        Only the known ``DiffConfig`` fields are forwarded; unknown keys are
        ignored so a reviewer config never crashes the diff.

        Args:
            context: The frozen review context.

        Returns:
            A DiffConfig when any known threshold is configured, else None.
        """
        raw: Mapping[str, Any] = self._config_for(context)
        known = {key: value for key, value in raw.items() if key in _DIFF_CONFIG_FIELDS}
        if not known:
            return None
        return DiffConfig(**known)
