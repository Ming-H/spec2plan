"""Example: Generate a plan for a blog system API."""

from spec2plan import Spec2Plan


def main() -> None:
    """Generate and print a blog system plan."""
    s2p = Spec2Plan()

    requirement = (
        "Build a RESTful blog API with user authentication, "
        "post creation/editing, comments, and search functionality."
    )

    plan = s2p.generate(requirement)
    print(plan)


if __name__ == "__main__":
    main()
