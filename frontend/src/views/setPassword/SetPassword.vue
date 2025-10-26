<template>
  <div>
    <div>
      <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 5 }" :wrapper-col="{ span: 14 }">
        <a-form-model-item prop="username" label="ユーザー名">
          <a-input size="large" v-model="form.username" />
        </a-form-model-item>
        <a-form-model-item prop="old_password" label="旧パスワード">
          <a-input-password size="large" v-model="form.old_password" />
        </a-form-model-item>
        <a-form-model-item prop="new_password" label="新パスワード">
          <a-input-password size="large" v-model="form.new_password" />
        </a-form-model-item>
        <a-form-model-item prop="confirm" label="パスワード確認">
          <a-input-password size="large" v-model="form.confirm" />
        </a-form-model-item>
      </a-form-model>
    </div>

    <a-row>
      <a-col :span="14" offset="5">
        <a-button type="link" style="float: left; padding: 0;" @click="$router.push('/user/login')">ログインに戻る</a-button>
      </a-col>
    </a-row>

    <a-row>
      <a-col :span="14" offset="5">
        <a-button type="primary" size="large" :loading="isLoading" style="width: 100%;" @click="setPassword">パスワードを変更する
        </a-button>
      </a-col>
    </a-row>
  </div>
</template>

<script>
  import { setPassword } from '@/api/user'

  export default {
    name: 'SetPassword',
    data() {
      return {
        isLoading: false,
        form: {
          username: '',
          old_password: '',
          new_password: '',
          confirm: '',
        },
        rules: {
          username: [{ required: true, message: '携帯コードを入力してください', trigger: 'change' }],
          old_password: [{ required: true, message: '旧パスワードを入力してください', trigger: 'change' }],
          new_password: [{ required: true, message: '新パスワードを入力してください', trigger: 'change' }],
          confirm: [
            { required: true, message: '新パスワードをもう一度入力してください', trigger: 'change' },
            { validator: this.validateConfirm, trigger: 'blur' },
          ],
        },
      };
    },
    methods: {
      validateConfirm(rule, value, callback) {
        return value === this.form.new_password ? callback() : callback(new Error('2回入力したパスワードは一致しません'))
      },
      setPassword() {
        this.$refs.form.validate(valid => {
          if (valid) {
            this.isLoading = true;
            setPassword(this.form)
              .then(() => {
                this.$message.success('設定成功');
                this.$router.push('/user/login');
              })
              .catch(err => {
                this.$message.error(err.response.data.error);
              })
              .finally(() => {
                this.isLoading = false;
              });
          }
        });
      },
    },
  }
</script>