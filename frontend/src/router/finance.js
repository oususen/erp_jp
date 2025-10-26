export default {
  path: '/finance',
  name: 'finance',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/finance/flow',
  children: [
    {
      path: 'payment',
      meta: { title: '支払いい', permission: 'payment' },
      component: () => import('@/views/finance/payment/index'),
    },
    {
      path: 'payment_create',
      meta: { title: '支払い新規登録い', permission: 'payment_create' },
      component: () => import('@/views/finance/paymentCreate/index'),
    },
    {
      path: 'payment_detail',
      meta: { title: 'お支払いいい詳細', permission: 'payment_detail' },
      component: () => import('@/views/finance/paymentDetail/index'),
    },
    {
      path: 'collection',
      meta: { title: '入金', permission: 'collection' },
      component: () => import('@/views/finance/collection/index'),
    },
    {
      path: 'collection_create',
      meta: { title: '新しい支払いいいの徴収', permission: 'collection_create' },
      component: () => import('@/views/finance/collectionCreate/index'),
    },
    {
      path: 'collection_detail',
      meta: { title: 'お支払いいい詳細', permission: 'collection_detail' },
      component: () => import('@/views/finance/collectionDetail/index'),
    },
    {
      path: 'arrears_payable',
      meta: { title: '買掛金', permission: 'arrears_payable' },
      component: () => import('@/views/finance/arrearsPayable/index'),
    },
    {
      path: 'arrears_payable_detail',
      meta: { title: '買掛金詳細', permission: 'arrears_payable_detail' },
      component: () => import('@/views/finance/arrearsPayableDetail/index'),
    },
    {
      path: 'arrears_receivable',
      meta: { title: '売掛金', permission: 'arrears_receivable' },
      component: () => import('@/views/finance/arrearsReceivable/index'),
    },
    {
      path: 'arrears_receivable_detail',
      meta: { title: '売掛金詳細', permission: 'arrears_receivable_detail' },
      component: () => import('@/views/finance/arrearsReceivableDetail/index'),
    },
    {
      path: 'account_transfer',
      meta: { title: '振出元口座', permission: 'account_transfer' },
      component: () => import('@/views/finance/accountTransfer/index'),
    },
    {
      path: 'income_and_pay',
      meta: { title: '日常収支', permission: 'income_and_pay' },
      component: () => import('@/views/finance/incomeAndPay/index'),
    },
    {
      path: 'flow',
      meta: { title: '資金明細', permission: 'flow' },
      component: () => import('@/views/finance/flow/index'),
    },
    {
      path: 'flow_detail',
      meta: { title: '資金明細詳細', permission: 'flow_detail' },
      component: () => import('@/views/finance/flowDetail/index'),
    },
    // {
    //   path: 'purchase_statement',
    //   meta: { title: '購買明細書', permission: 'purchase_statement' },
    //   component: () => import('@/views/finance/purchaseStatement/index'),
    // },
    // {
    //   path: 'transaction_record',
    //   meta: { title: '取引記録', permission: 'transaction_record' },
    //   component: () => import('@/views/finance/transactionRecord/index'),
    // },
    // {
    //   path: 'sales_statement',
    //   meta: { title: '販売伝票', permission: 'sales_statement' },
    //   component: () => import('@/views/finance/salesStatement/index'),
    // },
  ],
}