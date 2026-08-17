"""Plan package for Featuresmith.

This module provides the Plan primitive - a deterministic, inspectable plan
derived from accepted recommendations. The Plan is the central domain primitive
of the Dataset Contract lifecycle.
"""

from __future__ import annotations

from featuresmith.plan.compiler import compile_plan, compile_plan_from_recommendations
from featuresmith.plan.schema import PLAN_SCHEMA_VERSION, Plan, PlanItem

__all__ = [
    "PLAN_SCHEMA_VERSION",
    "Plan",
    "PlanItem",
    "compile_plan",
    "compile_plan_from_recommendations",
]
