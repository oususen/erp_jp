export default [
  {
    title: '連番',
    dataIndex: 'index',
    key: 'index',
    customRender: (value, item, index) => {
      return index + 1
    },
  },
  {
    title: 'ユーザー名',
    dataIndex: 'username',
    sorter: true,
  },
  {
    title: '従業員名',
    dataIndex: 'name',
    sorter: true,
  },
  {
    title: '携帯コード',
    dataIndex: 'phone',
  }, 
  {
    title: "状態",
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