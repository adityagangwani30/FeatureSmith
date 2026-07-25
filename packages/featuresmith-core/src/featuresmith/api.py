"""Public SDK entry module for Featuresmith."""

from __future__ import annotations

from typing import Any

from featuresmith.connectors.registry import default_registry
from featuresmith.core.dataset import Dataset
from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_result import RuleResult
from featuresmith.profiling import profile_dataset


def load(source: object) -> Dataset:
    """Load a supported tabular source into a normalized dataset.

    Args:
        source: A local CSV, Excel, or Parquet path, or an in-memory pandas or
            Polars dataframe.

    Returns:
        A normalized dataset suitable for later pipeline stages.

    Raises:
        ConnectorError: If the source is missing, unsupported, or unreadable.
    """
    return default_registry().load(source)


def profile(source: object) -> ProfileResult:
    """Profile a supported tabular source or Dataset and return statistical summaries.

    Args:
        source: A Dataset object, a local file path (CSV, Excel, Parquet),
            or an in-memory pandas or Polars dataframe.

    Returns:
        A strongly-typed ProfileResult containing detailed summaries and stats.

    Raises:
        ConnectorError: If the source is a file path/dataframe that fails to load.
    """
    if isinstance(source, Dataset):
        dataset = source
    else:
        dataset = load(source)
    return profile_dataset(dataset)


def analyze(
    source: object,
    *,
    target_column: str | None = None,
    enabled_rules: list[str] | None = None,
    rule_config: dict[str, Any] | None = None,
) -> RuleResult:
    """Analyze a tabular source or Dataset, computing profile stats and running rules.

    Args:
        source: A Dataset, a local file path, or an in-memory dataframe.
        target_column: Optional name of the target column.
        enabled_rules: Optional list of rule IDs to execute.
        rule_config: Optional dictionary of rule configurations, keyed by rule ID.

    Returns:
        A RuleResult containing the statistics and all rule findings.
    """
    if isinstance(source, Dataset):
        dataset = source
    else:
        dataset = load(source)
    prof_res = profile(dataset)

    from featuresmith.rules.engine import RuleEngine

    engine = RuleEngine()
    return engine.run(
        prof_res,
        target_column=target_column,
        enabled_rules=enabled_rules,
        rule_config=rule_config,
    )
