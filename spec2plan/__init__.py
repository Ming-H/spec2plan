"""Spec2Plan - Transform requirements into implementation plans."""

from spec2plan.core.generator import Generator

__all__ = ["Generator", "Spec2Plan"]
__version__ = "0.1.0"


class Spec2Plan:
    """Main entry point for generating implementation plans."""

    def __init__(self) -> None:
        self._generator = Generator()

    def generate(
        self, requirement: str, constraints: dict | None = None
    ) -> str:
        """Generate an implementation plan from a requirement.

        Args:
            requirement: Natural language description of the requirement
            constraints: Optional constraints (tech preferences, budget, etc.)

        Returns:
            Markdown formatted implementation plan
        """
        return self._generator.generate(requirement, constraints or {})
