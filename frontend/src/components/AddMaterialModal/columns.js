export default [
  {
    title: '商品コード',
    dataIndex: 'number',
    sorter: true,
  },
  {
    title: '商品名',
    dataIndex: 'name',
    sorter: true,
  },
  {
    title: '商品単位',
    dataIndex: 'unit_name',
  },
  {
    title: '操作',
    dataIndex: 'action',
    scopedSlots: { customRender: 'action' },
  },
]