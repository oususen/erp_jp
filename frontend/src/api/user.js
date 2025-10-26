import request from '@/utils/request';

export function getToken(data) {
  return request({ url: '/user/get_token/', method: 'post', data });
}

export function refreshToken(data) {
  return request({ url: '/user/refresh_token/', method: 'post', data });
}

export function getInfo(params) {
  return request({ url: '/user/info/', method: 'get', params });
}

export function setPassword(data) {
  return request({ url: '/user/set_password/', method: 'post', data });
}

export function fetchCsrfToken() {
  return request({ url: '/manage/super_user/get_csrf_token/', method: 'get' });
}
