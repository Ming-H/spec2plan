"""Requirement analyzer - extracts key information from natural language requirements."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from re import findall


class ProjectType(Enum):
    """Classification of project types."""

    WEB_APP = "web_app"
    API = "api"
    CLI = "cli"
    LIBRARY = "library"
    MOBILE = "mobile"
    DATA_PIPELINE = "data_pipeline"
    MICROSERVICE = "microservice"
    DESKTOP = "desktop"
    PLUGIN = "plugin"
    UNKNOWN = "unknown"


@dataclass
class AnalysisResult:
    """Result of requirement analysis."""

    raw_input: str
    project_type: ProjectType
    core_features: list[str]
    implied_features: list[str]
    constraints: dict[str, str]
    keywords: list[str] = field(default_factory=list)


class Analyzer:
    """Analyzes natural language requirements to extract structured information."""

    # Keywords that indicate different project types
    PROJECT_TYPE_KEYWORDS: dict[ProjectType, list[str]] = {
        ProjectType.WEB_APP: ["website", "web app", "web application", "dashboard", "admin panel"],
        ProjectType.API: ["api", "rest", "graphql", "backend", "service"],
        ProjectType.CLI: ["cli", "command line", "terminal tool", "script"],
        ProjectType.LIBRARY: ["library", "package", "sdk", "framework"],
        ProjectType.MOBILE: ["mobile app", "ios", "android", "app store"],
        ProjectType.DATA_PIPELINE: ["pipeline", "etl", "data processing", "batch job"],
        ProjectType.MICROSERVICE: ["microservice", "micro-service", "distributed", "service mesh"],
        ProjectType.DESKTOP: ["desktop app", "desktop application", "gui app", "electron", "qt"],
        ProjectType.PLUGIN: ["plugin", "extension", "add-on", "addon", "module"],
    }

    # Feature keywords
    FEATURE_KEYWORDS = {
        "authentication": ["auth", "login", "signup", "user", "authentication", "oauth", "jwt", "sso"],
        "database": ["database", "storage", "persist", "store data", "db", "sql", "nosql", "mongodb", "postgres"],
        "api": ["api", "endpoint", "rest", "graphql", "grpc", "swagger"],
        "frontend": ["ui", "frontend", "interface", "dashboard", "web", "react", "vue", "angular"],
        "realtime": ["realtime", "websocket", "live", "streaming", "socket", "push notification"],
        "search": ["search", "query", "filter", "elasticsearch", "full-text", "index"],
        "file_handling": ["upload", "download", "file", "attachment", "s3", "blob", "cdn"],
        "notifications": ["notification", "email", "alert", "notify", "sms", "push", "webhook"],
        "cron": ["schedule", "cron", "periodic", "batch", "job", "task queue", "celery"],
        "caching": ["cache", "redis", "memcached", "cdn", "lazy loading"],
        "logging": ["logging", "log", "monitoring", "metrics", "observability", "tracing"],
        "payment": ["payment", "stripe", "paypal", "checkout", "billing", "subscription"],
        "analytics": ["analytics", "tracking", "metrics", "reporting", "dashboard", "charts"],
        "chat": ["chat", "messaging", "conversation", "im", "instant message"],
        "export": ["export", "import", "csv", "excel", "pdf", "report"],
        "i18n": ["i18n", "internationalization", "localization", "multi-language", "translation"],
        "rate_limiting": ["rate limit", "throttle", "quota", "api key"],
        "encryption": ["encryption", "decrypt", "cryptographic", "security", "tls", "ssl"],
    }

    def analyze(self, requirement: str) -> AnalysisResult:
        """Analyze a requirement description.

        Args:
            requirement: Natural language requirement description

        Returns:
            AnalysisResult containing extracted information
        """
        requirement_lower = requirement.lower()

        # Detect project type
        project_type = self._detect_project_type(requirement_lower)

        # Extract features
        core_features = self._extract_features(requirement_lower)

        # Infer implied features
        implied_features = self._infer_implied_features(project_type, core_features)

        # Extract constraints
        constraints = self._extract_constraints(requirement)

        # Extract keywords for context
        keywords = self._extract_keywords(requirement)

        return AnalysisResult(
            raw_input=requirement,
            project_type=project_type,
            core_features=core_features,
            implied_features=implied_features,
            constraints=constraints,
            keywords=keywords,
        )

    def _detect_project_type(self, text: str) -> ProjectType:
        """Detect the type of project from the requirement text."""
        for project_type, keywords in self.PROJECT_TYPE_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return project_type
        return ProjectType.UNKNOWN

    def _extract_features(self, text: str) -> list[str]:
        """Extract explicitly mentioned features."""
        features = []
        for feature, keywords in self.FEATURE_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                features.append(feature)
        return features

    def _infer_implied_features(
        self, project_type: ProjectType, core_features: list[str]
    ) -> list[str]:
        """Infer features that are likely needed but not explicitly mentioned."""
        implied = []

        # Common implications
        if "authentication" in core_features:
            implied.extend(["user_management", "session_handling"])

        if project_type == ProjectType.WEB_APP:
            if "authentication" not in core_features:
                implied.append("authentication")
            if "database" not in core_features:
                implied.append("database")

        if project_type == ProjectType.API:
            implied.extend(["api_documentation", "error_handling"])

        # Remove duplicates while preserving order
        seen = set()
        result = []
        for f in implied:
            if f not in seen and f not in core_features:
                result.append(f)
                seen.add(f)

        return result

    def _extract_constraints(self, text: str) -> dict[str, str]:
        """Extract explicit constraints mentioned in the requirement."""
        constraints = {}
        text_lower = text.lower()

        # Language constraints
        if "python" in text_lower:
            constraints["language"] = "python"
        elif "golang" in text_lower or "go lang" in text_lower or " in go" in text_lower:
            constraints["language"] = "go"
        elif "java" in text_lower and "javascript" not in text_lower:
            constraints["language"] = "java"
        elif "javascript" in text_lower or "typescript" in text_lower or "node" in text_lower:
            constraints["language"] = "javascript/typescript"
        elif "rust" in text_lower:
            constraints["language"] = "rust"
        elif "kotlin" in text_lower:
            constraints["language"] = "kotlin"
        elif "c#" in text_lower or "csharp" in text_lower or ".net" in text_lower:
            constraints["language"] = "csharp"

        # Performance constraint
        if "fast" in text_lower or "performance" in text_lower or "high performance" in text_lower:
            constraints["performance"] = "high"

        # Complexity constraint
        if "simple" in text_lower or "minimal" in text_lower or "lightweight" in text_lower:
            constraints["complexity"] = "minimal"

        # Scalability constraint
        if "scalable" in text_lower or "scale" in text_lower:
            constraints["scalability"] = "high"

        return constraints

    def _extract_keywords(self, text: str) -> list[str]:
        """Extract significant nouns/keywords from the text."""
        # Simple extraction: words > 4 chars
        words = findall(r"\b[a-z]{4,}\b", text.lower())

        # Filter common words
        stopwords = {
            "with", "that", "this", "from", "have", "been", "were", "than",
            "when", "what", "where", "will", "your", "about", "would", "there",
        }

        return [w for w in words if w not in stopwords]
