"""Tests for the ReviewEngine orchestration pipeline."""

from __future__ import annotations

import pandas as pd
import pytest

import featuresmith as fs
from featuresmith.core.profile_result import ProfileResult
from featuresmith.review.base import BaseReviewer
from featuresmith.review.context import ReviewContext
from featuresmith.review.engine import REVIEW_ENGINE_VERSION, ReviewEngine
from featuresmith.review.registry import ReviewerRegistry
from featuresmith.review.schema import (
    ReviewCategory,
    ReviewSection,
    Severity,
)


class FakeReviewer(BaseReviewer):
    """A configurable reviewer for engine tests."""

    def __init__(
        self,
        reviewer_id: str,
        *,
        category: ReviewCategory = ReviewCategory.QUALITY,
        severity: Severity = Severity.INFO,
        requires_previous: bool = False,
        applicable: bool = True,
        raises: bool = False,
    ) -> None:
        """Configure the fake reviewer behavior."""
        self._id = reviewer_id
        self._category = category
        self._severity = severity
        self._requires_previous = requires_previous
        self._applicable = applicable
        self._raises = raises

    @property
    def id(self) -> str:
        """Return the reviewer ID."""
        return self._id

    @property
    def category(self) -> ReviewCategory:
        """Return the reviewer category."""
        return self._category

    @property
    def requires_previous_snapshot(self) -> bool:
        """Return whether a previous snapshot is required."""
        return self._requires_previous

    def applicable(self, context: ReviewContext) -> bool:
        """Return the configured applicability."""
        return self._applicable

    def review(self, context: ReviewContext) -> ReviewSection:
        """Produce a section or raise when configured to do so."""
        if self._raises:
            raise RuntimeError("boom")
        return ReviewSection(
            id=self.id,
            title=self.id,
            category=self.category,
            severity=self._severity,
        )


def build_profile() -> ProfileResult:
    """Build a ProfileResult from a small fixture dataframe."""
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": [1.0, 2.0, 3.0, 4.0, 5.0]})
    return fs.profile(df)


def test_zero_reviewers_completes() -> None:
    """The pipeline must complete successfully with zero reviewers."""
    result = ReviewEngine().run(profile=build_profile())

    assert result.engine_version == REVIEW_ENGINE_VERSION
    assert result.sections == ()
    assert result.overall_summary == "Review complete: no reviewers ran."
    assert result.dataset_summary.row_count == 5


def test_reviewer_produces_section() -> None:
    """A registered reviewer contributes its section to the result."""
    registry = ReviewerRegistry((FakeReviewer("review.quality.a"),))
    result = ReviewEngine(registry=registry).run(profile=build_profile())

    assert [section.id for section in result.sections] == ["review.quality.a"]


def test_broken_reviewer_is_fault_isolated() -> None:
    """A crashing reviewer degrades to a warning without crashing the run."""
    registry = ReviewerRegistry(
        (
            FakeReviewer("review.quality.broken", raises=True),
            FakeReviewer("review.quality.ok", severity=Severity.PASSED),
        )
    )
    result = ReviewEngine(registry=registry).run(profile=build_profile())

    assert [section.id for section in result.sections] == ["review.quality.ok"]
    assert result.overall_summary.endswith("1 reviewer(s) failed and were skipped.")


def test_enabled_reviewers_filter() -> None:
    """Only the allowlisted reviewer IDs run."""
    registry = ReviewerRegistry(
        (
            FakeReviewer("review.quality.a"),
            FakeReviewer("review.quality.b"),
        )
    )
    result = ReviewEngine(registry=registry).run(
        profile=build_profile(), enabled_reviewers=["review.quality.b"]
    )

    assert [section.id for section in result.sections] == ["review.quality.b"]


def test_enabled_categories_filter() -> None:
    """Only reviewers in the allowlisted categories run."""
    registry = ReviewerRegistry(
        (
            FakeReviewer("review.quality.a", category=ReviewCategory.QUALITY),
            FakeReviewer("review.schema.a", category=ReviewCategory.SCHEMA),
        )
    )
    result = ReviewEngine(registry=registry).run(
        profile=build_profile(), enabled_categories=[ReviewCategory.SCHEMA]
    )

    assert [section.id for section in result.sections] == ["review.schema.a"]


def test_previous_snapshot_reviewer_is_skipped() -> None:
    """Diff-category reviewers are skipped when no previous snapshot exists."""
    registry = ReviewerRegistry(
        (FakeReviewer("review.diff.a", requires_previous=True),)
    )
    result = ReviewEngine(registry=registry).run(profile=build_profile())

    assert result.sections == ()


def test_applicable_false_skips_reviewer() -> None:
    """Reviewers declaring themselves not applicable are skipped."""
    registry = ReviewerRegistry(
        (
            FakeReviewer("review.quality.skip", applicable=False),
            FakeReviewer("review.quality.run"),
        )
    )
    result = ReviewEngine(registry=registry).run(profile=build_profile())

    assert [section.id for section in result.sections] == ["review.quality.run"]


def test_unknown_reviewer_config_raises() -> None:
    """reviewer_config referencing an unknown reviewer ID raises ValueError."""
    engine = ReviewEngine()
    with pytest.raises(ValueError, match="Unknown reviewer ID"):
        engine.run(profile=build_profile(), reviewer_config={"review.missing": {}})
