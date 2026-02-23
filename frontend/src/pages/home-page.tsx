/**
 * 文件用途：展示前端模块当前状态与后续开发入口，作为首页占位页。
 * 使用方：`src/app/router.tsx` 的 index 路由。
 */

import type { ReactElement } from 'react'

/**
 * 作用：渲染项目首页信息卡片。
 * 入参：无。
 * 出参：首页组件。
 */
export function HomePage(): ReactElement {
  return (
    <section className="space-y-6">
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-900">当前阶段</h2>
        <p className="mt-2 text-sm leading-6 text-slate-600">
          已完成前端基础骨架，下一步进入回测参数表单、结果图表与实验任务页面的逐模块开发。
        </p>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h3 className="text-base font-semibold">回测参数页</h3>
          <p className="mt-2 text-sm text-slate-600">
            提供 ETF、定投频率、时间区间、交易成本等输入项。
          </p>
        </article>
        <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h3 className="text-base font-semibold">结果页</h3>
          <p className="mt-2 text-sm text-slate-600">
            展示净值曲线、收益分布、回撤与关键指标卡片。
          </p>
        </article>
        <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h3 className="text-base font-semibold">随机实验页</h3>
          <p className="mt-2 text-sm text-slate-600">
            支持批量随机起点实验和统计对比，辅助判断策略鲁棒性。
          </p>
        </article>
      </div>
    </section>
  )
}
