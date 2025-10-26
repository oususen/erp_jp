import { message } from "ant-design-vue";
import Cookies from "js-cookie";
import router from "@/router";
import axios from "axios";
import config from "./config"
const GET_TOKEN_URL = "/user/get_token/";
const REFRESH_TOKEN_URL = "/user/refresh_token/";
const LOGIN_PATH = "/user/login";
let requestQueue = [],
  isRefreshing = false;

const instance = axios.create({
  baseURL: config.baseURL,
  timeout: 10000,
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
});

instance.interceptors.request.use(
  (config) => {
    if (!config.url.includes(GET_TOKEN_URL) && !config.url.includes(REFRESH_TOKEN_URL)) {
      const accessToken = Cookies.get("access");
      if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`;
      } else if (config.headers.Authorization) {
        delete config.headers.Authorization;
      }
    }

    const csrfToken = Cookies.get("csrftoken");
    if (csrfToken && !config.headers["X-CSRFToken"]) {
      config.headers["X-CSRFToken"] = csrfToken;
    }

    console.info("Send request:", config);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

instance.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    if (!error.response) {
      if (error.message.includes("Network Error")) {
        message.error("接続が拒否されました。サーバーが起動しているか確認してください");
      }
      return Promise.reject(error);
    }
    if (!error.response) return Promise.reject(error);
    console.error("Request error:", error.response);

    if (error.response.status >= 500) {
      message.error("サーバーエラー発生発生");
      return Promise.reject(error);
    }

    if (error.response.status == 401 && !error.config.url.includes(REFRESH_TOKEN_URL)) {
      if (isRefreshing) {
        return new Promise((resolve) => {
          requestQueue.push(() => {
            resolve(instance(error.config));
          });
        });
      } else {
        isRefreshing = true;
        return refreshToken()
          .then((data) => {
            Cookies.set("access", data.access);
            requestQueue.forEach((fn) => fn());
            requestQueue = [];

            return instance(error.config);
          })
          .catch((error) => {
            if (error.response.status == 401) {
              redirectLogin();
              message.error("トークン期限切れ日切れ, 再ログインしてください");
            }
            
            return Promise.reject(error);
          })
          .finally(() => {
            isRefreshing = false;
          });
      }
    }

    message.error(error.response.data.detail || 'レスポンスエラー発生発生');
    return Promise.reject(error);
  }
);

function refreshToken() {
  return request({ url: REFRESH_TOKEN_URL, method: "post", data: { refresh: Cookies.get("refresh") } });
}

function redirectLogin() {
  requestQueue = [];
  router.push(LOGIN_PATH);
}

export default function request(item) {
  let { data = {} } = item;
  for (let key in data) {
    if (data[key] == undefined) delete data[key];
  }

  return instance(item);
}
