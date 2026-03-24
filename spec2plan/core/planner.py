"""Plan generator - breaks down architecture into executable tasks."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from spec2plan.core.analyzer import AnalysisResult, ProjectType
from spec2plan.core.architect import ArchitectureDesign


class TaskPhase(Enum):
    """Phases of development."""

    SETUP = "setup"
    FOUNDATION = "foundation"
    CORE_FEATURES = "core_features"
    INTEGRATION = "integration"
    TESTING = "testing"
    DEPLOYMENT = "deployment"


@dataclass
class Task:
    """A development task."""

    id: str
    title: str
    phase: TaskPhase
    description: str
    steps: list[str]
    acceptance_criteria: list[str]
    estimated_effort: str  # e.g., "2-4 hours", "1-2 days"
    dependencies: list[str] = field(default_factory=list)


@dataclass
class ImplementationPlan:
    """Complete implementation plan."""

    tasks: list[Task]
    risks: list[str]
    next_steps: list[str]


class Planner:
    """Generates implementation plans from architecture designs."""

    def plan(
        self, analysis: AnalysisResult, architecture: ArchitectureDesign
    ) -> ImplementationPlan:
        """Generate implementation plan from analysis and architecture.

        Args:
            analysis: Result from Analyzer
            architecture: Result from Architect

        Returns:
            ImplementationPlan with tasks and risks
        """
        tasks = self._generate_tasks(analysis, architecture)
        risks = self._identify_risks(analysis, architecture)
        next_steps = self._define_next_steps(analysis)

        return ImplementationPlan(
            tasks=tasks,
            risks=risks,
            next_steps=next_steps,
        )

    def _generate_tasks(
        self, analysis: AnalysisResult, architecture: ArchitectureDesign
    ) -> list[Task]:
        """Generate development tasks."""
        tasks = []
        task_id = 1

        # Phase 1: Setup
        tasks.append(Task(
            id=f"T{task_id:02d}",
            title="Project Setup",
            phase=TaskPhase.SETUP,
            description="Initialize project structure and development environment",
            steps=[
                f"Initialize {architecture.tech_stack.language} project",
                "Set up virtual environment and dependencies",
                "Configure linting and formatting tools",
                "Set up version control (.gitignore)",
                "Create basic project structure",
            ],
            acceptance_criteria=[
                "Project runs without errors",
                "Dependencies are installed",
                "Basic structure follows best practices",
            ],
            estimated_effort="1-2 hours",
        ))
        task_id += 1

        # Phase 2: Foundation - for API, Web App, Microservice
        if analysis.project_type in (ProjectType.API, ProjectType.WEB_APP, ProjectType.MICROSERVICE):
            tasks.append(Task(
                id=f"T{task_id:02d}",
                title="Core API Framework",
                phase=TaskPhase.FOUNDATION,
                description=f"Set up {architecture.tech_stack.backend_framework} application",
                steps=[
                    f"Initialize {architecture.tech_stack.backend_framework} app",
                    "Set up routing structure",
                    "Configure middleware (CORS, logging)",
                    "Add error handling middleware",
                    "Set up environment configuration",
                ],
                acceptance_criteria=[
                    "Server starts and responds to health checks",
                    "Routing works correctly",
                    "Error responses are properly formatted",
                ],
                estimated_effort="2-4 hours",
                dependencies=[f"T{task_id-1:02d}"],
            ))
            task_id += 1

        # Phase 2b: Foundation - for Desktop
        if analysis.project_type == ProjectType.DESKTOP:
            tasks.append(Task(
                id=f"T{task_id:02d}",
                title="Desktop Application Framework",
                phase=TaskPhase.FOUNDATION,
                description=f"Set up {architecture.tech_stack.backend_framework} desktop application",
                steps=[
                    f"Initialize {architecture.tech_stack.backend_framework} project",
                    "Set up main window and UI framework",
                    "Configure application lifecycle",
                    "Add error handling",
                    "Set up configuration management",
                ],
                acceptance_criteria=[
                    "Application window opens correctly",
                    "UI framework is functional",
                    "Basic navigation works",
                ],
                estimated_effort="2-4 hours",
                dependencies=[f"T{task_id-1:02d}"],
            ))
            task_id += 1

        # Phase 3: Database
        if "database" in analysis.core_features or "authentication" in analysis.core_features:
            tasks.append(Task(
                id=f"T{task_id:02d}",
                title="Database Setup",
                phase=TaskPhase.FOUNDATION,
                description=f"Configure {architecture.tech_stack.database} and ORM",
                steps=[
                    f"Set up {architecture.tech_stack.database} connection",
                    "Configure ORM / database client",
                    "Define base models/schemas",
                    "Create migration system",
                    "Add database seeding for development",
                ],
                acceptance_criteria=[
                    "Database connection works",
                    "Migrations can run successfully",
                    "Basic CRUD operations work",
                ],
                estimated_effort="3-6 hours",
                dependencies=[f"T{task_id-1:02d}"],
            ))
            task_id += 1

        # Phase 4: Authentication
        if "authentication" in analysis.core_features + analysis.implied_features:
            tasks.append(Task(
                id=f"T{task_id:02d}",
                title="Authentication System",
                phase=TaskPhase.CORE_FEATURES,
                description="Implement user authentication and authorization",
                steps=[
                    "Design user model/schema",
                    "Implement password hashing",
                    "Create registration endpoint",
                    "Create login endpoint with token generation",
                    "Add authentication middleware",
                    "Implement logout/refresh token flow",
                ],
                acceptance_criteria=[
                    "Users can register",
                    "Users can login and receive tokens",
                    "Protected endpoints require valid tokens",
                    "Passwords are properly hashed",
                ],
                estimated_effort="1-2 days",
                dependencies=[f"T{task_id-2:02d}"],
            ))
            task_id += 1

        # Phase 5: Feature-specific tasks based on detected features
        if "realtime" in analysis.core_features:
            tasks.append(Task(
                id=f"T{task_id:02d}",
                title="Real-time Communication",
                phase=TaskPhase.CORE_FEATURES,
                description="Implement WebSocket/real-time features",
                steps=[
                    "Set up WebSocket server",
                    "Implement connection management",
                    "Add event broadcasting",
                    "Handle reconnection logic",
                    "Add authentication for WebSocket",
                ],
                acceptance_criteria=[
                    "WebSocket connections establish correctly",
                    "Messages are broadcast to connected clients",
                    "Reconnection handles gracefully",
                ],
                estimated_effort="1-2 days",
                dependencies=[f"T{task_id-2:02d}"],
            ))
            task_id += 1

        if "search" in analysis.core_features:
            tasks.append(Task(
                id=f"T{task_id:02d}",
                title="Search Implementation",
                phase=TaskPhase.CORE_FEATURES,
                description="Implement search functionality",
                steps=[
                    "Set up search engine (Elasticsearch/PostgreSQL FTS)",
                    "Design index schema",
                    "Implement indexing pipeline",
                    "Create search API endpoints",
                    "Add filters and facets",
                ],
                acceptance_criteria=[
                    "Search returns relevant results",
                    "Indexing updates in near real-time",
                    "Filters work correctly",
                ],
                estimated_effort="1-2 days",
                dependencies=[f"T{task_id-2:02d}"],
            ))
            task_id += 1

        if "file_handling" in analysis.core_features:
            tasks.append(Task(
                id=f"T{task_id:02d}",
                title="File Upload/Storage",
                phase=TaskPhase.CORE_FEATURES,
                description="Implement file handling system",
                steps=[
                    "Set up storage backend (S3/local)",
                    "Implement upload API",
                    "Add file validation",
                    "Implement download functionality",
                    "Add virus scanning for uploads",
                ],
                acceptance_criteria=[
                    "Files upload successfully",
                    "Invalid files are rejected",
                    "Downloads work correctly",
                ],
                estimated_effort="1-2 days",
                dependencies=[f"T{task_id-2:02d}"],
            ))
            task_id += 1

        if "notifications" in analysis.core_features:
            tasks.append(Task(
                id=f"T{task_id:02d}",
                title="Notification System",
                phase=TaskPhase.CORE_FEATURES,
                description="Implement notification service",
                steps=[
                    "Design notification model",
                    "Implement email notifications",
                    "Add in-app notifications",
                    "Implement notification preferences",
                    "Add notification history",
                ],
                acceptance_criteria=[
                    "Emails are sent successfully",
                    "In-app notifications appear",
                    "Users can manage preferences",
                ],
                estimated_effort="1-2 days",
                dependencies=[f"T{task_id-2:02d}"],
            ))
            task_id += 1

        if "payment" in analysis.core_features:
            tasks.append(Task(
                id=f"T{task_id:02d}",
                title="Payment Integration",
                phase=TaskPhase.CORE_FEATURES,
                description="Implement payment processing",
                steps=[
                    "Integrate payment provider (Stripe/PayPal)",
                    "Implement checkout flow",
                    "Add webhook handlers",
                    "Implement subscription management",
                    "Add invoice generation",
                ],
                acceptance_criteria=[
                    "Payments process successfully",
                    "Webhooks handle events correctly",
                    "Invoices are generated accurately",
                ],
                estimated_effort="2-3 days",
                dependencies=[f"T{task_id-2:02d}"],
            ))
            task_id += 1

        # Phase 6: Core Features (generic)
        tasks.append(Task(
            id=f"T{task_id:02d}",
            title="Core Feature Implementation",
            phase=TaskPhase.CORE_FEATURES,
            description="Implement main business logic and endpoints",
            steps=[
                "Define data models for core entities",
                "Implement CRUD operations",
                "Add input validation",
                "Implement business logic",
                "Add error handling for edge cases",
            ],
            acceptance_criteria=[
                "All core endpoints work",
                "Data validation prevents invalid inputs",
                "Error cases are handled gracefully",
            ],
            estimated_effort="2-4 days",
            dependencies=[f"T{task_id-1:02d}"],
        ))
        task_id += 1

        # Phase 7: Integration
        if architecture.tech_stack.cache:
            tasks.append(Task(
                id=f"T{task_id:02d}",
                title="Cache Integration",
                phase=TaskPhase.INTEGRATION,
                description=f"Integrate {architecture.tech_stack.cache} for performance",
                steps=[
                    f"Set up {architecture.tech_stack.cache} client",
                    "Implement caching layer",
                    "Add cache invalidation logic",
                    "Add cache warming for frequent queries",
                ],
                acceptance_criteria=[
                    "Frequently accessed data is cached",
                    "Cache invalidation works correctly",
                    "Performance improvement is measurable",
                ],
                estimated_effort="4-8 hours",
                dependencies=[f"T{task_id-1:02d}"],
            ))
            task_id += 1

        # Phase 8: Testing
        tasks.append(Task(
            id=f"T{task_id:02d}",
            title="Testing",
            phase=TaskPhase.TESTING,
            description="Add comprehensive tests",
            steps=[
                "Set up testing framework",
                "Write unit tests for core logic",
                "Write integration tests for API",
                "Add API documentation tests",
                "Set up CI/CD pipeline",
            ],
            acceptance_criteria=[
                "Unit test coverage >70%",
                "Integration tests pass",
                "CI/CD runs successfully",
            ],
            estimated_effort="1-2 days",
            dependencies=[f"T{task_id-1:02d}"],
        ))
        task_id += 1

        # Phase 9: Deployment
        tasks.append(Task(
            id=f"T{task_id:02d}",
            title="Deployment",
            phase=TaskPhase.DEPLOYMENT,
            description=f"Deploy using {architecture.tech_stack.deployment}",
            steps=[
                f"Set up {architecture.tech_stack.deployment} configuration",
                "Create production environment config",
                "Set up monitoring and logging",
                "Configure backup strategy",
                "Deploy to production",
            ],
            acceptance_criteria=[
                "Application is accessible in production",
                "Monitoring captures errors and metrics",
                "Backup strategy is in place",
            ],
            estimated_effort="4-8 hours",
            dependencies=[f"T{task_id-1:02d}"],
        ))

        return tasks

    def _identify_risks(
        self, analysis: AnalysisResult, architecture: ArchitectureDesign
    ) -> list[str]:
        """Identify potential risks and mitigations."""
        risks = []

        # Technical risks
        if "authentication" in analysis.core_features:
            risks.append(
                "**Security**: Authentication implementation must follow OWASP guidelines. "
                "Use proven libraries (e.g., passlib, itsdangerous) and never store plain passwords."
            )

        if analysis.project_type == ProjectType.WEB_APP:
            risks.append(
                "**Scope Creep**: Frontend requirements can expand significantly. "
                "Define MVP scope clearly and defer nice-to-have features."
            )

        if architecture.tech_stack.database == "PostgreSQL" and "database" not in analysis.core_features:
            risks.append(
                "**Over-engineering**: PostgreSQL might be overkill for simple use cases. "
                "Consider SQLite for prototyping."
            )

        # General risks
        risks.extend([
            "**API Changes**: Backend API changes may break frontend integration. "
            "Use API versioning from the start.",
            "**Performance**: Unoptimized queries can cause issues. "
            "Add database indexes and query optimization early.",
        ])

        return risks

    def _define_next_steps(self, analysis: AnalysisResult) -> list[str]:
        """Define immediate next steps."""
        return [
            "1. Review and approve this plan",
            "2. Set up project repository",
            "3. Create detailed wireframes/mockups (if applicable)",
            "4. Schedule planning meeting to discuss details",
            "5. Begin with T01: Project Setup",
        ]
