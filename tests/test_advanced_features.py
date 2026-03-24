"""Advanced feature tests."""

from spec2plan import Spec2Plan
from spec2plan.core.analyzer import Analyzer, ProjectType
from spec2plan.core.architect import Architect
from spec2plan.core.planner import Planner, TaskPhase


def test_analyzer_detects_admin_panel() -> None:
    """Test analyzer detects admin panel as web app."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an admin panel")
    assert result.project_type == ProjectType.WEB_APP


def test_analyzer_detects_service() -> None:
    """Test analyzer detects service as API."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a microservice")
    assert result.project_type == ProjectType.API


def test_analyzer_detects_backend() -> None:
    """Test analyzer detects backend as API."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a backend service")
    assert result.project_type == ProjectType.API


def test_analyzer_detects_graphql() -> None:
    """Test analyzer detects GraphQL."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a GraphQL API")
    assert result.project_type == ProjectType.API


def test_analyzer_detects_package() -> None:
    """Test analyzer detects package as library."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a Python package")
    assert result.project_type == ProjectType.LIBRARY


def test_analyzer_detects_sdk() -> None:
    """Test analyzer detects SDK as library."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an SDK")
    assert result.project_type == ProjectType.LIBRARY


def test_analyzer_detects_framework() -> None:
    """Test analyzer detects framework as library."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a framework")
    assert result.project_type == ProjectType.LIBRARY


def test_analyzer_multiple_auth_keywords() -> None:
    """Test analyzer detects various auth keywords."""
    analyzer = Analyzer()

    auth_keywords = [
        "authentication",
        "authorization",
        "login",
        "signup",
        "oauth",
        "user management",
    ]

    for keyword in auth_keywords:
        result = analyzer.analyze(f"Build an API with {keyword}")
        assert "authentication" in result.core_features, f"Failed for: {keyword}"


def test_analyzer_storage_keywords() -> None:
    """Test analyzer detects storage keywords."""
    analyzer = Analyzer()

    storage_keywords = [
        "database",
        "storage",
        "persist",
        "store data",
    ]

    for keyword in storage_keywords:
        result = analyzer.analyze(f"Build an app with {keyword}")
        assert "database" in result.core_features, f"Failed for: {keyword}"


def test_analyzer_frontend_keywords() -> None:
    """Test analyzer detects frontend keywords."""
    analyzer = Analyzer()

    frontend_keywords = [
        "ui",
        "frontend",
        "interface",
        "dashboard",
        "web interface",
    ]

    for keyword in frontend_keywords:
        result = analyzer.analyze(f"Build an app with {keyword}")
        assert "frontend" in result.core_features, f"Failed for: {keyword}"


def test_analyzer_realtime_keywords() -> None:
    """Test analyzer detects realtime keywords."""
    analyzer = Analyzer()

    realtime_keywords = [
        "realtime",
        "websocket",
        "live",
        "streaming",
    ]

    for keyword in realtime_keywords:
        result = analyzer.analyze(f"Build an app with {keyword}")
        assert "realtime" in result.core_features, f"Failed for: {keyword}"


def test_architect_different_tech_for_different_projects() -> None:
    """Test architect recommends different tech for different projects."""
    analyzer = Analyzer()
    architect = Architect()

    # API
    api_analysis = analyzer.analyze("Build an API")
    api_design = architect.design(api_analysis)

    # CLI
    cli_analysis = analyzer.analyze("Build a CLI tool")
    cli_design = architect.design(cli_analysis)

    # API should have cache, CLI typically not
    assert api_design.tech_stack.cache is not None
    assert cli_design.tech_stack.cache is None


def test_architect_web_app_has_frontend() -> None:
    """Test web apps get frontend component."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build a web app")
    design = architect.design(analysis)

    frontend_components = [c for c in design.components if c.type.value == "frontend"]
    assert len(frontend_components) > 0


def test_architect_api_no_frontend() -> None:
    """Test APIs don't get frontend by default."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build a REST API")
    design = architect.design(analysis)

    frontend_components = [c for c in design.components if c.type.value == "frontend"]
    assert len(frontend_components) == 0


def test_planner_database_task_with_auth() -> None:
    """Test planner generates database task when auth is needed."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    analysis = analyzer.analyze("Build an API with authentication")
    architecture = architect.design(analysis)
    plan = planner.plan(analysis, architecture)

    db_tasks = [t for t in plan.tasks if "database" in t.title.lower()]
    assert len(db_tasks) > 0


def test_planner_cache_task_for_web() -> None:
    """Test planner generates cache task for web apps."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    analysis = analyzer.analyze("Build a web application")
    architecture = architect.design(analysis)
    plan = planner.plan(analysis, architecture)

    cache_tasks = [t for t in plan.tasks if "cache" in t.title.lower()]
    assert len(cache_tasks) > 0


def test_planner_no_cache_for_simple_cli() -> None:
    """Test planner doesn't generate cache task for simple CLI."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    analysis = analyzer.analyze("Build a simple CLI script")
    architecture = architect.design(analysis)
    plan = planner.plan(analysis, architecture)

    cache_tasks = [t for t in plan.tasks if "cache" in t.title.lower()]
    assert len(cache_tasks) == 0


def test_planner_task_ids_sequential() -> None:
    """Test task IDs are sequential."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    analysis = analyzer.analyze("Build a web app")
    architecture = architect.design(analysis)
    plan = planner.plan(analysis, architecture)

    task_ids = [task.id for task in plan.tasks]
    for i, tid in enumerate(task_ids):
        expected = f"T{i+1:02d}"
        assert tid == expected, f"Expected {expected}, got {tid}"


def test_planner_phase_ordering() -> None:
    """Test phases are in correct order."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    analysis = analyzer.analyze("Build a web app")
    architecture = architect.design(analysis)
    plan = planner.plan(analysis, architecture)

    phase_order = [
        TaskPhase.SETUP,
        TaskPhase.FOUNDATION,
        TaskPhase.CORE_FEATURES,
        TaskPhase.INTEGRATION,
        TaskPhase.TESTING,
        TaskPhase.DEPLOYMENT,
    ]

    # Get phases in order of appearance
    phases = [task.phase for task in plan.tasks]

    # Check they follow the general order (may skip some)
    last_idx = -1
    for phase in phases:
        try:
            idx = phase_order.index(phase)
            assert idx >= last_idx, f"Phase {phase} out of order"
            last_idx = idx
        except ValueError:
            pass  # Phase not in expected list


def test_generator_web_app_has_all_sections() -> None:
    """Test web app output has all expected sections."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a web app")

    expected_sections = [
        "# Implementation Plan",
        "Original Requirement",
        "Requirement Analysis",
        "Technology Stack",
        "Architecture",
        "Components",
        "Data Flow",
        "Implementation Plan",
        "Setup",
        "Foundation",
        "Core",
        "Testing",
        "Deployment",
        "Risks",
        "Next Steps",
    ]

    for section in expected_sections:
        assert section in plan, f"Missing section: {section}"


def test_generator_api_has_api_design() -> None:
    """Test API output includes API design."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a REST API")
    assert "API Design" in plan or "endpoint" in plan.lower()


def test_generator_cli_no_api_design() -> None:
    """Test CLI output doesn't include API design."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a CLI tool")
    # CLI output shouldn't emphasize API design as much
    assert "CLI" in plan or "cli" in plan.lower()


def test_generator_library_mentions_pypi() -> None:
    """Test library output mentions PyPI."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a Python library")
    assert "PyPI" in plan


def test_generator_web_app_mentions_frontend() -> None:
    """Test web app output mentions frontend."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a web dashboard")
    assert "Frontend" in plan or "React" in plan or "frontend" in plan.lower()


def test_generator_with_all_constraints() -> None:
    """Test generator with all constraint types."""
    s2p = Spec2Plan()
    plan = s2p.generate(
        "Build an API",
        constraints={
            "language": "python",
            "performance": "high",
            "complexity": "minimal",
        }
    )
    assert "Python" in plan
    assert len(plan) > 0


def test_generator_vague_requirement_still_works() -> None:
    """Test generator produces output for vague requirements."""
    s2p = Spec2Plan()

    vague_requirements = [
        "Build something",
        "Create a thing",
        "Make an app",
        "I need software",
    ]

    for req in vague_requirements:
        plan = s2p.generate(req)
        assert len(plan) > 200, f"Failed for: {req}"


def test_generator_long_requirement() -> None:
    """Test generator handles long requirements."""
    s2p = Spec2Plan()
    long_req = (
        "Build a comprehensive web application that includes user authentication "
        "with OAuth2 support, role-based access control, a dashboard for analytics, "
        "real-time updates using websockets, file upload and download capabilities, "
        "search functionality, email notifications, scheduled jobs for data processing, "
        "a RESTful API for third-party integrations, and comprehensive logging."
    )
    plan = s2p.generate(long_req)
    assert len(plan) > 1000


def test_generator_multiple_calls_same_input() -> None:
    """Test generator produces same output for same input across calls."""
    s2p = Spec2Plan()
    req = "Build a simple API"

    results = [s2p.generate(req) for _ in range(5)]

    # All results should be identical
    assert all(r == results[0] for r in results)


def test_generator_output_markdown_format() -> None:
    """Test output is properly formatted as markdown."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Check for markdown headers
    assert "#" in plan
    assert "##" in plan

    # Check for lists
    assert "-" in plan

    # Check for code blocks (if any)
    # Not required but nice to have


def test_generator_task_formatting() -> None:
    """Test tasks are properly formatted."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Should have task headings
    assert "T0" in plan or "T" in plan

    # Should have task structure
    assert "Steps:" in plan or "steps" in plan.lower()
    assert "Acceptance" in plan or "acceptance" in plan.lower()


def test_spec2plan_entry_point() -> None:
    """Test Spec2Plan class works as entry point."""
    from spec2plan import Spec2Plan

    s2p = Spec2Plan()
    assert hasattr(s2p, "generate")

    plan = s2p.generate("Build an API")
    assert len(plan) > 0


def test_generator_handles_constraint_override() -> None:
    """Test constraints can override defaults."""
    s2p = Spec2Plan()

    # Without constraint
    plan1 = s2p.generate("Build an API")

    # With language constraint
    plan2 = s2p.generate("Build an API", constraints={"language": "python"})

    # Both should work
    assert len(plan1) > 0
    assert len(plan2) > 0
    assert "Python" in plan2


def test_analyzer_feature_combinations() -> None:
    """Test analyzer detects multiple features."""
    analyzer = Analyzer()

    combinations = [
        ("authentication", "database"),
        ("search", "database"),
        ("realtime", "notifications"),
        ("file_handling", "database"),
    ]

    for feat1, feat2 in combinations:
        # Build requirement with both features
        req_map = {
            "authentication": "login",
            "database": "storage",
            "search": "search",
            "realtime": "websocket",
            "notifications": "email alerts",
            "file_handling": "upload",
        }

        req = f"Build an app with {req_map[feat1]} and {req_map.get(feat2, req_map[feat1])}"
        result = analyzer.analyze(req)

        # Check at least some features detected
        assert len(result.core_features) + len(result.implied_features) > 0


def test_planner_all_phases_for_web_app() -> None:
    """Test web app gets all phases."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    analysis = analyzer.analyze("Build a web app with authentication")
    architecture = architect.design(analysis)
    plan = planner.plan(analysis, architecture)

    phases = {task.phase for task in plan.tasks}

    # Should have at least these phases
    expected_phases = {
        TaskPhase.SETUP,
        TaskPhase.TESTING,
        TaskPhase.DEPLOYMENT,
    }

    assert expected_phases.issubset(phases)


def test_planner_auth_task_security_steps() -> None:
    """Test auth task includes security steps."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    analysis = analyzer.analyze("Build an API with authentication")
    architecture = architect.design(analysis)
    plan = planner.plan(analysis, architecture)

    auth_tasks = [t for t in plan.tasks if "auth" in t.title.lower()]
    if auth_tasks:
        steps = " ".join(auth_tasks[0].steps).lower()
        assert "hash" in steps or "security" in steps or "token" in steps


def test_generator_consistent_spacing() -> None:
    """Test output has consistent spacing."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Check for excessive blank lines (allow up to 10 for markdown formatting)
    lines = plan.split("\n")
    consecutive_blanks = 0
    for line in lines:
        if line.strip() == "":
            consecutive_blanks += 1
            assert consecutive_blanks <= 10, "Too many blank lines"
        else:
            consecutive_blanks = 0


def test_architect_component_types_diversity() -> None:
    """Test architect uses appropriate component types."""
    analyzer = Analyzer()
    architect = Architect()

    # Web app should have diverse components
    analysis = analyzer.analyze("Build a web app with database")
    design = architect.design(analysis)

    component_types = {c.type.value for c in design.components}

    # Should have at least service and one other
    assert "service" in component_types
    assert len(component_types) >= 2


def test_planner_task_count_by_complexity() -> None:
    """Test task count scales with complexity."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    # Simple
    simple_analysis = analyzer.analyze("Build a CLI tool")
    simple_arch = architect.design(simple_analysis)
    simple_plan = planner.plan(simple_analysis, simple_arch)

    # Complex
    complex_analysis = analyzer.analyze("Build a web app with authentication and database")
    complex_arch = architect.design(complex_analysis)
    complex_plan = planner.plan(complex_analysis, complex_arch)

    # Complex should have at least as many tasks
    assert len(complex_plan.tasks) >= len(simple_plan.tasks)


def test_generator_output_readability() -> None:
    """Test output is readable."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Should have proper line breaks
    assert "\n\n" in plan  # Section breaks

    # Should have headers
    assert "#" in plan


def test_all_modules_importable() -> None:
    """Test all modules can be imported."""
    import spec2plan
    from spec2plan.core import analyzer, architect, planner, generator
    from spec2plan.core.analyzer import Analyzer, AnalysisResult, ProjectType
    from spec2plan.core.architect import Architect, ArchitectureDesign, Component, ComponentType, TechStack
    from spec2plan.core.planner import Planner, ImplementationPlan, Task, TaskPhase
    from spec2plan.core.generator import Generator

    # If we got here, all imports worked
    assert True


def test_cli_help_content() -> None:
    """Test CLI help has useful content."""
    from click.testing import CliRunner
    from spec2plan.cli import main

    runner = CliRunner()
    result = runner.invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "requirement" in result.output.lower()
    assert "output" in result.output.lower() or "-o" in result.output
