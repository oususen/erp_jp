<template>
  <div>
    <a-card title="棚卸伝票詳細">
      <a-button slot="extra" type="primary" style="margin-right: 8px;" ghost v-print="'#printContent'"> <a-icon type="printer" />印刷</a-button>
      <a-button slot="extra" type="primary" ghost @click="() => { this.$router.go(-1); }"> <a-icon type="left" />戻る</a-button>
      <section id="printContent">
        <a-spin :spinning="loading">
          <img id="barcode" style="float: right" />
          <a-descriptions bordered>
            <a-descriptions-item label="棚卸コード数数量">
              {{ info.number }}
            </a-descriptions-item>
            <a-descriptions-item label="棚卸状況">
              {{ info.status_display }}
            </a-descriptions-item>
            <a-descriptions-item label="入庫">
              {{ info.warehouse_name }}
            </a-descriptions-item>
            <a-descriptions-item label="帳簿総数数量">
              {{ info.total_book_quantity }}
            </a-descriptions-item>
            <a-descriptions-item label="実総数数数量">
              {{ info.total_actual_quantity }}
            </a-descriptions-item>
            <a-descriptions-item label="棚卸超過総数数量">
              {{ info.total_surplus_quantity }}
            </a-descriptions-item>
            <a-descriptions-item label="棚卸超過総数数量">
              {{ info.total_surplus_amount }}
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
            :data-source="info.stock_check_goods_Items"
            :pagination="false">
            <div slot="batch" slot-scope="value, item">
              <a-button v-if="item.enable_batch_control" type="primary" size="small" @click="batchDetial(item)">ロットを表示する</a-button>
            </div>
          </a-table>
        </a-spin>
      </section>
    </a-card>
    <!-- ロット -->
    <a-modal
      :title="batchTitle"
      v-model="batchVisible"
      width="750px"
      cancelText="閉じる"
      :maskClosable="false"
      @cancel="batchVisible=false"
      @ok="confirmChoosed">
      <a-table
        rowkey="id"
        :columns="columnsBatch"
        :data-source="stockCheckBatchItems"
        :pagination="false"
        style="width: 100%">
      </a-table>
    </a-modal>
  </div>
</template>

<script>
  import { stockCheckDetail } from '@/api/warehouse'
  import JsBarcode from 'jsbarcode'

  export default {
    data() {
      return {
        loading: false,
        materialLoading: false,
        receiptOrder: undefined,
        batchTitle: '',
        batchVisible: false,
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
            title: 'ロット制御',
            dataIndex: 'enable_batch_control',
            key: 'enable_batch_control',
            width: 80,
            customRender: (value, item, index) => {
              return item.isTotal ? '' : (item.enable_batch_control ? '有効化' : '無効')
            },
          },
          {
            title: '実数数数量',
            dataIndex: 'actual_quantity',
            key: 'actual_quantity',
            width: 120,
          },
          {
            title: 'ロット',
            dataIndex: 'batch',
            scopedSlots: { customRender: 'batch' },
            width: 80
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
        columnsBatch: [
          {
            title: '連番',
            dataIndex: 'index',
            key: 'index',
            customRender: (value, item, index) => {
              return index + 1
            },
          },
          {
            title: "コード",
            dataIndex: "batch_number",
            key: "batch_number",
          },
          {
            title: "実数数数量",
            dataIndex: "actual_quantity",
            key: "actual_quantity",
          },
          {
            title: "製造日",
            dataIndex: "production_date",
            key: "production_date",
          }
        ],
        stockCheckBatchItems: []
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
        stockCheckDetail({ id: this.$route.query.id }).then(data => {
          this.info = data;
          this.info.stock_check_goods_Items = [
            ...this.info.stock_check_goods_Items,
            {
              id: '-1',
              isTotal: true,
              actual_quantity: this.info.total_actual_quantity,
            },
          ];
          this.getJsBarcode(data.number)
        }).finally(() => {
          this.loading = false;
        });
      },
      batchDetial(item,) {
        console.log(item,)
        this.batchTitle = 'ロットを管理する';
        this.stockCheckBatchItems = item.stock_check_batch_items;
        this.batchVisible = true;
      },
    },
    mounted() {
      this.initData();
    },
  }
</script>
<style>
</style>
