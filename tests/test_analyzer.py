"""Tests for the Analyzer module."""

from spec2plan.core.analyzer import Analyzer, ProjectType


def test_analyzer_detects_api_project() -> None:
    """Test that analyzer detects API projects."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a REST API for user management")
    assert result.project_type == ProjectType.API


def test_analyzer_detects_web_app() -> None:
    """Test that analyzer detects web applications."""
    analyzer = Analyzer()
    result = analyzer.analyze("Create a website for e-commerce")
    assert result.project_type == ProjectType.WEB_APP


def test_analyzer_detects_cli() -> None:
    """Test that analyzer detects CLI tools."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a CLI tool for data processing")
    assert result.project_type == ProjectType.CLI


def test_analyzer_extracts_auth_feature() -> None:
    """Test that analyzer extracts authentication feature."""
    analyzer = Analyzer()
    result = analyzer.analyze("API with login and signup")
    assert "authentication" in result.core_features


def test_analyzer_infers_database_for_web_apps() -> None:
    """Test that analyzer infers database for web apps."""
    analyzer = Analyzer()
    result = analyzer.analyze("Create a simple website")
    assert "database" in result.implied_features


def test_analyzer_extracts_python_constraint() -> None:
    """Test that analyzer extracts Python language constraint."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a Python API")
    assert result.constraints.get("language") == "python"


def test_analyzer_extracts_database_feature() -> None:
    """Test that analyzer extracts database feature."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an API with data persistence")
    assert "database" in result.core_features


def test_analyzer_extracts_search_feature() -> None:
    """Test that analyzer extracts search feature."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an API with search functionality")
    assert "search" in result.core_features


def test_analyzer_extracts_realtime_feature() -> None:
    """Test that analyzer extracts realtime feature."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a websocket app for live updates")
    assert "realtime" in result.core_features


def test_analyzer_extracts_file_handling_feature() -> None:
    """Test that analyzer extracts file handling feature."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an API with file upload")
    assert "file_handling" in result.core_features


def test_analyzer_extracts_notifications_feature() -> None:
    """Test that analyzer extracts notifications feature."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an app with email alerts")
    assert "notifications" in result.core_features


def test_analyzer_extracts_cron_feature() -> None:
    """Test that analyzer extracts cron feature."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a system with scheduled jobs")
    assert "cron" in result.core_features


def test_analyzer_detects_library_project() -> None:
    """Test that analyzer detects library projects."""
    analyzer = Analyzer()
    result = analyzer.analyze("Create a Python library for data processing")
    assert result.project_type == ProjectType.LIBRARY


def test_analyzer_detects_mobile_project() -> None:
    """Test that analyzer detects mobile projects."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a mobile app for iOS")
    assert result.project_type == ProjectType.MOBILE


def test_analyzer_detects_data_pipeline_project() -> None:
    """Test that analyzer detects data pipeline projects."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an ETL pipeline for data processing")
    assert result.project_type == ProjectType.DATA_PIPELINE


def test_analyzer_infers_user_management_with_auth() -> None:
    """Test that analyzer infers user management when auth is present."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an API with authentication")
    assert "user_management" in result.implied_features


def test_analyzer_infers_session_handling_with_auth() -> None:
    """Test that analyzer infers session handling when auth is present."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an API with login")
    assert "session_handling" in result.implied_features


def test_analyzer_infers_api_docs_for_api_projects() -> None:
    """Test that analyzer infers API documentation for API projects."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a REST API")
    assert "api_documentation" in result.implied_features


def test_analyzer_infers_error_handling_for_api_projects() -> None:
    """Test that analyzer infers error handling for API projects."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a REST API")
    assert "error_handling" in result.implied_features


def test_analyzer_extracts_javascript_constraint() -> None:
    """Test that analyzer extracts JavaScript language constraint."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a JavaScript API")
    assert result.constraints.get("language") == "javascript/typescript"


def test_analyzer_extracts_typescript_constraint() -> None:
    """Test that analyzer extracts TypeScript language constraint."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a TypeScript web app")
    assert result.constraints.get("language") == "javascript/typescript"


def test_analyzer_extracts_performance_constraint() -> None:
    """Test that analyzer extracts performance constraint."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a fast API")
    assert result.constraints.get("performance") == "high"


def test_analyzer_extracts_minimal_constraint() -> None:
    """Test that analyzer extracts minimal complexity constraint."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a simple API")
    assert result.constraints.get("complexity") == "minimal"


def test_analyzer_extracts_keywords() -> None:
    """Test that analyzer extracts keywords from text."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a RESTful API for user management")
    assert len(result.keywords) > 0


def test_analyzer_handles_empty_input() -> None:
    """Test that analyzer handles empty input gracefully."""
    analyzer = Analyzer()
    result = analyzer.analyze("")
    assert result.project_type == ProjectType.UNKNOWN


def test_analyzer_handles_unknown_project_type() -> None:
    """Test that analyzer returns UNKNOWN for unrecognized types."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build something generic")
    assert result.project_type == ProjectType.UNKNOWN


def test_analyzer_preserves_raw_input() -> None:
    """Test that analyzer preserves the original input."""
    analyzer = Analyzer()
    original = "Build a REST API for user management"
    result = analyzer.analyze(original)
    assert result.raw_input == original


def test_analyzer_no_duplicate_implied_features() -> None:
    """Test that analyzer doesn't duplicate implied features."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an API")
    implied_set = set(result.implied_features)
    assert len(result.implied_features) == len(implied_set)


def test_analyzer_no_implied_duplicates_with_core() -> None:
    """Test that implied features don't duplicate core features."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an API with authentication")
    core_set = set(result.core_features)
    for feature in result.implied_features:
        assert feature not in core_set


def test_analyzer_extracts_frontend_feature() -> None:
    """Test that analyzer extracts frontend feature."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build a web dashboard with UI")
    assert "frontend" in result.core_features


def test_analyzer_detects_dashboard_project() -> None:
    """Test that analyzer detects dashboard as web app."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an admin dashboard")
    assert result.project_type == ProjectType.WEB_APP


def test_analyzer_handles_multiple_features() -> None:
    """Test that analyzer extracts multiple features."""
    analyzer = Analyzer()
    result = analyzer.analyze("Build an API with authentication, search, and file upload")
    assert "authentication" in result.core_features
    assert "search" in result.core_features
    assert "file_handling" in result.core_features
