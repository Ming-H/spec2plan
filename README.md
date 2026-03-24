# Spec2Plan

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

### Transform Natural Language Requirements into Structured Implementation Plans

Spec2Plan is a powerful tool that converts natural language requirement descriptions into comprehensive, structured implementation plans. It analyzes requirements, recommends technology stacks, designs architecture, and breaks down tasks into actionable steps.

### Features

- **Requirement Analysis**: Extract core features, constraints, and implied requirements
- **Technology Selection**: Intelligent tech stack recommendations based on project type
- **Architecture Design**: Generate system architecture with components and data flow
- **Task Breakdown**: Decompose into prioritized, executable development tasks
- **Acceptance Criteria**: Define clear completion standards for each task
- **Risk Assessment**: Identify potential risks and mitigation strategies

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Spec2Plan                             │
│                       (Main Entry)                           │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       Generator                              │
│                  (Main Coordinator)                          │
└──────┬──────────────┬──────────────┬────────────────────────┘
       │              │              │
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Analyzer   │ │  Architect  │ │   Planner   │
│ (Requirement│ │ (Architecture│ │ (Task Plan) │
│  Analysis)  │ │   Designer) │ │             │
└─────────────┘ └─────────────┘ └─────────────┘
       │              │              │
       ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Output Template                          │
│                    (Markdown Plan)                           │
└─────────────────────────────────────────────────────────────┘
```

### Installation

```bash
pip install spec2plan
```

### Quick Start

```python
from spec2plan import Spec2Plan

# Create instance
s2p = Spec2Plan()

# Generate plan from natural language
plan = s2p.generate("Build a RESTful blog API with user authentication")

print(plan)
```

### CLI Usage

```bash
# Generate plan from requirement
spec2plan generate "Build a RESTful blog API with user authentication"

# From file
spec2plan generate --file requirements.txt

# With custom constraints
spec2plan generate "Build an API" --constraint language=python
```

### Output Structure

Generated plans include:

1. **Original Requirement**: The input requirement
2. **Requirement Analysis**:
   - Project Type (Web App, API, CLI, Library, etc.)
   - Core Features
   - Implied Features
3. **Technology Stack**: Recommended languages, frameworks, databases
4. **Architecture Design**:
   - Components
   - Data Flow
   - API Design
5. **Implementation Plan**:
   - Tasks grouped by phase (Setup, Foundation, Core, Integration, Testing, Deployment)
   - Dependencies between tasks
   - Estimated effort
6. **Risks and Mitigations**: Potential issues and solutions
7. **Next Steps**: Immediate actions to begin

### Supported Project Types

| Type | Description | Typical Stack |
|------|-------------|---------------|
| `WEB_APP` | Web applications | Python + FastAPI + React |
| `API` | REST/GraphQL APIs | Python + FastAPI + PostgreSQL |
| `CLI` | Command-line tools | Python + Click/Typer |
| `LIBRARY` | Libraries/SDKs | Python + setuptools |
| `MOBILE` | Mobile applications | React Native / Flutter |
| `DATA_PIPELINE` | Data processing | Python + Airflow + Spark |

### Feature Detection

Automatically identifies:
- Authentication systems
- Database requirements
- API endpoints
- Frontend needs
- Real-time features
- Search functionality
- File handling
- Notifications
- Scheduled tasks

### Examples

#### Blog API

```python
from spec2plan import Spec2Plan

s2p = Spec2Plan()
plan = s2p.generate(
    "Build a RESTful blog API with user authentication, "
    "post creation/editing, comments, and search functionality."
)
```

**Output highlights:**
- Project Type: API
- Tech Stack: FastAPI + PostgreSQL + Redis
- Tasks include: Auth system, Post CRUD, Comments, Search integration

#### CLI Tool

```python
plan = s2p.generate(
    "Create a CLI tool for managing TODO items with SQLite storage, "
    "supporting add, list, complete, and delete operations."
)
```

**Output highlights:**
- Project Type: CLI
- Tech Stack: Python + Click/Typer + SQLite
- Lightweight deployment approach

#### Web Dashboard

```python
plan = s2p.generate(
    "Build a real-time analytics dashboard web application with "
    "live data updates, user authentication, and export functionality."
)
```

**Output highlights:**
- Project Type: Web Application
- Tech Stack: FastAPI + PostgreSQL + Redis + React
- Frontend-backend separation architecture

### Project Structure

```
spec2plan/
├── spec2plan/
│   ├── __init__.py         # Main entry: Spec2Plan class
│   ├── cli.py              # Command-line interface
│   ├── core/
│   │   ├── analyzer.py     # Requirement analyzer
│   │   ├── architect.py    # Architecture designer
│   │   ├── planner.py      # Task planner
│   │   └── generator.py    # Main generator
│   └── templates/
│       └── plan.md.j2      # Jinja2 template
├── examples/
│   ├── blog_system.py      # Blog API example
│   ├── cli_tool.py         # CLI tool example
│   └── web_dashboard.py    # Web dashboard example
└── tests/                  # 339 tests
```

### Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=spec2plan

# Code linting
ruff check .
mypy spec2plan
```

### Test Coverage

- **339 tests** with **97% coverage**
- Comprehensive coverage of analyzer, architect, planner, and generator

### License

MIT

---

<a name="中文"></a>
## 中文

### 将自然语言需求转化为结构化实现计划

Spec2Plan 是一个强大的工具，能够将自然语言需求描述转化为全面、结构化的实现计划。它分析需求、推荐技术栈、设计架构，并将任务分解为可执行的步骤。

### 功能特性

- **需求分析**：提取核心功能、约束条件和隐含需求
- **技术选型**：基于项目类型的智能技术栈推荐
- **架构设计**：生成包含组件和数据流的系统架构
- **任务分解**：分解为优先级明确的可执行开发任务
- **验收标准**：为每个任务定义清晰的完成标准
- **风险评估**：识别潜在风险并提供缓解策略

### 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        Spec2Plan                             │
│                       (主入口)                                │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       Generator                              │
│                    (主生成器/协调器)                          │
└──────┬──────────────┬──────────────┬────────────────────────┘
       │              │              │
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Analyzer   │ │  Architect  │ │   Planner   │
│ (需求分析器) │ │(架构设计师)  │ │ (计划生成器) │
└─────────────┘ └─────────────┘ └─────────────┘
       │              │              │
       ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────┐
│                     输出模板                                  │
│                  (Markdown 计划)                             │
└─────────────────────────────────────────────────────────────┘
```

### 安装

```bash
pip install spec2plan
```

### 快速开始

```python
from spec2plan import Spec2Plan

# 创建实例
s2p = Spec2Plan()

# 从自然语言生成计划
plan = s2p.generate("构建一个带用户认证的 RESTful 博客 API")

print(plan)
```

### 命令行使用

```bash
# 从需求生成计划
spec2plan generate "构建一个带用户认证的 RESTful 博客 API"

# 从文件读取
spec2plan generate --file requirements.txt

# 带自定义约束
spec2plan generate "构建一个 API" --constraint language=python
```

### 输出结构

生成的计划包含：

1. **原始需求**：输入的需求描述
2. **需求分析**：
   - 项目类型（Web 应用、API、CLI、库等）
   - 核心功能
   - 隐含功能
3. **技术栈**：推荐的语言、框架、数据库
4. **架构设计**：
   - 组件说明
   - 数据流向
   - API 设计
5. **实施计划**：
   - 按阶段分组的任务（初始化、基础、核心、集成、测试、部署）
   - 任务依赖关系
   - 预估工作量
6. **风险与缓解**：潜在问题和解决方案
7. **下一步**：开始工作的即时行动

### 支持的项目类型

| 类型 | 描述 | 典型技术栈 |
|------|------|------------|
| `WEB_APP` | 网站应用 | Python + FastAPI + React |
| `API` | REST/GraphQL API | Python + FastAPI + PostgreSQL |
| `CLI` | 命令行工具 | Python + Click/Typer |
| `LIBRARY` | 库/SDK | Python + setuptools |
| `MOBILE` | 移动应用 | React Native / Flutter |
| `DATA_PIPELINE` | 数据处理 | Python + Airflow + Spark |

### 功能识别

自动识别：
- 认证系统
- 数据库需求
- API 端点
- 前端需求
- 实时功能
- 搜索功能
- 文件处理
- 通知系统
- 定时任务

### 示例

#### 博客 API

```python
from spec2plan import Spec2Plan

s2p = Spec2Plan()
plan = s2p.generate(
    "构建一个 RESTful 博客 API，包含用户认证、"
    "文章创建/编辑、评论和搜索功能。"
)
```

**输出要点：**
- 项目类型：API
- 技术栈：FastAPI + PostgreSQL + Redis
- 任务包含：认证系统、文章增删改查、评论、搜索集成

#### CLI 工具

```python
plan = s2p.generate(
    "创建一个管理 TODO 项目的 CLI 工具，使用 SQLite 存储，"
    "支持添加、列表、完成和删除操作。"
)
```

**输出要点：**
- 项目类型：CLI
- 技术栈：Python + Click/Typer + SQLite
- 轻量级部署方案

#### Web 仪表板

```python
plan = s2p.generate(
    "构建一个实时分析仪表板 Web 应用，"
    "包含实时数据更新、用户认证和导出功能。"
)
```

**输出要点：**
- 项目类型：Web 应用
- 技术栈：FastAPI + PostgreSQL + Redis + React
- 前后端分离架构

### 项目结构

```
spec2plan/
├── spec2plan/
│   ├── __init__.py         # 主入口：Spec2Plan 类
│   ├── cli.py              # 命令行接口
│   ├── core/
│   │   ├── analyzer.py     # 需求分析器
│   │   ├── architect.py    # 架构设计师
│   │   ├── planner.py      # 计划生成器
│   │   └── generator.py    # 主生成器
│   └── templates/
│       └── plan.md.j2      # Jinja2 模板
├── examples/
│   ├── blog_system.py      # 博客 API 示例
│   ├── cli_tool.py         # CLI 工具示例
│   └── web_dashboard.py    # Web 仪表板示例
└── tests/                  # 339 个测试
```

### 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 带覆盖率运行
pytest --cov=spec2plan

# 代码检查
ruff check .
mypy spec2plan
```

### 测试覆盖

- **339 个测试**，**97% 覆盖率**
- 全面覆盖分析器、架构师、计划器和生成器

### 许可证

MIT
