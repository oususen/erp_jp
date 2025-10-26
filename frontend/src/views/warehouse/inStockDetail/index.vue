<template>
  <div>
    <a-card title="入庫通知の詳細">
      <a-button slot="extra" type="primary" style="margin-right: 8px;" ghost v-print="'#printContent'"> <a-icon type="printer" />印刷</a-button>
      <a-button slot="extra" type="primary" ghost @click="() => { this.$router.go(-1); }"> <a-icon type="left" />戻る</a-button>
      <section id="printContent">
        <a-spin :spinning="loading">
          <img id="barcode" style="float: right" />
          <a-descriptions bordered>
            <a-descriptions-item label="入庫コード">
              {{ info.number }}
            </a-descriptions-item>
            <a-descriptions-item label="入庫タイプ">
              {{ info.type_display }}
            </a-descriptions-item>
            <a-descriptions-item label="入庫">
              {{ info.warehouse_name }}
            </a-descriptions-item>
            <a-descriptions-item :label="info.type === 'purchase' ? '購買伝票' : (info.type === 'sales_return' ? '販売返品伝票' : '在庫振替伝票')">
              {{ info.type === 'purchase' ? info.purchase_order_number : (info.type === 'sales_return' ? info.sales_return_order_number : info.stock_transfer_order_number) }}
            </a-descriptions-item>
            <!-- <a-descriptions-item label="処理日">
              {{ info.handle_time }}
            </a-descriptions-item>
            <a-descriptions-item label="そのその他費用">
              {{ info.other_amount }}
            </a-descriptions-item>
            <a-descriptions-item label="備考">
              {{ info.remark }}
            </a-descriptions-item> -->
          </a-descriptions>
          <a-divider orientation="left" style="margin-top: 30px;">商品情報</a-divider>
          <a-table
            rowKey="id"
            size="middle"
            :columns="columns"
            :data-source="info.stock_in_goods_items"
            :pagination="false" />
        </a-spin>
      </section>
    </a-card>
  </div>
</template>

<script>
  import { stockInOrderDetail } from '@/api/warehouse'
  import JsBarcode from 'jsbarcode'
  import NP from 'number-precision'

  export default {
    data() {
      return {
        loading: false,
        materialLoading: false,
        info: {},
        columns: [
          {
            title: '連番',
            dataIndex: 'index',
            key: 'index',
            width: 45,
            customRender: (value, item, index) => {
              return item.isTotal ? '合計' : (index + 1)
            },
          },
          {
            title: '商品名',
            dataIndex: 'goods_name',
            key: 'goods_name',
            width: 150,
          },
          {
            title: '商品コード',
            dataIndex: 'goods_number',
            key: 'goods_number',
            width: 150,
          },
          {
            title: '単位',
            dataIndex: 'unit_name',
            key: 'unit_name',
            width: 80,
          },
          {
            title: '総入庫数',
            dataIndex: 'stock_in_quantity',
            key: 'stock_in_quantity',
            width: 120,
          },
          {
            title: '入庫残数数数量',
            dataIndex: 'remain_quantity',
            key: 'remain_quantity',
            width: 120,
          },
          {
            title: '品質保証期間日数',
            dataIndex: 'shelf_life_days',
            key: 'shelf_life_days',
            width: 120,
          },
          // {
          //   title: '金金額',
          //   dataIndex: 'totalAmount',
          //   key: 'totalAmount',
          //   width: 200,
          //   customRender: (value, item) => {
          //     if (item.isTotal) return value;
          //     value = NP.times(item.stock_in_quantity, item.purchase_price);
          //     return item.id ? NP.round(value, 2) : ''
          //   },
          // }
        ],
      }
    },
    created(){
      this.initData();
    },
    methods: {
      getJsBarcode(number) {
        JsBarcode("#barcode", number, {
          lineColor: '#000',
          width: 2,
          height: 40,
          displayValue: true
        });
      },
      initData() {
        this.loading = true;
        stockInOrderDetail({ id: this.$route.query.id }).then(data => {
          this.info = data;
          this.info.stock_in_goods_items = [
            ...this.info.stock_in_goods_items,
            {
              id: '-1',
              isTotal: true,
              stock_in_quantity: this.info.total_quantity,
            },
          ];
          this.getJsBarcode(data.number)
        }).finally(() => {
          this.loading = false;
        });
      },
    },
    mounted() {
      this.initData();
    },
  }
</script>
<style>
</style>
