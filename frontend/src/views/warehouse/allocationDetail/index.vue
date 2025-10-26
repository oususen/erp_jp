<template>
  <div>
    <a-card title="在庫振替伝票詳細">
       <a-button slot="extra" type="primary" style="margin-right: 8px;" ghost v-print="'#printContent'"> <a-icon type="printer" />印刷</a-button>
      <a-button slot="extra" type="primary" ghost @click="() => { this.$router.go(-1); }"> <a-icon type="left" />戻る</a-button>
      <section id="printContent">
        <a-spin :spinning="loading">
          <img id="barcode" style="float: right" />
          <a-descriptions bordered>
            <a-descriptions-item label="転送コード">
              {{ info.number }}
            </a-descriptions-item>
            <a-descriptions-item label="出荷入庫">
              {{ info.out_warehouse_name }}
            </a-descriptions-item>
            <a-descriptions-item label="入荷入庫">
              {{ info.in_warehouse_name }}
            </a-descriptions-item>
            <a-descriptions-item label="担当者">
              {{ info.handler_name }}
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
            :data-source="info.stock_transfer_goods_items"
            :pagination="false" />
        </a-spin>
      </section>
    </a-card>
  </div>
</template>

<script>
  import { stockTransferDetail } from '@/api/warehouse'
  import JsBarcode from 'jsbarcode'

  export default {
    data() {
      return {
        loading: false,
        materialLoading: false,
        receiptOrder: undefined,
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
            title: '転送数数数量',
            dataIndex: 'stock_transfer_quantity',
            key: 'stock_transfer_quantity',
            width: 120,
          },
        ],
        columnsAccount: [
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
            title: '決済口座',
            dataIndex: 'account_name',
            key: 'account_name',
            width: 200,
          },
          {
            title: '支払いい金金金額',
            dataIndex: 'payment_amount',
            key: 'payment_amount',
            width: 200,
          }
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
        stockTransferDetail({ id: this.$route.query.id }).then(data => {
          this.info = data;
          this.info.stock_transfer_goods_items = [
            ...this.info.stock_transfer_goods_items,
            {
              id: '-1',
              isTotal: true,
              stock_transfer_quantity: this.info.total_quantity,
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
