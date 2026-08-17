"""Public SDK entry module for Featuresmith."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from featuresmith.connectors.registry import default_registry
from featuresmith.core.dataset import Dataset as Dataset
from featuresmith.core.exceptions import (
    ConnectorError as ConnectorError,
)
from featuresmith.core.exceptions import (
    SourceNotFoundError as SourceNotFoundError,
)
from featuresmith.core.exceptions import (
    SourceParseError as SourceParseError,
)
from featuresmith.core.exceptions import (
    UnsupportedFormatError as UnsupportedFormatError,
)
from featuresmith.core.profile_result import ProfileResult as ProfileResult
from featuresmith.core.rule_result import RuleResult as RuleResult
from featuresmith.diff.render import render_diff as render_diff
from featuresmith.diff.schema import DatasetDiffResult as DatasetDiffResult
from featuresmith.plan import PLAN_SCHEMA_VERSION as PLAN_SCHEMA_VERSION
from featuresmith.plan import Plan as Plan
from featuresmith.plan import PlanItem as PlanItem
from featuresmith.plan.compiler import compile_plan as compile_plan
from featuresmith.profiling import profile_dataset
from featuresmith.recommendation.engine import (
    RecommendationEngine as RecommendationEngine,
)
from featuresmith.recommendation.schema import Recommendation as Recommendation
from featuresmith.review.render import render as render
from featuresmith.review.schema import (
    ReviewCategory as ReviewCategory,
)
from featuresmith.review.schema import (
    ReviewResult as ReviewResult,
)
from featuresmith.review.schema import (
    ReviewSection as ReviewSection,
)
from featuresmith.review.schema import (
    Severity as Severity,
)
from featuresmith.scoring.schema import (
    DimensionScore as DimensionScore,
)
from featuresmith.scoring.schema import (
    MLReadinessScore as MLReadinessScore,
)


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


def profile(
    source: object,
    *,
    max_correlation_columns: int = 100,
    max_frequency_table_size: int = 1000,
) -> ProfileResult:
    """Profile a supported source or Dataset and compute statistical summaries.

    Args:
        source: The data source to profile. This can be a pre-loaded Dataset
            object, a string representing a local file path (CSV, Excel,
            Parquet), or an in-memory pandas or Polars DataFrame.
        max_correlation_columns: Limit correlation computations to prevent
            combinatorial blowup (default 100).
        max_frequency_table_size: Maximum entries to keep in categorical
            frequency tables (default 1000).

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
    return profile_dataset(
        dataset,
        max_correlation_columns=max_correlation_columns,
        max_frequency_table_size=max_frequency_table_size,
    )


def analyze(
    source: object,
    *,
    target_column: str | None = None,
    enabled_rules: list[str] | None = None,
    rule_config: dict[str, Any] | None = None,
    max_correlation_columns: int = 100,
    max_frequency_table_size: int = 1000,
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
        max_frequency_table_size: Maximum entries to keep in categorical
            frequency tables (default 1000).

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
    prof_res = profile(
        dataset,
        max_correlation_columns=max_correlation_columns,
        max_frequency_table_size=max_frequency_table_size,
    )

    from featuresmith.rules.engine import RuleEngine

    engine = RuleEngine()
    return engine.run(
        prof_res,
        target_column=target_column,
        enabled_rules=enabled_rules,
        rule_config=rule_config,
    )


def diff(
    old: object,
    new: object,
    *,
    target_column: str | None = None,
    max_correlation_columns: int = 100,
    max_frequency_table_size: int = 1000,
) -> DatasetDiffResult:
    """Compare two versions of a dataset and summarize exactly what changed.

    The Dataset Diff Engine profiles both snapshots through the existing
    profiling engine, then reuses the leakage reviewers when a target column is
    provided. No new analysis of raw data is performed here — the diff is
    computed entirely from the two ``ProfileResult`` snapshots.

    Args:
        old: The older dataset snapshot. This can be a pre-loaded Dataset, a
            string representing a local file path, or an in-memory dataframe.
        new: The newer dataset snapshot, in the same accepted forms.
        target_column: Optional name of the target column in both datasets,
            used for the leakage comparison between snapshots.
        max_correlation_columns: Limit correlation computations during
            profiling (default 100).
        max_frequency_table_size: Maximum entries to keep in categorical
            frequency tables (default 1000).

    Returns:
        DatasetDiffResult: A frozen, serializable comparison of the two
            snapshots including schema, structure, quality, and (when a target
            is given) leakage deltas plus an overall health verdict.

    Raises:
        ConnectorError: If either snapshot fails to load before profiling.

    Examples:
        >>> import pandas as pd
        >>> import featuresmith as fs
        >>> old_df = pd.DataFrame({"a": [1, 2, 3], "b": [1.0, 2.0, 3.0]})
        >>> new_df = pd.DataFrame({"a": [1, 2, 3, 4], "c": [1, 2, 3, 4]})
        >>> diff = fs.diff(old_df, new_df)
        >>> diff.summary.columns_added
        1
    """
    if isinstance(old, Dataset):
        old_dataset = old
    else:
        old_dataset = load(old)
    if isinstance(new, Dataset):
        new_dataset = new
    else:
        new_dataset = load(new)
    previous = profile(
        old_dataset,
        max_correlation_columns=max_correlation_columns,
        max_frequency_table_size=max_frequency_table_size,
    )
    current = profile(
        new_dataset,
        max_correlation_columns=max_correlation_columns,
        max_frequency_table_size=max_frequency_table_size,
    )

    from featuresmith.diff.engine import compute_diff

    return compute_diff(
        previous,
        current,
        target_column=target_column,
    )


def diff_findings(result: DatasetDiffResult) -> list[Any]:
    """Return the diff findings for an existing DatasetDiffResult.

    Findings speak the same language as every other review finding and drive
    severity-based exit-code gating on surfaces such as the CLI. This accessor
    never re-runs a comparison.

    Args:
        result: An existing DatasetDiffResult.

    Returns:
        The list of RuleFinding objects derived from the diff.
    """
    from featuresmith.diff.findings import findings_from_diff

    return findings_from_diff(result)


def review(
    source: object,
    *,
    previous: object | None = None,
    target_column: str | None = None,
    enabled_reviewers: Sequence[str] | None = None,
    enabled_categories: Sequence[ReviewCategory] | None = None,
    reviewer_config: Mapping[str, Mapping[str, Any]] | None = None,
    max_correlation_columns: int = 100,
    max_frequency_table_size: int = 1000,
) -> ReviewResult:
    """Run an engineering review of a tabular source or Dataset.

    The Review Engine composes the existing profiling and rule engines into a
    single structured review. It accepts the same sources as ``fs.analyze()``
    (Dataset, file path, or in-memory dataframe) and returns one frozen,
    serializable ReviewResult.

    Args:
        source: The data source to review. This can be a pre-loaded Dataset
            object, a string representing a local file path (CSV, Excel,
            Parquet), or an in-memory pandas or Polars DataFrame.
        previous: Optional prior snapshot for diff-aware review, in the same
            accepted forms. When provided, the DiffReviewer compares the
            current dataset against it and attaches the DatasetDiffResult to
            ``result.diff``.
        target_column: Optional name of the target column in the dataset,
            forwarded for reviewers that use it.
        enabled_reviewers: Optional list of reviewer IDs to execute. If not
            provided, the engine runs all registered reviewers.
        enabled_categories: Optional list of reviewer categories to execute.
            If not provided, all categories are considered.
        reviewer_config: Optional dictionary of configurations keyed by
            reviewer ID.
        max_correlation_columns: Limit correlation computations during
            profiling (default 100).
        max_frequency_table_size: Maximum entries to keep in categorical
            frequency tables (default 1000).

    Returns:
        ReviewResult: The canonical Review Engine output containing the
            aggregated review sections and an overall summary. When ``previous``
            is provided, the result also carries the DatasetDiffResult on its
            ``diff`` field.

    Raises:
        ConnectorError: If the source is a file path or dataframe that fails to
            load before profiling.
        ValueError: If reviewer_config references an unknown reviewer ID.

    Notes:
        The review reuses ``fs.analyze()`` internally to obtain the profile and
        rule findings, so reviewers never re-read or re-profile the dataset.
        The previous snapshot is profiled once through the existing profiling
        engine; the DiffReviewer then compares the two profiles without
        re-profiling either dataset.

    Examples:
        >>> import pandas as pd
        >>> import featuresmith as fs
        >>> df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> result = fs.review(df)
        >>> result.overall_summary
        '8 of 8 sections passed with 0 finding(s) identified across the review.'
    """
    if isinstance(source, Dataset):
        dataset = source
    else:
        dataset = load(source)

    previous_profile = None
    if previous is not None:
        if isinstance(previous, Dataset):
            previous_dataset = previous
        else:
            previous_dataset = load(previous)
        previous_profile = profile(
            previous_dataset,
            max_correlation_columns=max_correlation_columns,
            max_frequency_table_size=max_frequency_table_size,
        )

    analysis = analyze(
        dataset,
        target_column=target_column,
        max_correlation_columns=max_correlation_columns,
        max_frequency_table_size=max_frequency_table_size,
    )

    from featuresmith.review.engine import ReviewEngine

    engine = ReviewEngine()
    return engine.run(
        profile=analysis.profile,
        dataset=dataset,
        findings=analysis.findings,
        target_column=target_column,
        previous_profile=previous_profile,
        enabled_reviewers=enabled_reviewers,
        enabled_categories=enabled_categories,
        reviewer_config=reviewer_config,
    )


def score(result: ReviewResult) -> MLReadinessScore | None:
    """Return the ML Readiness Score for an existing ReviewResult.

    This is a convenience accessor for callers who already hold a ReviewResult;
    it never performs a second analysis pass. When the result already carries a
    score (e.g. from ``fs.review()``) it is returned as-is; otherwise the score
    is computed deterministically from the result's sections.

    Args:
        result: An existing ReviewResult.

    Returns:
        The versioned MLReadinessScore, or None when no scoring dimension is
        applicable to the review.

    Examples:
        >>> import pandas as pd
        >>> import featuresmith as fs
        >>> df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> result = fs.review(df)
        >>> score = fs.score(result)
        >>> score.overall
        100.0
    """
    if result.score is not None:
        return result.score
    from featuresmith.scoring.aggregator import compute_score

    return compute_score(result)


def plan(
    result: ReviewResult,
    *,
    accept: list[str] | None = None,
) -> Plan:
    """Compile a deterministic Plan from accepted recommendations in a ReviewResult.

    The Plan is the central domain primitive of the Dataset Contract lifecycle.
    It represents an ordered, inspectable set of steps derived from accepted
    recommendations, with full traceability back to the originating findings
    and reviewers.

    Args:
        result: An existing ReviewResult containing recommendations.
        accept: List of recommendation IDs to include in the Plan. If None or
            empty, returns an empty Plan.

    Returns:
        A deterministic Plan with items corresponding to the accepted recommendations.

    Raises:
        ValueError: If any accepted recommendation ID is not found in the review's recommendations.

    Examples:
        >>> import pandas as pd
        >>> import featuresmith as fs
        >>> df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> result = fs.review(df)
        >>> plan = fs.plan(result, accept=["rec.quality.missingness.age"])
        >>> len(plan.items)
        1
    """
    from featuresmith.plan.compiler import compile_plan

    accepted = accept or []
    return compile_plan(result, accepted)
