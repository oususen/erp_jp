export default {
  path: '/',
  name: 'account',
  component: () => import('@/layouts/BaseLayout'),
  children: [
    {
      path: 'role',
      name: 'role',
      meta: { title: 'ロール管理', permission: 'role' },
      component: () => import('@/views/role/Role'),
    },
    {
      path: 'account',
      name: 'Account', 
      meta: { title: '账号管理', permission: 'account' },
      component: () => import('@/views/account/Account'),
    },
    {
      path: 'config',
      name: 'config', 
      meta: { title: 'システム設定', permission: 'config' },
      component: () => import('@/views/config/Config'),
    },
  ],
}