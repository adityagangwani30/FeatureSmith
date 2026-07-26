"""JSON formatting for Featuresmith CLI results."""

from __future__ import annotations

import json

from featuresmith.api import RuleResult
from featuresmith_cli.utils import SEVERITY_LEVELS


def format_json(result: RuleResult, severity_threshold: str) -> str:
    """Serialize the RuleResult to JSON, filtering findings by severity threshold.

    Args:
        result: The canonical RuleResult from the SDK.
        severity_threshold: The severity level threshold to filter findings by.

    Returns:
        str: A JSON-serialized string of the result.
    """
    result_dict = result.to_dict()
    threshold_rank = SEVERITY_LEVELS.get(severity_threshold, 1)

    # Filter findings inside the dictionary representation
    filtered_findings = [
        finding
        for finding in result_dict.get("findings", [])
        if SEVERITY_LEVELS.get(finding.get("severity"), 1) >= threshold_rank
    ]
    result_dict["findings"] = filtered_findings

    return json.dumps(result_dict, indent=2)
