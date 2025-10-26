<template>
  <div>
    <a-card title="生産計画詳細">
      <a-button slot="extra" type="primary" style="margin-right: 8px;" ghost v-print="'#printContent'">
        <a-icon type="printer" />印刷</a-button
      >
      <a-button
        slot="extra"
        type="primary"
        ghost
        @click="
          () => {
            this.$router.go(-1);
          }
        "
      >
        <a-icon type="left" />戻る</a-button
      >
      <section id="printContent">
        <a-spin :spinning="loading">
          <img id="barcode" style="float: right" />
          <a-descriptions bordered>
            <a-descriptions-item label="生産計画コード">
              {{ item.number }}
            </a-descriptions-item>
            <a-descriptions-item label="販売伝票コード">
              {{ item.sales_order_number }}
            </a-descriptions-item>
            <a-descriptions-item label="状態">
              {{ item.status_display }}
            </a-descriptions-item>
            <a-descriptions-item label="商品コード">
              {{ item.goods_number }}
            </a-descriptions-item>
            <a-descriptions-item label="商品名">
              {{ item.goods_name }}
            </a-descriptions-item>
            <a-descriptions-item label="予定数数数量">
              {{ item.total_quantity }}
            </a-descriptions-item>
            <a-descriptions-item label="完了数数数量">
              {{ item.quantity_produced }}
            </a-descriptions-item>
            <a-descriptions-item label="計画開始時間">
              {{ item.start_time }}
            </a-descriptions-item>
            <a-descriptions-item label="計画終了時間">
              {{ item.end_time }}
            </a-descriptions-item>
            <a-descriptions-item label="作成時間">
              {{ item.create_time }}
            </a-descriptions-item>
            <a-descriptions-item label="作成者">
              {{ item.creator_name }}
            </a-descriptions-item>
          </a-descriptions>
        </a-spin>
      </section>
    </a-card>
  </div>
</template>

<script>
import { productionOrderDetail } from "@/api/production";
import JsBarcode from "jsbarcode";

export default {
  data() {
    return {
      loading: false,
      item: {},
    };
  },
  methods: {
    getJsBarcode(number) {
      JsBarcode("#barcode", number, {
        lineColor: "#000",
        width: 2,
        height: 40,
        displayValue: true,
      });
    },
    initData() {
      this.loading = true;
      productionOrderDetail({ id: this.$route.query.id })
        .then((data) => {
          this.item = data;
          this.getJsBarcode(data.number);
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
  mounted() {
    this.initData();
  },
};
</script>
<style></style>
