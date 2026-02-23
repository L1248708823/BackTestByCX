/**
 * 文件用途：集中管理应用路由、导航结构与页面壳布局。
 * 使用方：`src/App.tsx` 通过 `RouterProvider` 挂载本路由配置。
 */
import { NavLink, Outlet, createBrowserRouter } from 'react-router-dom'
import type { ReactElement } from 'react'
import { BacktestPage } from '../pages/backtest-page'
import { ExperimentsPage } from '../pages/experiments-page'
import { HomePage } from '../pages/home-page'

type NavItem = {
  /** 导航对应的路由路径。 */
  path: string
  /** 导航项在界面上的显示名称。 */
  label: string
  /** 导航项用途说明。 */
  description: string
}

const navItems: NavItem[] = [
  { path: '/', label: '项目总览', description: '查看进度与入口' },
  { path: '/backtest', label: '策略回测', description: '配置并运行单次回测' },
  { path: '/experiments', label: '随机实验', description: '批量实验与统计对比' },
]

/**
 * 作用：渲染应用统一布局（顶部导航 + 页面内容）。
 * 入参：无。
 * 出参：根布局组件。
 */
function RootLayout(): ReactElement {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white/95 backdrop-blur-sm">
        <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-4">
          <div>
            <p className="text-sm font-medium text-slate-500">BackTestByCX</p>
            <h1 className="text-xl font-semibold">个人 A 股 ETF 回测工作台</h1>
          </div>
          <nav className="flex gap-2">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  [
                    'rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-slate-900 text-white'
                      : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900',
                  ].join(' ')
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto w-full max-w-6xl px-4 py-8">
        <Outlet />
      </main>
    </div>
  )
}

export const appRouter = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'backtest', element: <BacktestPage /> },
      { path: 'experiments', element: <ExperimentsPage /> },
    ],
  },
])
