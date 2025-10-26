<template>
  <div>
    <a-table :columns="columns" :data-source="items" size="small" :pagination="pagination" @change="tableChange" :loading="loading">
      <div slot="date" slot-scope="value">{{moment(value).format('YYYY-MM-DD')}}</div>
      <div slot="relation_order" slot-scope="value">
        <a-button type="link" @click="openInvoice(value)">表示</a-button>
      </div>
    </a-table>
  </div>
</template>

<script>
  import moment from 'moment'

  export default {
    name: 'FlowPane',
    props: ['items', 'loading', 'pagination'],
    data() {
      return {
        moment,
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
            title: '販売単価',
            dataIndex: 'sales_price',
            key: 'sales_price',
          },
          {
            title: '総金金金額',
            dataIndex: 'total_amount',
            key: 'total_amount',
          },
          {
            title: '販売伝票コード',
            dataIndex: 'sales_order_number',
            key: 'sales_order_number',
          },
          {
            title: '入庫',
            dataIndex: 'warehouse_name',
            key: 'warehouse_name',
          },
          {
            title: '仕入先',
            dataIndex: 'supplier_name',
            key: 'supplier_name',
          },
          {
            title: '作成者',
            dataIndex: 'creator_name',
            key: 'creator_name',
          },
          {
            title: '作成時間',
            dataIndex: 'create_time',
            key: 'create_time',
          },
        ],
      };
    },
    methods: {
      tableChange(pagination, filters, sorter) {
        this.$emit('tableChange', pagination, filters, sorter)
      },
      openInvoice(id) {
        window.open(`/invoice/sales?id=${id}`);
      },
    },
  }
</script>