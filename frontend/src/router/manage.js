export default {
  path: '/',
  name: 'manage',
  component: () => import('@/layouts/BaseLayout'),
  children: [
    // {
    //   path: 'warehouse',
    //   name: 'warehouse',
    //   meta: { title: '入庫管理', permission: 'warehouse' },
    //   component: () => import('@/views/warehouse/Warehouse'),
    // },
  ],
}