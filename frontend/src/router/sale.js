export default {
  path: '/sale',
  name: 'sale',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/sale/sale_create',
  children: [
    {
      path: 'sale_create',
      meta: { title: '販売伝票作成', permission: 'sale_create' },
      component: () => import('@/views/sale/saleCreate/index'),
    },
    {
      path: 'sale_record',
      meta: { title: '販売記録', permission: 'sale_record' },
      component: () => import('@/views/sale/saleRecord/index'),
    },
    {
      path: 'sale_record_detail',
      meta: { title: '販売記録詳細', permission: 'sale_record_detail' },
      component: () => import('@/views/sale/saleRecordDetail/index'),
    },
    {
      path: 'sale_return_create',
      meta: { title: '販売返品', permission: 'sale_return_create' },
      component: () => import('@/views/sale/saleReturnCreate/index'),
    },
    {
      path: 'sale_return_record',
      meta: { title: '販売返品記録', permission: 'sale_return_record' },
      component: () => import('@/views/sale/saleReturnRecord/index'),
    },
    {
      path: 'sale_return_detail',
      meta: { title: '返品記録詳細', permission: 'sale_return_detail' },
      component: () => import('@/views/sale/saleReturnDetail/index'),
    },
  ],
}