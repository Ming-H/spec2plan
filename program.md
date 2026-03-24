# Spec2Plan - 项目规范文档

## 项目概述

**项目名称**: Spec2Plan

**一句话描述**: 将自然语言需求描述转化为结构化实现计划的工具

**核心价值**: 开发者常常面对模糊的需求描述，Spec2Plan 帮助将需求快速转化为可执行的技术方案，包含架构设计、技术选型、任务拆解和验收标准。

## 功能规范

### 输入
- 自然语言需求描述（一句话或多段落）
- 可选：额外约束条件（如技术栈偏好、预算、时间限制）

### 输出
完整的 Markdown 格式实现计划，包含：

1. **需求分析**
   - 核心功能提取
   - 隐含需求推断
   - 约束条件识别

2. **技术选型**
   - 后端框架推荐
   - 前端技术栈
   - 数据库选择
   - 基础设施/部署方案
   - 每项选型的理由说明

3. **架构设计**
   - 系统分层描述
   - 核心模块划分
   - 数据流向说明
   - 关键接口定义

4. **实现计划**
   - 分阶段任务列表
   - 每个任务的：
     - 具体执行步骤
     - 预估工作量
     - 验收标准
     - 依赖关系

5. **风险识别**
   - 技术风险
   - 业务风险
   - 建议缓解方案

## 技术架构

### 核心模块

```
spec2plan/
├── core/
│   ├── analyzer.py     # 需求分析器 - 解析输入需求
│   ├── architect.py    # 架构设计师 - 生成技术方案
│   ├── planner.py      # 计划生成器 - 拆解任务
│   └── generator.py    # 主生成器 - 协调整体流程
└── templates/
    └── plan.md.j2      # Jinja2 输出模板
```

### 模块职责

#### Analyzer (需求分析器)
- 使用规则和模式匹配提取关键信息
- 识别领域类型（Web应用、CLI工具、库等）
- 提取功能关键词
- 推断隐含需求

#### Architect (架构设计师)
- 基于需求领域推荐技术栈
- 生成系统架构描述
- 定义核心组件和接口

#### Planner (计划生成器)
- 将架构设计分解为开发任务
- 建立任务依赖关系
- 定义验收标准

#### Generator (主生成器)
- 协调各模块执行
- 使用模板渲染最终输出
- 处理错误和异常

### 技术栈

- **语言**: Python 3.11+
- **模板引擎**: Jinja2
- **配置管理**: TOML (pyproject.toml)
- **测试**: pytest
- **代码质量**: ruff, mypy

## API 设计

### 主要接口

```python
class Spec2Plan:
    def generate(self, requirement: str, constraints: dict | None = None) -> str:
        """生成实现计划"""
        pass
```

### 使用示例

```python
from spec2plan import Spec2Plan

s2p = Spec2Plan()
plan = s2p.generate("Build a RESTful blog API with user authentication")
print(plan)
```

## 开发里程碑

### Phase 1: 核心框架
- [x] 项目结构搭建
- [x] Analyzer 基础实现（关键词提取）
- [x] Architect 基础实现（规则-based 推荐）
- [x] Planner 基础实现（简单任务拆解）
- [x] Generator 基础实现 + Jinja2 模板

### Phase 2: 功能增强
- [x] 需求分类器（Web/API/CLI/Library等）
- [x] 技术栈数据库扩展
- [x] 任务依赖关系建模
- [x] 风险识别模块

### Phase 3: 质量提升
- [x] 示例完善（3个不同场景：博客API、CLI工具、Web仪表板）
- [x] 单元测试覆盖 79% (目标 >60%)
- [x] 文档完善 (README + program.md + PROJECT.md)
- [x] CLI 工具封装

## 验收标准

1. [x] 可以从简单需求生成合理计划
2. [x] 生成的计划结构清晰、可读性强
3. [x] 技术选型有明确依据说明
4. [x] 至少提供3个可运行的示例
5. [x] 单元测试覆盖率 >60%

## 项目状态

- 创建日期: 2026-03-24
- 当前版本: 0.1.0
- 开发模式: AutoResearch
- 状态: **已完成** (Phase 1, 2, 3 完全实现)

## CLI 工具

```bash
# 安装
pip install -e .

# 使用
spec2plan "Build a RESTful blog API"

# 带选项
spec2plan -l python -o plan.md "Build an API"
```

## 项目目录

```
spec2plan/
├── program.md          # 本规范文档
├── README.md           # 用户文档
├── pyproject.toml      # 项目配置
├── spec2plan/
│   ├── __init__.py     # 主入口: Spec2Plan 类
│   ├── core/
│   │   ├── analyzer.py   # 需求分析器
│   │   ├── architect.py  # 架构设计师
│   │   ├── planner.py    # 计划生成器
│   │   └── generator.py  # 主生成器
│   └── templates/
│       ├── plan.md.j2    # Jinja2 模板
│       └── plan_md_j2.py # 备用模板
├── examples/
│   ├── blog_system.py    # 博客 API 示例
│   ├── cli_tool.py       # CLI 工具示例
│   └── web_dashboard.py  # Web 仪表板示例
└── tests/
    ├── test_analyzer.py  # 分析器测试
    └── test_generator.py # 生成器测试
```
