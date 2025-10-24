export default [
  {
    title: '番号',
    dataIndex: 'index',
    key: 'index',
    customRender: (value, item, index) => {
      return index + 1
    },
  },
  {
    title: '用户名',
    dataIndex: 'username',
    sorter: true,
  },
  {
    title: '员工姓名',
    dataIndex: 'name',
    sorter: true,
  },
  {
    title: '手机号',
    dataIndex: 'phone',
  }, 
  {
    title: "ステータス",
    dataIndex: "is_active",
    key: "is_active",
    scopedSlots: { customRender: "is_active" },
  },
  {
    title: 'ロール',
    dataIndex: 'role_items',
    scopedSlots: { customRender: 'role_names' },
  },
  {
    title: '操作',
    dataIndex: 'action',
    scopedSlots: { customRender: 'action' },
    width: '256px'
  },
]