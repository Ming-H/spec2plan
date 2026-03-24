"""Tests for the Architect module."""

from spec2plan.core.analyzer import Analyzer, ProjectType
from spec2plan.core.architect import Architect, ComponentType


def test_architect_designs_api_stack() -> None:
    """Test that architect designs appropriate tech stack for API."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build a REST API")
    design = architect.design(analysis)

    assert design.tech_stack.language == "Python"
    assert design.tech_stack.backend_framework == "FastAPI"
    assert design.tech_stack.database == "PostgreSQL"


def test_architect_designs_cli_stack() -> None:
    """Test that architect designs appropriate tech stack for CLI."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build a CLI tool")
    design = architect.design(analysis)

    assert design.tech_stack.language == "Python"
    assert "Click" in design.tech_stack.backend_framework or "Typer" in design.tech_stack.backend_framework


def test_architect_includes_cache_for_web_apps() -> None:
    """Test that architect includes cache layer for web apps."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build a web application")
    design = architect.design(analysis)

    assert design.tech_stack.cache is not None


def test_architect_generates_components() -> None:
    """Test that architect generates architectural components."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build an API with authentication")
    design = architect.design(analysis)

    assert len(design.components) > 0
    service_components = [c for c in design.components if c.type == ComponentType.SERVICE]
    assert len(service_components) > 0


def test_architect_includes_database_component_when_needed() -> None:
    """Test that architect includes database when authentication is needed."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build an API with user authentication")
    design = architect.design(analysis)

    db_components = [c for c in design.components if c.type == ComponentType.DATABASE]
    assert len(db_components) > 0


def test_architect_designs_api_for_web_apps() -> None:
    """Test that architect generates API design for web apps."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build a web application")
    design = architect.design(analysis)

    assert design.api_design is not None
    assert "GET" in design.api_design


def test_architect_respects_language_constraint() -> None:
    """Test that architect respects language constraint."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build a Python API")
    design = architect.design(analysis)

    assert design.tech_stack.language == "Python"


def test_architect_generates_data_flow() -> None:
    """Test that architect generates data flow description."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build an API")
    design = architect.design(analysis)

    assert len(design.data_flow) > 0
    assert "Client" in design.data_flow or "User" in design.data_flow


def test_architect_includes_frontend_for_web_apps() -> None:
    """Test that architect includes frontend component for web apps."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build a web dashboard")
    design = architect.design(analysis)

    frontend_components = [c for c in design.components if c.type == ComponentType.FRONTEND]
    assert len(frontend_components) > 0
    assert design.tech_stack.frontend is not None


def test_architect_component_interfaces() -> None:
    """Test that components have defined interfaces."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build an API")
    design = architect.design(analysis)

    for component in design.components:
        assert len(component.interfaces) > 0
        assert len(component.responsibility) > 0


def test_architect_handles_unknown_project_type() -> None:
    """Test that architect handles unknown project types gracefully."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build something")
    design = architect.design(analysis)

    # Should still generate a design with defaults
    assert design.tech_stack is not None
    assert len(design.components) > 0


def test_architect_no_cache_for_cli() -> None:
    """Test that CLI tools don't get cache by default."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build a simple CLI script")
    design = architect.design(analysis)

    assert design.tech_stack.cache is None
