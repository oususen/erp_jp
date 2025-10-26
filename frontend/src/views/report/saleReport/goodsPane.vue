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
            title: '単位',
            dataIndex: 'unit_name',
            key: 'unit_name',
          },
          {
            title: '総販売回数数数量',
            dataIndex: 'total_sales_quantity',
            key: 'total_sales_quantity',
          },
          {
            title: '販売総金金額',
            dataIndex: 'total_sales_amount',
            key: 'total_sales_amount',
          },
          {
            title: '最低販売価格',
            dataIndex: 'min_sales_price',
            key: 'min_sales_price',
          },
          {
            title: '平均販売価格',
            dataIndex: 'avg_sales_price',
            key: 'avg_sales_price',
          },
          {
            title: '最高販売価格',
            dataIndex: 'max_sales_price',
            key: 'max_sales_price',
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