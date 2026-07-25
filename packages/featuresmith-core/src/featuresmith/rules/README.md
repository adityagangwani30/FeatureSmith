# Featuresmith Rule Engine

The Rule Engine translates deterministic profiling statistics (`ProfileResult`) into structured quality and leakage findings (`RuleFinding[]`).

## Architecture & Data Flow

The data flow through the Featuresmith pipeline is as follows:

```
Raw Data
   │
   ▼
[Connector] -> Dataset
                 │
                 ▼
          [Profiler] -> ProfileResult
                           │
                           ▼
                    [Rule Engine] -> RuleResult (Profile + Findings)
                                       │
                                       ▼
                       [Future Recommendation Engine]
```

1. **Dataset**: A normalized representation of raw source data (CSV, Parquet, pandas/Polars DataFrame).
2. **ProfileResult**: The canonical, strongly-typed summary statistics computed by the Profiling Engine.
3. **Rule Engine**: Runs deterministic, stateless rules over `ProfileResult` to discover data quality issues or potential target leakage.
4. **RuleFinding**: Represents a single issue or check that fired (e.g. high missing values, high correlation).
5. **RuleResult**: The aggregated output, carrying the profile, all findings, execution metadata, and details about any rule failures.
6. **Future Recommendation Engine**: Will consume these `RuleFinding` objects to propose ranked, explainable preprocessing actions.

---

## Extension: How to Add a New Rule

All rules inherit from the `BaseRule` class in [base.py](./base.py).

### Step 1: Create a Rule Class

Create a new file in this directory (or inside a subpackage) and inherit from `BaseRule`.

```python
from featuresmith.core.profile_result import ProfileResult
from featuresmith.core.rule_finding import RuleFinding
from featuresmith.rules.base import BaseRule


class MyCustomRule(BaseRule):
    """Flags columns that violate custom logic."""

    def __init__(self, my_threshold: float = 10.0) -> None:
        self.my_threshold = my_threshold

    @property
    def id(self) -> str:
        # Stable unique identifier
        return "quality.my_custom_rule"

    @property
    def name(self) -> str:
        return "My Custom Rule"

    @property
    def description(self) -> str:
        return "Checks for my custom condition."

    @property
    def category(self) -> str:
        # Category must be one of: "quality", "statistical", or "leakage"
        return "quality"

    @property
    def severity(self) -> str:
        # Severity must be one of: "info", "warning", or "critical"
        return "warning"

    @property
    def enabled_by_default(self) -> bool:
        return True

    def evaluate(self, profile: ProfileResult) -> list[RuleFinding]:
        findings = []
        # Access statistics via profile.column_profiles, profile.numeric_profiles, etc.
        for col_name, col_prof in profile.column_profiles.items():
            if col_prof.missing_percentage > self.my_threshold:
                findings.append(
                    RuleFinding(
                        rule_id=self.id,
                        rule_name=self.name,
                        category=self.category,
                        severity=self.severity,
                        column_name=col_name,
                        title=f"Custom issue in '{col_name}'",
                        description=f"Violated custom threshold of {self.my_threshold}",
                        evidence={
                            "value": col_prof.missing_percentage,
                            "threshold": self.my_threshold,
                        },
                    )
                )
        return findings
```

### Step 2: Register the Rule

Import and register your rule in the default registry located in [registry.py](./registry.py):

```python
def default_registry() -> RuleRegistry:
    # ...
    from featuresmith.rules.my_custom_rule import MyCustomRule

    return RuleRegistry(
        (
            # ... existing rules
            MyCustomRule(),
        )
    )
```

### Step 3: Write Tests

Add positive and negative test cases to `tests/rules/test_rules.py`. Every rule must ship with at least one test scenario where it triggers, and one where it does not.
