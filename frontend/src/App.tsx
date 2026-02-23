/**
 * 文件用途：应用根组件，只负责接入全局路由容器。
 * 使用方：`src/main.tsx` 在应用启动时渲染本组件。
 */
import { RouterProvider } from 'react-router-dom'
import type { ReactElement } from 'react'
import { appRouter } from './app/router'

/**
 * 作用：渲染应用级路由。
 * 入参：无。
 * 出参：React 路由 Provider 组件。
 */
function App(): ReactElement {
  return <RouterProvider router={appRouter} />
}

export default App
