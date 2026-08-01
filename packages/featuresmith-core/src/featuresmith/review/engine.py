"""Orchestrator for the Review Engine's five-stage pipeline."""

from __future__ import annotations

import traceback
from collections.abc import Mapping, Sequence
from typing import Any

from featuresmith.core.dataset import Dataset
from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.review.aggregator import ResultAggregator
from featuresmith.review.base import BaseReviewer
from featuresmith.review.context import ReviewConfig, ReviewContext
from featuresmith.review.registry import ReviewerRegistry, default_registry
from featuresmith.review.schema import ReviewCategory, ReviewResult, ReviewSection

REVIEW_ENGINE_VERSION = "0.1.0"


class ReviewEngine:
    """Orchestrates the fixed five-stage review pipeline.

    The pipeline is a fixed sequence; only reviewer dispatch varies by
    configuration:

    1. Resolve inputs (profile plus rule findings).
    2. Build the ReviewContext.
    3. Dispatch applicable reviewers in isolation.
    4. Aggregate the produced sections into a ReviewResult.
    5. Render (handled by the surface via ``featuresmith.review.render``).

    A crashing reviewer degrades to a recorded failure and is skipped; it never
    aborts the whole review, matching the existing rule-execution isolation
    guarantee.
    """

    def __init__(
        self,
        registry: ReviewerRegistry | None = None,
        aggregator: ResultAggregator | None = None,
    ) -> None:
        """Initialize the engine with a registry and aggregator.

        Args:
            registry: The reviewer registry; defaults to the empty built-in one.
            aggregator: The result aggregator; defaults to a new aggregator.
        """
        self.registry = registry or default_registry()
        self.aggregator = aggregator or ResultAggregator()

    def run(
        self,
        *,
        profile: ProfileResult,
        dataset: Dataset | None = None,
        findings: Sequence[RuleFinding] = (),
        target_column: str | None = None,
        enabled_reviewers: Sequence[str] | None = None,
        enabled_categories: Sequence[ReviewCategory] | None = None,
        reviewer_config: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> ReviewResult:
        """Execute the review pipeline against a computed profile.

        Args:
            profile: The computed ProfileResult of the dataset.
            dataset: The normalized dataset under review, when available.
            findings: The rule findings already computed by ``fs.analyze()``.
            target_column: Optional name of the target column, forwarded for
                reviewers that use it.
            enabled_reviewers: Optional allowlist of reviewer IDs to execute.
            enabled_categories: Optional allowlist of reviewer categories to
                execute.
            reviewer_config: Optional per-reviewer configuration keyed by
                reviewer ID.

        Returns:
            A frozen ReviewResult containing the aggregated sections.

        Raises:
            ValueError: If reviewer_config references an unknown reviewer ID.
        """
        config = ReviewConfig(
            target_column=target_column,
            enabled_reviewers=enabled_reviewers or (),
            enabled_categories=enabled_categories or (),
            reviewer_config=reviewer_config or {},
        )
        self._validate_config(config)

        context = ReviewContext(
            profile=profile,
            dataset=dataset,
            findings=findings,
            config=config,
        )

        sections: list[ReviewSection] = []
        failed: dict[str, str] = {}
        for reviewer in self.registry.list_reviewers():
            if not self._reviewer_enabled(reviewer, config):
                continue
            if reviewer.requires_previous_snapshot and context.previous_profile is None:
                continue
            if not reviewer.applicable(context):
                continue
            try:
                sections.append(reviewer.review(context))
            except Exception as error:
                failed[reviewer.id] = "".join(
                    traceback.format_exception(type(error), error, error.__traceback__)
                )

        return self.aggregator.aggregate(
            engine_version=REVIEW_ENGINE_VERSION,
            dataset_summary=profile.dataset_summary,
            sections=sections,
            failed_reviewers=failed,
        )

    def _validate_config(self, config: ReviewConfig) -> None:
        """Raise if reviewer configuration references an unknown reviewer."""
        for reviewer_id in config.reviewer_config:
            if not self.registry.get(reviewer_id):
                raise ValueError(f"Unknown reviewer ID in config: '{reviewer_id}'")

    def _reviewer_enabled(self, reviewer: BaseReviewer, config: ReviewConfig) -> bool:
        """Return whether a reviewer passes the configured filters."""
        if config.enabled_reviewers and reviewer.id not in config.enabled_reviewers:
            return False
        if (
            config.enabled_categories
            and reviewer.category not in config.enabled_categories
        ):
            return False
        return True
