/**
 * 文件用途：随机实验页面占位，后续承接批量实验任务配置与统计展示。
 * 使用方：`src/app/router.tsx` 的 `/experiments` 路由。
 */

import type { ReactElement } from 'react'

/**
 * 作用：渲染随机实验页面占位说明。
 * 入参：无。
 * 出参：随机实验页面组件。
 */
export function ExperimentsPage(): ReactElement {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">随机实验</h2>
      <p className="mt-2 text-sm leading-6 text-slate-600">
        该页面将用于批量随机起点实验、统计分位数分布，并生成可追溯报告。
      </p>
    </section>
  )
}
