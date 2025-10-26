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
    title: '商品コード',
    dataIndex: 'goods_number',
    key: 'goods_number',
  },
  {
    title: '商品名',
    dataIndex: 'goods_name',
    key: 'goods_name',
  },
  {
    title: '仕様',
    dataIndex: 'goods_spec',
    key: 'goods_spec',
  },
  {
    title: '単位',
    dataIndex: 'unit_name',
    key: 'unit_name',
  },
  {
    title: '棚卸コード数数量',
    dataIndex: 'total_quantity',
    key: 'total_quantity',
  },
  {
    title: '操作',
    dataIndex: 'action',
    key: 'action',
    scopedSlots: { customRender: 'action' },
  },
]