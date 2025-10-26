<template>
  <div>
    <a-card title="資金明細詳細">
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
            <a-descriptions-item label="決済口座名">
              {{ info.account_name }}
            </a-descriptions-item>
            <a-descriptions-item label="決済口座コード">
              {{ info.account_number }}
            </a-descriptions-item>
            <a-descriptions-item label="明細タイプ">
              {{ info.type_display }}
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
            <a-descriptions-item label="支払いい書類">
              {{ info.payment_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="支払いいい文書を無効化">
              {{ info.void_payment_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="入金伝票">
              {{ info.collection_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="支払いいい入金伝票を無効化">
              {{ info.void_collection_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="収支伝票い">
              {{ info.charge_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="収支伝票い書類を無効化">
              {{ info.void_charge_order_number }}
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
