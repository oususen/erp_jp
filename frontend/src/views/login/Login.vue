<template>
  <div>
    <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 6 }" :wrapper-col="{ span: 14 }">
      <a-form-model-item prop="username" label="ユーザー名">
        <a-input size="large" v-model="form.username" autocomplete="username" />
      </a-form-model-item>
      <a-form-model-item prop="password" label="パスワード">
        <a-input-password size="large" v-model="form.password" autocomplete="current-password" />
      </a-form-model-item>
    </a-form-model>
    <a-row>
      <a-col :span="14" offset="5">
        <a-button type="primary" size="large" :loading="isLoading" style="width: 100%;" @click="login">ログイン</a-button>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import Cookies from 'js-cookie';
import { fetchCsrfToken, getToken } from '@/api/user';

export default {
  name: 'Login',
  data() {
    return {
      selectedKeys: ['login'],
      isLoading: false,
      form: {
        number: 'ADMIN',
        username: '',
        password: '',
      },
      rules: {
        username: [
          { required: true, message: 'ユーザー名を入力してください', trigger: 'change' },
        ],
        password: [
          { required: true, message: 'パスワードを入力してください', trigger: 'change' },
        ],
      },
      second: 60,
      is_send: false,
      warn: '',
      code_interval: null,
    };
  },
  methods: {
    initialize() {
      document.onkeypress = (e) => {
        let code = document.all ? event.keyCode : e.which;
      };
      this.ensureCsrfToken();
    },
    ensureCsrfToken() {
      if (!Cookies.get('csrftoken')) {
        fetchCsrfToken().catch(() => {});
      }
    },
    login() {
      this.$refs.form.validate((valid) => {
        if (!valid) {
          return;
        }
        this.isLoading = true;
        const ensureToken = Cookies.get('csrftoken') ? Promise.resolve() : fetchCsrfToken();

        ensureToken
          .catch(() => {})
          .finally(() => {
            getToken(this.form)
              .then((data) => {
                Cookies.set('access', data.access);
                Cookies.set('refresh', data.refresh);
                this.$message.success('ログインに成功しました');
                // ページ遷移の前に少し待機してクッキーが設定されるのを確認
                this.$nextTick(() => {
                  this.$router.push('/basicData/client');
                });
              })
              .finally(() => {
                this.isLoading = false;
              });
          });
      });
    },
  },
  created() {
    this.initialize();
  },
};
</script>
