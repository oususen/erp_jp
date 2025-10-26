<template>
  <div>
    <a-card title="入庫記録詳細">
      <a-button slot="extra" type="primary" style="margin-right: 8px;" ghost v-print="'#printContent'"> <a-icon type="printer" />印刷</a-button>
      <a-button slot="extra" type="primary" ghost @click="() => { this.$router.go(-1); }"> <a-icon type="left" />戻る</a-button>
      <section id="printContent">
        <a-spin :spinning="loading">
          <img id="barcode" style="float: right" />
          <a-descriptions bordered>
            <a-descriptions-item label="入庫コード">
              {{ info.stock_in_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="担当者">
              {{ info.handler_name }}
            </a-descriptions-item>
            <a-descriptions-item label="処理日">
              {{ info.handle_time }}
            </a-descriptions-item>
            <a-descriptions-item label="入庫">
              {{ info.warehouse_name }}
            </a-descriptions-item>
            <a-descriptions-item label="処理日">
              {{ info.handle_time }}
            </a-descriptions-item>
            <a-descriptions-item label="備考">
              {{ info.remark }}
            </a-descriptions-item>
          </a-descriptions>
          <a-divider orientation="left" style="margin-top: 30px;">商品情報</a-divider>
          <a-table
            rowKey="id"
            size="middle"
            :columns="columns"
            :data-source="info.stock_in_record_goods_items"
            :pagination="false" />
        </a-spin>
      </section>
    </a-card>
  </div>
</template>

<script>
  import { stockInRecordDetail } from '@/api/warehouse'
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
            title: '入庫数数数量',
            dataIndex: 'stock_in_quantity',
            key: 'stock_in_quantity',
            width: 120,
          },
          {
            title: 'コード付きロット',
            dataIndex: 'batch_number',
            key: 'batch_number',
            width: 120,
          },
          {
            title: '製造日',
            dataIndex: 'production_date',
            key: 'production_date',
            width: 120,
          },
          {
            title: '期限切れ日',
            dataIndex: 'expiration_date',
            key: 'expiration_date',
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
        stockInRecordDetail({ id: this.$route.query.id }).then(data => {
          this.info = data;
          this.info.stock_in_record_goods_items = [
            ...this.info.stock_in_record_goods_items,
            {
              id: '-1',
              isTotal: true,
              stock_in_quantity: this.info.total_quantity,
            },
          ];
          this.getJsBarcode(data.stock_in_order_number)
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
