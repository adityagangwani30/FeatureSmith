"""Render pipeline that turns a ReviewResult or Plan into surface-native output."""

from __future__ import annotations

import abc
from collections.abc import Iterable

from featuresmith.plan.schema import Plan
from featuresmith.review.schema import ReviewResult
from featuresmith.scoring.schema import MLReadinessScore

Renderable = ReviewResult | Plan


class BaseRenderer(abc.ABC):
    """Base class for rendering a ReviewResult or Plan into one output format.

    Renderers are pure functions over the frozen object: they must never
    recompute or reinterpret a finding. Each surface owns only a renderer that
    turns the one canonical artifact into its native idiom.
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Return the target identifier this renderer produces."""
        pass

    @abc.abstractmethod
    def render(self, result: Renderable) -> str:
        """Render the result into the target format.

        Args:
            result: The frozen ReviewResult or Plan.

        Returns:
            The rendered output as a string.
        """
        pass


class ConsoleRenderer(BaseRenderer):
    """Render a ReviewResult as a deterministic plain-text terminal report.

    The output carries no ANSI styling so any thin surface can emit it
    directly; the CLI is a thin wrapper over this renderer.
    """

    @property
    def name(self) -> str:
        """Return the target identifier "console"."""
        return "console"

    def render(self, result: Renderable) -> str:
        """Render the result as a plain-text terminal report.

        Args:
            result: The frozen ReviewResult.

        Returns:
            The plain-text report.
        """
        if not isinstance(result, ReviewResult):
            raise TypeError("ConsoleRenderer only supports ReviewResult")
        lines: list[str] = ["Featuresmith Dataset Review"]
        summary = result.dataset_summary
        lines.append(f"Rows: {summary.row_count:,} | Columns: {summary.column_count:,}")
        lines.append(f"Engine: v{result.engine_version}")
        lines.append(f"Generated: {result.generated_at.isoformat()}")
        lines.append("")
        lines.append(result.overall_summary)
        lines.append("")
        if not result.sections:
            lines.append("No review sections produced.")
        for section in result.sections:
            lines.append(
                f"[{section.severity.value.upper()}] {section.title} ({section.id})"
            )
            if section.findings:
                for finding in section.findings:
                    column = finding.column_name or "(dataset)"
                    lines.append(f"  - {finding.title} [{column}]")
                    lines.append(f"      {finding.description}")
            else:
                lines.append("  No issues found.")
        if result.score is not None:
            lines.extend(self._render_score(result.score))
        return "\n".join(lines)

    def _render_score(self, score: MLReadinessScore) -> list[str]:
        """Render the ML Readiness Score block for the report.

        Args:
            score: The frozen MLReadinessScore to render.

        Returns:
            The score block lines, always pairing the overall number with its
            per-dimension breakdown and explanation.
        """
        lines: list[str] = [
            "",
            f"ML Readiness Score (scoring v{score.scoring_version})",
        ]
        lines.append(f"Overall: {score.overall:g}/100")
        lines.append("")
        for dimension in score.dimensions:
            suffix = (
                f" ({len(dimension.contributing_findings)} finding(s))"
                if dimension.contributing_findings
                else ""
            )
            lines.append(f"  {dimension.label}: {dimension.score:g}/100{suffix}")
        lines.append("")
        lines.append(f"Summary: {score.summary}")
        actions = [
            action
            for dimension in score.dimensions
            if dimension.score < 100.0
            for action in dimension.suggested_actions
        ]
        if actions:
            lines.append("")
            lines.append("What would improve this score:")
            lines.extend(f"  - {action}" for action in actions)
        if score.positive_findings:
            lines.append("")
            lines.append("Healthy dimensions:")
            lines.extend(f"  + {statement}" for statement in score.positive_findings)
        return lines


class RendererRegistry:
    """Registry of named renderers for review output targets."""

    def __init__(self, renderers: Iterable[BaseRenderer] = ()) -> None:
        """Initialize the registry with an optional set of initial renderers.

        Args:
            renderers: Iterable of renderer instances to register.
        """
        self._renderers: dict[str, BaseRenderer] = {}
        for renderer in renderers:
            self.register(renderer)

    def register(self, renderer: BaseRenderer) -> None:
        """Register a new renderer instance.

        Args:
            renderer: An instance of a BaseRenderer subclass.
        """
        self._renderers[renderer.name] = renderer

    def unregister(self, renderer: BaseRenderer | str) -> None:
        """Unregister a renderer by instance or name.

        Args:
            renderer: The renderer instance or renderer name to unregister.
        """
        name = renderer if isinstance(renderer, str) else renderer.name
        if name in self._renderers:
            del self._renderers[name]

    def get(self, name: str) -> BaseRenderer | None:
        """Retrieve a registered renderer by name.

        Args:
            name: The renderer name.

        Returns:
            The registered BaseRenderer instance, or None if not found.
        """
        return self._renderers.get(name)

    def render(self, name: str, result: ReviewResult | Plan) -> str:
        """Render the result with a named renderer.

        Args:
            name: The renderer name.
            result: The frozen ReviewResult or Plan.

        Returns:
            The rendered output as a string.

        Raises:
            ValueError: If no renderer is registered under the name.
        """
        renderer = self.get(name)
        if renderer is None:
            raise ValueError(f"Unknown renderer: '{name}'")
        return renderer.render(result)


class PlanRenderer(BaseRenderer):
    """Render a Plan as a deterministic plain-text terminal report.

    The output carries no ANSI styling so any thin surface can emit it
    directly; the CLI is a thin wrapper over this renderer.
    """

    @property
    def name(self) -> str:
        """Return the target identifier "plan_console"."""
        return "plan_console"

    def render(self, result: Renderable) -> str:
        """Render the plan as a plain-text terminal report.

        Args:
            result: The frozen Plan.

        Returns:
            The plain-text report.
        """
        if not isinstance(result, Plan):
            raise TypeError("PlanRenderer only supports Plan")
        plan = result
        lines: list[str] = ["Featuresmith Plan"]
        lines.append(f"Plan Schema Version: {plan.plan_schema_version}")
        lines.append(
            f"Accepted Recommendations: {len(plan.accepted_recommendation_ids)}"
        )
        lines.append(f"Plan Items: {len(plan.items)}")
        lines.append("")

        if not plan.items:
            lines.append("No plan items (no recommendations accepted).")
            return "\n".join(lines)

        for idx, item in enumerate(plan.items, 1):
            severity_marker = f"[{item.severity.upper()}]"
            lines.append(f"{idx}. {severity_marker} {item.title}")
            lines.append(f"   ID: {item.id}")
            lines.append(f"   From Recommendation: {item.recommendation_id}")
            lines.append(f"   Confidence: {item.confidence:.2f}")
            lines.append(f"   Severity: {item.severity}")
            if item.affected_columns:
                lines.append(f"   Affected Columns: {', '.join(item.affected_columns)}")
            lines.append(f"   Action: {item.suggested_action}")
            lines.append(f"   Rationale: {item.rationale}")
            if item.originating_findings:
                lines.append(
                    f"   Originating Findings: {len(item.originating_findings)}"
                )
            if item.originating_reviewers:
                lines.append(
                    f"   Originating Reviewers: {', '.join(item.originating_reviewers)}"
                )
            lines.append("")

        return "\n".join(lines)


def default_registry() -> RendererRegistry:
    """Return the built-in renderer registry.

    Only the console renderer ships in this foundation sprint; dashboard,
    HTML, and JSON renderers are future surfaces.
    """
    return RendererRegistry((ConsoleRenderer(), PlanRenderer()))


def render(result: ReviewResult | Plan, target: str = "console") -> str:
    """Render a ReviewResult or Plan into the requested target format.

    Args:
        result: The frozen ReviewResult or Plan.
        target: Output target name. Only "console" ships in this foundation
            sprint.

    Returns:
        The rendered output as a string.

    Raises:
        ValueError: If the target renderer is not registered.
    """
    # Determine the renderer based on the type of result
    if isinstance(result, Plan):
        renderer_name = "plan_console"
    else:
        renderer_name = target
    return default_registry().render(renderer_name, result)
