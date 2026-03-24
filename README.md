# Spec2Plan

Transform natural language requirements into structured implementation plans.

## Quick Start

```python
from spec2plan import Spec2Plan

s2p = Spec2Plan()
plan = s2p.generate("Build a RESTful blog API with user authentication")
print(plan)
```

## Features

- **Requirement Analysis**: Extract core features and constraints
- **Technology Selection**: Recommend appropriate tech stack
- **Architecture Design**: Generate system architecture descriptions
- **Task Breakdown**: Decompose into executable steps
- **Acceptance Criteria**: Define completion for each step

## Installation

```bash
pip install spec2plan
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
mypy spec2plan
```

## Project Structure

```
spec2plan/
├── core/
│   ├── analyzer.py    # Requirement analysis
│   ├── architect.py   # Architecture design
│   ├── planner.py     # Plan generation
│   └── generator.py   # Main generator
└── templates/
    └── plan.md.j2     # Plan template
```

## License

MIT
