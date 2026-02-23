/**
 * 文件用途：回测参数配置页面占位，后续承接表单与提交逻辑。
 * 使用方：`src/app/router.tsx` 的 `/backtest` 路由。
 */

import type { ReactElement } from 'react'

/**
 * 作用：渲染回测页面占位说明。
 * 入参：无。
 * 出参：回测页面组件。
 */
export function BacktestPage(): ReactElement {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">策略回测</h2>
      <p className="mt-2 text-sm leading-6 text-slate-600">
        该页面将用于配置回测参数、触发回测任务，并查看实时执行状态。
      </p>
    </section>
  )
}
