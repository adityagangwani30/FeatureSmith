"""Timestamp and future-information leakage detectors."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date
from typing import Any

from featuresmith.core.profile_result import ProfileResult
from featuresmith.rules.leakage.base import LeakagePatternDetector
from featuresmith.rules.leakage.schema import LeakageFinding

# Unmistakable outcome markers used even when no target is declared. Columns
# with these names are very likely the target/outcome itself, so they warrant a
# low-confidence "possible outcome column" finding rather than silence.
_UNMISTAKABLE_OUTCOME = frozenset(
    {
        "target",
        "label",
        "outcome",
        "churn",
        "default",
        "prediction",
        "predicted",
        "actual",
    }
)

# Broader outcome-like markers considered when a target IS declared and the
# column is not the target itself.
_OUTCOME_LIKE = _UNMISTAKABLE_OUTCOME | frozenset(
    {"result", "score", "response", "class", "flag", "y", "t"}
)


class TimestampLeakageDetector(LeakagePatternDetector):
    """Flags datetime columns that extend past a declared prediction cutoff.

    The cutoff is explicit user configuration (``prediction_cutoff``, an ISO
    date) because inferring a cutoff automatically risks false confidence — the
    open design question in ``Dataset-Diff-And-Leakage-Detection.md`` §15.
    Without a configured cutoff the detector returns no findings.
    """

    @property
    def id(self) -> str:
        return "timestamp"

    @property
    def name(self) -> str:
        return "Timestamp Leakage"

    def detect(
        self,
        profile: ProfileResult,
        *,
        target_column: str | None = None,
        config: Mapping[str, Any] | None = None,
    ) -> list[LeakageFinding]:
        del target_column  # The timestamp detector does not use a target column.
        config = config or {}
        cutoff_raw = config.get("prediction_cutoff")
        if cutoff_raw is None:
            return []

        try:
            cutoff = date.fromisoformat(str(cutoff_raw))
        except ValueError:
            # A malformed cutoff yields no findings rather than a crash; the
            # engine would otherwise degrade the whole reviewer.
            return []

        findings: list[LeakageFinding] = []
        for col_name, dt_prof in profile.datetime_profiles.items():
            if dt_prof.maximum is None:
                continue
            try:
                max_dt = date.fromisoformat(dt_prof.maximum[:10])
            except ValueError:
                continue
            if max_dt <= cutoff:
                continue

            days_beyond = (max_dt - cutoff).days
            all_future = False
            if dt_prof.minimum is not None:
                try:
                    all_future = date.fromisoformat(dt_prof.minimum[:10]) > cutoff
                except ValueError:
                    all_future = False

            if all_future and days_beyond >= 30:
                confidence = 0.85
            elif days_beyond >= 30:
                confidence = 0.7
            else:
                confidence = 0.55

            findings.append(
                LeakageFinding(
                    pattern=self.id,
                    column_name=col_name,
                    title=f"Timestamps extend past the prediction cutoff in '{col_name}'",
                    rationale=(
                        f"The latest value in '{col_name}' is {dt_prof.maximum}, which is "
                        f"after the declared prediction cutoff of {cutoff_raw}. Values that "
                        "are only known after the prediction point can leak the outcome."
                    ),
                    evidence={
                        "prediction_cutoff": cutoff_raw,
                        "latest_timestamp": dt_prof.maximum,
                        "days_after_cutoff": days_beyond,
                    },
                    confidence=confidence,
                    severity="warning",
                    suggested_action=(
                        f"Verify whether values in '{col_name}' are knowable at prediction "
                        "time. If not, drop the column or lag it so it stays within the cutoff."
                    ),
                )
            )
        return findings


class FutureInfoDetector(LeakagePatternDetector):
    """Flags outcome-adjacent fields and columns that extend past an event time.

    Two deterministic signals are recognized: columns whose name marks them as
    likely outcome/target fields, and datetime columns whose latest value
    exceeds a declared ``event_timestamp_column`` (information from after the
    event that produced the row).
    """

    @property
    def id(self) -> str:
        return "future_info"

    @property
    def name(self) -> str:
        return "Future Information"

    def detect(
        self,
        profile: ProfileResult,
        *,
        target_column: str | None = None,
        config: Mapping[str, Any] | None = None,
    ) -> list[LeakageFinding]:
        config = config or {}
        findings: list[LeakageFinding] = []

        pearson = profile.correlation_summary.pearson

        # Signal 1: datetime columns that extend beyond a declared event timestamp.
        event_column = config.get("event_timestamp_column")
        if isinstance(event_column, str) and event_column in profile.datetime_profiles:
            event_max = profile.datetime_profiles[event_column].maximum
            if event_max is not None:
                for col_name, dt_prof in profile.datetime_profiles.items():
                    if col_name == event_column or dt_prof.maximum is None:
                        continue
                    if dt_prof.maximum <= event_max:
                        continue
                    findings.append(
                        LeakageFinding(
                            pattern=self.id,
                            column_name=col_name,
                            title=f"Column '{col_name}' extends beyond the event timestamp",
                            rationale=(
                                f"The latest value in '{col_name}' ({dt_prof.maximum}) is after "
                                f"the declared event timestamp '{event_column}' ({event_max}). "
                                "Information recorded after the event can leak the outcome."
                            ),
                            evidence={
                                "event_timestamp_column": event_column,
                                "event_timestamp_max": event_max,
                                "latest_timestamp": dt_prof.maximum,
                            },
                            confidence=0.6,
                            severity="warning",
                            suggested_action=(
                                f"Inspect '{col_name}'; if it is recorded after the event that "
                                "determines the outcome, it must not be used as a feature."
                            ),
                        )
                    )

        # Signal 2: outcome-adjacent column names.
        for col_name in profile.column_profiles:
            is_unmistakable = _name_matches(col_name, _UNMISTAKABLE_OUTCOME)
            if (
                target_column is not None
                and col_name != target_column
                and _name_matches(col_name, _OUTCOME_LIKE)
            ):
                corr = pearson.get(col_name, {}).get(target_column)
                if corr is not None and abs(corr) >= 0.5:
                    findings.append(
                        _outcome_finding(
                            col_name,
                            target_column,
                            confidence=0.85,
                            severity="critical",
                            strong_correlation=True,
                        )
                    )
                elif corr is None or abs(corr) >= 0.2:
                    findings.append(
                        _outcome_finding(
                            col_name,
                            target_column,
                            confidence=0.5,
                            severity="info",
                            strong_correlation=False,
                        )
                    )
            elif (
                target_column is None and col_name != target_column and is_unmistakable
            ):
                findings.append(
                    _outcome_finding(
                        col_name,
                        None,
                        confidence=0.4,
                        severity="info",
                        strong_correlation=False,
                    )
                )

        return findings


def _outcome_finding(
    col_name: str,
    target_column: str | None,
    *,
    confidence: float,
    severity: str,
    strong_correlation: bool,
) -> LeakageFinding:
    """Build a finding for an outcome-adjacent column."""
    if target_column is not None and strong_correlation:
        title = (
            f"Outcome-like field '{col_name}' is strongly correlated with the target"
        )
        rationale = (
            f"Column '{col_name}' is named like the outcome and correlates with the "
            f"declared target '{target_column}', which may mean it encodes the outcome."
        )
        action = (
            f"Check whether '{col_name}' holds the outcome or a post-hoc result; if so, "
            "exclude it from the feature set."
        )
    elif target_column is not None:
        title = f"Outcome-like field '{col_name}' is not the declared target"
        rationale = (
            f"Column '{col_name}' is named like the outcome but is not the declared target "
            f"'{target_column}'; it may still encode the outcome."
        )
        action = (
            f"Confirm whether '{col_name}' is a legitimate feature or contains outcome "
            "information that should be excluded."
        )
    else:
        title = f"Column '{col_name}' looks like the outcome or target"
        rationale = (
            f"Column '{col_name}' has an outcome-like name. If it holds the target, it "
            "must be declared as the target column and excluded from the features."
        )
        action = (
            f"Declare '{col_name}' as the target column if it holds the outcome, or rename "
            "it if it is a legitimate feature."
        )

    return LeakageFinding(
        pattern="future_info",
        column_name=col_name,
        title=title,
        rationale=rationale,
        evidence={
            "target_column": target_column,
            "outcome_like": True,
        },
        confidence=confidence,
        severity=severity,
        suggested_action=action,
    )


def _name_matches(name: str, markers: frozenset[str]) -> bool:
    """Return whether a column name matches any of the outcome markers.

    A name matches when it equals a marker or ends with ``_<marker>``.

    Args:
        name: The column name.
        markers: The set of marker names to match.

    Returns:
        True when the name matches a marker, False otherwise.
    """
    lower = name.lower()
    if lower in markers:
        return True
    return any(lower.endswith(f"_{marker}") for marker in markers)
