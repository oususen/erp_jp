export default {
  path: '/user',
  name: 'user',
  component: () => import('@/layouts/UserLayout'),
  children: [
    {
      path: 'login',
      name: 'login',
      meta: { title: 'ログイン' },
      component: () => import('@/views/login/Login'),
    },

    {
      path: 'set_password',
      name: 'setPassword',
      meta: { title: 'パスワード設定' },
      component: () => import('@/views/setPassword/SetPassword'),
    },
  ],
}