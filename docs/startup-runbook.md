# 启动与联调手册（Windows 执行）

更新时间：2026-02-23

## 1. 目标

1. 统一前后端启动流程，避免“我这边能跑你那边跑不起来”。
2. 统一联调入口和验证步骤。
3. 作为后续持续维护的运行基线文档。

## 2. 启动前检查

1. 已完成 `docs/install-guide-windows.md` 的安装步骤。
2. 已查看 `docs/manual-operations-playbook.md` 并按台账执行人工命令。
3. `frontend/` 和 `backend/` 目录已初始化。
4. 后端 `.env` 已配置。
5. 前端构建校验通过：`pnpm --filter frontend build`。

## 3. 后端启动（你执行）

1. 进入目录：`cd backend`
2. 校验版本：`py -3.12 --version`（必须为 Python 3.12）。
3. 激活环境（PowerShell）：`.venv\\Scripts\\Activate.ps1`
4. 启动服务：`uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
5. 健康检查：访问 `http://localhost:8000/api/v1/health`。
6. 文档检查：访问 `http://localhost:8000/api/v1/docs`，确认 OpenAPI 可打开。

## 4. 前端启动（你执行）

1. 进入目录：`cd frontend`
2. 启动服务：`pnpm dev --host --port 5173`
3. 页面检查：访问 `http://localhost:5173`。

## 5. 联调检查清单

1. 健康检查接口 `/api/v1/health` 返回 `status=ok`。
2. 单次回测接口 `/api/v1/backtests/run` 返回结构化结果。
3. OpenAPI 页面 `/api/v1/docs` 正常可访问。
4. 随机实验与 AI 报告接口暂未落地（后续模块再验证）。
5. 错误场景下前端能看到可执行提示（前端联调阶段验证）。

## 6. 测试命令（你执行）

1. 后端单元测试：`pytest`
2. 后端覆盖率：`pytest --cov`
3. 前端测试：`pnpm test`
4. 前端构建：`pnpm build`

## 7. 常见启动问题

1. 端口冲突：更换端口并同步前端代理配置。
2. CORS 报错：检查前端代理或后端跨域白名单。
3. API 404：确认前端请求前缀与后端路由一致。
4. AI 接口超时：先降级模型再重试，记录请求参数。
5. `Cannot find native binding`：按 `docs/manual-operations-playbook.md` 的 A1.F1~A1.F3 执行清理与重装。

## 8. 维护规则（必须执行）

1. 启动命令变化后，必须同步更新本手册。
2. 增加新服务（如 worker）时，补充对应启动章节。
3. 每次联调关键变更都写入 `localDoc/TODO.md`。
