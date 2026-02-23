/**
 * 文件用途：定义前端 Vite 构建配置，统一挂载 React 与 Tailwind 插件。
 * 使用方：开发命令 `pnpm dev` 与构建命令 `pnpm build` 会读取本配置。
 */
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})
