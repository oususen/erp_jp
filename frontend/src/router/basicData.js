export default {
  path: '/basicData',
  name: 'basicData',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/basicData/client_classification',
  children: [
    {
      path: 'client',
      meta: { title: '顧客', permission: 'client' },
      component: () => import('@/views/basicData/client/index'),
    },
    {
      path: 'supplier',
      meta: { title: '仕入先', permission: 'supplier' },
      component: () => import('@/views/basicData/supplier/index'),
    },
    {
      path: 'warehouse',
      meta: { title: '入庫', permission: 'warehouse' },
      component: () => import('@/views/basicData/warehouse/index'),
    },
    {
      path: 'settlement_account',
      meta: { title: '決済口座', permission: 'settlement_account' },
      component: () => import('@/views/basicData/settlementAccount/index'),
    },
    {
      path: 'revenue_expenditure_items',
      meta: { title: ' 収支項目', permission: 'revenue_expenditure_items' },
      component: () => import('@/views/basicData/revenueExpenditureItems/index'),
    },
  ],
}