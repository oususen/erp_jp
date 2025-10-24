export default {
  path: '/report',
  name: 'report',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/report/sale_report',
  children: [
    {
      path: 'sale_report',
      meta: { title: '販売レポート', permission: 'sale_report' },
      component: () => import('@/views/report/saleReport/index'),
    },
    {
      path: 'purchase_report',
      meta: { title: '購買レポート', permission: 'purchase_report' },
      component: () => import('@/views/report/purchaseReport/index'),
    },
    {
      path: 'stock_report',
      meta: { title: '在庫レポート', permission: 'stock_report' },
      component: () => import('@/views/report/stockReport/index'),
    },
    {
      path: 'income_expense_statistics',
      meta: { title: '収支統計', permission: 'income_expense_statistics' },
      component: () => import('@/views/report/incomeExpenseStatistics/index'),
    },
    {
      path: 'batch_report',
      meta: { title: 'バッチレポート', permission: 'batch_report' },
      component: () => import('@/views/report/batchReport/index'),
    },
  ],
}