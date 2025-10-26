<template>
  <div>
    <a-card title="在庫推移詳細">
      <a-button slot="extra" type="primary" ghost @click="() => { this.$router.go(-1); }"> <a-icon type="left" />戻る</a-button>
      <section id="pdfDom">
        <a-spin :spinning="loading">
          <a-descriptions bordered>
            <a-descriptions-item label="作成者">
              {{ info.creator_name }}
            </a-descriptions-item>
            <a-descriptions-item label="作成時間">
              {{ info.create_time }}
            </a-descriptions-item>
            <a-descriptions-item label="入庫">
              {{ info.warehouse_name }}
            </a-descriptions-item>
            <a-descriptions-item label="商品名">
              {{ info.goods_name }}
            </a-descriptions-item>
            <a-descriptions-item label="商品コード">
              {{ info.goods_number }}
            </a-descriptions-item>
            <a-descriptions-item label="単位名">
              {{ info.unit_name }}
            </a-descriptions-item>
            <a-descriptions-item label="明細タイプ">
              {{ info.type_display }}
            </a-descriptions-item>
            <a-descriptions-item label="変更前数数数量">
              {{ info.quantity_before }}
            </a-descriptions-item>
            <a-descriptions-item label="変更数数数量">
              {{ info.quantity_change }}
            </a-descriptions-item>
            <a-descriptions-item label="変更後数数数量">
              {{ info.quantity_after }}
            </a-descriptions-item>
            <a-descriptions-item label="購買伝票コード">
              {{ info.purchase_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="購買伝票コード無効">
              {{ info.void_purchase_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="購入返品伝票コード">
              {{ info.purchase_return_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="購買返品伝票コード無効">
              {{ info.void_purchase_return_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="販売伝票コード">
              {{ info.sales_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="販売伝票コード無効">
              {{ info.void_sales_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="販売返品伝票コード">
              {{ info.sales_return_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="販売返品伝票コード無効">
              {{ info.void_sales_return_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="入庫届出コード">
              {{ info.stock_in_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="入庫通知コード無効">
              {{ info.void_stock_in_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="出庫通知コード">
              {{ info.stock_out_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="出庫通知コード無効">
              {{ info.void_stock_out_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="在庫伝票コード">
              {{ info.stock_check_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="棚卸伝票コード無効">
              {{ info.void_stock_check_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="ダイヤルコード">
              {{ info.stock_transfer_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="振替伝票コード無効">
              {{ info.void_stock_transfer_order_number }}
            </a-descriptions-item>
          </a-descriptions>
        </a-spin>
      </section>
    </a-card>
  </div>
</template>

<script>
  import { inventoryFlowsDetail } from '@/api/warehouse'
  
  export default {
    data() {
      return {
        loading: false,
        info: {},
      }
    },
    created(){
      this.initData();
    },
    methods: {
      initData() {
        this.info = JSON.parse(this.$route.query.item);
        // this.loading = true;
        // inventoryFlowsDetail({ id: this.$route.query.id }).then(data => {
        //   this.info = data;
        // }).finally(() => {
        //   this.loading = false;
        // });
      },
    },
    mounted() {
      this.initData();
    },
  }
</script>
<style>
</style>
