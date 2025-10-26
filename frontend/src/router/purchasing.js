export default {
  path: '/purchasing',
  name: 'purchasing',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/purchasing/purchase_create',
  children: [
    {
      path: 'purchase_create',
      meta: { title: '購買伝票作成', permission: 'purchase_create' },
      component: () => import('@/views/purchasing/purchaseCreate/index'),
    },
    {
      path: 'purchase_record',
      meta: { title: '購買記録', permission: 'purchase_record' },
      component: () => import('@/views/purchasing/purchaseRecord/index'),
    },
    {
      path: 'purchase_record_detail',
      meta: { title: '購買記録詳細', permission: 'purchase_record_detail' },
      component: () => import('@/views/purchasing/purchaseRecordDetail/index'),
    },
    {
      path: 'purchase_return_create',
      meta: { title: '購買返品', permission: 'purchase_return_create' },
      component: () => import('@/views/purchasing/purchaseReturnCreate/index'),
    },
    {
      path: 'return_record',
      meta: { title: '返品記録', permission: 'return_record' },
      component: () => import('@/views/purchasing/returnRecord/index'),
    },
    {
      path: 'return_record_detail',
      meta: { title: '返品記録詳細', permission: 'return_record_detail' },
      component: () => import('@/views/purchasing/returnRecordDetail/index'),
    },
  ],
}