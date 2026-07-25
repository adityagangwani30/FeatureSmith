"""Public SDK entry module for Featuresmith."""

from __future__ import annotations

from typing import Any

from featuresmith.connectors.registry import default_registry
from featuresmith.core.dataset import Dataset
from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_result import RuleResult
from featuresmith.profiling import profile_dataset


def load(source: object) -> Dataset:
    """Load a supported tabular source into a normalized Dataset.

    Args:
        source: The data source to load. This can be a string representing a
            local file path (CSV, Excel, Parquet), or an in-memory pandas
            DataFrame or Polars DataFrame.

    Returns:
        Dataset: A normalized view of the loaded tabular dataset, containing
            the dataframe backend, schema, dtypes, and metadata.

    Raises:
        ConnectorError: If the source is missing, has an unsupported format,
            is corrupted, or is of an invalid type.

    Notes:
        For file paths, Featuresmith utilizes Polars for CSV and Parquet formats
        by default, and pandas for Excel formats. In-memory dataframes are
        wrapped without copying the underlying memory.

    Examples:
        >>> import pandas as pd
        >>> import featuresmith as fs
        >>> df = pd.DataFrame({"a": [1, 2, 3]})
        >>> dataset = fs.load(df)
        >>> dataset.row_count
        3
    """
    return default_registry().load(source)


def profile(source: object, *, max_correlation_columns: int = 100) -> ProfileResult:
    """Profile a supported source or Dataset and compute statistical summaries.

    Args:
        source: The data source to profile. This can be a pre-loaded Dataset
            object, a string representing a local file path (CSV, Excel,
            Parquet), or an in-memory pandas or Polars DataFrame.
        max_correlation_columns: Limit correlation computations to prevent
            combinatorial blowup (default 100).

    Returns:
        ProfileResult: A strongly-typed statistical profile containing dataset
            summaries, column profiles, correlations, and logical types.

    Raises:
        ConnectorError: If the source is a file path or dataframe that fails to
            load before profiling.

    Notes:
        This is a deterministic profiling engine. The statistical calculations
        run on the underlying dataframe backend using vectorized Polars or pandas
        APIs. The resulting ProfileResult is frozen and fully serializable.

    Examples:
        >>> import polars as pl
        >>> import featuresmith as fs
        >>> df = pl.DataFrame({"a": [1.0, 2.0, None]})
        >>> prof = fs.profile(df)
        >>> prof.dataset_summary.column_count
        1
        >>> prof.column_profiles["a"].missing_count
        1
    """
    if isinstance(source, Dataset):
        dataset = source
    else:
        dataset = load(source)
    return profile_dataset(dataset, max_correlation_columns=max_correlation_columns)


def analyze(
    source: object,
    *,
    target_column: str | None = None,
    enabled_rules: list[str] | None = None,
    rule_config: dict[str, Any] | None = None,
    max_correlation_columns: int = 100,
) -> RuleResult:
    """Analyze a tabular source or Dataset, computing profile stats and running rules.

    Args:
        source: The data source to analyze. This can be a pre-loaded Dataset
            object, a string representing a local file path (CSV, Excel,
            Parquet), or an in-memory pandas or Polars DataFrame.
        target_column: Optional name of the target column in the dataset, used
            specifically for evaluating potential target leakage.
        enabled_rules: Optional list of rule IDs to execute. If not provided,
            the engine runs all rules that are enabled by default.
        rule_config: Optional dictionary of configurations keyed by rule ID.
            For example, `{"quality.missing_value_threshold": {"threshold": 15.0}}`.
        max_correlation_columns: Limit correlation computations during profiling to
            prevent combinatorial blowup (default 100).

    Returns:
        RuleResult: The canonical output of the Rule Engine containing the
            computed ProfileResult, aggregated list of RuleFindings, list of
            executed rule IDs, and execution time metadata.

    Raises:
        ConnectorError: If the source is a file path or dataframe that fails to
            load before profiling.

    Notes:
        This function integrates connector loading, profiling, and rule
        evaluation into a single public endpoint. The evaluation of rules is
        deterministic and isolated; a crash in any single rule does not cause
        the function to fail, but is recorded in the failed_rules mapping.

    Examples:
        >>> import pandas as pd
        >>> import featuresmith as fs
        >>> df = pd.DataFrame({
        ...     "x": [1, 2, 3, 4, 5],
        ...     "y": [1.0, 2.0, 3.0, 4.0, 5.0],
        ...     "target": [0, 1, 0, 1, 0]
        ... })
        >>> result = fs.analyze(df, target_column="target")
        >>> len(result.findings) >= 0
        True
    """
    if isinstance(source, Dataset):
        dataset = source
    else:
        dataset = load(source)
    prof_res = profile(dataset, max_correlation_columns=max_correlation_columns)

    from featuresmith.rules.engine import RuleEngine

    engine = RuleEngine()
    return engine.run(
        prof_res,
        target_column=target_column,
        enabled_rules=enabled_rules,
        rule_config=rule_config,
    )
