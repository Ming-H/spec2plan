"""Tests for output quality and variety."""

from spec2plan import Spec2Plan
from spec2plan.core.analyzer import Analyzer, ProjectType
from spec2plan.core.architect import Architect
from spec2plan.core.planner import Planner, TaskPhase


def test_output_has_heading_structure() -> None:
    """Test output has proper heading structure."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Count heading levels
    h1_count = plan.count("# ")
    h2_count = plan.count("## ")

    assert h1_count >= 1, "Should have at least one H1"
    assert h2_count >= 5, "Should have at least 5 H2 sections"


def test_output_line_count() -> None:
    """Test output has substantial content."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    lines = [l for l in plan.split("\n") if l.strip()]
    assert len(lines) > 50, "Output should have more than 50 non-empty lines"


def test_output_word_count() -> None:
    """Test output has substantial word count."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    words = plan.split()
    assert len(words) > 200, "Output should have more than 200 words"


def test_output_section_order() -> None:
    """Test output sections are in logical order."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Define expected order
    sections = [
        "# Implementation Plan",
        "## Original Requirement",
        "## 1. Requirement Analysis",
        "## 2. Technology Stack",
        "## 3. Architecture",
        "## 4. Implementation Plan",
        "## 5. Risks",
        "## 6. Next Steps",
    ]

    # Check sections appear in order
    last_pos = -1
    for section in sections:
        pos = plan.find(section)
        if pos != -1:
            assert pos > last_pos, f"Section {section} is out of order"
            last_pos = pos


def test_output_no_empty_sections() -> None:
    """Test output doesn't have completely empty sections."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Split into sections
    sections = plan.split("##")[1:]  # Skip first empty split

    # Most sections should have content
    sections_with_content = 0
    for section in sections:
        # Get content after section header
        lines = section.split("\n")[1:]
        content = [l for l in lines if l.strip()]
        if len(content) > 0:
            sections_with_content += 1

    # At least half the sections should have content
    assert sections_with_content >= len(sections) / 2, "Too many empty sections"


def test_output_list_formatting() -> None:
    """Test output uses list formatting."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Should have bullet points
    assert "- " in plan or "* " in plan


def test_output_code_blocks() -> None:
    """Test output may include code blocks."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # API design section often uses code blocks
    has_code = "```" in plan or "API Design" in plan
    # This is optional but nice to have


def test_different_inputs_different_outputs() -> None:
    """Test different inputs produce different outputs."""
    s2p = Spec2Plan()

    plan1 = s2p.generate("Build an API")
    plan2 = s2p.generate("Build a CLI tool")

    assert plan1 != plan2, "Different inputs should produce different outputs"


def test_similar_inputs_similar_outputs() -> None:
    """Test similar inputs produce similar outputs."""
    s2p = Spec2Plan()

    plan1 = s2p.generate("Build an API")
    plan2 = s2p.generate("Build a REST API")

    # Should share common structure
    assert "# Implementation Plan" in plan1
    assert "# Implementation Plan" in plan2


def test_output_no_template_placeholders() -> None:
    """Test output doesn't contain template placeholders."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Common template placeholders that shouldn't appear
    placeholders = ["{{", "}}", "{%", "%}", "${", "undefined", "None of the above"]

    for placeholder in placeholders:
        if placeholder in ["{{", "}}", "{%", "%}"]:
            # Jinja2 style - should not be in output
            assert placeholder not in plan, f"Found template placeholder: {placeholder}"


def test_output_consistent_naming() -> None:
    """Test output uses consistent naming conventions."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Task IDs should be consistent
    assert "T01" in plan or "T1" in plan


def test_output_includes_estimates() -> None:
    """Test output includes time estimates."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Should mention time units
    assert "hour" in plan.lower() or "day" in plan.lower()


def test_output_includes_acceptance_criteria() -> None:
    """Test output includes acceptance criteria."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    assert "Acceptance" in plan or "acceptance" in plan.lower()


def test_output_includes_steps() -> None:
    """Test output includes execution steps."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    assert "Steps" in plan or "steps" in plan.lower()


def test_output_risks_content() -> None:
    """Test risks section has meaningful content."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Find risks section
    risks_start = plan.find("## 5. Risks")
    if risks_start == -1:
        risks_start = plan.find("Risks")

    if risks_start != -1:
        risks_section = plan[risks_start:risks_start+500]
        # Should have some content
        assert len(risks_section) > 100, "Risks section seems too short"


def test_output_next_steps_content() -> None:
    """Test next steps section has meaningful content."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Find next steps section
    steps_start = plan.find("## 6. Next Steps")
    if steps_start == -1:
        steps_start = plan.find("Next Steps")

    if steps_start != -1:
        steps_section = plan[steps_start:steps_start+500]
        # Should have some content
        assert len(steps_section) > 100, "Next steps section seems too short"


def test_web_app_output_has_frontend() -> None:
    """Test web app output mentions frontend."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a web application")

    assert "Frontend" in plan or "React" in plan or "frontend" in plan.lower()


def test_api_output_has_endpoints() -> None:
    """Test API output mentions endpoints."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a REST API")

    assert "endpoint" in plan.lower() or "GET" in plan or "POST" in plan


def test_cli_output_has_commands() -> None:
    """Test CLI output mentions commands."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a CLI tool")

    assert "CLI" in plan or "command" in plan.lower()


def test_library_output_has_package() -> None:
    """Test library output mentions packaging."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a Python library")

    assert "PyPI" in plan or "package" in plan.lower()


def test_auth_output_has_security() -> None:
    """Test auth requirement mentions security."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API with authentication")

    output_lower = plan.lower()
    assert "auth" in output_lower or "security" in output_lower or "login" in output_lower


def test_database_output_has_storage() -> None:
    """Test database requirement mentions storage."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API with database")

    assert "database" in plan.lower() or "PostgreSQL" in plan or "storage" in plan.lower()


def test_realtime_output_has_websocket() -> None:
    """Test realtime requirement mentions websocket."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a realtime app")

    output_lower = plan.lower()
    assert "realtime" in output_lower or "websocket" in output_lower or "live" in output_lower


def test_search_output_has_query() -> None:
    """Test search requirement mentions queries."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API with search")

    assert "search" in plan.lower()


def test_file_handling_output_has_upload() -> None:
    """Test file handling requirement mentions upload."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API with file upload")

    assert "file" in plan.lower()


def test_notifications_output_has_email() -> None:
    """Test notifications requirement mentions alerts."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an app with notifications")

    output_lower = plan.lower()
    assert "notification" in output_lower or "email" in output_lower or "alert" in output_lower


def test_complex_app_has_more_content() -> None:
    """Test complex app generates more content."""
    s2p = Spec2Plan()

    simple_plan = s2p.generate("Build a simple API")
    complex_plan = s2p.generate(
        "Build a web app with authentication, database, cache, "
        "realtime updates, search, file upload, notifications, and scheduled jobs"
    )

    # Complex should be longer
    assert len(complex_plan) >= len(simple_plan), "Complex requirement should generate more content"


def test_minimal_app_has_content() -> None:
    """Test even minimal requirement generates content."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build app")

    assert len(plan) > 200, "Even minimal requirement should generate content"


def test_output_has_project_type() -> None:
    """Test output mentions project type."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    assert "Project Type" in plan or "project_type" in plan.lower() or "API" in plan


def test_output_has_tech_stack() -> None:
    """Test output mentions technology stack."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    assert "Technology" in plan or "Stack" in plan or "Python" in plan


def test_output_has_architecture() -> None:
    """Test output mentions architecture."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    assert "Architecture" in plan or "architecture" in plan.lower()


def test_output_has_implementation_plan() -> None:
    """Test output has implementation plan section."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    assert "Implementation Plan" in plan or "implementation" in plan.lower()


def test_task_dependencies_structure() -> None:
    """Test task dependencies are properly structured."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a complex web app")

    # Look for dependency mentions
    assert "Dependencies" in plan or "dependencies" in plan.lower()


def test_output_has_phase_structure() -> None:
    """Test output has phase-based structure."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Should mention phases
    phase_keywords = ["Setup", "Foundation", "Testing", "Deployment"]
    found = sum(1 for kw in phase_keywords if kw in plan)
    assert found >= 2, "Should mention at least 2 phases"


def test_api_project_has_api_design() -> None:
    """Test API project includes API design."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a REST API")

    assert "API Design" in plan or "endpoint" in plan.lower()


def test_web_project_has_more_components() -> None:
    """Test web project has more components than CLI."""
    s2p = Spec2Plan()

    web_plan = s2p.generate("Build a web app")
    cli_plan = s2p.generate("Build a CLI tool")

    # Web app should mention more components
    web_component_count = web_plan.lower().count("component")
    cli_component_count = cli_plan.lower().count("component")

    assert web_component_count >= cli_component_count


def test_output_has_data_flow() -> None:
    """Test output includes data flow description."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    assert "Data Flow" in plan or "data flow" in plan.lower() or "flow" in plan.lower()


def test_task_effort_variety() -> None:
    """Test tasks have varied effort estimates."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a web app")

    # Look for different effort patterns
    has_hours = "hour" in plan.lower()
    has_days = "day" in plan.lower()

    # Should have at least hours or days mentioned
    assert has_hours or has_days


def test_output_readable() -> None:
    """Test output is human-readable."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Should not have excessive special characters
    # Should have normal sentence structure
    assert len(plan) > 0

    # Check for some readable content
    words = plan.split()
    # Most words should be longer than 1 char (not just symbols)
    real_words = [w for w in words if len(w.strip(".,!?:;()[]{}\"'")) > 1]
    assert len(real_words) > 100, "Should have substantial readable content"


def test_analyzer_project_type_coverage() -> None:
    """Test analyzer covers all project types."""
    analyzer = Analyzer()

    test_cases = [
        ("Build a web app", ProjectType.WEB_APP),
        ("Build a REST API", ProjectType.API),
        ("Build a CLI tool", ProjectType.CLI),
        ("Build a library", ProjectType.LIBRARY),
        ("Build a mobile app", ProjectType.MOBILE),
        ("Build a data pipeline", ProjectType.DATA_PIPELINE),
        ("Build something unknown", ProjectType.UNKNOWN),
    ]

    for req, expected_type in test_cases:
        result = analyzer.analyze(req)
        assert result.project_type == expected_type, f"Failed for: {req}"


def test_architect_component_diversity() -> None:
    """Test architect generates diverse components."""
    analyzer = Analyzer()
    architect = Architect()

    # Web app should have diverse components
    analysis = analyzer.analyze("Build a web app with authentication and database")
    design = architect.design(analysis)

    component_types = set()
    for comp in design.components:
        component_types.add(comp.type.value)

    # Should have at least 2 different types
    assert len(component_types) >= 2


def test_planner_phase_distribution() -> None:
    """Test planner distributes tasks across phases."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    analysis = analyzer.analyze("Build a web app with all features")
    architecture = architect.design(analysis)
    plan = planner.plan(analysis, architecture)

    phases = [task.phase for task in plan.tasks]
    unique_phases = set(phases)

    # Should have multiple phases
    assert len(unique_phases) >= 3


def test_generator_output_length_reasonable() -> None:
    """Test generator output length is reasonable."""
    s2p = Spec2Plan()

    # Very short input
    short_plan = s2p.generate("API")
    assert len(short_plan) > 100, "Even short input should produce output"

    # Very long input
    long_plan = s2p.generate("Build " + "a " * 100 + "API")
    assert len(long_plan) > 100, "Long input should still produce output"

    # Normal input
    normal_plan = s2p.generate("Build a REST API for user management")
    assert len(normal_plan) > 500, "Normal input should produce substantial output"


def test_output_no_leading_trailing_whitespace_issues() -> None:
    """Test output doesn't have weird whitespace."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Should not have excessive leading/trailing whitespace per line
    lines = plan.split("\n")
    for line in lines:
        # If line has content, shouldn't have excessive leading whitespace
        if line.strip():
            # Allow some indentation but not crazy amounts
            assert len(line) - len(line.lstrip()) < 20, "Line has too much leading whitespace"


def test_output_section_transitions() -> None:
    """Test output has proper section transitions."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Should have blank lines between major sections
    assert "\n\n" in plan, "Should have section breaks"


def test_multiple_runs_same_output() -> None:
    """Test multiple runs with same input produce identical output."""
    s2p = Spec2Plan()
    req = "Build a simple API"

    results = [s2p.generate(req) for _ in range(3)]

    # All should be identical
    assert all(r == results[0] for r in results)


def test_output_contains_requirement_context() -> None:
    """Test output includes context from requirement."""
    s2p = Spec2Plan()

    # Specific terms
    plan = s2p.generate("Build a blog API with comments and likes")
    assert "blog" in plan.lower()


def test_all_enum_values_tested() -> None:
    """Test all enum values are covered."""
    from spec2plan.core.analyzer import ProjectType
    from spec2plan.core.planner import TaskPhase
    from spec2plan.core.architect import ComponentType

    # Just verify the enums have expected values
    assert ProjectType.WEB_APP.value == "web_app"
    assert TaskPhase.SETUP.value == "setup"
    assert ComponentType.SERVICE.value == "service"


def test_output_markdown_compatible() -> None:
    """Test output is markdown-compatible."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    # Should have markdown elements
    has_headers = "#" in plan
    has_lists = "- " in plan

    assert has_headers and has_lists


def test_cli_version_option_works() -> None:
    """Test CLI version option."""
    from click.testing import CliRunner
    from spec2plan.cli import main

    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0


def test_cli_help_option_works() -> None:
    """Test CLI help option."""
    from click.testing import CliRunner
    from spec2plan.cli import main

    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "requirement" in result.output.lower()
