"""CLI tool for Spec2Plan."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import click
from spec2plan import Spec2Plan

if TYPE_CHECKING:
    from collections.abc import Sequence


@click.command()
@click.argument("requirement")
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    help="Output file path (default: stdout)",
)
@click.option(
    "-l",
    "--language",
    help="Preferred programming language",
)
@click.option(
    "-c",
    "--constraint",
    multiple=True,
    help="Additional constraints (key=value format)",
)
@click.version_option(version="0.1.0")
def main(
    requirement: str,
    output: str | None,
    language: str | None,
    constraint: tuple[str, ...],
) -> None:
    """Generate an implementation plan from a natural language requirement.

    Example:
        spec2plan "Build a RESTful blog API with user authentication"
    """
    # Parse constraints
    constraints: dict[str, str] = {}

    if language:
        constraints["language"] = language

    for c in constraint:
        if "=" in c:
            key, value = c.split("=", 1)
            constraints[key.strip()] = value.strip()
        else:
            constraints[c] = "true"

    # Generate plan
    s2p = Spec2Plan()
    plan = s2p.generate(requirement, constraints or None)

    # Output
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(plan)
        click.echo(f"Plan written to {output_path}")
    else:
        click.echo(plan)


if __name__ == "__main__":
    main()
