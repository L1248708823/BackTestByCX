# Backend（FastAPI）

更新时间：2026-02-23

## 1. 模块目标

1. 提供回测系统后端 API 骨架。
2. 固化“路由层不写业务逻辑”的分层约束。
3. 为后续接入策略引擎、数据源适配器、实验模块预留扩展点。

## 2. 当前已实现（骨架）

1. FastAPI 入口：`app/main.py`
2. v1 路由聚合：`app/api/v1/router.py`
3. 健康检查接口：`GET /api/v1/health`
4. 回测占位接口：`POST /api/v1/backtests/run`
5. Pydantic 请求/响应模型：`app/schemas/backtest.py`
6. Service 分层示例：`app/services/backtest_service.py`
7. 基础测试：`tests/test_health.py`

## 3. 目录结构

```text
backend/
  app/
    main.py
    core/
      config.py
    api/
      deps.py
      v1/
        router.py
        health.py
        backtest.py
    schemas/
      common.py
      backtest.py
    services/
      backtest_service.py
  tests/
    test_health.py
  requirements.txt
  requirements-dev.txt
  pyproject.toml
  .env.example
```

## 4. Python 版本约束

1. 统一基线：`Python 3.12`。
2. `pyproject.toml` 已写 `requires-python = ">=3.12,<3.13"`。

## 5. 你在 Windows 需要执行的命令

请以 `docs/manual-operations-playbook.md` 的模块 B 为准。

## 6. 下一步（模块 B.1 之后）

1. 引入真实数据源适配接口（AkShare Provider）。
2. 把 `BacktestService` 的占位逻辑替换为真实策略引擎调用。
3. 增加回测结果持久化与 run_id 查询接口。
