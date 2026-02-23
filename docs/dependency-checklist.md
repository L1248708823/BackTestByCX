# 依赖与插件清单（含选择理由）

更新时间：2026-02-23

## 1. 使用说明

1. 你在 Windows 手动安装，助手只提供清单与步骤。
2. 本文分为：`当前已装`、`必须补齐`、`后置引入`。
3. 目标是“够用可扩展”，避免一次装太多导致排错困难。

## 2. 当前前端状态（实际扫描）

已安装（`frontend/package.json`）：

1. `react` / `react-dom`
2. `vite` / `@vitejs/plugin-react`
3. `typescript` / `@types/react` / `@types/react-dom`
4. `eslint` 相关

已接入（本轮代码已完成）：

1. Tailwind 已接入 `frontend/vite.config.ts` 与 `frontend/src/index.css`。
2. 路由骨架已接入：`frontend/src/app/router.tsx`。
3. 服务端状态层已接入：`QueryClientProvider + ReactQueryDevtools`。
4. 默认 Vite Demo 示例已移除，替换为项目占位页面结构。

## 3. 前端架构决策（你关心的重点）

## 3.1 是否需要路由

结论：`需要`，现在就引入 `react-router-dom`。  
理由：

1. 你的产品天然多页面（参数页、结果页、实验页、报告页）。
2. 不做路由会导致页面状态难复用，后期拆分成本更高。
3. 路由是稳定基础能力，不属于过度设计。

## 3.2 是否需要状态管理

结论：分两层，不一次引入全局 store。  
理由与方案：

1. 服务端状态：`必须` 用 `@tanstack/react-query`。  
原因：接口请求缓存、重试、失效控制、加载状态统一。
2. 客户端全局状态：`暂不引入 Zustand/Redux`。  
原因：当前还没复杂跨页共享，先用组件状态 + URL 参数足够。
3. 触发引入全局 store 条件：  
至少出现 3 个页面共享同一复杂 UI 状态，且 props 传递明显失控。

## 3.3 表单与校验

结论：`react-hook-form + zod + @hookform/resolvers`。  
理由：

1. 回测参数表单复杂，手写校验维护成本高。
2. 类型与校验规则可复用，减少前后端参数不一致风险。

## 3.4 请求层与图表层

1. 请求层：`axios`（拦截器、超时、统一错误映射更直观）。
2. 图表层：`echarts + echarts-for-react`（回测曲线、分布图能力足够）。
3. 时间工具：`dayjs`（轻量且足够）。

## 4. 前端必须补齐依赖（模块 A.1）

安装命名提醒：

1. npm 包名区分大小写，必须使用小写包名（如 `zustand`）。
2. 不要把二选一方案写成一个包名（如 `Zustand/Redux` 会 404）。

## 4.1 生产依赖（你执行）

```bash
cd frontend
pnpm add react-router-dom @tanstack/react-query @tanstack/react-query-devtools axios zod react-hook-form @hookform/resolvers echarts echarts-for-react dayjs
```

## 4.2 开发依赖（你执行）

```bash
cd frontend
pnpm add -D tailwindcss @tailwindcss/vite prettier eslint-config-prettier vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event msw
```

## 4.3 Tailwind 接入检查（你执行）

1. `frontend/vite.config.ts` 含 `@tailwindcss/vite` 插件。
2. `frontend/src/index.css` 含 `@import "tailwindcss";`。

## 4.4 Vite 稳定版本校正（你执行）

背景：`vite@8 beta` 在 WSL + pnpm 场景可能触发 `rolldown` 原生绑定缺失。  
当前方案：已将项目改为 `vite@^7.1.11` 稳定线，避免该类环境问题。

```bash
pnpm install
pnpm --filter frontend build
```

如果仍报 native binding 相关错误，再执行：

```powershell
Remove-Item -Recurse -Force node_modules, frontend/node_modules
pnpm install
pnpm --filter frontend build
```

## 5. 前端后置依赖（先不装）

1. `zustand`：等出现真实跨页复杂本地状态再引入。
2. `@tanstack/react-table`：等明细表格交互复杂后再引入。
3. 组件库（如 `antd` / `mui`）：当前用 Tailwind 足够，避免体积和学习负担。

## 6. 后端依赖（FastAPI）

版本基线：

1. Python：`3.12`

当前骨架已落地（`backend/requirements.txt`）：

1. `fastapi`
2. `uvicorn[standard]`
3. `pydantic-settings`

后续能力扩展（按模块逐步引入，不一次性全装）：

## 6.1 生产依赖

1. `fastapi`
2. `uvicorn[standard]`
3. `pydantic`
4. `pydantic-settings`
5. `sqlalchemy`
6. `alembic`
7. `akshare`
8. `pandas`
9. `numpy`
10. `httpx`
11. `tenacity`
12. `python-dotenv`
13. `openai`

## 6.2 开发依赖

1. `pytest`
2. `pytest-asyncio`
3. `pytest-cov`
4. `respx`
5. `ruff`
6. `mypy`

## 7. IDE 插件（推荐）

1. `ESLint`
2. `Prettier - Code formatter`
3. `Python`
4. `Pylance`
5. `Ruff`
6. `SQLite Viewer`
7. `REST Client` 或 `Thunder Client`

## 8. 维护规则（必须执行）

1. 每次新增/删除依赖后，必须同步更新本文。
2. 手工安装命令必须同步到 `docs/manual-operations-playbook.md`。
3. 依赖变更需在 `localDoc/TODO.md` 记录日期与影响范围。
4. 主版本升级前必须写兼容性评估。
