"""Tests for the Review Engine context carrier objects."""

from __future__ import annotations

import pandas as pd

import featuresmith as fs
from featuresmith.review.context import ReviewConfig, ReviewContext
from featuresmith.review.schema import ReviewCategory


def test_review_config_defaults() -> None:
    """ReviewConfig defaults to no filtering and no configuration."""
    config = ReviewConfig()

    assert config.target_column is None
    assert config.enabled_reviewers == ()
    assert config.enabled_categories == ()
    assert config.reviewer_config == {}


def test_review_config_freezes_fields() -> None:
    """ReviewConfig freezes sequence and mapping fields."""
    config = ReviewConfig(
        enabled_reviewers=["review.a"],
        enabled_categories=[ReviewCategory.QUALITY],
        reviewer_config={"review.a": {"threshold": 5.0}},
    )

    assert isinstance(config.enabled_reviewers, tuple)
    assert isinstance(config.enabled_categories, tuple)
    assert config.enabled_categories[0] is ReviewCategory.QUALITY
    assert config.reviewer_config["review.a"]["threshold"] == 5.0


def test_review_context_defaults() -> None:
    """ReviewContext requires a profile and defaults the rest."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    profile = fs.profile(df)

    context = ReviewContext(profile=profile)

    assert context.profile is profile
    assert context.dataset is None
    assert context.findings == ()
    assert context.config.enabled_reviewers == ()
    assert context.metadata == {}
    assert context.previous_profile is None


def test_review_context_freezes_fields() -> None:
    """ReviewContext freezes findings and metadata."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    profile = fs.profile(df)

    context = ReviewContext(
        profile=profile,
        findings=[],
        metadata={"source": "memory"},
    )

    assert isinstance(context.findings, tuple)
    assert context.metadata["source"] == "memory"
