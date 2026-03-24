"""Fallback template content used when Jinja2 file is not available."""

TEMPLATE = """# Implementation Plan

## Original Requirement

> {{ requirement }}

## 1. Requirement Analysis

**Project Type**: {{ analysis.project_type.value }}

**Core Features**:
{% for feature in analysis.core_features %}
- {{ feature }}
{% endfor %}

**Implied Features**:
{% for feature in analysis.implied_features %}
- {{ feature }}
{% endfor %}

## 2. Technology Stack

- **Language**: {{ architecture.tech_stack.language }}
- **Backend**: {{ architecture.tech_stack.backend_framework }}
- **Database**: {{ architecture.tech_stack.database }}
{% if architecture.tech_stack.cache %}
- **Cache**: {{ architecture.tech_stack.cache }}
{% endif %}
{% if architecture.tech_stack.frontend %}
- **Frontend**: {{ architecture.tech_stack.frontend }}
{% endif %}
- **Deployment**: {{ architecture.tech_stack.deployment }}

## 3. Architecture

### Components
{% for component in architecture.components %}

**{{ component.name }}** ({{ component.type.value }})
- Technology: {{ component.technology }}
- Responsibility: {{ component.responsibility }}
{% endfor %}

### Data Flow

{{ architecture.data_flow }}
{% if architecture.api_design %}

### API Design

```
{{ architecture.api_design }}
```
{% endif %}

## 4. Implementation Plan

{% for task in plan.tasks %}
**{{ task.id }}: {{ task.title }}** ({{ task.estimated_effort }})

{{ task.description }}

**Steps**:
{% for step in task.steps %}
- {{ step }}
{% endfor %}

**Acceptance Criteria**:
{% for criteria in task.acceptance_criteria %}
- {{ criteria }}
{% endfor %}

{% endfor %}

## 5. Risks and Mitigations
{% for risk in plan.risks %}

- {{ risk }}
{% endfor %}

## 6. Next Steps
{% for step in plan.next_steps %}

{{ step }}
{% endfor %}
"""
