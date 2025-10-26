<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? '入庫編集' : '入庫を追加' }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="name" label="入庫名">
            <a-input v-model="form.name" />
          </a-form-model-item>
          <a-form-model-item prop="number" label="入庫コード">
            <a-input v-model="form.number" />
          </a-form-model-item>
          <a-form-model-item prop="manager" label="管理者">
            <a-select v-model="form.manager" style="width: 100%">
              <a-select-option v-for="item in usersOptions" :key="item.id" :value="item.id">
                {{ item.name }}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="phone" label="携帯コード">
            <a-input v-model="form.phone" />
          </a-form-model-item>
          <a-form-model-item prop="address" label="住所">
            <a-input v-model="form.address" />
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
        </a-form-model>
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { warehouseCreate, warehouseUpdate } from '@/api/basicData'
  
  export default {
    name: 'FormModal',
    props: ['visible', 'form', 'usersOptions'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        rules: {
          name: [{ required: true, message: '入庫名を入力してください', trigger: 'change' }],
          number: [{ required: true, message: '入庫コードを入力してください', trigger: 'change' }],
        },
        loading: false,
      };
    },
    methods: {
      confirm() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.loading = true;
            let func = this.form.id ? warehouseUpdate : warehouseCreate;
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