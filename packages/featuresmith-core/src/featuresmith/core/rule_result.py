"""Serializable model representing the result of a rule engine run."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_finding import RuleFinding


@dataclass(frozen=True, slots=True)
class RuleResult:
    """The canonical output of the Featuresmith Rule Engine.

    Attributes:
        profile: The ProfileResult used for the evaluation.
        findings: The list of rule findings generated.
        executed_rules: List of rule IDs that were successfully executed.
        execution_time_ms: Total time taken to run the rules in milliseconds.
        failed_rules: Mapping from rule ID to the exception message/traceback for any rules that failed.
    """

    profile: ProfileResult
    findings: Sequence[RuleFinding]
    executed_rules: Sequence[str]
    execution_time_ms: float
    failed_rules: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze mutable fields to improve immutability consistency."""
        from types import MappingProxyType

        object.__setattr__(self, "findings", tuple(self.findings))
        object.__setattr__(self, "executed_rules", tuple(self.executed_rules))
        object.__setattr__(
            self, "failed_rules", MappingProxyType(dict(self.failed_rules))
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the rule result to a dictionary of primitive values.

        Returns:
            A dictionary representation suitable for JSON serialization.
        """
        from typing import cast

        from featuresmith.core.profile_result import _asdict_custom

        return cast(dict[str, Any], _asdict_custom(self))
