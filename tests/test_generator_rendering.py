"""Tests for Generator rendering functionality."""

from spec2plan.core.generator import Generator
from spec2plan.core.analyzer import Analyzer, AnalysisResult, ProjectType
from spec2plan.core.architect import Architect, ArchitectureDesign, TechStack, Component
from spec2plan.core.planner import Planner, ImplementationPlan, Task, TaskPhase


def test_generator_initializes() -> None:
    """Test that Generator initializes correctly."""
    generator = Generator()
    assert generator._analyzer is not None
    assert generator._architect is not None
    assert generator._planner is not None
    assert generator._template_env is not None


def test_generator_analyze_integration() -> None:
    """Test generator integrates with analyzer."""
    generator = Generator()
    analysis = generator._analyzer.analyze("Build an API")
    assert analysis.project_type == ProjectType.API


def test_generator_architect_integration() -> None:
    """Test generator integrates with architect."""
    generator = Generator()
    analysis = generator._analyzer.analyze("Build an API")
    design = generator._architect.design(analysis)
    assert design.tech_stack is not None


def test_generator_planner_integration() -> None:
    """Test generator integrates with planner."""
    generator = Generator()
    analysis = generator._analyzer.analyze("Build an API")
    design = generator._architect.design(analysis)
    plan = generator._planner.plan(analysis, design)
    assert len(plan.tasks) > 0


def test_generator_render_fallback_basic() -> None:
    """Test fallback rendering produces basic output."""
    generator = Generator()

    # Create minimal test data
    analysis = AnalysisResult(
        raw_input="Test requirement",
        project_type=ProjectType.API,
        core_features=["api"],
        implied_features=["api_documentation"],
        constraints={}
    )

    tech_stack = TechStack(
        language="Python",
        backend_framework="FastAPI",
        database="PostgreSQL",
        cache="Redis",
        deployment="Docker"
    )

    design = ArchitectureDesign(
        tech_stack=tech_stack,
        components=[
            Component(
                name="API Service",
                type=type("ComponentType", (), {"value": "service"})(),
                technology="FastAPI",
                responsibility="Handle requests",
                interfaces=["HTTP"]
            )
        ],
        data_flow="Client -> Service -> Database",
        api_design="GET /api/resources"
    )

    task = Task(
        id="T01",
        title="Test Task",
        phase=TaskPhase.SETUP,
        description="Test description",
        steps=["Step 1", "Step 2"],
        acceptance_criteria=["Done"],
        estimated_effort="1 hour"
    )

    plan = ImplementationPlan(
        tasks=[task],
        risks=["Test risk"],
        next_steps=["Step 1"]
    )

    result = generator._render_fallback("Test", analysis, design, plan)
    assert len(result) > 0
    assert "# Implementation Plan" in result


def test_generator_render_with_all_project_types() -> None:
    """Test generator rendering with all project types."""
    generator = Generator()

    project_types = [
        ("Build a web app", ProjectType.WEB_APP),
        ("Build an API", ProjectType.API),
        ("Build a CLI tool", ProjectType.CLI),
        ("Build a library", ProjectType.LIBRARY),
    ]

    for requirement, expected_type in project_types:
        plan = generator.generate(requirement)
        assert len(plan) > 0
        assert expected_type.value in plan.lower() or "web" in plan.lower() or "api" in plan.lower()


def test_generator_output_contains_original_requirement() -> None:
    """Test that output contains the original requirement."""
    generator = Generator()
    requirement = "Build a RESTful API for blog posts"
    output = generator.generate(requirement)
    assert requirement in output


def test_generator_handles_various_features() -> None:
    """Test generator handles various feature combinations."""
    generator = Generator()

    requirements = [
        "Build an API with authentication",
        "Build a web app with database",
        "Build a realtime dashboard",
        "Build a CLI tool with file handling",
    ]

    for req in requirements:
        output = generator.generate(req)
        assert len(output) > 100


def test_generator_includes_component_details() -> None:
    """Test that output includes component details."""
    generator = Generator()
    output = generator.generate("Build an API")
    assert "Component" in output
    assert "Technology" in output


def test_generator_includes_phase_organization() -> None:
    """Test that tasks are organized by phase."""
    generator = Generator()
    output = generator.generate("Build a web app")
    # Should have phase headers
    assert "Setup" in output or "setup" in output.lower()


def test_generator_includes_task_ids() -> None:
    """Test that tasks have IDs."""
    generator = Generator()
    output = generator.generate("Build an API")
    assert "T0" in output or "T1" in output


def test_generator_includes_task_effort() -> None:
    """Test that tasks include effort estimates."""
    generator = Generator()
    output = generator.generate("Build an API")
    assert "hour" in output.lower() or "day" in output.lower()


def test_generator_includes_risks_section() -> None:
    """Test that output includes risks."""
    generator = Generator()
    output = generator.generate("Build an API")
    assert "Risk" in output


def test_generator_includes_next_steps() -> None:
    """Test that output includes next steps."""
    generator = Generator()
    output = generator.generate("Build an API")
    assert "Next" in output and "Step" in output


def test_generator_with_webapp_includes_frontend() -> None:
    """Test web app output includes frontend."""
    generator = Generator()
    output = generator.generate("Build a web dashboard")
    assert "Frontend" in output or "frontend" in output.lower()


def test_generator_with_auth_includes_security() -> None:
    """Test auth requirement includes security mentions."""
    generator = Generator()
    output = generator.generate("Build an API with authentication")
    assert "auth" in output.lower()


def test_generator_output_structure() -> None:
    """Test output has proper structure."""
    generator = Generator()
    output = generator.generate("Build an API")

    # Check for main sections
    required = ["#", "##"]
    for marker in required:
        assert marker in output


def test_generator_task_dependencies() -> None:
    """Test tasks show dependencies when applicable."""
    generator = Generator()
    output = generator.generate("Build a web app")
    # Some tasks should have dependencies
    assert "Dependencies" in output or "dependencies" in output.lower()


def test_generator_acceptance_criteria() -> None:
    """Test tasks include acceptance criteria."""
    generator = Generator()
    output = generator.generate("Build an API")
    assert "Acceptance" in output or "acceptance" in output.lower()


def test_generator_task_steps() -> None:
    """Test tasks include steps."""
    generator = Generator()
    output = generator.generate("Build an API")
    assert "Steps" in output or "steps" in output.lower()


def test_generator_multiple_runs_consistent() -> None:
    """Test multiple runs produce consistent output."""
    generator = Generator()
    req = "Build a simple API"
    output1 = generator.generate(req)
    output2 = generator.generate(req)
    assert output1 == output2


def test_generator_with_complex_stack() -> None:
    """Test with complex tech stack."""
    generator = Generator()
    output = generator.generate("Build a web app with database, cache, and realtime features")
    assert "PostgreSQL" in output or "database" in output.lower()


def test_generator_minimal_project() -> None:
    """Test with minimal project description."""
    generator = Generator()
    output = generator.generate("Build an API")
    assert len(output) > 500  # Should still produce substantial output


def test_generator_includes_data_flow() -> None:
    """Test output includes data flow description."""
    generator = Generator()
    output = generator.generate("Build an API")
    assert "Data Flow" in output or "data flow" in output.lower()


def test_generator_cache_for_web_apps() -> None:
    """Test web apps include cache."""
    generator = Generator()
    output = generator.generate("Build a web application")
    assert "Cache" in output or "cache" in output.lower() or "Redis" in output


def test_generator_deployment_info() -> None:
    """Test output includes deployment information."""
    generator = Generator()
    output = generator.generate("Build an API")
    assert "Deployment" in output or "deployment" in output.lower()


def test_generator_tech_stack_section() -> None:
    """Test output includes technology stack section."""
    generator = Generator()
    output = generator.generate("Build an API")
    assert "Technology" in output or "Stack" in output


def test_generator_implied_features_section() -> None:
    """Test output includes implied features."""
    generator = Generator()
    output = generator.generate("Build a web app")
    assert "Implied" in output or "implied" in output.lower()


def test_generator_task_phases() -> None:
    """Test tasks are grouped by phase."""
    generator = Generator()
    output = generator.generate("Build an API")
    # Check for at least some phase indicators
    phase_keywords = ["Setup", "Foundation", "Core", "Testing", "Deployment"]
    found = sum(1 for phase in phase_keywords if phase in output)
    assert found >= 3  # At least 3 phases should be mentioned


def test_generator_error_handling_integration() -> None:
    """Test that implied error handling is included for APIs."""
    generator = Generator()
    output = generator.generate("Build a REST API")
    assert "error" in output.lower()


def test_generator_api_design_for_apis() -> None:
    """Test API projects include API design."""
    generator = Generator()
    output = generator.generate("Build a REST API")
    assert "API Design" in output or "endpoint" in output.lower()


def test_generator_with_vague_requirement() -> None:
    """Test generator handles vague requirements."""
    generator = Generator()
    output = generator.generate("Build something")
    assert len(output) > 100  # Should still produce output
