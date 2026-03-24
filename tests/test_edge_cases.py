"""Edge case and integration tests."""

import pytest
from spec2plan import Spec2Plan
from spec2plan.core.analyzer import Analyzer, ProjectType
from spec2plan.core.architect import Architect
from spec2plan.core.planner import Planner


def test_spec2plan_class_integration() -> None:
    """Test Spec2Plan class as main entry point."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a simple API")
    assert len(plan) > 0
    assert "API" in plan


def test_spec2plan_multiple_calls() -> None:
    """Test Spec2Plan can be called multiple times."""
    s2p = Spec2Plan()
    plan1 = s2p.generate("Build an API")
    plan2 = s2p.generate("Build a CLI")
    assert len(plan1) > 0
    assert len(plan2) > 0
    assert plan1 != plan2


def test_analyzer_case_insensitive() -> None:
    """Test analyzer is case insensitive."""
    analyzer = Analyzer()
    result1 = analyzer.analyze("Build a REST API")
    result2 = analyzer.analyze("BUILD A REST API")
    result3 = analyzer.analyze("build a rest api")
    assert result1.project_type == result2.project_type == result3.project_type


def test_analyzer_with_special_characters() -> None:
    """Test analyzer handles special characters."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an API with OAuth2, JWT, & SSL!")
    assert result.project_type == ProjectType.API


def test_analyzer_with_numbers() -> None:
    """Test analyzer handles numbers in requirement."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build API v2 with JSON responses")
    assert len(result.keywords) > 0


def test_analyzer_very_long_requirement() -> None:
    """Test analyzer handles very long requirements."""
    analyzer = Analyzer()
    long_req = "Build an API " + "with features " * 50
    result = analyzer.analyze(long_req)
    assert result.project_type == ProjectType.API


def test_analyzer_unicode_characters() -> None:
    """Test analyzer handles unicode characters."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an API for 日本語 users")
    assert len(result.core_features) > 0


def test_architect_with_all_project_types() -> None:
    """Test architect handles all project types."""
    analyzer = Analyzer()
    architect = Architect()

    project_types = [
        ProjectType.WEB_APP,
        ProjectType.API,
        ProjectType.CLI,
        ProjectType.LIBRARY,
        ProjectType.MOBILE,
        ProjectType.DATA_PIPELINE,
        ProjectType.UNKNOWN,
    ]

    for pt in project_types:
        # Create a result with each project type
        from spec2plan.core.analyzer import AnalysisResult
        analysis = AnalysisResult(
            raw_input=f"Build a {pt.value}",
            project_type=pt,
            core_features=[],
            implied_features=[],
            constraints={}
        )
        design = architect.design(analysis)
        assert design.tech_stack is not None
        assert len(design.components) > 0


def test_architect_component_count_by_type() -> None:
    """Test architect generates appropriate number of components."""
    analyzer = Analyzer()
    architect = Architect()

    # CLI should have fewer components
    cli_analysis = analyzer.analyze("Build a simple CLI")
    cli_design = architect.design(cli_analysis)

    # Web app should have more components
    web_analysis = analyzer.analyze("Build a web app with authentication")
    web_design = architect.design(web_analysis)

    assert len(web_design.components) >= len(cli_design.components)


def test_planner_task_phases_order() -> None:
    """Test planner generates tasks in logical phase order."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    analysis = analyzer.analyze("Build a web app")
    architecture = architect.design(analysis)
    plan = planner.plan(analysis, architecture)

    phases = [task.phase for task in plan.tasks]
    # First task should be SETUP
    assert phases[0] == Planner.__bases__[0].__dict__.get("SETUP") or "SETUP" in str(phases[0])


def test_planner_effort_estimates_range() -> None:
    """Test planner provides varied effort estimates."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    analysis = analyzer.analyze("Build a web app")
    architecture = architect.design(analysis)
    plan = planner.plan(analysis, architecture)

    efforts = [task.estimated_effort for task in plan.tasks]
    # Should have some variety in effort estimates
    effort_texts = " ".join(efforts)
    assert "hour" in effort_texts.lower()
    assert "day" in effort_texts.lower()


def test_planner_risks_by_feature() -> None:
    """Test planner generates appropriate risks for features."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    # With authentication
    auth_analysis = analyzer.analyze("Build an API with authentication")
    auth_architecture = architect.design(auth_analysis)
    auth_plan = planner.plan(auth_analysis, auth_architecture)

    # Without authentication
    simple_analysis = analyzer.analyze("Build a simple API")
    simple_architecture = architect.design(simple_analysis)
    simple_plan = planner.plan(simple_analysis, simple_architecture)

    # Auth version should have security risk
    auth_risks = " ".join(auth_plan.risks).lower()
    assert "security" in auth_risks or "auth" in auth_risks


def test_generator_output_size_consistency() -> None:
    """Test generator produces reasonably sized output."""
    s2p = Spec2Plan()

    simple = s2p.generate("Build an API")
    complex_req = s2p.generate("Build a web app with authentication, database, search, realtime, and notifications")

    # Complex requirement should generally produce more output
    assert len(complex_req) >= len(simple) * 0.8  # At least 80% as long


def test_generator_all_sections_present() -> None:
    """Test generator produces all required sections."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    required_headers = [
        "# Implementation Plan",
        "## Original Requirement",
        "## 1. Requirement Analysis",
        "## 2. Technology Stack",
        "## 3. Architecture",
        "## 4. Implementation Plan",
        "## 5. Risks and Mitigations",
        "## 6. Next Steps",
    ]

    for header in required_headers:
        assert header in plan


def test_generator_preserves_requirement_quotes() -> None:
    """Test generator preserves quotes in requirement."""
    s2p = Spec2Plan()
    req = 'Build an API called "MyAPI"'
    plan = s2p.generate(req)
    assert req in plan or "MyAPI" in plan


def test_implied_features_no_duplicates() -> None:
    """Test implied features don't have duplicates."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an API")

    implied_set = set(result.implied_features)
    assert len(result.implied_features) == len(implied_set)


def test_core_and_implied_no_overlap() -> None:
    """Test core and implied features don't overlap."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an API with authentication")

    core_set = set(result.core_features)
    for implied in result.implied_features:
        assert implied not in core_set


def test_task_dependencies_valid() -> None:
    """Test task dependencies reference valid tasks."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    analysis = analyzer.analyze("Build a web app")
    architecture = architect.design(analysis)
    plan = planner.plan(analysis, architecture)

    task_ids = {task.id for task in plan.tasks}

    for task in plan.tasks:
        for dep in task.dependencies:
            assert dep in task_ids, f"Task {task.id} depends on non-existent task {dep}"


def test_all_tasks_have_description() -> None:
    """Test all tasks have non-empty description."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    analysis = analyzer.analyze("Build an API")
    architecture = architect.design(analysis)
    plan = planner.plan(analysis, architecture)

    for task in plan.tasks:
        assert len(task.description) > 0


def test_all_tasks_have_title() -> None:
    """Test all tasks have non-empty title."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    analysis = analyzer.analyze("Build an API")
    architecture = architect.design(analysis)
    plan = planner.plan(analysis, architecture)

    for task in plan.tasks:
        assert len(task.title) > 0


def test_component_interfaces_not_empty() -> None:
    """Test all components have at least one interface."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build a web app")
    design = architect.design(analysis)

    for component in design.components:
        assert len(component.interfaces) > 0


def test_component_responsibility_not_empty() -> None:
    """Test all components have responsibility defined."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build an API")
    design = architect.design(analysis)

    for component in design.components:
        assert len(component.responsibility) > 0


def test_tech_stack_all_fields_filled() -> None:
    """Test tech stack has required fields filled."""
    analyzer = Analyzer()
    architect = Architect()

    analysis = analyzer.analyze("Build an API")
    design = architect.design(analysis)

    stack = design.tech_stack
    assert len(stack.language) > 0
    assert len(stack.backend_framework) > 0
    assert len(stack.database) > 0
    assert len(stack.deployment) > 0


def test_data_flow_not_empty() -> None:
    """Test data flow is not empty."""
    analyzer = Analyzer()
    architect = Architect()

    for req in ["Build an API", "Build a web app", "Build a CLI"]:
        analysis = analyzer.analyze(req)
        design = architect.design(analysis)
        assert len(design.data_flow) > 0


def test_plan_has_next_steps() -> None:
    """Test plan always has next steps."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    analysis = analyzer.analyze("Build something")
    architecture = architect.design(analysis)
    plan = planner.plan(analysis, architecture)

    assert len(plan.next_steps) > 0


def test_plan_has_risks() -> None:
    """Test plan always includes some risks."""
    analyzer = Analyzer()
    architect = Architect()
    planner = Planner()

    analysis = analyzer.analyze("Build an API")
    architecture = architect.design(analysis)
    plan = planner.plan(analysis, architecture)

    assert len(plan.risks) > 0


def test_constraints_preserved_in_analysis() -> None:
    """Test constraints are preserved in analysis result."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a Python API with high performance")

    assert result.constraints.get("language") == "python"
    assert result.constraints.get("performance") == "high"


def test_empty_constraints_handled() -> None:
    """Test empty constraints dict is handled."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API", constraints={})
    assert len(plan) > 0


def test_none_constraints_handled() -> None:
    """Test None constraints is handled."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API", constraints=None)
    assert len(plan) > 0


def test_whitespace_only_requirement() -> None:
    """Test requirement with only whitespace."""
    analyzer = Analyzer()
    result = analyzer.analyze("   ")
    assert result.project_type == ProjectType.UNKNOWN


def test_newline_in_requirement() -> None:
    """Test requirement with newlines."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an API\nwith authentication")
    assert result.project_type == ProjectType.API


def test_tab_in_requirement() -> None:
    """Test requirement with tabs."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an API\twith database")
    assert result.project_type == ProjectType.API


def test_multiple_spaces_in_requirement() -> None:
    """Test requirement with multiple spaces."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build   an   API")
    assert result.project_type == ProjectType.API


def test_mixed_case_keywords() -> None:
    """Test mixed case keywords are detected."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a ReSt Api")
    assert result.project_type == ProjectType.API


def test_keyword_extraction_filters_stops() -> None:
    """Test keyword extraction filters stop words."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a REST API that will have features")
    # "that", "will", "have" should be filtered
    assert "that" not in result.keywords
    assert "will" not in result.keywords


def test_analysis_result_dataclass() -> None:
    """Test AnalysisResult is a proper dataclass."""
    from spec2plan.core.analyzer import AnalysisResult

    result = AnalysisResult(
        raw_input="Test",
        project_type=ProjectType.API,
        core_features=[],
        implied_features=[],
        constraints={}
    )

    assert result.raw_input == "Test"
    assert result.project_type == ProjectType.API


def test_architecture_design_dataclass() -> None:
    """Test ArchitectureDesign is a proper dataclass."""
    from spec2plan.core.architect import ArchitectureDesign, TechStack

    design = ArchitectureDesign(
        tech_stack=TechStack(
            language="Python",
            backend_framework="FastAPI",
            database="PostgreSQL"
        ),
        components=[],
        data_flow="Test flow"
    )

    assert design.tech_stack.language == "Python"
    assert design.data_flow == "Test flow"


def test_implementation_plan_dataclass() -> None:
    """Test ImplementationPlan is a proper dataclass."""
    from spec2plan.core.planner import ImplementationPlan

    plan = ImplementationPlan(
        tasks=[],
        risks=["Test risk"],
        next_steps=["Step 1"]
    )

    assert len(plan.risks) == 1
    assert len(plan.next_steps) == 1


def test_task_dataclass() -> None:
    """Test Task is a proper dataclass."""
    from spec2plan.core.planner import Task, TaskPhase

    task = Task(
        id="T01",
        title="Test",
        phase=TaskPhase.SETUP,
        description="Test task",
        steps=["Step 1"],
        acceptance_criteria=["Done"],
        estimated_effort="1 hour"
    )

    assert task.id == "T01"
    assert task.phase == TaskPhase.SETUP


def test_project_type_enum_values() -> None:
    """Test ProjectType enum has expected values."""
    assert ProjectType.WEB_APP.value == "web_app"
    assert ProjectType.API.value == "api"
    assert ProjectType.CLI.value == "cli"
    assert ProjectType.LIBRARY.value == "library"
    assert ProjectType.MOBILE.value == "mobile"
    assert ProjectType.DATA_PIPELINE.value == "data_pipeline"
    assert ProjectType.UNKNOWN.value == "unknown"


def test_task_phase_enum_values() -> None:
    """Test TaskPhase enum has expected values."""
    from spec2plan.core.planner import TaskPhase

    assert TaskPhase.SETUP.value == "setup"
    assert TaskPhase.FOUNDATION.value == "foundation"
    assert TaskPhase.CORE_FEATURES.value == "core_features"
    assert TaskPhase.INTEGRATION.value == "integration"
    assert TaskPhase.TESTING.value == "testing"
    assert TaskPhase.DEPLOYMENT.value == "deployment"


def test_component_type_enum_values() -> None:
    """Test ComponentType enum has expected values."""
    from spec2plan.core.architect import ComponentType

    assert ComponentType.SERVICE.value == "service"
    assert ComponentType.DATABASE.value == "database"
    assert ComponentType.CACHE.value == "cache"
    assert ComponentType.QUEUE.value == "queue"
    assert ComponentType.STORAGE.value == "storage"
    assert ComponentType.FRONTEND.value == "frontend"
    assert ComponentType.GATEWAY.value == "gateway"


def test_generator_handles_all_feature_keywords() -> None:
    """Test generator handles all feature keywords."""
    s2p = Spec2Plan()

    features = [
        "authentication",
        "database",
        "search",
        "realtime",
        "file_handling",
        "notifications",
        "cron",
    ]

    for feature in features:
        # Build requirement with feature
        if feature == "authentication":
            req = "Build an API with authentication"
        elif feature == "database":
            req = "Build an app with database"
        elif feature == "search":
            req = "Build an API with search"
        elif feature == "realtime":
            req = "Build an app with realtime updates"
        elif feature == "file_handling":
            req = "Build an API with file upload"
        elif feature == "notifications":
            req = "Build an app with notifications"
        elif feature == "cron":
            req = "Build an app with scheduled jobs"

        plan = s2p.generate(req)
        assert len(plan) > 100


def test_all_project_types_generate_output() -> None:
    """Test all project types generate valid output."""
    s2p = Spec2Plan()

    requirements = [
        ("Build a web application", "web"),
        ("Build a REST API", "api"),
        ("Build a CLI tool", "cli"),
        ("Build a library", "library"),
        ("Build a mobile app", "mobile"),
        ("Build a data pipeline", "pipeline"),
    ]

    for req, keyword in requirements:
        plan = s2p.generate(req)
        assert len(plan) > 200
