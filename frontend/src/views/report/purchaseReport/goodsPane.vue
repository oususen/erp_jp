<template>
  <div>
    <a-table :columns="columns" :data-source="items" size="small" :pagination="pagination" @change="tableChange" :loading="loading">
      <div slot="avg_retail_price" slot-scope="value">{{NP.round(value, 2)}}</div>
    </a-table>
  </div>
</template>

<script>
  import NP from 'number-precision'

  export default {
    name: 'GoodsPane',
    props: ['items', 'loading', 'pagination'],
    data() {
      return {
        NP,
        columns: [
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
            title: '分類名',
            dataIndex: 'category_name',
            key: 'category_name',
          },
          {
            title: '単位',
            dataIndex: 'unit_name',
            key: 'unit_name',
          },
          {
            title: '合計購入数数数量',
            dataIndex: 'total_purchase_quantity',
            key: 'total_purchase_quantity',
          },
          {
            title: '購買総金金金額',
            dataIndex: 'total_purchase_amount',
            key: 'total_purchase_amount',
          },
          {
            title: '最低購買価格',
            dataIndex: 'min_purchase_price',
            key: 'min_purchase_price',
          },
          {
            title: '平均購買価格',
            dataIndex: 'avg_purchase_price',
            key: 'avg_purchase_price',
          },
          {
            title: '最高購買価格',
            dataIndex: 'max_purchase_price',
            key: 'max_purchase_price',
          },
        ],
      };
    },
    methods: {
      tableChange(pagination, filters, sorter) {
        this.$emit('tableChange', pagination, filters, sorter)
      },
    }
  }
</script>