<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{ form.id ? "生産計画編集" : "生産計画新規登録" }}</div>
      <div>
        <a-form-model ref="form" :model="dataForm" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="number" label="生産指示コード">
            <a-input v-model="dataForm.number" />
          </a-form-model-item>
          <a-form-model-item prop="is_related" label="タイプ">
            <a-radio-group v-model="dataForm.is_related" button-style="solid" @change="switchType">
              <a-radio-button :value="false">在庫生産</a-radio-button>
              <a-radio-button :value="true">受注生産</a-radio-button>
            </a-radio-group>
          </a-form-model-item>
          <a-form-model-item v-if="!dataForm.is_related" prop="goods" label="商品">
            <goods-select v-model="dataForm.goods" :defaultItem="{ ...dataForm }" />
          </a-form-model-item>
          <a-form-model-item v-if="dataForm.is_related" prop="sales_order" label="販売伝票">
            <sales-order-select
              v-model="dataForm.sales_order"
              :defaultItem="{ ...dataForm }"
              @select="
                (item) => {
                  dataForm.sales_goods_items = item.sales_goods_items;
                  dataForm.goods = undefined;
                }
              "
            />
          </a-form-model-item>
          <a-form-model-item v-if="dataForm.is_related" prop="goods" label="商品">
            <a-select v-model="dataForm.goods" style="width: 100%;">
              <a-select-option v-for="item in dataForm.sales_goods_items" :key="item.goods" :value="item.goods">
                {{ item.goods_name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="total_quantity" label="予定数数数量">
            <a-input-number v-model="dataForm.total_quantity" style="width: 100%;" />
          </a-form-model-item>
          <a-form-model-item prop="start_time" label="開始時間">
            <a-date-picker
              v-model="dataForm.start_time"
              placeholder="時間を選択してください"
              valueFormat="YYYY-MM-DD HH:mm:ss"
              show-time
              style="width: 100%;"
            />
          </a-form-model-item>
          <a-form-model-item prop="end_time" label="終了時間">
            <a-date-picker
              v-model="dataForm.end_time"
              placeholder="時間を選択してください"
              valueFormat="YYYY-MM-DD HH:mm:ss"
              show-time
              style="width: 100%;"
            />
          </a-form-model-item>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
import { productionOrderCreate, productionOrderUpdate, productionOrderNumber } from "@/api/production";

export default {
  components: {
    GoodsSelect: () => import("@/components/GoodsSelect/index"),
    SalesOrderSelect: () => import("@/components/SalesOrderSelect/index"),
  },
  props: ["visible", "form"],
  model: { prop: "visible", event: "cancel" },
  data() {
    return {
      rules: {
        number: [{ required: true, message: "コードを入力してください", trigger: "change" }],
        goods: [{ required: true, message: "生産商品を選択してください", trigger: "change" }],
        total_quantity: [{ required: true, message: "予定数数数量を入力してください", trigger: "change" }],
      },
      loading: false,
      dataForm: {},
    };
  },
  methods: {
    confirm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.loading = true;
          let func = this.dataForm.id ? productionOrderUpdate : productionOrderCreate;
          func(this.dataForm)
            .then((data) => {
              this.$message.success(this.form.id ? "更新成功" : "新規登録成功");
              this.$emit(this.form.id ? "update" : "create", data);
              this.cancel();
            })
            .finally(() => {
              this.loading = false;
            });
        }
      });
    },
    cancel() {
      this.$emit("cancel", false);
      this.$refs.form.resetFields();
    },
    switchType() {
      this.dataForm = { ...this.dataForm, sales_order: undefined, goods: undefined };
    },
  },
  watch: {
    visible(value) {
      if (value) {
        if (this.form.id) {
          this.dataForm = { ...this.form };
        } else {
          this.dataForm = { is_related: false };
          productionOrderNumber().then((data) => {
            this.dataForm = { ...this.dataForm, number: data.number };
          });
        }
      }
    },
  },
};
</script>

<style scoped></style>
