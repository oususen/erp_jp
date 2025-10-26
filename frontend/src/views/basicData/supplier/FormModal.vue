<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? '仕入先編集' : '仕入先新規登録' }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="name" label="仕入先名">
            <a-input v-model="form.name" />
          </a-form-model-item>
          <a-form-model-item prop="number" label="仕入先コード">
            <a-input v-model="form.number" />
          </a-form-model-item>
          <a-form-model-item prop="contact" label="連絡先">
            <a-input v-model="form.contact" />
          </a-form-model-item>
          <a-form-model-item prop="phone" label="携帯コード">
            <a-input v-model="form.phone" />
          </a-form-model-item>
          <a-form-model-item prop="email" label="メールアドレス">
            <a-input v-model="form.email" />
          </a-form-model-item>
          <a-form-model-item prop="address" label="住所">
            <a-input v-model="form.address" />
          </a-form-model-item>
          <a-form-model-item prop="bank_account" label="銀行口座">
            <a-input v-model="form.bank_account" />
          </a-form-model-item>
          <a-form-model-item prop="bank_name" label="取引銀行">
            <a-input v-model="form.bank_name" />
          </a-form-model-item>
          <a-form-model-item prop="remark" label="備考">
            <a-input v-model="form.remark" allowClear />
          </a-form-model-item>
          <a-form-model-item prop="is_active" label="状態">
            <a-select v-model="form.is_active" style="width: 100%;">
              <a-select-option :value="true">有効化</a-select-option>
              <a-select-option :value="false">凍結</a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="initial_arrears_amount" label="初期未払金金金額">
            <a-input-number v-model="form.initial_arrears_amount" style="width: 100%;" />
          </a-form-model-item>
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>


<script>
  import { supplierCreate, supplierUpdate } from '@/api/basicData'
  
  export default {
    name: 'FormModal',
    props: ['visible', 'form', 'suppliersClassificationOptions'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        rules: {
          name: [{ required: true, message: '名称を入力してください', trigger: 'change' }],
          number: [{ required: true, message: 'コードを入力してください', trigger: 'change' }],
          initial_arrears_amount: [
            { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: '初期未払金金金額の形式が不正です', trigger: 'change' }
          ],
        },
        loading: false,
      };
    },
    methods: {
      confirm() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.loading = true;
            let func = this.form.id ? supplierUpdate : supplierCreate;
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