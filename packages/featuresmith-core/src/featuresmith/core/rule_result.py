"""Serializable model representing the result of a rule engine run."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
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
    findings: list[RuleFinding]
    executed_rules: list[str]
    execution_time_ms: float
    failed_rules: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the rule result to a dictionary of primitive values.

        Returns:
            A dictionary representation suitable for JSON serialization.
        """
        return asdict(self)
