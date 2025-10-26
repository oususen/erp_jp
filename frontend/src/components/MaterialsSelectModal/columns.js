export const columns = [
  {
    title: '連番',
    dataIndex: 'index',
    key: 'index',
    customRender: (value, item, index) => {
      return index + 1
    },
  },
  {
    title: '名称',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: 'コード',
    dataIndex: 'number',
    key: 'number',
  },
  {
    title: 'バーコード',
    dataIndex: 'barcode',
    key: 'barcode',
  },
  {
    title: '単位名',
    dataIndex: 'unit_name',
    key: 'unit_name',
  },
  {
    title: '操作',
    dataIndex: 'action',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
]