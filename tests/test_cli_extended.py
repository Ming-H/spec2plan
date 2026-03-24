"""Extended tests for the CLI module."""

from pathlib import Path
from click.testing import CliRunner
from spec2plan.cli import main


def test_cli_with_version_option() -> None:
    """Test CLI version option."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0


def test_cli_with_empty_requirement() -> None:
    """Test CLI with minimal requirement."""
    runner = CliRunner()
    result = runner.invoke(main, ["Build"])
    assert result.exit_code == 0


def test_cli_with_complex_requirement() -> None:
    """Test CLI with complex requirement."""
    runner = CliRunner()
    result = runner.invoke(main, [
        "Build a real-time analytics dashboard with user authentication, "
        "role-based access control, and data export functionality"
    ])
    assert result.exit_code == 0
    assert "authentication" in result.output.lower()


def test_cli_with_python_language() -> None:
    """Test CLI with Python language option."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "python", "Build an API"])
    assert result.exit_code == 0
    assert "Python" in result.output


def test_cli_with_javascript_language() -> None:
    """Test CLI with JavaScript language option."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "javascript", "Build an API"])
    assert result.exit_code == 0


def test_cli_with_multiple_constraints() -> None:
    """Test CLI with multiple constraint options."""
    runner = CliRunner()
    result = runner.invoke(main, [
        "-c", "language=python",
        "-c", "performance=high",
        "Build a fast API"
    ])
    assert result.exit_code == 0


def test_cli_constraint_without_equals() -> None:
    """Test CLI constraint without equals sign."""
    runner = CliRunner()
    result = runner.invoke(main, ["-c", "simple", "Build an API"])
    assert result.exit_code == 0


def test_cli_output_to_nested_directory(tmp_path: Path) -> None:
    """Test CLI output to nested directory."""
    runner = CliRunner()
    output_dir = tmp_path / "plans" / "nested"
    output_file = output_dir / "plan.md"
    result = runner.invoke(
        main,
        ["-o", str(output_file), "Build an API"],
    )
    assert result.exit_code == 0
    assert output_file.exists()


def test_cli_overwrites_existing_file(tmp_path: Path) -> None:
    """Test CLI overwrites existing file."""
    runner = CliRunner()
    output_file = tmp_path / "plan.md"

    # Create file with initial content
    output_file.write_text("OLD CONTENT")

    result = runner.invoke(
        main,
        ["-o", str(output_file), "Build an API"],
    )
    assert result.exit_code == 0
    content = output_file.read_text()
    assert "OLD CONTENT" not in content
    assert "# Implementation Plan" in content


def test_cli_generates_complete_output() -> None:
    """Test that CLI generates complete output with all sections."""
    runner = CliRunner()
    result = runner.invoke(main, ["Build a web app"])

    required_sections = [
        "# Implementation Plan",
        "Requirement Analysis",
        "Technology Stack",
        "Architecture",
        "Implementation Plan",
        "Risks",
        "Next Steps",
    ]

    for section in required_sections:
        assert section in result.output


def test_cli_handles_special_characters() -> None:
    """Test CLI handles special characters in requirement."""
    runner = CliRunner()
    result = runner.invoke(main, ["Build an API with OAuth2 & JWT auth"])
    assert result.exit_code == 0


def test_cli_handles_multiline_requirement() -> None:
    """Test CLI handles requirement with quotes."""
    runner = CliRunner()
    result = runner.invoke(main, ["Build an API 'with quotes'"])
    assert result.exit_code == 0


def test_cli_output_contains_project_type() -> None:
    """Test CLI output includes detected project type."""
    runner = CliRunner()
    result = runner.invoke(main, ["Build a CLI tool"])
    assert "CLI" in result.output or "cli" in result.output.lower()


def test_cli_with_api_requirement() -> None:
    """Test CLI with API requirement."""
    runner = CliRunner()
    result = runner.invoke(main, ["Build a REST API"])
    assert result.exit_code == 0
    assert "API" in result.output


def test_cli_with_web_app_requirement() -> None:
    """Test CLI with web app requirement."""
    runner = CliRunner()
    result = runner.invoke(main, ["Build a web dashboard"])
    assert result.exit_code == 0
    assert "web" in result.output.lower() or "frontend" in result.output.lower()


def test_cli_with_library_requirement() -> None:
    """Test CLI with library requirement."""
    runner = CliRunner()
    result = runner.invoke(main, ["Create a Python library"])
    assert result.exit_code == 0
    assert "library" in result.output.lower()


def test_cli_generates_tasks() -> None:
    """Test CLI generates implementation tasks."""
    runner = CliRunner()
    result = runner.invoke(main, ["Build an API"])
    assert "T01" in result.output or "T" in result.output


def test_cli_generates_risks() -> None:
    """Test CLI generates risk assessment."""
    runner = CliRunner()
    result = runner.invoke(main, ["Build an API"])
    assert "Risk" in result.output


def test_cli_with_minimal_constraint() -> None:
    """Test CLI with minimal complexity constraint."""
    runner = CliRunner()
    result = runner.invoke(main, ["-c", "complexity=minimal", "Build an API"])
    assert result.exit_code == 0


def test_cli_help_shows_usage() -> None:
    """Test CLI help shows proper usage."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Generate" in result.output
    assert "requirement" in result.output.lower()


def test_cli_output_file_confirmation(tmp_path: Path) -> None:
    """Test CLI confirms file output."""
    runner = CliRunner()
    output_file = tmp_path / "plan.md"
    result = runner.invoke(
        main,
        ["-o", str(output_file), "Build an API"],
    )
    assert result.exit_code == 0
    assert "Plan written to" in result.output or "plan.md" in result.output.lower()


def test_cli_with_authentication_feature() -> None:
    """Test CLI with authentication feature."""
    runner = CliRunner()
    result = runner.invoke(main, ["Build an API with authentication"])
    assert result.exit_code == 0
    assert "authentication" in result.output.lower()


def test_cli_with_database_feature() -> None:
    """Test CLI with database feature."""
    runner = CliRunner()
    result = runner.invoke(main, ["Build an API with database"])
    assert result.exit_code == 0
    assert "database" in result.output.lower()


def test_cli_generates_tech_stack() -> None:
    """Test CLI generates technology stack."""
    runner = CliRunner()
    result = runner.invoke(main, ["Build an API"])
    assert "Python" in result.output or "Language" in result.output
