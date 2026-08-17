from importlib import import_module

import featuresmith as fs


def test_workspace_packages_import() -> None:
    import_module("featuresmith")
    import_module("featuresmith.api")
    import_module("featuresmith.review")
    import_module("featuresmith_cli")
    import_module("featuresmith_dashboard")


def test_public_api_symbols_exported() -> None:
    """Verify all v0.3.0 and v0.4.0 public API symbols are exported on featuresmith."""
    expected_symbols = [
        "ConnectorError",
        "Dataset",
        "DatasetDiffResult",
        "DimensionScore",
        "MLReadinessScore",
        "PLAN_SCHEMA_VERSION",
        "Plan",
        "PlanItem",
        "ProfileResult",
        "Recommendation",
        "RecommendationEngine",
        "ReviewCategory",
        "ReviewResult",
        "ReviewSection",
        "RuleResult",
        "Severity",
        "SourceNotFoundError",
        "SourceParseError",
        "UnsupportedFormatError",
        "analyze",
        "compile_plan",
        "compile_plan_from_recommendations",
        "diff",
        "diff_findings",
        "load",
        "plan",
        "profile",
        "render",
        "render_diff",
        "review",
        "score",
    ]
    for symbol in expected_symbols:
        assert hasattr(fs, symbol), (
            f"Public symbol '{symbol}' is missing from featuresmith"
        )
