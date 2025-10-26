<template>
  <div>
    <a-card title="入金伝票詳細">
       <a-button slot="extra" type="primary" style="margin-right: 8px;" ghost v-print="'#printContent'"> <a-icon type="printer" />印刷</a-button>
      <a-button slot="extra" type="primary" ghost @click="() => { this.$router.go(-1); }"> <a-icon type="left" />戻る</a-button>
      <section id="printContent">
        <a-spin :spinning="loading">
          <img id="barcode" style="float: right" />
          <a-descriptions bordered>
            <a-descriptions-item label="購入コード">
              {{ info.number }}
            </a-descriptions-item>
            <a-descriptions-item label="顧客">
              {{ info.client_name }}
            </a-descriptions-item>
            <a-descriptions-item label="担当者">
              {{ info.handler_name }}
            </a-descriptions-item>
            <a-descriptions-item label="処理日">
              {{ info.handle_time }}
            </a-descriptions-item>
            <a-descriptions-item label="割引金金額">
              {{ info.discount_amount }}
            </a-descriptions-item>
            <a-descriptions-item label="備考">
              {{ info.remark }}
            </a-descriptions-item>
          </a-descriptions>
          <a-divider orientation="left" style="margin-top: 30px;">決済口座情報</a-divider>
          <a-table
            rowKey="id"
            size="middle"
            :columns="columnsAccount"
            :data-source="info.collection_account_items"
            :pagination="false" />
        </a-spin>
      </section>
    </a-card>
  </div>
</template>

<script>
  import { collectioOrderDetail } from '@/api/finance'
  import JsBarcode from 'jsbarcode'
  import NP from 'number-precision'

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
            title: '購入数数数量',
            dataIndex: 'purchase_quantity',
            key: 'purchase_quantity',
            width: 120,
          },
          {
            title: '購買単価（円）',
            dataIndex: 'purchase_price',
            key: 'purchase_price',
            width: 120,
          },
          {
            title: '金金額',
            dataIndex: 'totalAmount',
            key: 'totalAmount',
            width: 200,
            customRender: (value, item) => {
              if (item.isTotal) return value;
              value = NP.times(item.purchase_quantity, item.purchase_price);
              return item.id ? NP.round(value, 2) : ''
            },
          }
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
            dataIndex: 'collection_amount',
            key: 'collection_amount',
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
        let collectionAmount = 0;
        this.loading = true;
        collectioOrderDetail({ id: this.$route.query.id }).then(data => {
          this.info = data;
          data.collection_account_items.map(item => { collectionAmount += Number(item.collection_amount) });
          this.info.collection_account_items = [
            ...this.info.collection_account_items,
            {
              id: '-1',
              isTotal: true,
              collection_amount: collectionAmount,
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
