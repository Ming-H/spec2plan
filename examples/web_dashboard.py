"""Example: Generate a plan for a web dashboard."""

from spec2plan import Spec2Plan


def main() -> None:
    """Generate and print a web dashboard plan."""
    s2p = Spec2Plan()

    requirement = (
        "Build a real-time analytics dashboard web application with "
        "live data updates, user authentication, and export functionality."
    )

    plan = s2p.generate(requirement)
    print(plan)


if __name__ == "__main__":
    main()
