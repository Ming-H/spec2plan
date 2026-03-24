"""Main generator - coordinates the plan generation pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader, select_autoescape

from spec2plan.core.analyzer import Analyzer
from spec2plan.core.architect import Architect
from spec2plan.core.planner import Planner

if TYPE_CHECKING:
    from spec2plan.core.analyzer import AnalysisResult
    from spec2plan.core.architect import ArchitectureDesign
    from spec2plan.core.planner import ImplementationPlan


class Generator:
    """Coordinates the plan generation pipeline."""

    def __init__(self) -> None:
        self._analyzer = Analyzer()
        self._architect = Architect()
        self._planner = Planner()
        self._template_env = self._setup_template_env()

    def _setup_template_env(self) -> Environment:
        """Set up Jinja2 template environment."""
        template_dir = Path(__file__).parent.parent / "templates"

        # Check if template exists, otherwise use fallback
        if not template_dir.exists():
            # No template files yet, we'll use a simple inline template
            return Environment(
                loader=FileSystemLoader("."),
                autoescape=select_autoescape(),
            )

        return Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(),
        )

    def generate(self, requirement: str, constraints: dict | None = None) -> str:
        """Generate an implementation plan from a requirement.

        Args:
            requirement: Natural language requirement description
            constraints: Optional constraints dict

        Returns:
            Markdown formatted implementation plan
        """
        # Step 1: Analyze the requirement
        analysis = self._analyzer.analyze(requirement)

        # Step 2: Design architecture
        architecture = self._architect.design(analysis)

        # Step 3: Generate implementation plan
        plan = self._planner.plan(analysis, architecture)

        # Step 4: Render output
        return self._render_plan(requirement, analysis, architecture, plan)

    def _render_plan(
        self,
        requirement: str,
        analysis: AnalysisResult,
        architecture: ArchitectureDesign,
        plan: ImplementationPlan,
    ) -> str:
        """Render the plan using template or fallback."""

        template_data = {
            "requirement": requirement,
            "analysis": analysis,
            "architecture": architecture,
            "plan": plan,
        }

        # Try to use template file
        try:
            template = self._template_env.get_template("plan.md.j2")
            return template.render(**template_data)
        except Exception:
            # Fallback to simple rendering
            return self._render_fallback(requirement, analysis, architecture, plan)

    def _render_fallback(
        self,
        requirement: str,
        analysis: AnalysisResult,
        architecture: ArchitectureDesign,
        plan: ImplementationPlan,
    ) -> str:
        """Fallback rendering when template is not available."""
        lines = [
            "# Implementation Plan",
            "",
            f"## Original Requirement",
            "",
            f"> {requirement}",
            "",
            f"## 1. Requirement Analysis",
            "",
            f"**Project Type**: {analysis.project_type.value}",
            "",
            f"**Core Features**:",
            "",
        ]

        for feature in analysis.core_features:
            lines.append(f"- {feature}")

        lines.extend([
            "",
            f"**Implied Features**:",
            "",
        ])

        for feature in analysis.implied_features:
            lines.append(f"- {feature}")

        lines.extend([
            "",
            f"## 2. Technology Stack",
            "",
            f"- **Language**: {architecture.tech_stack.language}",
            f"- **Backend**: {architecture.tech_stack.backend_framework}",
            f"- **Database**: {architecture.tech_stack.database}",
        ])

        if architecture.tech_stack.cache:
            lines.append(f"- **Cache**: {architecture.tech_stack.cache}")

        if architecture.tech_stack.frontend:
            lines.append(f"- **Frontend**: {architecture.tech_stack.frontend}")

        lines.append(f"- **Deployment**: {architecture.tech_stack.deployment}")

        lines.extend([
            "",
            f"## 3. Architecture",
            "",
            f"### Components",
            "",
        ])

        for component in architecture.components:
            lines.extend([
                f"**{component.name}** ({component.type.value})",
                f"- Technology: {component.technology}",
                f"- Responsibility: {component.responsibility}",
                "",
            ])

        lines.extend([
            "### Data Flow",
            "",
            architecture.data_flow,
            "",
        ])

        if architecture.api_design:
            lines.extend([
                "### API Design",
                "",
                "```\n" + architecture.api_design + "\n```",
                "",
            ])

        lines.extend([
            "## 4. Implementation Plan",
            "",
        ])

        current_phase = None
        for task in plan.tasks:
            if task.phase != current_phase:
                current_phase = task.phase
                lines.append(f"### {task.phase.value.title()}")
                lines.append("")

            lines.extend([
                f"**{task.id}: {task.title}** ({task.estimated_effort})",
                "",
                f"{task.description}",
                "",
                "Steps:",
            ])

            for step in task.steps:
                lines.append(f"- {step}")

            lines.extend([
                "",
                "Acceptance Criteria:",
            ])

            for criteria in task.acceptance_criteria:
                lines.append(f"- {criteria}")

            if task.dependencies:
                lines.append(f"\nDependencies: {', '.join(task.dependencies)}")

            lines.append("")

        lines.extend([
            "## 5. Risks and Mitigations",
            "",
        ])

        for risk in plan.risks:
            lines.append(f"- {risk}")

        lines.extend([
            "",
            "## 6. Next Steps",
            "",
        ])

        for step in plan.next_steps:
            lines.append(step)

        return "\n".join(lines)
