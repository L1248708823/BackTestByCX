# 单次回测接口契约冻结说明

## 1. 目标

本文用于冻结 `POST /api/v1/backtests/run` 的唯一口径，解决当前 PRD、技术设计文档和后端骨架之间字段不一致的问题。

本次冻结遵循两个原则：

1. 只保留一套字段命名，不做页面层或接口层双轨兼容。
2. 先为 MVP 提供足够稳定的契约，再在后续阶段替换占位实现。

## 2. 当前发现的问题

冻结前存在这些冲突：

1. PRD 使用 `invest_amount / frequency / cost_model` 表达请求参数。
2. 后端骨架使用 `initial_capital / periodic_investment / investment_day`。
3. 响应中缺少 `input_snapshot / engine_version / metric_definition_version`。
4. 错误结构没有统一，当前主要依赖 FastAPI 默认 422 响应。

这会直接导致前后端各自理解不同字段，后续很容易写出兼容兜底代码。

## 3. 冻结后的请求结构

接口：`POST /api/v1/backtests/run`

请求体字段：

1. `symbol`
   - ETF 代码，例如 `510300`
2. `start_date`
   - 回测开始日期，格式 `YYYY-MM-DD`
3. `end_date`
   - 回测结束日期，格式 `YYYY-MM-DD`
4. `strategy_id`
   - 策略标识，MVP 固定为 `dca`
5. `initial_capital`
   - 初始现金，单位 CNY
6. `periodic_investment_amount`
   - 每次定投金额，单位 CNY
7. `investment_frequency`
   - `weekly` 或 `monthly`
8. `monthly_investment_day`
   - 当频率为 `monthly` 时必填，取值 `1-28`
9. `weekly_investment_weekday`
   - 当频率为 `weekly` 时必填，取值 `1-5`
10. `cost_model`
   - 成本模型配置

字段补充约定：

1. `strategy_id`
   - 当前 MVP 默认使用 `dca`
   - 该字段保留不是兼容代码，而是明确的策略入口字段
   - 前端和后端都只维护这一套策略入口命名，不允许再出现 `strategy_name` 等平行字段
2. `initial_capital`
   - 表示回测开始时账户已有现金
   - 单位固定为人民币元
3. `periodic_investment_amount`
   - 表示每次定投实际投入金额
   - 单位固定为人民币元
4. `investment_frequency`
   - 仅允许 `weekly` 或 `monthly`
   - 不允许出现第三种频率字符串占位
5. `monthly_investment_day`
   - 仅在 `investment_frequency=monthly` 时生效
   - 当前限制在 `1-28`，避免月末跨月复杂度
6. `weekly_investment_weekday`
   - 仅在 `investment_frequency=weekly` 时生效
   - 当前限制在 `1-5`，对应周一到周五
7. `cost_model.slippage_rate`
   - 当前为保留字段
   - 默认值为 `0`
   - 后续真实回测引擎接入时直接沿用该字段，不再新增第二套滑点字段

成本模型当前冻结字段：

1. `enabled`
2. `commission_rate`
3. `min_commission`
4. `slippage_rate`

说明：

1. `monthly_investment_day` 与 `weekly_investment_weekday` 互斥。
2. `start_date` 不允许晚于 `end_date`。
3. 当前不再使用 `periodic_investment`、`investment_day` 这些旧字段名。

## 4. 冻结后的成功响应结构

成功响应字段：

1. `run_id`
2. `request_id`
3. `strategy_id`
4. `engine_version`
5. `metric_definition_version`
6. `input_snapshot`
7. `summary`
8. `nav_series`
9. `drawdown_series`
10. `capital_curve`
11. `records`
12. `message`

其中：

1. `input_snapshot` 是请求参数快照，用于可复现性和导出。
2. `summary` 是结果页指标卡的唯一来源。
3. `nav_series`、`drawdown_series`、`capital_curve` 是图表层直接消费的数据。
4. `records` 是表格和导出层直接消费的数据。
5. `run_id` 是运行结果标识，用于后续结果查询和持久化铺路。
6. `request_id` 是请求追踪标识，用于日志排查和错误定位。
7. `engine_version` 与 `metric_definition_version` 必须和结果一起返回，不能只存在于后端内部。

## 5. 冻结后的错误结构

统一错误结构：

1. `code`
2. `message`
3. `details`
4. `request_id`

当前已覆盖：

1. 请求体验证错误：`validation_error`
2. HTTP 异常：`http_error`

## 6. 本次冻结的意义

冻结完成后，单次回测接口已经具备三个能力：

1. 前端可以直接围绕唯一字段口径开发参数页和结果页。
2. 后端可以在不改 API 形状的前提下，把占位逻辑替换成真实回测引擎。
3. AI 报告和随机实验后续也可以基于同一套基础结果结构继续扩展。

## 7. 后续紧接动作

本次只冻结单次回测契约，不处理以下内容：

1. 随机实验接口契约
2. AI 报告接口契约
3. 真实回测引擎实现
4. 数据源适配器实现

下一步应继续冻结：

1. `POST /api/experiments/run`
2. `POST /api/reports/generate`
