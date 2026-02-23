# Windows 安装手册（手动执行）

更新时间：2026-02-22

## 1. 适用范围

1. 适用于你在 Windows 主机手动安装依赖。
2. 适用于当前项目“前后端分离 + 同仓库”的开发方式。
3. 助手在 WSL 环境，不直接操作你的 Windows 安装过程。
4. 所有人工命令以 `docs/manual-operations-playbook.md` 为准。

## 2. 安装前准备

1. 安装 Node.js（建议 LTS 版本）。
2. 安装 pnpm（建议 9.x）。
3. 安装 Python（建议 3.11 或 3.12）。
4. 安装 Git。
5. 准备可用网络访问 Python 包与 npm 包镜像。

## 3. 项目目录约定

1. 项目根目录：`/mnt/e/py/cx回测`（WSL 视角）。
2. 你在 Windows 侧对应目录打开项目即可。
3. 后续默认目录结构：
   - `frontend/`
   - `backend/`
   - `docs/`
   - `localDoc/`

## 4. 前端安装步骤（你执行）

1. 进入前端目录：`cd frontend`
2. 安装依赖：`pnpm install`
3. 如需单独增加依赖：
   - 生产依赖：`pnpm add <pkg>`
   - 开发依赖：`pnpm add -D <pkg>`

## 5. 后端安装步骤（你执行）

1. 进入后端目录：`cd backend`
2. 创建虚拟环境：`python -m venv .venv`
3. 激活虚拟环境（Windows PowerShell）：`.venv\\Scripts\\Activate.ps1`
4. 安装基础依赖：`pip install -r requirements.txt`
5. 安装开发依赖：`pip install -r requirements-dev.txt`

## 6. 环境变量步骤（你执行）

1. 在 `backend/` 下维护 `.env` 文件。
2. 最小配置建议：
   - `DATA_PROVIDER=akshare`
   - `MODEL_PRIMARY=<provider/model-id>`
   - `MODEL_FALLBACK=<provider/model-id>`
   - `LLM_API_KEY=<your-key>`
   - `RISK_FREE_RATE=0.02`
3. 不要把真实密钥提交到代码仓库。

## 7. 常见问题排查

1. `pnpm` 权限或重命名错误：优先在 Windows 终端执行安装，不在 `/mnt` 路径混用多终端并发安装。
2. Python 包安装失败：先确认 Python 与 pip 指向同一解释器。
3. C 扩展编译失败：优先使用预编译轮子版本，必要时切换 Python 次版本。

## 8. 维护规则（必须执行）

1. 安装流程变化时，必须同步更新本手册。
2. 依赖管理策略变化时，同时更新 `docs/dependency-checklist.md`。
3. 每次手册更新，在 `localDoc/TODO.md` 增加变更记录。
