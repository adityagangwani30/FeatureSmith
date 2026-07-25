"""Explicit rule registry for Featuresmith rules."""

from __future__ import annotations

from collections.abc import Iterable

from featuresmith.rules.base import BaseRule


class RuleRegistry:
    """Registry that holds all available rules for analysis execution.

    Registration is kept explicit and static in this phase.
    """

    def __init__(self, rules: Iterable[BaseRule] = ()) -> None:
        """Initialize registry with a set of initial rules."""
        self._rules: dict[str, BaseRule] = {}
        for rule in rules:
            self.register(rule)

    def register(self, rule: BaseRule) -> None:
        """Register a new rule instance.

        Args:
            rule: An instance of a rule subclassing BaseRule.
        """
        self._rules[rule.id] = rule

    def unregister(self, rule: BaseRule | str) -> None:
        """Unregister a rule by instance or ID.

        Args:
            rule: The rule instance or rule ID to unregister.
        """
        rule_id = rule if isinstance(rule, str) else rule.id
        if rule_id in self._rules:
            del self._rules[rule_id]

    def list_rules(self) -> list[BaseRule]:
        """List all currently registered rules.

        Returns:
            A list of registered rule instances.
        """
        return list(self._rules.values())


def default_registry() -> RuleRegistry:
    """Return the default RuleRegistry loaded with the 8 seed rules."""
    from featuresmith.rules.cardinality import HighCardinalityRule
    from featuresmith.rules.constants import ConstantColumnsRule, FullyEmptyColumnsRule
    from featuresmith.rules.correlation import HighCorrelationRule
    from featuresmith.rules.duplicates import DuplicateRowsRule
    from featuresmith.rules.leakage import LeakageRuleTargetCorrelation
    from featuresmith.rules.missing import MissingValueThresholdRule
    from featuresmith.rules.outliers import OutlierDetectionRule

    return RuleRegistry(
        (
            MissingValueThresholdRule(),
            DuplicateRowsRule(),
            ConstantColumnsRule(),
            FullyEmptyColumnsRule(),
            HighCardinalityRule(),
            OutlierDetectionRule(),
            HighCorrelationRule(),
            LeakageRuleTargetCorrelation(),
        )
    )
