export default {
  path: '/goods',
  name: 'goods',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/finance/classification',
  children: [
    {
      path: 'classification',
      meta: { title: '商品カテゴリ', permission: 'classification' },
      component: () => import('@/views/goods/classification/index'),
    },
    {
      path: 'unit',
      meta: { title: '商品単位', permission: 'unit' },
      component: () => import('@/views/goods/unit/index'),
    },
    {
      path: 'information',
      meta: { title: '商品情報', permission: 'information' },
      component: () => import('@/views/goods/information/index'),
    },
    {
      path: 'temporary_warning',
      meta: { title: '期限切れ間近警告', permission: 'temporary_warning' },
      component: () => import('@/views/goods/temporaryWarning/index'),
    },
  ],
}