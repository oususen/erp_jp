<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{ form.id ? "決済口座編集" : "決済口座新規登録" }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="name" label="口座名">
            <a-input v-model="form.name" />
          </a-form-model-item>
          <a-form-model-item prop="number" label="口座コード">
            <a-input v-model="form.number" />
          </a-form-model-item>
          <a-form-model-item prop="type" label="口座タイプ">
            <a-select v-model="form.type" style="width: 100%">
              <a-select-option v-for="item in typeOptions" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="holder" label="口座名義人">
            <a-input v-model="form.holder" />
          </a-form-model-item>
          <a-form-model-item prop="card_number" label="口座コード">
            <a-input v-model="form.card_number" />
          </a-form-model-item>
          <a-form-model-item prop="remark" label="備考">
            <a-input v-model="form.remark" allowClear />
          </a-form-model-item>
          <a-form-model-item prop="is_active" label="状態">
            <a-select v-model="form.is_active" style="width: 100%">
              <a-select-option :value="true">有効化</a-select-option>
              <a-select-option :value="false">凍結</a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="initial_balance_amount" label="初期残高">
            <a-input-number v-model="form.initial_balance_amount" style="width: 100%" />
          </a-form-model-item>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
import { settlementAccountCreate, settlementAccountUpdate } from "@/api/basicData";

export default {
  name: "FormModal",
  props: ["visible", "form"],
  model: { prop: "visible", event: "cancel" },
  data() {
    return {
      typeOptions: [
        { id: "cash", name: "現金" },
        { id: "alipay", name: "Alipay" },
        { id: "wechat", name: "WeChatウォレット" },
        { id: "bank_account", name: "銀行口座" },
        { id: "other", name: "その他" },
      ],
      rules: {
        name: [
          { required: true, message: "口座名を入力してください", trigger: "change" },
          { max: 64, message: "最大長を超えています（64）", trigger: "change" },
        ],
        number: [
          { required: true, message: "口座コードを入力してください", trigger: "change" },
          { max: 32, message: "最大長を超えています（32）", trigger: "change" },
        ],
        initial_balance_amount: [
          { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: "初期残高の形式が不正です", trigger: "change" },
        ],
      },
      loading: false,
    };
  },
  methods: {
    confirm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.loading = true;
          let func = this.form.id ? settlementAccountUpdate : settlementAccountCreate;
          func(this.form)
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
  },
};
</script>

<style scoped></style>
