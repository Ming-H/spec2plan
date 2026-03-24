"""Tests for the Generator module."""

from spec2plan import Spec2Plan


def test_generator_produces_output() -> None:
    """Test that generator produces non-empty output."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build a simple API")
    assert len(plan) > 0
    assert "# Implementation Plan" in plan


def test_generator_includes_requirement() -> None:
    """Test that generator includes original requirement."""
    s2p = Spec2Plan()
    requirement = "Build a RESTful blog API"
    plan = s2p.generate(requirement)
    assert requirement in plan


def test_generator_includes_sections() -> None:
    """Test that generator includes all main sections."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API")

    required_sections = [
        "# Implementation Plan",
        "## 1. Requirement Analysis",
        "## 2. Technology Stack",
        "## 3. Architecture",
        "## 4. Implementation Plan",
        "## 5. Risks and Mitigations",
        "## 6. Next Steps",
    ]

    for section in required_sections:
        assert section in plan


def test_generator_with_constraints() -> None:
    """Test generator with explicit constraints."""
    s2p = Spec2Plan()
    plan = s2p.generate("Build an API", constraints={"language": "python"})
    assert "Python" in plan
