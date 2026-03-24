"""Tests for the CLI module."""

from pathlib import Path

from click.testing import CliRunner
from spec2plan.cli import main


def test_cli_runs() -> None:
    """Test that CLI can be invoked."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Generate an implementation plan" in result.output


def test_cli_generates_plan() -> None:
    """Test that CLI generates a plan."""
    runner = CliRunner()
    result = runner.invoke(main, ["Build a simple API"])
    assert result.exit_code == 0
    assert "# Implementation Plan" in result.output


def test_cli_with_language() -> None:
    """Test CLI with language option."""
    runner = CliRunner()
    result = runner.invoke(main, ["-l", "python", "Build an API"])
    assert result.exit_code == 0
    assert "Python" in result.output


def test_cli_with_constraints() -> None:
    """Test CLI with constraint option."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["-c", "performance=high", "Build a fast API"],
    )
    assert result.exit_code == 0


def test_cli_output_to_file(tmp_path: Path) -> None:
    """Test CLI output to file."""
    runner = CliRunner()
    output_file = tmp_path / "plan.md"
    result = runner.invoke(
        main,
        ["-o", str(output_file), "Build an API"],
    )
    assert result.exit_code == 0
    assert output_file.exists()
    content = output_file.read_text()
    assert "# Implementation Plan" in content
