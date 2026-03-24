# Spec2Plan 项目完整文档

## 项目概述

**项目名称**: Spec2Plan

**版本**: 0.1.0

**一句话描述**: 将自然语言需求描述转化为结构化实现计划的工具

**核心价值**: 开发者常常面对模糊的需求描述，Spec2Plan 帮助将需求快速转化为可执行的技术方案，包含架构设计、技术选型、任务拆解和验收标准。

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        Spec2Plan                             │
│                       (主入口)                                │
└─────────────────────────────┬───────────────────────────────┘
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
│                   AnalysisResult                             │
│  - project_type (项目类型)                                   │
│  - core_features (核心功能)                                  │
│  - implied_features (隐含功能)                               │
│  - constraints (约束条件)                                    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                 ArchitectureDesign                           │
│  - tech_stack (技术栈)                                      │
│  - components (组件)                                        │
│  - data_flow (数据流)                                       │
│  - api_design (API设计)                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                ImplementationPlan                           │
│  - tasks (任务列表)                                         │
│  - risks (风险识别)                                         │
│  - next_steps (下一步)                                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Jinja2 Template                           │
│                  (Markdown输出模板)                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                      Markdown 输出
```

## 核心模块详细说明

### 1. Analyzer (需求分析器)

**文件**: `spec2plan/core/analyzer.py`

**职责**:
- 从自然语言需求中提取关键信息
- 识别项目类型（Web应用、API、CLI工具、库等）
- 提取核心功能关键词
- 推断隐含需求
- 识别约束条件

**主要方法**:
```python
def analyze(requirement: str) -> AnalysisResult
```

**支持的项目类型**:
- `WEB_APP`: 网站应用
- `API`: REST/GraphQL API
- `CLI`: 命令行工具
- `LIBRARY`: 库/SDK
- `MOBILE`: 移动应用
- `DATA_PIPELINE`: 数据处理管道
- `UNKNOWN`: 未知类型

**可识别的功能特征**:
- authentication (认证)
- database (数据库)
- api (API)
- frontend (前端)
- realtime (实时)
- search (搜索)
- file_handling (文件处理)
- notifications (通知)
- cron (定时任务)

### 2. Architect (架构设计师)

**文件**: `spec2plan/core/architect.py`

**职责**:
- 基于需求分析结果推荐技术栈
- 生成系统架构描述
- 定义核心组件和接口
- 描述数据流向

**主要方法**:
```python
def design(analysis: AnalysisResult) -> ArchitectureDesign
```

**技术栈推荐**:
| 项目类型 | 语言 | 后端框架 | 数据库 | 缓存 | 前端 | 部署 |
|---------|------|---------|--------|------|------|------|
| WEB_APP | Python | FastAPI | PostgreSQL | Redis | React+TS | Docker+CloudRun |
| API | Python | FastAPI | PostgreSQL | Redis | - | Docker+K8s |
| CLI | Python | Click/Typer | SQLite | - | - | PyPI |
| LIBRARY | Python | - | - | - | - | PyPI |

**组件类型**:
- SERVICE: 服务组件
- DATABASE: 数据库
- CACHE: 缓存
- QUEUE: 消息队列
- STORAGE: 存储
- FRONTEND: 前端
- GATEWAY: 网关

### 3. Planner (计划生成器)

**文件**: `spec2plan/core/planner.py`

**职责**:
- 将架构设计分解为开发任务
- 建立任务依赖关系
- 定义验收标准
- 识别项目风险

**主要方法**:
```python
def plan(analysis: AnalysisResult, architecture: ArchitectureDesign) -> ImplementationPlan
```

**任务阶段**:
1. SETUP: 项目初始化
2. FOUNDATION: 基础设施搭建
3. CORE_FEATURES: 核心功能实现
4. INTEGRATION: 集成优化
5. TESTING: 测试
6. DEPLOYMENT: 部署

**任务结构**:
- id: 任务编号 (T01, T02, ...)
- title: 任务标题
- phase: 所属阶段
- description: 任务描述
- steps: 具体执行步骤
- acceptance_criteria: 验收标准
- estimated_effort: 预估工作量
- dependencies: 依赖任务

### 4. Generator (主生成器)

**文件**: `spec2plan/core/generator.py`

**职责**:
- 协调各模块执行
- 使用模板渲染最终输出
- 处理错误和异常

**主要方法**:
```python
def generate(requirement: str, constraints: dict | None = None) -> str
```

## API文档

### 主入口类

```python
from spec2plan import Spec2Plan

# 创建实例
s2p = Spec2Plan()

# 生成计划
plan = s2p.generate(
    requirement="Build a RESTful blog API with user authentication",
    constraints={"language": "python"}  # 可选
)
```

### 核心模块API

```python
from spec2plan.core.analyzer import Analyzer
from spec2plan.core.architect import Architect
from spec2plan.core.planner import Planner
from spec2plan.core.generator import Generator

# 单独使用各模块
analyzer = Analyzer()
analysis = analyzer.analyze("Build an API")

architect = Architect()
architecture = architect.design(analysis)

planner = Planner()
plan = planner.plan(analysis, architecture)

# 或使用Generator协调
generator = Generator()
result = generator.generate("Build an API")
```

## 输出格式

生成的Markdown计划包含以下部分:

1. **Original Requirement**: 原始需求
2. **Requirement Analysis**: 需求分析
   - Project Type: 项目类型
   - Core Features: 核心功能
   - Implied Features: 隐含功能
3. **Technology Stack**: 技术栈
4. **Architecture**: 架构设计
   - Components: 组件说明
   - Data Flow: 数据流向
   - API Design: API设计（如适用）
5. **Implementation Plan**: 实施计划
   - 按阶段分组的任务列表
6. **Risks and Mitigations**: 风险与缓解措施
7. **Next Steps**: 下一步行动

## 使用示例

### 示例1: 博客API

```python
from spec2plan import Spec2Plan

s2p = Spec2Plan()
plan = s2p.generate(
    "Build a RESTful blog API with user authentication, "
    "post creation/editing, comments, and search functionality."
)
print(plan)
```

**输出要点**:
- 项目类型: API
- 技术栈: FastAPI + PostgreSQL + Redis
- 包含认证系统、缓存集成等任务

### 示例2: CLI工具

```python
from spec2plan import Spec2Plan

s2p = Spec2Plan()
plan = s2p.generate(
    "Create a CLI tool for managing TODO items with SQLite storage, "
    "supporting add, list, complete, and delete operations."
)
print(plan)
```

**输出要点**:
- 项目类型: CLI
- 技术栈: Python + Click/Typer + SQLite
- 轻量级部署方案

### 示例3: Web仪表板

```python
from spec2plan import Spec2Plan

s2p = Spec2Plan()
plan = s2p.generate(
    "Build a real-time analytics dashboard web application with "
    "live data updates, user authentication, and export functionality."
)
print(plan)
```

**输出要点**:
- 项目类型: Web应用
- 技术栈: FastAPI + PostgreSQL + Redis + React
- 包含前后端分离架构

## 开发状态

### Phase 1: 核心框架 ✅
- [x] 项目结构搭建
- [x] Analyzer 基础实现（关键词提取）
- [x] Architect 基础实现（规则推荐）
- [x] Planner 基础实现（任务拆解）
- [x] Generator 基础实现 + Jinja2 模板

### Phase 2: 功能增强 ✅
- [x] 需求分类器（Web/API/CLI/Library等）
- [x] 技术栈数据库扩展
- [x] 任务依赖关系建模
- [x] 风险识别模块

### Phase 3: 质量提升 ✅
- [x] 示例完善（3个不同场景）
- [x] 单元测试覆盖 77% (目标 >60%)
- [x] 文档完善 (README + program.md + PROJECT.md)
- [x] CLI 工具封装

## 测试

**测试覆盖**: 77%

**运行测试**:
```bash
cd /Users/z/Documents/work/spec2plan
pytest tests/ -v --cov=spec2plan
```

**测试文件**:
- `tests/test_analyzer.py`: 分析器测试
- `tests/test_generator.py`: 生成器测试

## 项目目录

```
spec2plan/
├── program.md          # 项目规范文档
├── PROJECT.md          # 项目完整文档 (本文件)
├── README.md           # 用户文档
├── pyproject.toml      # 项目配置
├── spec2plan/
│   ├── __init__.py     # 主入口: Spec2Plan 类
│   ├── core/
│   │   ├── __init__.py
│   │   ├── analyzer.py   # 需求分析器
│   │   ├── architect.py  # 架构设计师
│   │   ├── planner.py    # 计划生成器
│   │   └── generator.py  # 主生成器
│   └── templates/
│       ├── __init__.py
│       ├── plan.md.j2    # Jinja2 模板
│       └── plan_md_j2.py # 备用模板
├── examples/
│   ├── blog_system.py    # 博客 API 示例
│   ├── cli_tool.py       # CLI 工具示例
│   └── web_dashboard.py  # Web 仪表板示例
└── tests/
    ├── __init__.py
    ├── test_analyzer.py  # 分析器测试
    └── test_generator.py # 生成器测试
```

## 开发命令

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行示例
python examples/blog_system.py
python examples/cli_tool.py
python examples/web_dashboard.py

# 代码检查
ruff check .
mypy spec2plan

# 格式化代码
ruff format .
```

## TODO / 未来改进

1. **增强功能**
   - 支持更多编程语言的技术栈推荐
   - 添加AI辅助需求分析（集成LLM）
   - 支持自定义模板

2. **质量提升**
   - 提高测试覆盖率到90%+
   - 添加更多边缘情况测试
   - 性能优化

3. **用户体验**
   - CLI工具封装
   - 支持配置文件
   - 输出格式选择（Markdown/JSON/HTML）

4. **文档完善**
   - API文档生成
   - 贡献指南
   - 变更日志

## 许可证

MIT
