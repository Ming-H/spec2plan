"""Architecture designer - generates technical architecture recommendations."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from spec2plan.core.analyzer import AnalysisResult, ProjectType


class ComponentType(Enum):
    """Types of architectural components."""

    SERVICE = "service"
    DATABASE = "database"
    CACHE = "cache"
    QUEUE = "queue"
    STORAGE = "storage"
    FRONTEND = "frontend"
    GATEWAY = "gateway"
    LOAD_BALANCER = "load_balancer"
    MESSAGE_BROKER = "message_broker"
    API_GATEWAY = "api_gateway"
    MONITORING = "monitoring"
    AUTH_SERVICE = "auth_service"


@dataclass
class TechStack:
    """Recommended technology stack."""

    language: str
    backend_framework: str
    database: str
    cache: str | None = None
    frontend: str | None = None
    deployment: str = "docker"
    reasoning: dict[str, str] | None = None


@dataclass
class Component:
    """An architectural component."""

    name: str
    type: ComponentType
    technology: str
    responsibility: str
    interfaces: list[str]


@dataclass
class ArchitectureDesign:
    """Complete architecture design."""

    tech_stack: TechStack
    components: list[Component]
    data_flow: str
    api_design: str | None = None


class Architect:
    """Designs technical architecture based on analyzed requirements."""

    # Default tech stack recommendations by project type
    DEFAULT_STACKS: dict[ProjectType, TechStack] = {
        ProjectType.WEB_APP: TechStack(
            language="Python",
            backend_framework="FastAPI",
            database="PostgreSQL",
            cache="Redis",
            frontend="React + TypeScript",
            deployment="Docker + Cloud Run",
        ),
        ProjectType.API: TechStack(
            language="Python",
            backend_framework="FastAPI",
            database="PostgreSQL",
            cache="Redis",
            deployment="Docker + Kubernetes",
        ),
        ProjectType.CLI: TechStack(
            language="Python",
            backend_framework="Click/Typer",
            database="SQLite",
            deployment="PyPI",
        ),
        ProjectType.LIBRARY: TechStack(
            language="Python",
            backend_framework="None (library)",
            database="None",
            deployment="PyPI",
        ),
        ProjectType.MICROSERVICE: TechStack(
            language="Python",
            backend_framework="FastAPI + gRPC",
            database="PostgreSQL",
            cache="Redis",
            deployment="Docker + Kubernetes",
        ),
        ProjectType.DESKTOP: TechStack(
            language="Python",
            backend_framework="PyQt/PySide",
            database="SQLite",
            deployment="PyInstaller",
        ),
        ProjectType.PLUGIN: TechStack(
            language="Python",
            backend_framework="Plugin Framework",
            database="None",
            deployment="Package Registry",
        ),
        ProjectType.MOBILE: TechStack(
            language="Python",
            backend_framework="Kivy/BeeWare",
            database="SQLite",
            deployment="App Store/Play Store",
        ),
        ProjectType.DATA_PIPELINE: TechStack(
            language="Python",
            backend_framework="Airflow/Prefect",
            database="PostgreSQL",
            deployment="Docker + Kubernetes",
        ),
    }

    # Go language tech stack recommendations
    GO_STACKS: dict[ProjectType, TechStack] = {
        ProjectType.WEB_APP: TechStack(
            language="Go",
            backend_framework="Gin/Echo",
            database="PostgreSQL",
            cache="Redis",
            frontend="React + TypeScript",
            deployment="Docker + Kubernetes",
        ),
        ProjectType.API: TechStack(
            language="Go",
            backend_framework="Gin/Echo",
            database="PostgreSQL",
            cache="Redis",
            deployment="Docker + Kubernetes",
        ),
        ProjectType.CLI: TechStack(
            language="Go",
            backend_framework="Cobra",
            database="SQLite/BoltDB",
            deployment="GitHub Releases",
        ),
        ProjectType.LIBRARY: TechStack(
            language="Go",
            backend_framework="None (library)",
            database="None",
            deployment="Go Modules",
        ),
    }

    # Java language tech stack recommendations
    JAVA_STACKS: dict[ProjectType, TechStack] = {
        ProjectType.WEB_APP: TechStack(
            language="Java",
            backend_framework="Spring Boot",
            database="PostgreSQL",
            cache="Redis",
            frontend="React + TypeScript",
            deployment="Docker + Kubernetes",
        ),
        ProjectType.API: TechStack(
            language="Java",
            backend_framework="Spring Boot",
            database="PostgreSQL",
            cache="Redis",
            deployment="Docker + Kubernetes",
        ),
        ProjectType.CLI: TechStack(
            language="Java",
            backend_framework="Picocli",
            database="SQLite/H2",
            deployment="Maven Central",
        ),
        ProjectType.LIBRARY: TechStack(
            language="Java",
            backend_framework="None (library)",
            database="None",
            deployment="Maven Central",
        ),
    }

    def design(self, analysis: AnalysisResult) -> ArchitectureDesign:
        """Generate architecture design from analyzed requirements.

        Args:
            analysis: Result from Analyzer

        Returns:
            ArchitectureDesign with tech stack and components
        """
        # Get or create tech stack
        tech_stack = self._select_tech_stack(analysis)

        # Generate components
        components = self._design_components(analysis, tech_stack)

        # Define data flow
        data_flow = self._describe_data_flow(analysis, components)

        # API design if applicable
        api_design = self._design_api(analysis) if analysis.project_type in (
            ProjectType.API, ProjectType.WEB_APP, ProjectType.MICROSERVICE
        ) else None

        return ArchitectureDesign(
            tech_stack=tech_stack,
            components=components,
            data_flow=data_flow,
            api_design=api_design,
        )

    def _select_tech_stack(self, analysis: AnalysisResult) -> TechStack:
        """Select appropriate technology stack."""
        # Check for explicit language constraints
        if "language" in analysis.constraints:
            language = analysis.constraints["language"].lower()

            # Go language stacks
            if "go" in language or "golang" in language:
                return self.GO_STACKS.get(
                    analysis.project_type,
                    self.GO_STACKS[ProjectType.API],
                )

            # Java language stacks
            if "java" in language and "javascript" not in language:
                return self.JAVA_STACKS.get(
                    analysis.project_type,
                    self.JAVA_STACKS[ProjectType.API],
                )

            # JavaScript/TypeScript stacks (fallback to Python default with different language)
            if "javascript" in language or "typescript" in language or "node" in language:
                base = self.DEFAULT_STACKS.get(
                    analysis.project_type,
                    self.DEFAULT_STACKS[ProjectType.API],
                )
                base.language = "JavaScript/TypeScript"
                if analysis.project_type in (ProjectType.API, ProjectType.WEB_APP):
                    base.backend_framework = "Express.js/NestJS"
                return base

            # Python language stacks (default)
            if "python" in language:
                base = self.DEFAULT_STACKS.get(
                    analysis.project_type,
                    self.DEFAULT_STACKS[ProjectType.API],
                )
                base.language = "Python"
                return base

        # Return default for project type
        return self.DEFAULT_STACKS.get(
            analysis.project_type,
            self.DEFAULT_STACKS[ProjectType.API],
        )

    def _design_components(
        self, analysis: AnalysisResult, tech_stack: TechStack
    ) -> list[Component]:
        """Design architectural components."""
        components = []

        # Core service component
        components.append(Component(
            name="API Service",
            type=ComponentType.SERVICE,
            technology=tech_stack.backend_framework,
            responsibility="Handle business logic and request processing",
            interfaces=["HTTP REST API", "WebSocket (if needed)"],
        ))

        # Database if needed
        if any(f in analysis.core_features for f in ["database", "authentication", "storage"]):
            components.append(Component(
                name="Data Store",
                type=ComponentType.DATABASE,
                technology=tech_stack.database,
                responsibility="Persist application data and user information",
                interfaces=["SQL/NoSQL queries", "ORM interface"],
            ))

        # Cache for performance
        if tech_stack.cache:
            components.append(Component(
                name="Cache Layer",
                type=ComponentType.CACHE,
                technology=tech_stack.cache,
                responsibility="Cache frequently accessed data for performance",
                interfaces=["Key-value GET/SET"],
            ))

        # Frontend for web apps
        if analysis.project_type == ProjectType.WEB_APP and tech_stack.frontend:
            components.append(Component(
                name="Frontend Application",
                type=ComponentType.FRONTEND,
                technology=tech_stack.frontend,
                responsibility="User interface and client-side logic",
                interfaces=["HTTP API", "WebSocket"],
            ))

        # Message broker for microservices
        if analysis.project_type == ProjectType.MICROSERVICE:
            components.append(Component(
                name="Message Broker",
                type=ComponentType.MESSAGE_BROKER,
                technology="RabbitMQ/Kafka",
                responsibility="Inter-service communication and event streaming",
                interfaces=["AMQP", "Kafka Protocol"],
            ))
            components.append(Component(
                name="API Gateway",
                type=ComponentType.API_GATEWAY,
                technology="Kong/APISIX",
                responsibility="Request routing, rate limiting, and authentication",
                interfaces=["HTTP/HTTPS", "gRPC"],
            ))

        # Monitoring for complex systems
        if analysis.project_type in (ProjectType.MICROSERVICE, ProjectType.DATA_PIPELINE, ProjectType.WEB_APP):
            components.append(Component(
                name="Monitoring System",
                type=ComponentType.MONITORING,
                technology="Prometheus/Grafana",
                responsibility="System metrics, logging, and alerting",
                interfaces=["Prometheus metrics", "Log aggregation"],
            ))

        # Auth service if authentication is needed
        if "authentication" in analysis.core_features + analysis.implied_features:
            components.append(Component(
                name="Auth Service",
                type=ComponentType.AUTH_SERVICE,
                technology="OAuth2/OIDC",
                responsibility="User authentication and authorization",
                interfaces=["OAuth2", "JWT", "OIDC"],
            ))

        return components

    def _describe_data_flow(
        self, analysis: AnalysisResult, components: list[Component]
    ) -> str:
        """Describe the data flow through the system."""
        flows = []

        if analysis.project_type == ProjectType.API:
            flows = [
                "1. Client -> API Gateway: HTTP Request",
                "2. API Gateway -> Service: Route to appropriate handler",
                "3. Service -> Cache: Check for cached data",
                "4. Service -> Database: Query/Update data if cache miss",
                "5. Service -> Client: HTTP Response",
            ]
        elif analysis.project_type == ProjectType.WEB_APP:
            flows = [
                "1. User -> Frontend: User interaction",
                "2. Frontend -> API: HTTP Request",
                "3. API -> Cache/Database: Data operations",
                "4. API -> Frontend: JSON Response",
                "5. Frontend: Update UI",
            ]
        elif analysis.project_type == ProjectType.CLI:
            flows = [
                "1. User -> CLI: Command invocation",
                "2. CLI -> Core Logic: Parse and execute",
                "3. Core Logic -> Database: Read/Write (if needed)",
                "4. CLI -> User: Display results",
            ]
        elif analysis.project_type == ProjectType.MICROSERVICE:
            flows = [
                "1. Client -> API Gateway: Request routing",
                "2. API Gateway -> Service Mesh: Load balancing",
                "3. Service A -> Service B: Inter-service communication",
                "4. Services -> Message Queue: Async processing",
                "5. Services -> Database: Data persistence",
                "6. Services -> Client: Aggregated response",
            ]
        elif analysis.project_type == ProjectType.DESKTOP:
            flows = [
                "1. User -> Desktop UI: User interaction",
                "2. UI Layer -> Business Logic: Process request",
                "3. Business Logic -> Local Storage: Read/Write data",
                "4. Business Logic -> External API: Network requests (if needed)",
                "5. UI Layer: Update display",
            ]
        elif analysis.project_type == ProjectType.DATA_PIPELINE:
            flows = [
                "1. Data Source -> Ingestion: Extract data",
                "2. Ingestion -> Transformation: Clean and transform",
                "3. Transformation -> Validation: Data quality checks",
                "4. Validation -> Loading: Load to destination",
                "5. Loading -> Data Warehouse: Persist results",
            ]
        else:
            flows = [
                "1. External Input -> Application Core",
                "2. Core -> Business Logic Processing",
                "3. Core -> External Output / Storage",
            ]

        return "\n".join(flows)

    def _design_api(self, analysis: AnalysisResult) -> str:
        """Design API structure if applicable."""
        endpoints = [
            "GET /health - Health check",
            "GET /api/v1/resources - List resources",
            "POST /api/v1/resources - Create resource",
            "GET /api/v1/resources/{id} - Get resource details",
            "PUT /api/v1/resources/{id} - Update resource",
            "DELETE /api/v1/resources/{id} - Delete resource",
        ]

        if "authentication" in analysis.core_features:
            endpoints.extend([
                "POST /api/v1/auth/register - User registration",
                "POST /api/v1/auth/login - User login",
                "POST /api/v1/auth/logout - User logout",
                "GET /api/v1/auth/me - Get current user",
            ])

        return "\n".join(endpoints)
