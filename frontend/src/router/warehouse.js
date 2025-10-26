export default {
  path: '/warehouse',
  name: 'warehouse',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/warehouse/inStock',
  children: [
    {
      path: 'inStock',
      meta: { title: '入庫タスク', permission: 'stock_in' },
      component: () => import('@/views/warehouse/inStock/index'),
    },
    {
      path: 'inStock_create',
      meta: { title: '入庫の作成', permission: 'stock_in' },
      component: () => import('@/views/warehouse/inStockCreate/index'),
    },
    {
      path: 'inStock_detail',
      meta: { title: '入庫通知の詳細', permission: 'stock_in' },
      component: () => import('@/views/warehouse/inStockDetail/index'),
    },
    {
      path: 'inStock_record_detail',
      meta: { title: '入庫記録詳細', permission: 'stock_in' },
      component: () => import('@/views/warehouse/inStockRecordDetail/index'),
    },
    {
      path: 'outStock',
      meta: { title: '出庫タスク', permission: 'stock_out' },
      component: () => import('@/views/warehouse/outStock/index'),
    },
    {
      path: 'outStock_create',
      meta: { title: '出庫登録', permission: 'stock_out' },
      component: () => import('@/views/warehouse/outStockCreate/index'),
    },
    {
      path: 'outStock_detail',
      meta: { title: '出庫通知の詳細', permission: 'stock_out' },
      component: () => import('@/views/warehouse/outStockDetail/index'),
    },
    {
      path: 'outStock_record_detail',
      meta: { title: '出庫記録詳細', permission: 'stock_out' },
      component: () => import('@/views/warehouse/outStockRecordDetail/index'),
    },
    {
      path: 'allocation',
      meta: { title: '在庫振替', permission: 'stock_transfer' },
      component: () => import('@/views/warehouse/allocation/index'),
    },
    {
      path: 'allocation_create',
      meta: { title: '在庫振替登録', permission: 'stock_transfer' },
      component: () => import('@/views/warehouse/allocationCreate/index'),
    },
    {
      path: 'allocationDetail_detail',
      meta: { title: '在庫振替伝票詳細', permission: 'stock_transfer' },
      component: () => import('@/views/warehouse/allocationDetail/index'),
    },
    {
      path: 'inventory',
      meta: { title: '棚卸', permission: 'stock_check' },
      component: () => import('@/views/warehouse/inventory/index'),
    },
    {
      path: 'inventory_create',
      meta: { title: '棚卸登録', permission: 'stock_check' },
      component: () => import('@/views/warehouse/inventoryCreate/index'),
    },
    {
      path: 'inventory_detail',
      meta: { title: '棚卸詳細', permission: 'stock_check' },
      component: () => import('@/views/warehouse/inventoryDetail/index'),
    },
    {
      path: 'flow',
      meta: { title: '在庫推移', permission: 'inventory_flow' },
      component: () => import('@/views/warehouse/flow/index'),
    },
    {
      path: 'flow_detail',
      meta: { title: '在庫推移詳細', permission: 'inventory_flow' },
      component: () => import('@/views/warehouse/flowDetail/index'),
    },
  ],
}