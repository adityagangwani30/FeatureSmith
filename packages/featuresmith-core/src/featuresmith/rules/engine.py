"""Orchestrator for executing deterministic rules."""

from __future__ import annotations

import inspect
import time
import traceback
from typing import Any

from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.core.rule_result import RuleResult
from featuresmith.rules.registry import RuleRegistry, default_registry


class RuleEngine:
    """Orchestrates rule execution and generates a unified RuleResult."""

    def __init__(self, registry: RuleRegistry | None = None) -> None:
        """Initialize RuleEngine with a registry, defaulting to built-ins."""
        self.registry = registry or default_registry()

    def run(
        self,
        profile: ProfileResult,
        *,
        target_column: str | None = None,
        enabled_rules: list[str] | None = None,
        rule_config: dict[str, dict[str, Any]] | None = None,
    ) -> RuleResult:
        """Execute rules against the given ProfileResult.

        Args:
            profile: The computed ProfileResult.
            target_column: Optional name of the target column for leakage detection.
            enabled_rules: Optional list of rule IDs to execute. If None, runs
                all rules where enabled_by_default is True.
            rule_config: Optional dictionary of rule configurations, keyed by rule ID.

        Returns:
            A RuleResult containing execution stats, findings, and any failures.
        """
        # Validate rule configuration before execution
        if rule_config:
            for rule_id, config in rule_config.items():
                rule = self.registry.get(rule_id)
                if not rule:
                    raise ValueError(f"Unknown rule ID in config: '{rule_id}'")

                sig = inspect.signature(rule.__class__)
                try:
                    check_config = dict(config)
                    if (
                        rule_id == "leakage.potential_leakage"
                        and "target_column" not in check_config
                        and target_column is not None
                    ):
                        check_config["target_column"] = target_column

                    # 1. Bind parameters to check names
                    bound = sig.bind(**check_config)

                    # 2. Check parameter types against annotations
                    from typing import get_type_hints

                    type_hints = get_type_hints(rule.__class__.__init__)

                    for param_name, param_value in bound.arguments.items():
                        if param_name in type_hints:
                            annotation = type_hints[param_name]
                            import types
                            from typing import Union, get_args, get_origin

                            def is_instance_of_type(val: Any, t: Any) -> bool:
                                origin = get_origin(t)
                                if origin is Union or origin is types.UnionType:
                                    return any(
                                        is_instance_of_type(val, arg)
                                        for arg in get_args(t)
                                    )
                                if t is Any:
                                    return True
                                if t is None or t is type(None):
                                    return val is None
                                if t is float and isinstance(val, int):
                                    return True
                                if isinstance(t, type):
                                    return isinstance(val, t)
                                return True

                            if not is_instance_of_type(param_value, annotation):
                                raise TypeError(
                                    f"Incorrect type for parameter '{param_name}'. "
                                    f"Expected {annotation}, got {type(param_value).__name__}."
                                )

                    # 3. Instantiate to check range/value constraints
                    _ = rule.__class__(**check_config)
                except (TypeError, ValueError) as e:
                    raise type(e)(
                        f"Invalid configuration for rule '{rule_id}': {e}"
                    ) from e

        start_time = time.perf_counter()

        findings: list[RuleFinding] = []
        executed_rules: list[str] = []
        failed_rules: dict[str, str] = {}

        # Determine which rules to run
        all_rules = self.registry.list_rules()
        rules_to_run = []
        for rule in all_rules:
            if enabled_rules is not None:
                if rule.id in enabled_rules:
                    rules_to_run.append(rule)
            else:
                if rule.enabled_by_default:
                    rules_to_run.append(rule)

        for rule in rules_to_run:
            try:
                # Resolve rule configuration overrides
                config = {}
                if rule_config and rule.id in rule_config:
                    config.update(rule_config[rule.id])

                # Inject target column for leakage detection rule
                if rule.id == "leakage.potential_leakage" and target_column is not None:
                    config["target_column"] = target_column

                # If we have configuration, instantiate a new configured instance of the rule
                if config:
                    rule_instance = rule.__class__(**config)
                else:
                    rule_instance = rule

                # Evaluate the rule
                rule_findings = rule_instance.evaluate(profile)
                findings.extend(rule_findings)
                executed_rules.append(rule.id)
            except Exception as e:
                # Isolate rule failure to prevent crashing the whole pipeline
                failed_rules[rule.id] = "".join(
                    traceback.format_exception(type(e), e, e.__traceback__)
                )

        execution_time_ms = (time.perf_counter() - start_time) * 1000.0

        return RuleResult(
            profile=profile,
            findings=findings,
            executed_rules=executed_rules,
            execution_time_ms=execution_time_ms,
            failed_rules=failed_rules,
        )
