"""Example: Generate a plan for a CLI tool."""

from spec2plan import Spec2Plan


def main() -> None:
    """Generate and print a CLI tool plan."""
    s2p = Spec2Plan()

    requirement = (
        "Create a CLI tool for managing TODO items with SQLite storage, "
        "supporting add, list, complete, and delete operations."
    )

    plan = s2p.generate(requirement)
    print(plan)


if __name__ == "__main__":
    main()
