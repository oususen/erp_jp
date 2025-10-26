export default {
  path: '/production',
  name: 'production',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/production/plan',
  children: [
    {
      path: 'plan',
      meta: { title: '生産計画' },
      component: () => import('@/views/production/productionPlan/index'),
    },
    {
      path: 'detial',
      meta: { title: '生産計画詳細' },
      component: () => import('@/views/production/productionDetial/index'),
    },
    {
      path: 'task',
      meta: { title: '生産タスク' },
      component: () => import('@/views/production/productionTask/index'),
    },
    {
      path: 'record',
      meta: { title: '生産実績' },
      component: () => import('@/views/production/productionRecord/index'),
    },
  ],
}