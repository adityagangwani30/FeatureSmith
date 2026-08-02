"""Base interface for deterministic leakage pattern detectors."""

from __future__ import annotations

import abc
from collections.abc import Mapping
from typing import Any

from featuresmith.core.profile_result import ProfileResult
from featuresmith.rules.leakage.schema import LeakageFinding


class LeakagePatternDetector(abc.ABC):
    """Abstract base class for one deterministic leakage pattern.

    A detector is a pure, side-effect-free function over a computed
    ProfileResult: it never re-reads or re-profiles the dataset and never
    infers a target column on its own. Detectors are the matured successors of
    the rule engine's naive leakage rules (``Architecture.md`` §9) and live
    under ``featuresmith.rules.leakage`` per
    ``Dataset-Diff-And-Leakage-Detection.md`` §8.2/§9.
    """

    @property
    @abc.abstractmethod
    def id(self) -> str:
        """Return the stable pattern identifier (e.g. "target_correlation")."""
        pass

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Return the human-readable detector name."""
        pass

    @abc.abstractmethod
    def detect(
        self,
        profile: ProfileResult,
        *,
        target_column: str | None = None,
        config: Mapping[str, Any] | None = None,
    ) -> list[LeakageFinding]:
        """Detect this pattern against a computed profile.

        Args:
            profile: The precomputed ProfileResult of the dataset.
            target_column: The declared target column, or None when the user
                did not declare one. Detectors never infer a target.
            config: Optional detector configuration keyed by detector-specific
                setting names.

        Returns:
            A list of LeakageFinding instances (empty when the pattern is
            absent or when the detector lacks the required configuration).
        """
        pass
