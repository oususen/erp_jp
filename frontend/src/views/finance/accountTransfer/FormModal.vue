<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? '振出元口座編集' : '振出元口座新規登録' }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="out_account" label="振出元口座">
            <a-select v-model="form.out_account" style="width: 100%">
              <a-select-option v-for="item in accountsItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="transfer_out_time" label="振出日時">
            <a-date-picker v-model="form.transfer_out_time" valueFormat="YYYY-MM-DDThh:mm" style="width: 100%" />
          </a-form-model-item>
          <a-form-model-item prop="in_account" label="振込先口座">
            <a-select v-model="form.in_account" style="width: 100%">
              <a-select-option v-for="item in accountsItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="transfer_in_time" label="振込日時">
            <a-date-picker v-model="form.transfer_in_time" valueFormat="YYYY-MM-DDThh:mm" style="width: 100%" />
          </a-form-model-item>
          <a-form-model-item prop="transfer_amount" label="振込金金金額">
            <a-input-number v-model="form.transfer_amount" style="width: 100%;" />
          </a-form-model-item>
          <a-form-model-item prop="service_charge_amount" label="手数料金金金額">
            <a-input-number v-model="form.service_charge_amount" style="width: 100%;" />
          </a-form-model-item>
          <a-form-model-item prop="service_charge_payer" label="料金支払いい者">
            <a-select v-model="form.service_charge_payer" style="width: 100%">
              <a-select-option v-for="item in chargeItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="handler" label="担当者">
            <a-select v-model="form.handler" style="width: 100%">
              <a-select-option v-for="item in handlerItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="handle_time" label="処理時間">
            <a-date-picker v-model="form.handle_time" valueFormat="YYYY-MM-DD" style="width: 100%" />
          </a-form-model-item>
          <a-form-model-item prop="remark" label="備考">
            <a-input v-model="form.remark" allowClear />
          </a-form-model-item>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { accountTransferOrderCreate } from '@/api/finance'
  
  export default {
    name: 'FormModal',
    props: ['visible', 'form', 'handlerItems', 'accountsItems'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        chargeItems: [
          { id: 'transfer_in', name: '口座に送金して支払いいいます' },
          { id: 'transfer_out', name: '振出元口座によるお支払いいい' }
        ],
        rules: {
          out_account: [{ required: true, message: '振込先口座を選択してください', trigger: 'change' }],
          transfer_out_time: [{ required: true, message: '振出日時を選択してください', trigger: 'change' }],
          in_account: [{ required: true, message: '振込先口座を選択してください', trigger: 'change' }],
          transfer_in_time: [{ required: true, message: '振込先口座を選択してください', trigger: 'change' }],
          transfer_amount: [
            { required: true, message: '振込金金金額を入力してください', trigger: 'change' },
            { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: '振込金金金額の形式が不正です', trigger: 'change' }
          ],
          service_charge_amount: [
            { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: '手数料金金金額の形式が不正です', trigger: 'change' }
          ],
          handler: [{ required: true, message: '担当者ーを選択してください', trigger: 'change' }],
          handle_time: [{ required: true, message: '処理時間を選択してください', trigger: 'change' }],
        },
        loading: false,
      };
    },
    methods: {
      confirm() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.loading = true;
            let func = this.form.id ? accountTransferOrderCreate : accountTransferOrderCreate;
            func(this.form).then(data => {
              this.$message.success(this.form.id ? '更新成功' : '新規登録成功');
              this.$emit(this.form.id ? 'update' : 'create', data);
              this.cancel();
            }).finally(() => {
              this.loading = false;
            });
          }
        });
      },
      cancel() {
        this.$emit('cancel', false);
        this.$refs.form.resetFields();
      },
    },
  }
</script>

<style scoped>
</style>