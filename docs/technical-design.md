# 技术设计文档（MVP）

## 1. 文档目标

本文用于回答并固化以下关键工程问题：

1. AI 用什么模型、如何接入才可替换。
2. 系统如何支撑后续新增策略。
3. 哪些模块可复用、哪些不可复用。
4. 前后端分离怎么做。
5. 前后端是否放同一仓库。

本文是 `prd.md` 的技术实现补充，面向工程落地。

## 2. 核心技术决策（先给结论）

1. 架构：前后端分离，后端 FastAPI，前端 React 独立 SPA。
2. 仓库：MVP 使用同一仓库（Monorepo 目录组织），后续可平滑拆分。
3. 策略扩展：采用“策略接口 + 策略注册中心 + 统一执行上下文”。
4. AI：采用“多 Provider 适配层”，默认接一个主模型 + 一个降级模型。
5. 结果模型：所有策略输出统一结果 Schema，避免前端和 AI 反复适配。

## 3. 系统分层设计

## 3.1 后端分层

1. `api`：FastAPI 路由与请求校验。
2. `application`：任务编排，串联 data/engine/report。
3. `domain`：策略接口、回测核心模型、指标定义。
4. `infrastructure`：数据源适配、数据库、AI Provider、日志。

这四层的边界必须保持：`api` 不直接依赖具体数据源，不直接写策略逻辑。

## 3.2 前端分层

1. `pages`：参数页、结果页、实验页。
2. `features`：回测配置、结果图表、实验统计、报告展示。
3. `services`：调用后端 API 的薄层封装。
4. `types`：与后端契约同步的类型定义。

前端禁止自行重算核心指标，所有核心指标以后端为准。
前端使用 React + TypeScript，采用函数组件与 Hooks。

## 3.3 注释与文档化约束（强制）

1. 所有非极简文件必须在文件头写用途说明。
2. 所有非极简函数必须有注释，至少包含作用、入参、出参。
3. 核心模型字段必须补充语义说明；明显通用字段可省略。
4. API 层请求/响应模型字段必须写明业务含义。
5. 复杂逻辑必须补“为什么这样做”说明，避免仅描述“做了什么”。

## 4. AI 模型选型与接入方案

## 4.1 选型原则

1. 第一优先：输出稳定且结构可控。
2. 第二优先：成本可接受（支持大量试验后批量生成报告）。
3. 第三优先：可替换（避免绑死某一家模型平台）。

## 4.2 首版建议

1. 主模型：通用高质量文本模型（用于完整长报告）。
2. 降级模型：更低成本模型（用于失败兜底或批量低优先级报告）。
3. 严格约束：MVP 中 AI 只读取内部结构化结果，不读取外部新闻与实时检索。

说明：这里故意不把模型名写死到代码，改为配置项 `MODEL_PRIMARY` / `MODEL_FALLBACK`，避免后续换模型需要改业务逻辑。

## 4.3 AI 适配接口（建议）

```python
class ReportLLMProvider(Protocol):
    def generate_report(self, prompt: str, temperature: float = 0.2) -> str: ...
```

```python
class ReportService:
    def __init__(self, provider: ReportLLMProvider): ...
    def build_prompt(self, payload: ReportPayload) -> str: ...
    def generate(self, payload: ReportPayload) -> ReportResult: ...
```

## 4.4 为什么这样设计

1. 可替换：切换模型只改 Provider，不影响业务层。
2. 可测试：可以用 FakeProvider 做稳定测试。
3. 可控：Prompt 模板和输出清洗集中管理。

## 5. 策略扩展架构

## 5.1 策略接口定义（关键）

```python
class Strategy(Protocol):
    name: str
    version: str
    def validate_params(self, params: dict) -> None: ...
    def on_bar(self, ctx: "StrategyContext") -> "StrategySignal": ...
```

`StrategyContext` 最少包含：

1. 当前时间与行情切片。
2. 当前持仓与现金状态。
3. 回测配置（成本模型、频率规则）。

`StrategySignal` 统一为标准动作：

1. `BUY`
2. `SELL`
3. `HOLD`

## 5.2 策略注册中心

通过注册中心管理策略，避免散落 `if/else`：

1. `strategy_registry.register("dca", DcaStrategy)`
2. `strategy_registry.create(name, params)`

新增策略时只做三件事：

1. 新增策略实现类。
2. 在注册中心注册。
3. 补充参数校验和测试样例。

## 5.3 扩展生命周期

1. MVP：仅 `dca`。
2. V2：新增 `ma_rotation` 等策略，不影响 API 主结构。
3. V3：若策略增多，再引入策略元数据中心（参数表单可动态生成）。

## 6. 复用边界：哪些能复用，哪些不能复用

## 6.1 可复用（应沉淀为公共能力）

1. 数据标准化模型（OHLCV + 交易日对齐）。
2. 成本计算模块（佣金/税费/最低费用）。
3. 指标计算模块（收益、回撤、波动、夏普）。
4. 回测结果 Schema 与导出能力。
5. 图表组件（净值、回撤、分布图）。
6. AI 报告模板框架（章节骨架可复用）。

## 6.2 不建议复用（保持策略或场景隔离）

1. 策略内部决策逻辑（不同策略强耦合，不要抽成“大一统规则函数”）。
2. 策略参数解释文案（每个策略语义不同）。
3. 面试展示专用页面动效（业务价值低，避免污染核心模块）。

结论：复用“基础设施和结果结构”，隔离“策略决策细节”。

## 7. 前后端分离落地方案

## 7.1 通信方式

1. REST API（MVP 足够）。
2. 返回统一 JSON 结构，包含 `request_id` 与 `engine_version`。
3. 前端通过 `services` 调用，不在组件内直接拼接 URL。
4. 前端技术栈固定为 React + TypeScript（MVP 阶段不切换框架）。

## 7.2 接口契约管理

1. 后端导出 OpenAPI。
2. 前端基于 OpenAPI 生成或维护类型定义。
3. 契约变更必须版本化（至少记录破坏性变更）。

## 7.3 本地开发联调

1. 前端 dev server 与后端本地服务分开启动。
2. 前端通过代理转发 `/api` 到后端，避免 CORS 噪音。

## 8. 仓库组织：同仓库还是分仓库

## 8.1 MVP 建议：同仓库（Monorepo 目录）

建议目录：

```text
project-root/
  backend/
  frontend/
  docs/
  localDoc/
```

原因：

1. 你是单人开发，协作成本低，同仓库效率更高。
2. PRD/技术文档/代码同步演进更容易。
3. 面试展示时更直观，避免多仓库跳转。

## 8.2 何时拆分为多仓库

满足以下任一条件再拆：

1. 前后端发布节奏严重不同。
2. 前端团队和后端团队分离。
3. 需要独立权限控制和流水线隔离。

结论：当前阶段不拆仓库，先保证交付速度与一致性。

## 9. 配置与环境管理

建议使用 `.env` 管理关键配置：

1. `DATA_PROVIDER=akshare`
2. `MODEL_PRIMARY=<provider/model-id>`
3. `MODEL_FALLBACK=<provider/model-id>`
4. `LLM_API_BASE`
5. `LLM_API_KEY`
6. `RISK_FREE_RATE`

原则：配置可变，代码不写死。

## 10. 风险点与规避策略

1. 风险：过早支持太多策略导致架构失控。  
   规避：先把接口抽象做好，策略数量保持最小。
2. 风险：AI 报告不稳定，面试演示翻车。  
   规避：固定报告结构 + 降级模型 + 可重试。
3. 风险：前端和后端字段漂移。  
   规避：OpenAPI 契约驱动 + 类型同步。
4. 风险：为了复用而过度抽象。  
   规避：只抽象已出现 2 次以上的稳定模式。

## 11. 下一步实施清单（技术文档之后）

1. 搭建目录骨架（`backend/`、`frontend/`、`docs/`）。
2. 定义后端核心类型与策略接口。
3. 先实现 `dca` 策略贯通单次回测。
4. 打通前端参数页 -> 回测结果页。
5. 再叠加随机实验与 AI 报告。
