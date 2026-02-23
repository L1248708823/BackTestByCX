# 人工操作台账（你在 Windows 执行）

更新时间：2026-02-23

## 1. 文档目的

1. 记录所有需要你人工执行的命令，避免口头遗漏。
2. 每个模块完成后立即停下验证，防止连续开发放大 bug。
3. 形成可追溯的“命令 -> 结果 -> 问题”链路，便于复盘和 review。

## 1.5 当前关联仓库信息

1. 本地目录：`/mnt/e/py/cx回测`
2. 远程仓库：`https://github.com/L1248708823/BackTestByCX.git`
3. 远程名：`origin`

## 2. 使用规则（必须执行）

1. 只要某一步需要你执行命令，必须先写入本台账，再执行。
2. 每个模块结束后必须执行“模块停靠验证清单”。
3. 执行结果（成功/失败 + 关键日志）要回填到 `localDoc/TODO.md`。
4. 助手不会在未记录命令含义的情况下要求你直接运行。
5. Monorepo 初始化按 `docs/monorepo-bootstrap-guide.md` 逐步执行。

## 3. 命令标记规范

1. `【你执行】`：需要你在 Windows 终端执行。
2. `【助手执行】`：由助手在当前工作区执行（不需要你操作）。
3. `【验证】`：用于确认本模块是否通过。

## 4. 模块停靠验证清单（每个模块必走）

1. 功能是否按预期完成（是/否）。
2. 核心命令是否执行成功（是/否）。
3. 是否有告警或异常日志（有/无）。
4. 是否更新了文档与 TODO（是/否）。
5. 是否允许进入下一模块（你确认）。

---

## 5. 模块 A：Monorepo 骨架（讨论期命令清单）

说明：当前阶段先讨论并固化方案，尚未开始安装依赖与初始化代码。  
以下命令用于“开始模块 A 时”的第一轮环境确认。

当前状态：无用占位文件 `frontend/package.json` 已移除，前端将用官方脚手架初始化。

| 步骤 | 执行方 | 命令 | 作用说明 | 预期结果 | 失败时先看什么 |
| --- | --- | --- | --- | --- | --- |
| A1 | 你执行 | `node -v` | 检查 Node.js 是否可用 | 输出 Node 版本号（建议 LTS） | Node 未安装或 PATH 未生效 |
| A2 | 你执行 | `pnpm -v` | 检查 pnpm 是否可用 | 输出 pnpm 版本（建议 9.x） | pnpm 未安装或 corepack 未启用 |
| A3 | 你执行 | `git --version` | 检查 Git 是否可用 | 输出 Git 版本号 | Git 未安装 |
| A4 | 你执行 | `python --version` | 检查 Python 版本（可选） | 输出版本或报错 | 无 Python 不阻塞模块 A |

> 备注：详细执行步骤见 `docs/monorepo-bootstrap-guide.md`。

---

## 5.5 仓库关联与校验（已执行）

| 步骤 | 执行方 | 命令 | 作用说明 | 预期结果 | 失败时先看什么 |
| --- | --- | --- | --- | --- | --- |
| G1 | 助手执行 | `git init -b main` | 初始化本地 Git 仓库 | 生成 `.git` 目录 | 当前目录权限与路径 |
| G2 | 助手执行 | `git remote add origin <repo-url>` | 绑定远程仓库 | `origin` 出现在远程列表 | 远程名重复或 URL 写错 |
| G3 | 你执行 | `git remote -v` | 校验远程是否关联正确 | fetch/push 均指向目标仓库 | 当前目录不是仓库 |
| G4 | 你执行 | `git status --short` | 查看当前未跟踪/变更文件 | 出现待提交文件列表 | 不在项目根目录执行 |

> 关键提醒：仅绑定远程还不具备“可回滚历史”，至少要完成一次提交。

| G5 | 你执行 | `git config user.name "<你的名字>"` | 配置提交用户名 | 无报错 | 名字包含特殊字符时引号 |
| G6 | 你执行 | `git config user.email "<你的邮箱>"` | 配置提交邮箱 | 无报错 | 邮箱格式或输入错误 |
| G7 | 你执行 | `git add .` | 暂存当前文件用于首次提交 | 无报错 | 注意先确认 `.gitignore` 已生效 |
| G7.1 | 你执行 | `git status --short` | 二次确认暂存内容正确 | 不应出现 `.codex/`、`localDoc/` | `.gitignore` 未生效或路径写错 |
| G8 | 你执行 | `git commit -m "chore: initialize project docs and architecture"` | 生成首个提交快照 | 输出 commit hash | 用户信息未配置或无暂存变更 |
| G9 | 你执行 | `git push -u origin main` | 推送到远程并建立上游分支 | push 成功 | 网络、权限、仓库访问权限 |

---

## 6. 模块 A 完成后的验证命令（预留）

当你按 `docs/monorepo-bootstrap-guide.md` 初始化完前端后，执行如下命令：

1. `【你执行】cd frontend && pnpm dev`
2. `【你执行】cd .. && pnpm install`
3. `【你执行】pnpm turbo run build --dry`

每条命令的作用、预期输出、失败排查已写在 `docs/monorepo-bootstrap-guide.md`。

---

## 6.5 模块 A.1：前端基础依赖与插件补齐（你执行）

说明：前端脚手架已完成后，补齐路由、请求层、服务端状态、表单校验、图表和 Tailwind。  
本轮助手已完成代码接入（路由骨架 + Tailwind + Query Provider），你只需执行安装/验证。

| 步骤 | 执行方 | 命令 | 作用说明 | 预期结果 | 失败时先看什么 |
| --- | --- | --- | --- | --- | --- |
| A1.1 | 你执行 | `cd frontend` | 进入前端目录 | 进入 `frontend` | 当前路径错误 |
| A1.2 | 你执行 | `pnpm add react-router-dom @tanstack/react-query @tanstack/react-query-devtools axios zod react-hook-form @hookform/resolvers echarts echarts-for-react dayjs` | 安装前端核心生产依赖 | 安装成功无冲突 | 网络、pnpm 镜像、锁文件冲突 |
| A1.3 | 你执行 | `pnpm add -D tailwindcss @tailwindcss/vite prettier eslint-config-prettier vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event msw` | 安装开发与测试依赖 | 安装成功无冲突 | 版本冲突、网络问题 |
| A1.4 | 你执行 | `cd ..` | 返回仓库根目录 | 回到项目根目录 | 路径错误 |
| A1.5 | 你执行 | `pnpm install` | 让根工作区锁文件与 `vite@7` 稳定版本重新对齐 | 安装完成无报错 | 网络问题、权限问题 |

| 验证 | 执行方 | 命令 | 作用说明 | 预期结果 | 失败时先看什么 |
| --- | --- | --- | --- | --- | --- |
| A1.V1 | 你执行 | `cd frontend && pnpm dev` | 验证前端依赖可运行 | 开发服务正常启动 | 依赖未安装或配置冲突 |
| A1.V1.1 | 你执行 | `cd .. && pnpm --filter frontend build` | 验证前端构建是否通过 | build 成功产出 dist | 重点看 vite/rolldown 报错 |
| A1.V2 | 你执行 | `cd .. && pnpm turbo run build --dry` | 验证 Monorepo 任务仍正常 | 可看到任务图 | turbo/workspace 配置问题 |

若 A1.V1.1 报 `Cannot find native binding`，执行应急修复：

| 应急 | 执行方 | 命令 | 作用说明 | 预期结果 | 失败时先看什么 |
| --- | --- | --- | --- | --- | --- |
| A1.F1 | 你执行 | `Remove-Item -Recurse -Force node_modules, frontend/node_modules` | 清理可能损坏的可选依赖安装产物 | 目录清理完成 | 路径错误或权限不足 |
| A1.F2 | 你执行 | `pnpm install` | 重新安装工作区依赖 | 安装完成无报错 | 网络、pnpm 缓存、锁文件冲突 |
| A1.F3 | 你执行 | `pnpm --filter frontend build` | 复验构建状态 | build 成功 | Node 版本/系统架构不匹配 |

---

## 6.8 模块 B.1：后端 FastAPI 基础骨架验证（你执行）

说明：本轮助手已完成后端骨架代码落地。你现在只需要按顺序执行命令，验证服务可启动、接口可访问、测试可运行。  
注意：后端 Python 版本统一基线是 `3.12`，不再混用 3.11。

| 步骤 | 执行方 | 命令 | 作用说明 | 预期结果 | 失败时先看什么 |
| --- | --- | --- | --- | --- | --- |
| B1.1 | 你执行 | `cd backend` | 进入后端目录 | 当前目录变为 `backend` | 路径错误 |
| B1.2 | 你执行 | `py -3.12 --version` | 校验 Python 3.12 可用 | 输出 `Python 3.12.x` | 未安装 Python Launcher 或未安装 3.12 |
| B1.3 | 你执行 | `py -3.12 -m venv .venv` | 创建后端虚拟环境 | 生成 `.venv` 目录 | Python 版本不对、权限问题 |
| B1.4 | 你执行 | `.\\.venv\\Scripts\\Activate.ps1` | 激活虚拟环境 | 终端前缀出现 `(.venv)` | PowerShell 执行策略限制 |
| B1.5 | 你执行 | `python -m pip install --upgrade pip` | 升级 pip 以减少安装兼容问题 | 升级成功无报错 | 镜像与网络问题 |
| B1.6 | 你执行 | `pip install -r requirements-dev.txt` | 安装后端运行/开发依赖 | 安装成功无冲突 | 网络、代理、镜像配置 |
| B1.7 | 你执行 | `Copy-Item .env.example .env` | 生成本地环境变量文件 | `backend/.env` 生成 | 文件权限或路径错误 |
| B1.8 | 你执行 | `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` | 启动后端服务 | 控制台显示启动成功 | 依赖未安装、端口占用 |

| 验证 | 执行方 | 命令/访问点 | 作用说明 | 预期结果 | 失败时先看什么 |
| --- | --- | --- | --- | --- | --- |
| B1.V1 | 你执行 | 访问 `http://localhost:8000/api/v1/health` | 验证健康检查接口 | 返回 `{\"status\":\"ok\",\"service\":\"backend\"}` | 服务未启动、路由前缀错误 |
| B1.V2 | 你执行 | 访问 `http://localhost:8000/api/v1/docs` | 验证 OpenAPI 文档 | Swagger 页面可打开 | docs 路径或启动命令错误 |
| B1.V3 | 你执行 | 新开终端后 `cd backend` + 激活 `.venv` + `pytest` | 验证后端测试基线 | 至少 1 个测试通过 | 依赖未安装、PYTHONPATH 配置 |

---

## 7. 回填模板（复制到 TODO 或评论）

```text
模块：
执行日期：
命令：
结果：
关键日志：
是否通过：
阻塞点：
```
