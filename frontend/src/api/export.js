import Cookies from 'js-cookie'
import axios from 'axios'


// 顧客
export function clientExport(params) {
  return axios({
    url: '/api/clients/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 仕入先
export function supplierExport(params) {
  return axios({
    url: '/api/suppliers/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 入庫
export function warehouseExport(params) {
  return axios({
    url: '/api/warehouses/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 決済口座
export function settlementAccountExport(params) {
  return axios({
    url: '/api/accounts/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 収支項目
export function revenueExpenditureItemsExport(params) {
  return axios({
    url: '/api/charge_items/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 商品カテゴリ
export function goodsClassificationExport(params) {
  return axios({
    url: '/api/goods_categories/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 商品情報
export function goodsInformationExport(params) {
  return axios({
    url: '/api/goods/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// 商品単位
export function goodsUnitExport(params) {
  return axios({
    url: '/api/goods_units/export/',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
    responseType: 'blob',
    method: 'get',
    params,
  })
}

// // 原料マスタ
// export function materialDictExport(params) {
//   return axios({
//     url: '/api/materials/export/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     responseType: 'blob',
//     method: 'get',
//     params,
//   })
// }

// // 商品マスタ
// export function productsDictExport(params) {
//   return axios({
//     url: '/api/products/export/',
//     headers: { 'X-CSRFToken': Cookies.get('csrftoken'), Authorization: 'Bearer ' + Cookies.get('access') },
//     responseType: 'blob',
//     method: 'get',
//     params,
//   })
// }

