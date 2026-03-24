"""Integration tests for full Spec2Plan workflow."""

from spec2plan import Spec2Plan
from spec2plan.core.analyzer import Analyzer, ProjectType
from spec2plan.core.architect import Architect
from spec2plan.core.planner import Planner
from spec2plan.core.generator import Generator


def test_full_workflow_simple_api() -> None:
    """Test complete workflow for simple API."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a REST API")

    assert "# Implementation Plan" in plan
    assert "API" in plan
    assert "Python" in plan
    assert "FastAPI" in plan


def test_full_workflow_web_app() -> None:
    """Test complete workflow for web app."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a web dashboard")

    assert "web" in plan.lower()
    assert "Frontend" in plan or "React" in plan


def test_full_workflow_cli() -> None:
    """Test complete workflow for CLI tool."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a CLI tool for file management")

    assert "CLI" in plan
    assert "Click" in plan or "Typer" in plan


def test_full_workflow_library() -> None:
    """Test complete workflow for library."""
    s2p = Spec2Plan()
    plan = s2p.generate("Create a Python library for data processing")

    assert "library" in plan.lower()
    assert "PyPI" in plan


def test_workflow_with_auth() -> None:
    """Test workflow with authentication."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API with OAuth2 authentication")

    assert "authentication" in plan.lower()
    assert "auth" in plan.lower()


def test_workflow_with_database() -> None:
    """Test workflow with database."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an app with PostgreSQL database")

    assert "PostgreSQL" in plan
    assert "database" in plan.lower()


def test_workflow_complex_app() -> None:
    """Test workflow for complex application."""
    s2p = Spec2Plan()
    plan = s2p.generate(
        "Build a real-time analytics dashboard with user authentication, "
        "PostgreSQL database, Redis cache, and REST API"
    )

    assert len(plan) > 1500
    assert "authentication" in plan.lower()
    assert "PostgreSQL" in plan
    assert "Redis" in plan
    assert "API" in plan


def test_generator_module_workflow() -> None:
    """Test generator module directly."""
    generator = Generator()
    plan = generator.generate("Build an API")

    assert len(plan) > 0
    assert "# Implementation Plan" in plan


def test_analyzer_architect_planner_integration() -> None:
    """Test analyzer-architect-planner pipeline."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    # Analyze
    analysis = analyzer.analyze("Build a web app with authentication")
    assert analysis.project_type == ProjectType.WEB_APP
    assert "authentication" in analysis.core_features

    # Design
    architecture = architect.design(analysis)
    assert architecture.tech_stack is not None
    assert len(architecture.components) > 0

    # Plan
    plan = planner.plan(analysis, architecture)
    assert len(plan.tasks) > 0
    assert len(plan.risks) > 0
    assert len(plan.next_steps) > 0


def test_workflow_preserves_requirement() -> None:
    """Test workflow preserves original requirement."""
    s2p = Spec2Plan()
    requirement = "Build a RESTful blog API with comments"
    plan = s2p.generate(requirement)

    assert requirement in plan


def test_workflow_includes_all_phases() -> None:
    """Test workflow includes all development phases."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a web app")

    phases = ["Setup", "Foundation", "Core", "Testing", "Deployment"]
    for phase in phases:
        assert phase in plan


def test_workflow_generates_dependencies() -> None:
    """Test workflow generates task dependencies."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a complex web app")

    assert "Dependencies" in plan or "dependencies" in plan.lower()


def test_workflow_empty_constraints() -> None:
    """Test workflow with empty constraints."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API", constraints={})

    assert len(plan) > 0


def test_workflow_none_constraints() -> None:
    """Test workflow with None constraints."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API", constraints=None)

    assert len(plan) > 0


def test_workflow_language_constraint() -> None:
    """Test workflow with language constraint."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API", constraints={"language": "python"})

    assert "Python" in plan


def test_workflow_multiple_constraints() -> None:
    """Test workflow with multiple constraints."""
    s2p = Spec2Plan()
    plan = s2p.generate(
        "Build an API",
        constraints={"language": "python", "performance": "high"}
    )

    assert "Python" in plan


def test_vague_requirement_workflow() -> None:
    """Test workflow with vague requirement."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build something")

    assert len(plan) > 200


def test_minimal_requirement_workflow() -> None:
    """Test workflow with minimal requirement."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build app")

    assert len(plan) > 200


def test_one_word_requirement() -> None:
    """Test workflow with one word requirement."""
    s2p = Spec2Plan()
    plan = s2p.generate("API")

    assert len(plan) > 100


def test_workflow_realtime_feature() -> None:
    """Test workflow with realtime feature."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an app with realtime updates")

    assert "realtime" in plan.lower() or "websocket" in plan.lower()


def test_workflow_search_feature() -> None:
    """Test workflow with search feature."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API with search functionality")

    assert "search" in plan.lower()


def test_workflow_file_handling_feature() -> None:
    """Test workflow with file handling."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API with file upload")

    assert "file" in plan.lower()


def test_workflow_notifications_feature() -> None:
    """Test workflow with notifications."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an app with email notifications")

    assert "notification" in plan.lower()


def test_workflow_scheduled_jobs_feature() -> None:
    """Test workflow with scheduled jobs."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an app with scheduled tasks")

    assert "schedule" in plan.lower() or "cron" in plan.lower()


def test_workflow_mobile_app() -> None:
    """Test workflow for mobile app."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a mobile app")

    assert "mobile" in plan.lower()


def test_workflow_data_pipeline() -> None:
    """Test workflow for data pipeline."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an ETL data pipeline")

    assert "pipeline" in plan.lower() or "etl" in plan.lower()


def test_workflow_all_project_types() -> None:
    """Test workflow for all project types."""
    s2p = Spec2Plan()

    types = [
        ("Build a web application", "web"),
        ("Build a REST API", "api"),
        ("Build a CLI tool", "cli"),
        ("Build a library", "library"),
        ("Build a mobile app", "mobile"),
        ("Build a data pipeline", "pipeline"),
    ]

    for req, keyword in types:
        plan = s2p.generate(req)
        assert len(plan) > 200, f"Failed for {keyword}"
        assert keyword in plan.lower(), f"Missing {keyword} in output"


def test_generator_implied_features_for_web() -> None:
    """Test generator includes implied features for web apps."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a simple web app")

    # Web apps should imply database
    assert "database" in plan.lower()


def test_generator_implied_features_for_api() -> None:
    """Test generator includes implied features for APIs."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a REST API")

    # APIs should imply documentation and error handling
    output_lower = plan.lower()
    assert "document" in output_lower or "api" in output_lower


def test_workflow_acceptance_criteria_present() -> None:
    """Test workflow includes acceptance criteria."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    assert "Acceptance" in plan or "acceptance" in plan.lower()


def test_workflow_effort_estimates_present() -> None:
    """Test workflow includes effort estimates."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    assert "hour" in plan.lower() or "day" in plan.lower()


def test_workflow_task_steps_present() -> None:
    """Test workflow includes task steps."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    assert "Steps:" in plan or "steps" in plan.lower()


def test_workflow_component_details() -> None:
    """Test workflow includes component details."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    assert "Component" in plan or "component" in plan.lower()


def test_workflow_data_flow_present() -> None:
    """Test workflow includes data flow."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    assert "Data Flow" in plan or "data flow" in plan.lower()


def test_workflow_risks_present() -> None:
    """Test workflow includes risks."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    assert "Risk" in plan or "risk" in plan.lower()


def test_workflow_next_steps_present() -> None:
    """Test workflow includes next steps."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    assert "Next Steps" in plan or ("next" in plan.lower() and "step" in plan.lower())


def test_workflow_tech_stack_present() -> None:
    """Test workflow includes tech stack."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    assert "Technology" in plan or "Stack" in plan


def test_multiple_instances_independent() -> None:
    """Test multiple Spec2Plan instances are independent."""
    s2p1 = Spec2Plan()
    s2p2 = Spec2Plan()

    plan1 = s2p1.generate("Build an API")
    plan2 = s2p2.generate("Build a CLI")

    assert plan1 != plan2


def test_workflow_reproducible() -> None:
    """Test same input produces same output."""
    s2p = Spec2Plan()
    req = "Build an API"

    plan1 = s2p.generate(req)
    plan2 = s2p.generate(req)

    assert plan1 == plan2


def test_workflow_case_insensitive() -> None:
    """Test workflow is case insensitive."""
    s2p = Spec2Plan()

    plan1 = s2p.generate("Build a REST API")
    plan2 = s2p.generate("BUILD A REST API")
    plan3 = s2p.generate("build a rest api")

    # All should detect as API
    assert "api" in plan1.lower()
    assert "api" in plan2.lower()
    assert "api" in plan3.lower()


def test_workflow_with_special_characters() -> None:
    """Test workflow handles special characters."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API with OAuth2 & JWT auth!")

    assert len(plan) > 100


def test_workflow_with_numbers() -> None:
    """Test workflow handles numbers."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build API v2 with JSON responses")

    assert len(plan) > 100


def test_workflow_with_quotes() -> None:
    """Test workflow handles quotes."""
    s2p = Spec2Plan()
    plan = s2p.generate('Build an API called "MyAPI"')

    assert len(plan) > 100
    assert "MyAPI" in plan


def test_analyzer_all_keywords() -> None:
    """Test analyzer detects all feature keywords."""
    analyzer = Analyzer()

    tests = [
        ("Build an API with authentication", "authentication"),
        ("Build an app with database", "database"),
        ("Build an API", "api"),
        ("Build a web UI", "frontend"),
        ("Build a realtime app", "realtime"),
        ("Build an app with search", "search"),
        ("Build an app with file upload", "file_handling"),
        ("Build an app with notifications", "notifications"),
        ("Build an app with scheduled jobs", "cron"),
    ]

    for req, expected_feature in tests:
        result = analyzer.analyze(req)
        assert expected_feature in result.core_features, f"Failed to detect {expected_feature} in: {req}"


def test_architect_all_project_types_have_stack() -> None:
    """Test architect provides stack for all project types."""
    analyzer = Analyzer()
    architect = Architect()

    requirements = [
        "Build a web app",
        "Build an API",
        "Build a CLI",
        "Build a library",
        "Build a mobile app",
        "Build a data pipeline",
    ]

    for req in requirements:
        analysis = analyzer.analyze(req)
        design = architect.design(analysis)
        assert design.tech_stack is not None
        assert len(design.tech_stack.language) > 0
        assert len(design.tech_stack.backend_framework) > 0 or design.tech_stack.backend_framework == "None (library)"


def test_planner_all_projects_have_tasks() -> None:
    """Test planner generates tasks for all project types."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    requirements = [
        "Build a web app",
        "Build an API",
        "Build a CLI",
        "Build a library",
    ]

    for req in requirements:
        analysis = analyzer.analyze(req)
        design = architect.design(analysis)
        plan = planner.plan(analysis, design)
        assert len(plan.tasks) > 0
        assert len(plan.risks) > 0
        assert len(plan.next_steps) > 0


def test_all_modules_work_together() -> None:
    """Test all modules work together seamlessly."""
    from spec2plan import Spec2Plan
    from spec2plan.core.analyzer import Analyzer
    from spec2plan.core.architect import Architect
    from spec2plan.core.planner import Planner
    from spec2plan.core.generator import Generator

    # Use high-level API
    s2p = Spec2Plan()
    plan1 = s2p.generate("Build an API")

    # Use low-level API
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()
    generator = Generator()

    analysis = analyzer.analyze("Build an API")
    architecture = architect.design(analysis)
    impl_plan = planner.plan(analysis, architecture)
    plan2 = generator._render_plan("Build an API", analysis, architecture, impl_plan)

    # Both should work
    assert len(plan1) > 0
    assert len(plan2) > 0


def test_workflow_consistent_output_format() -> None:
    """Test workflow always produces consistent output format."""
    s2p = Spec2Plan()

    requirements = [
        "Build an API",
        "Build a web app",
        "Build a CLI tool",
    ]

    for req in requirements:
        plan = s2p.generate(req)
        # Should always start with heading
        assert plan.lstrip().startswith("#")
        # Should have main sections
        assert "##" in plan


def test_complete_end_to_end_workflow() -> None:
    """Test complete end-to-end workflow."""
    # This is the main workflow a user would follow
    s2p = Spec2Plan()

    # User provides requirement
    requirement = "Build a blog API with user authentication, posts, comments, and search"

    # Generate plan
    plan = s2p.generate(requirement)

    # Verify output
    assert requirement in plan
    assert "authentication" in plan.lower()
    assert "API" in plan
    assert "Python" in plan or "Language" in plan
    assert "T0" in plan  # Task IDs

    # Verify structure
    lines = plan.split("\n")
    non_empty = [l for l in lines if l.strip()]
    assert len(non_empty) > 50  # Should have substantial content


def test_spec2plan_is_callable() -> None:
    """Test Spec2Plan has the expected interface."""
    s2p = Spec2Plan()

    assert hasattr(s2p, "generate")
    assert callable(s2p.generate)

    # Test with minimal args
    plan = s2p.generate("Test")
    assert len(plan) > 0


def test_generator_fallback_rendering() -> None:
    """Test generator fallback rendering works."""
    from spec2plan.core.generator import Generator
    from spec2plan.core.analyzer import AnalysisResult, ProjectType
    from spec2plan.core.architect import ArchitectureDesign, TechStack
    from spec2plan.core.planner import ImplementationPlan

    generator = Generator()

    # Create minimal objects
    analysis = AnalysisResult(
        raw_input="Test",
        project_type=ProjectType.API,
        core_features=[],
        implied_features=[],
        constraints={}
    )

    tech_stack = TechStack(
        language="Python",
        backend_framework="FastAPI",
        database="PostgreSQL"
    )

    architecture = ArchitectureDesign(
        tech_stack=tech_stack,
        components=[],
        data_flow="Test flow"
    )

    impl_plan = ImplementationPlan(
        tasks=[],
        risks=[],
        next_steps=[]
    )

    # Should work with minimal data
    result = generator._render_fallback("Test", analysis, architecture, impl_plan)
    assert len(result) > 0
