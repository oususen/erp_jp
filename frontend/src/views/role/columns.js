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
    title: '名称',
    dataIndex: 'name',
    sorter: true,
  },
  {
    title: '備考',
    dataIndex: 'remark',
    ellipsis: true,
  },
  {
    title: '操作',
    dataIndex: 'action',
    scopedSlots: { customRender: 'action' },
    width: '156px'
  },
]