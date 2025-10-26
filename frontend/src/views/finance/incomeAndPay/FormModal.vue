<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? '日常収支編集' : '日常収支新規登録' }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="number" label="コード">
            <a-input v-model="form.number" />
          </a-form-model-item>
          <a-form-model-item prop="type" label="収支タイプ">
            <a-select v-model="form.type" style="width: 100%">
              <a-select-option v-for="item in typeItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="client" label="顧客">
            <a-select v-model="form.client" style="width: 100%">
              <a-select-option v-for="item in clientsItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="supplier" label="仕入先">
            <a-select v-model="form.supplier" style="width: 100%">
              <a-select-option v-for="item in suppliersItems" :key="item.id" :value="item.id">
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
          <a-form-model-item prop="charge_item" label="収支項目">
            <a-select v-model="form.charge_item" style="width: 100%">
              <a-select-option v-for="item in chargeItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="account" label="決済口座">
            <a-select v-model="form.account" style="width: 100%">
              <a-select-option v-for="item in accountsItems" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="total_amount" label="売掛金/お支払いいい金金金額">
            <a-input-number v-model="form.total_amount" style="width: 100%;" />
          </a-form-model-item>
          <a-form-model-item prop="charge_amount" label="実収入/お支払いいい金金金額">
            <a-input-number v-model="form.charge_amount" style="width: 100%;" />
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
  import { chargeOrderCreate } from '@/api/finance'
  
  export default {
    name: 'FormModal',
    props: ['visible', 'form', 'clientsItems', 'suppliersItems', 'chargeItems', 'handlerItems', 'accountsItems'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        typeItems: [
          { id: 'income', name: '収入' },
          { id: 'expenditure', name: '支出' }
        ],
        rules: {
          number: [{ required: true, message: 'コードを入力してください', trigger: 'change' }],
          type: [{ required: true, message: 'お支払いいいタイプを選択してください', trigger: 'change' }],
          account: [{ required: true, message: '決済口座を選択してください', trigger: 'change' }],
          total_amount: [
            { required: true, message: '売掛金を入力してください/お支払いいい金金金額', trigger: 'change' },
            { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: '売掛金/支払いいい金金金額の形式が間違っています', trigger: 'change' }
          ],
          charge_item: [
            { required: true, message: '収支項目を選択してください', trigger: 'change' },
          ],
          charge_amount: [
            { required: true, message: '実収入を入力してください/お支払いいい金金金額', trigger: 'change' },
            { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: '実収入/支払いいい金金金額の形式が間違っています', trigger: 'change' }
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
            let func = this.form.id ? chargeOrderCreate : chargeOrderCreate;
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