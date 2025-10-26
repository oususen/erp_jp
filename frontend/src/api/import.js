import request from '@/utils/request';
import Cookies from 'js-cookie'
import axios from 'axios'


// 顧客テンプレート
export function clientTemplate(params) {
  return axios({
    url: '/api/clients/import_template/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 顧客インポート
export function clientImport(data) {
  return axios({
    url: '/api/clients/import_data/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// 仕入先テンプレート
export function supplierTemplate(params) {
  return axios({
    url: '/api/suppliers/import_template/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 仕入先インポート
export function supplierImport(data) {
  return axios({
    url: '/api/suppliers/import_data/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// 入庫テンプレート
export function warehouseTemplate(params) {
  return axios({
    url: '/api/warehouses/import_template/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 入庫インポート
export function warehouseImport(data) {
  return axios({
    url: '/api/warehouses/import_data/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// 決済口座テンプレート
export function settlementAccountTemplate(params) {
  return axios({
    url: '/api/accounts/import_template/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 決済口座インポート
export function settlementAccountImport(data) {
  return axios({
    url: '/api/accounts/import_data/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// 収支項目テンプレート
export function revenueExpenditureItemsTemplate(params) {
  return axios({
    url: '/api/charge_items/import_template/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 収支項目インポート
export function revenueExpenditureItemsImport(data) {
  return axios({
    url: '/api/charge_items/import_data/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// 商品カテゴリのテンプレート
export function goodsClassificationTemplate(params) {
  return axios({
    url: '/api/goods_categories/import_template/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 商品カテゴリのインポート
export function goodsClassificationImport(data) {
  return axios({
    url: '/api/goods_categories/import_data/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// 商品情報テンプレート
export function goodsInformationTemplate(params) {
  return axios({
    url: '/api/goods/import_template/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 商品情報のインポート
export function goodsInformationImport(data) {
  return axios({
    url: '/api/goods/import_data/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// 商品単位テンプレート
export function goodsUnitTemplate(params) {
  return axios({
    url: '/api/goods_units/import_template/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 商品単位のインポート
export function goodsUnitImport(data) {
  return axios({
    url: '/api/goods_units/import_data/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    method: 'post',
    data,
  })
}

// // 原料マスタテンプレート
// export function materialDictTemplate(params) {
//   return axios({
//     url: '/api/materials/import_template/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     responseType: 'blob',
//     method: 'get',
//     params,
//   })
// }

// // 原料マスタインポート
// export function materialDictImport(data) {
//   return axios({
//     url: '/api/materials/import_data/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     method: 'post',
//     data,
//   })
// }

// // 商品マスタテンプレート
// export function productsDictTemplate(params) {
//   return axios({
//     url: '/api/products/import_template/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     responseType: 'blob',
//     method: 'get',
//     params,
//   })
// }

// // 商品マスタインポート
// export function productsDictImport(data) {
//   return axios({
//     url: '/api/products/import_data/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     method: 'post',
//     data,
//   })
// }

