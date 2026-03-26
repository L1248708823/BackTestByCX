# BackTestByCX

个人 A 股 ETF 回测项目，当前目标是完成一个本地可运行、可验证、可演示的 MVP。

## 项目说明

- 前端：React + TypeScript
- 后端：FastAPI + Python 3.12
- 仓库结构：`frontend/` + `backend/` + `docs/`
- 运行约束：依赖安装和项目启动由你在 Windows 环境手动执行；助手在 WSL 中负责代码与文档修改

## 文档入口

- 安装说明：[docs/install-guide-windows.md](docs/install-guide-windows.md)
- 启动与联调：[docs/startup-runbook.md](docs/startup-runbook.md)
- 人工操作台账：[docs/manual-operations-playbook.md](docs/manual-operations-playbook.md)
- MVP 主线设计：[docs/plans/2026-03-26-mvp-mainline-design.md](docs/plans/2026-03-26-mvp-mainline-design.md)

## 第一次启动

适用于第一次在当前机器上拉起前后端，或本地依赖、虚拟环境还没准备好的情况。

### 1. 前端准备

在仓库根目录执行：

```bash
pnpm install
pnpm --filter frontend exec tsc -b
pnpm --filter frontend build
pnpm turbo run build --dry
```

如果 `pnpm --filter frontend build` 报 `Cannot find native binding`，按下面顺序执行后重试：

```powershell
Remove-Item -Recurse -Force node_modules, frontend/node_modules
pnpm install
pnpm --filter frontend build
```

### 2. 后端准备

在第一个终端执行：

```powershell
cd backend
py -3.12 --version
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

说明：

- 如果 `backend/.venv` 已存在且确认是 Python 3.12，可以跳过 `py -3.12 -m venv .venv`
- 如果 `backend/.env` 已存在且配置可用，可以跳过 `Copy-Item .env.example .env`

### 3. 前端启动

在第二个终端执行：

```powershell
cd frontend
pnpm dev --host --port 5173
```

说明：

- 如果 `5173` 被占用，Vite 会自动切换端口，请以终端实际输出的地址为准

### 4. 启动后验证

- 前端页面：以 `pnpm dev` 终端实际输出的本地地址为准（默认是 `http://localhost:5173`）
- 后端健康检查：`http://localhost:8000/api/v1/health`
- 后端接口文档：`http://localhost:8000/api/v1/docs`

后端测试在新终端执行：

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest
```

## 快速启动

适用于你已经完成过一次依赖安装、虚拟环境创建和 `.env` 配置，只需要重新拉起项目。

### 1. 启动后端

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 启动前端

```powershell
cd frontend
pnpm dev --host --port 5173
```

### 3. 快速检查

- 前端是否可打开
- `/api/v1/health` 是否返回 `{"status":"ok","service":"backend"}`
- `/api/v1/docs` 是否可访问

## 当前状态

- 前端骨架页面已可运行
- 后端骨架接口已提供健康检查与回测占位接口
- 当前主线处于 P0 基线验证与 P1 契约冻结之间

## 注意事项

- 当前前端没有 `pnpm test` 脚本，P0 阶段以 `tsc -b`、`build`、`turbo --dry` 作为基线验证
- 前端页面验证可以在你手动启动后，由助手使用 Chrome MCP 继续做结构和控制台检查
- 涉及依赖新增时，先确认原因和最小方案，再执行安装
