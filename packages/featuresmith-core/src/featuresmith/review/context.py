"""Typed carrier objects shared between Review Engine pipeline stages."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from featuresmith.core.dataset import Dataset
from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.review.schema import ReviewCategory


@dataclass(frozen=True, slots=True)
class ReviewConfig:
    """Resolved configuration for a single review run.

    Attributes:
        target_column: Optional name of the target column, forwarded for
            reviewers that use it.
        enabled_reviewers: Optional allowlist of reviewer IDs to execute; when
            empty, all registered reviewers are considered.
        enabled_categories: Optional allowlist of reviewer categories to
            execute; when empty, all categories are considered.
        reviewer_config: Per-reviewer configuration keyed by reviewer ID.
    """

    target_column: str | None = None
    enabled_reviewers: Sequence[str] = ()
    enabled_categories: Sequence[ReviewCategory] = ()
    reviewer_config: Mapping[str, Mapping[str, Any]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze mutable fields to keep the config immutable."""
        object.__setattr__(self, "enabled_reviewers", tuple(self.enabled_reviewers))
        object.__setattr__(self, "enabled_categories", tuple(self.enabled_categories))
        frozen = {
            key: MappingProxyType(dict(value))
            for key, value in self.reviewer_config.items()
        }
        object.__setattr__(self, "reviewer_config", MappingProxyType(frozen))


@dataclass(frozen=True, slots=True)
class ReviewContext:
    """Everything a reviewer may read to produce a section.

    The context is immutable; reviewers read from it and never mutate it.

    Attributes:
        profile: The computed ProfileResult of the reviewed dataset.
        dataset: The normalized dataset under review, when available.
        findings: The RuleFinding objects already computed by ``fs.analyze()``.
        config: The resolved review configuration.
        metadata: Read-only descriptive metadata about the run.
        previous_profile: Optional profile of a prior snapshot; populated when
            diff-category reviewers are active (future).
    """

    profile: ProfileResult
    dataset: Dataset | None = None
    findings: Sequence[RuleFinding] = ()
    config: ReviewConfig = field(default_factory=ReviewConfig)
    metadata: Mapping[str, Any] = field(default_factory=dict)
    previous_profile: ProfileResult | None = None

    def __post_init__(self) -> None:
        """Freeze mutable fields to keep the context immutable."""
        object.__setattr__(self, "findings", tuple(self.findings))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
