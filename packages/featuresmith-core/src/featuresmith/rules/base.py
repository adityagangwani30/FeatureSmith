"""Abstract base class for all Featuresmith rules."""

from __future__ import annotations

import abc

from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_finding import RuleFinding


class BaseRule(abc.ABC):
    """Abstract base class for deterministic rule evaluation.

    Attributes:
        id: Unique stable identifier for the rule (e.g. "quality.missing_value_threshold").
        name: Short human-readable name for the rule.
        description: High-level description of what the rule flags.
        category: Category of the rule ("quality", "statistical", "leakage").
        severity: Default severity level ("info", "warning", "critical").
        enabled_by_default: True if the rule runs by default.
    """

    @property
    @abc.abstractmethod
    def id(self) -> str:
        """The stable namespaced identifier of the rule."""
        pass

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """A human-readable name of the rule."""
        pass

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """A detailed description of the rule's purpose."""
        pass

    @property
    @abc.abstractmethod
    def category(self) -> str:
        """The category of the rule: 'quality', 'statistical', or 'leakage'."""
        pass

    @property
    @abc.abstractmethod
    def severity(self) -> str:
        """The severity level: 'info', 'warning', or 'critical'."""
        pass

    @property
    @abc.abstractmethod
    def enabled_by_default(self) -> bool:
        """Whether this rule is active by default in the engine."""
        pass

    @abc.abstractmethod
    def evaluate(self, profile: ProfileResult) -> list[RuleFinding]:
        """Evaluate this rule against a computed ProfileResult.

        Args:
            profile: The precomputed ProfileResult structure.

        Returns:
            A list of RuleFinding instances.
        """
        pass
