# 依赖清单（Windows 手动安装版）

更新时间：2026-02-22

## 1. 说明

1. 你在 Windows 环境执行安装，助手无法代替你本机安装依赖。
2. 本清单按 MVP 最小可用原则整理，避免一次性引入过多库。
3. 版本策略建议使用“主版本锁定 + 小版本跟随”。

## 2. 前端依赖（React）

## 2.1 生产依赖

- `react`
- `react-dom`
- `react-router-dom`
- `@tanstack/react-query`
- `axios`
- `zod`
- `react-hook-form`
- `@hookform/resolvers`
- `echarts`
- `echarts-for-react`
- `dayjs`

## 2.2 开发依赖

- `typescript`
- `vite`
- `@vitejs/plugin-react`
- `@types/react`
- `@types/react-dom`
- `eslint`
- `@typescript-eslint/parser`
- `@typescript-eslint/eslint-plugin`
- `eslint-plugin-react-hooks`
- `eslint-plugin-react-refresh`
- `prettier`
- `eslint-config-prettier`
- `vitest`
- `@testing-library/react`
- `@testing-library/jest-dom`
- `@testing-library/user-event`
- `msw`

## 3. 后端依赖（FastAPI）

## 3.1 生产依赖

- `fastapi`
- `uvicorn[standard]`
- `pydantic`
- `pydantic-settings`
- `sqlalchemy`
- `alembic`
- `akshare`
- `pandas`
- `numpy`
- `httpx`
- `tenacity`
- `python-dotenv`
- `openai`

## 3.2 开发依赖

- `pytest`
- `pytest-asyncio`
- `pytest-cov`
- `respx`
- `ruff`
- `mypy`

## 4. IDE 插件（推荐）

- `ESLint`
- `Prettier - Code formatter`
- `Python`
- `Pylance`
- `Ruff`
- `SQLite Viewer`
- `REST Client` 或 `Thunder Client`

## 5. 维护规则（必须执行）

1. 每次新增/删除依赖后，必须同步更新本文件。
2. 依赖变更需在 `localDoc/TODO.md` 记录“日期 + 模块 + 文件”。
3. 若存在破坏性升级（主版本变更），必须补充迁移说明。

