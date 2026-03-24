"""Extended tests for the Generator module."""

from spec2plan import Spec2Plan
from spec2plan.core.analyzer import ProjectType


def test_generator_handles_simple_requirement() -> None:
    """Test generator with a simple requirement."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a simple API")
    assert len(plan) > 100
    assert "API" in plan


def test_generator_handles_complex_requirement() -> None:
    """Test generator with a complex requirement."""
    s2p = Spec2Plan()
    plan = s2p.generate(
        "Build a real-time analytics dashboard web application with "
        "live data updates, user authentication, role-based access control, "
        "data export functionality, and scheduled report generation."
    )
    assert "authentication" in plan.lower()
    assert "dashboard" in plan.lower()


def test_generator_includes_project_type() -> None:
    """Test that generator includes detected project type."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a CLI tool")
    assert "cli" in plan.lower()


def test_generator_includes_core_features() -> None:
    """Test that generator includes core features in output."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API with authentication and search")
    assert "authentication" in plan.lower()
    assert "search" in plan.lower()


def test_generator_includes_implied_features() -> None:
    """Test that generator includes implied features."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a web app")
    # Web apps should imply database
    assert "database" in plan.lower()


def test_generator_includes_tech_stack() -> None:
    """Test that generator includes technology stack."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")
    assert "Python" in plan
    assert "FastAPI" in plan


def test_generator_includes_architecture() -> None:
    """Test that generator includes architecture section."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")
    assert "Architecture" in plan
    assert "Components" in plan


def test_generator_includes_tasks() -> None:
    """Test that generator includes implementation tasks."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")
    assert "Implementation Plan" in plan
    assert "T" in plan  # Task IDs like T01, T02


def test_generator_includes_risks() -> None:
    """Test that generator includes risk assessment."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API with authentication")
    assert "Risks" in plan


def test_generator_includes_next_steps() -> None:
    """Test that generator includes next steps."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")
    assert "Next Steps" in plan


def test_generator_handles_empty_constraints() -> None:
    """Test generator with None constraints."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API", constraints=None)
    assert len(plan) > 0


def test_generator_handles_multiple_constraints() -> None:
    """Test generator with multiple constraints."""
    s2p = Spec2Plan()
    plan = s2p.generate(
        "Build an API",
        constraints={"language": "python", "performance": "high"}
    )
    assert "Python" in plan


def test_generator_respects_language_constraint() -> None:
    """Test that generator respects language constraint."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API", constraints={"language": "python"})
    assert "Python" in plan


def test_generator_includes_data_flow() -> None:
    """Test that generator includes data flow description."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")
    assert "Data Flow" in plan


def test_generator_includes_api_design_for_apis() -> None:
    """Test that generator includes API design for API projects."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a REST API")
    assert "API Design" in plan


def test_generator_handles_cli_project() -> None:
    """Test generator properly handles CLI projects."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a CLI tool for file management")
    assert "CLI" in plan
    assert "Click" in plan or "Typer" in plan


def test_generator_handles_library_project() -> None:
    """Test generator properly handles library projects."""
    s2p = Spec2Plan()
    plan = s2p.generate("Create a Python library")
    assert "library" in plan.lower()
    assert "PyPI" in plan


def test_generator_handles_web_app_project() -> None:
    """Test generator properly handles web app projects."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a web dashboard")
    assert "React" in plan or "frontend" in plan.lower()


def test_generator_includes_phase_sections() -> None:
    """Test that generator includes phase sections in plan."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")
    expected_phases = ["Setup", "Foundation", "Core", "Testing", "Deployment"]
    for phase in expected_phases:
        assert phase in plan


def test_generator_generates_consistent_output() -> None:
    """Test that generator produces consistent output for same input."""
    s2p = Spec2Plan()
    plan1 = s2p.generate("Build a simple API")
    plan2 = s2p.generate("Build a simple API")
    assert plan1 == plan2


def test_generator_output_is_markdown() -> None:
    """Test that generator output is markdown formatted."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")
    # Strip leading whitespace before checking
    assert plan.lstrip().startswith("#")
    assert "##" in plan


def test_generator_handles_long_requirement() -> None:
    """Test generator with very long requirement."""
    s2p = Spec2Plan()
    long_req = "Build an API " + "with features " * 20
    plan = s2p.generate(long_req)
    assert len(plan) > 0


def test_generator_includes_task_details() -> None:
    """Test that tasks include detailed information."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")
    assert "Steps:" in plan or "steps" in plan.lower()
    assert "Acceptance" in plan or "acceptance" in plan.lower()


def test_generator_includes_effort_estimates() -> None:
    """Test that tasks include effort estimates."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")
    assert "hour" in plan.lower() or "day" in plan.lower()


def test_generator_handles_auth_requirements() -> None:
    """Test generator handles authentication requirements."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API with OAuth2 authentication")
    assert "authentication" in plan.lower()
    assert "auth" in plan.lower()


def test_generator_handles_database_requirements() -> None:
    """Test generator handles database requirements."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API with PostgreSQL database")
    assert "PostgreSQL" in plan
    assert "database" in plan.lower()


def test_generator_handles_realtime_requirements() -> None:
    """Test generator handles realtime requirements."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a realtime app with websockets")
    assert "realtime" in plan.lower() or "websocket" in plan.lower()


def test_generator_outputs_structured_sections() -> None:
    """Test that generator outputs properly structured sections."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")
    lines = plan.split("\n")
    # Should have multiple sections
    section_headers = [l for l in lines if l.startswith("#")]
    assert len(section_headers) >= 6


def test_generator_minimal_constraint_output() -> None:
    """Test generator with minimal complexity constraint."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a simple API", constraints={"complexity": "minimal"})
    assert len(plan) > 0
