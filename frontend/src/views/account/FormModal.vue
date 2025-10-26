<template>
  <div>
    <a-modal v-model="visible" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? 'アカウント編集' : 'アカウント新規登録' }}</div>
      <div>
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 4 }" :wrapper-col="{ span: 16 }">
          <a-form-model-item prop="username" label="ユーザー名">
            <a-input v-model="form.username" />
          </a-form-model-item>
          <a-form-model-item prop="name" label="従業員名">
            <a-input v-model="form.name" />
          </a-form-model-item>
          <a-form-model-item prop="phone" label="携帯コード">
            <a-input v-model="form.phone" />
          </a-form-model-item>
          <a-form-model-item prop="email" label="メールアドレス">
            <a-input v-model="form.email" />
          </a-form-model-item>
          <a-form-model-item prop="sex" label="性別">
          <a-select
            default-value="man"
            style="width: 100%"
            v-model="form.sex">
            <a-select-option value="man"> 男性性 </a-select-option>
            <a-select-option value="woman"> 女性 </a-select-option>
          </a-select>
        </a-form-model-item>
          <a-form-model-item prop="is_active" label="状態">
            <a-select v-model="form.is_active" style="width: 100%;">
              <a-select-option :value="true">有効化</a-select-option>
              <a-select-option :value="false">無効化</a-select-option>
            </a-select>
          </a-form-model-item>
          <a-form-model-item prop="roles" label="ロール">
            <a-select v-model="form.roles" mode="multiple" allowClear style="width: 100%;">
              <a-select-option v-for="item in roleItems" :key="item.id" :value="item.id">{{item.name}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
        </a-form-model>

        <div v-if="!form.id" style="color: rgb(255, 77, 79); text-align: center;">
          デフォルト初期パスワードは: 123456, ログイン後パスワードを変更してください
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script>
  import { userCreate, userUpdate } from '@/api/account'
  import rules from './rules.js'

  export default {
    name: 'FormModal',
    props: ['visible', 'form', 'roleItems'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        rules,
        loading: false,
      };
    },
    methods: {
      confirm() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.loading = true;
            let func = this.form.id ? userUpdate : userCreate;
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