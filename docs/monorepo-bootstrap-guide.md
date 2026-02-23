# Monorepo 基础初始化手册（模块 A：前端官方脚手架）

更新时间：2026-02-23

当前状态：

1. 根 Monorepo 文件已创建：`package.json`、`pnpm-workspace.yaml`、`turbo.json`。
2. `frontend/` 已完成官方脚手架初始化；若你已完成此步，可跳过 5.1。

## 1. 目标与范围

1. 本手册用于初始化 Monorepo 基础骨架。
2. 采用“先基础、后扩展”的节奏，每一步都可停下验证。
3. 模块 A 仅做前端官方初始化 + Tailwind 基础接入。
4. 兼容“当前环境没有 Python”的情况。

## 2. 关键策略（避免后期返工）

1. 先完成 JS/TS 工作区与任务编排，再接 Python 后端任务。
2. 前端必须使用官方脚手架生成，避免手写占位 `package.json` 冲突。
3. 模块 A 不强制要求后端可运行，只要求仓库结构和前端可初始化。
4. 根 `package.json` 只做 `turbo run` 委托，不写具体任务逻辑。
5. 除 Tailwind 外，其它业务依赖后置到后续模块。

## 3. 模块 A 完成标准

1. 前端由官方脚手架生成（React + TypeScript）。
2. `frontend` 可正常安装依赖与执行开发命令。
3. Tailwind 以 Vite 插件方式接入，`src/index.css` 有 `@import "tailwindcss";`。
4. 根目录执行 `pnpm turbo run build --dry` 不报配置错误。

## 4. 执行前检查（你执行）

1. `node -v`
2. `pnpm -v`
3. `git --version`
4. `python --version`（可选，失败不阻塞模块 A）

说明：

1. 若第 4 条失败，不影响本模块。
2. Python 相关步骤放到模块 B。

## 5. 初始化步骤（你执行，官方流程）

## 5.1 使用官方脚手架创建前端（Vite 交互模式）

```bash
pnpm create vite frontend
```

说明：

1. 这是 Vite 官方推荐命令的 pnpm 交互式版本。
2. 若提示目录非空，先确认 `frontend/` 内没有你要保留的文件。
3. 若 `frontend/` 已存在脚手架文件（如 `src/main.tsx`、`vite.config.ts`），可直接跳到 5.2。

交互选择建议（逐步选择）：

1. `Select a framework`：选择 `React`  
原因：与你项目技术栈约束一致。
2. `Select a variant`：选择 `TypeScript`  
原因：当前项目要求前端使用 TS，便于类型约束和后续契约联动。

## 5.2 安装前端依赖

```bash
cd frontend
pnpm install
```

## 5.3 接入 Tailwind（Vite 插件方式）

```bash
pnpm add -D tailwindcss @tailwindcss/vite
```

### 5.3.1 修改 `frontend/vite.config.ts`

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

### 5.3.2 修改 `frontend/src/index.css`

```css
@import "tailwindcss";
```

## 5.4 返回仓库根目录

```bash
cd ..
```

## 6. 模块 A 验证（你执行）

1. `cd frontend && pnpm dev`
2. 浏览器打开 `http://localhost:5173`，确认前端可运行。
3. `Ctrl + C` 结束前端服务，回到根目录。
4. 根目录执行：`pnpm install`
5. 根目录执行：`pnpm turbo run build --dry`

预期结果：

1. 前端页面可以正常打开。
2. 根目录没有 workspace 或 turbo 配置错误。

---

## 7. 模块 A 停靠点（必须停下）

完成上述验证后，暂停，不进入模块 B。  
先把以下内容反馈给我：

1. 前端 `pnpm dev` 是否成功启动。
2. 根目录 `pnpm install` 与 `pnpm turbo run build --dry` 输出关键行。
3. 是否出现报错。
4. 目录结构截图或 `tree` 输出（可选）。

---

## 8. 模块 B 预告（先不执行）

模块 B 才处理：

1. Python 3.12 + FastAPI 初始化。
2. `backend` 接入任务脚本。
3. 后端最小健康检查接口。

你现在只做模块 A。

## 9. 参考来源（官方）

1. Vite 官方入门（create-vite）：https://vite.dev/guide/
2. Tailwind 官方 Vite 安装（v4）：https://tailwindcss.com/docs/installation/using-vite
